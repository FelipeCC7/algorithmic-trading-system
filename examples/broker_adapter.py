"""
Broker Adapter Pattern Implementation
Demonstrates the architecture for multi-broker integration
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
from enum import Enum


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Order:
    """Unified order representation across all brokers"""
    symbol: str
    side: OrderSide
    quantity: float
    order_type: OrderType
    price: Optional[float] = None
    stop_price: Optional[float] = None
    metadata: Dict[str, Any] = None


@dataclass
class ExecutionResult:
    """Standardized execution result"""
    order_id: str
    broker_order_id: str
    status: str
    executed_quantity: float
    executed_price: float
    timestamp: datetime
    fees: float
    metadata: Dict[str, Any] = None


@dataclass
class MarketData:
    """Unified market data structure"""
    symbol: str
    bid: float
    ask: float
    last_price: float
    volume: float
    timestamp: datetime


class BrokerAdapter(ABC):
    """
    Abstract base class for broker adapters
    Implements adapter pattern for multi-broker support
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connected = False
        self._rate_limiter = RateLimiter(
            calls_per_second=config.get('rate_limit', 10)
        )

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to broker"""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Close broker connection"""
        pass

    @abstractmethod
    async def execute_order(self, order: Order) -> ExecutionResult:
        """Execute order through broker API"""
        pass

    @abstractmethod
    async def get_market_data(self, symbol: str) -> MarketData:
        """Fetch current market data"""
        pass

    @abstractmethod
    async def get_positions(self) -> List[Dict[str, Any]]:
        """Get current open positions"""
        pass

    async def _apply_rate_limit(self):
        """Apply rate limiting to API calls"""
        await self._rate_limiter.acquire()


class RateLimiter:
    """Simple rate limiter for API calls"""

    def __init__(self, calls_per_second: int):
        self.calls_per_second = calls_per_second
        self.semaphore = asyncio.Semaphore(calls_per_second)
        self.reset_time = 1.0 / calls_per_second

    async def acquire(self):
        async with self.semaphore:
            await asyncio.sleep(self.reset_time)


class MetaTraderAdapter(BrokerAdapter):
    """
    MetaTrader 5 broker adapter implementation
    Handles MT5-specific API calls and data transformation
    """

    async def connect(self) -> bool:
        """
        Establish connection to MetaTrader 5
        """
        # Simplified for demonstration
        print(f"Connecting to MT5 with config: {self.config['server']}")
        await asyncio.sleep(0.1)  # Simulate connection time
        self.connected = True
        return True

    async def disconnect(self) -> bool:
        """Close MT5 connection"""
        print("Disconnecting from MT5")
        self.connected = False
        return True

    async def execute_order(self, order: Order) -> ExecutionResult:
        """
        Execute order through MT5 API
        Handles order transformation and result parsing
        """
        await self._apply_rate_limit()

        # Transform unified order to MT5 format
        mt5_order = self._transform_order_to_mt5(order)

        # Simulate execution (in production, this would call MT5 API)
        await asyncio.sleep(0.05)  # Simulate network latency

        # Return standardized result
        return ExecutionResult(
            order_id=f"INT_{datetime.now().timestamp()}",
            broker_order_id=f"MT5_{datetime.now().timestamp()}",
            status="FILLED",
            executed_quantity=order.quantity,
            executed_price=order.price or 1.2345,  # Simulated
            timestamp=datetime.now(),
            fees=order.quantity * 0.0001,  # Simulated commission
            metadata={"broker": "MT5", "latency_ms": 50}
        )

    async def get_market_data(self, symbol: str) -> MarketData:
        """Fetch market data from MT5"""
        await self._apply_rate_limit()

        # Simulate API call
        await asyncio.sleep(0.02)

        return MarketData(
            symbol=symbol,
            bid=1.2344,
            ask=1.2346,
            last_price=1.2345,
            volume=1000000,
            timestamp=datetime.now()
        )

    async def get_positions(self) -> List[Dict[str, Any]]:
        """Get open positions from MT5"""
        await self._apply_rate_limit()

        # Simulate API call
        await asyncio.sleep(0.03)

        return [
            {
                "symbol": "EURUSD",
                "quantity": 10000,
                "side": "BUY",
                "entry_price": 1.2340,
                "current_price": 1.2345,
                "pnl": 50.0
            }
        ]

    def _transform_order_to_mt5(self, order: Order) -> Dict[str, Any]:
        """Transform unified order to MT5 specific format"""
        return {
            "symbol": order.symbol,
            "action": order.side.value,
            "volume": order.quantity / 100000,  # Convert to lots
            "type": self._map_order_type(order.order_type),
            "price": order.price,
            "sl": order.stop_price
        }

    def _map_order_type(self, order_type: OrderType) -> int:
        """Map unified order type to MT5 constants"""
        mapping = {
            OrderType.MARKET: 0,
            OrderType.LIMIT: 1,
            OrderType.STOP: 2,
            OrderType.STOP_LIMIT: 3
        }
        return mapping.get(order_type, 0)


class BrokerFactory:
    """
    Factory pattern for creating broker adapters
    Simplifies multi-broker support
    """

    _adapters = {
        "mt5": MetaTraderAdapter,
        # Add more brokers as needed:
        # "interactive_brokers": InteractiveBrokersAdapter,
        # "binance": BinanceAdapter,
    }

    @classmethod
    def create_adapter(cls, broker_name: str, config: Dict[str, Any]) -> BrokerAdapter:
        """Create appropriate broker adapter based on name"""
        adapter_class = cls._adapters.get(broker_name.lower())
        if not adapter_class:
            raise ValueError(f"Unknown broker: {broker_name}")
        return adapter_class(config)


# Example usage
async def main():
    """Demonstration of multi-broker architecture"""

    # Demo credentials - not real
    # Create adapter for MT5
    config = {
        "server": "MetaQuotes-Demo",
        "login": 12345,
        "password": "demo",
        "rate_limit": 10
    }

    adapter = BrokerFactory.create_adapter("mt5", config)

    # Connect to broker
    await adapter.connect()

    # Create and execute order
    order = Order(
        symbol="EURUSD",
        side=OrderSide.BUY,
        quantity=10000,
        order_type=OrderType.MARKET
    )

    result = await adapter.execute_order(order)
    print(f"Execution result: {result}")

    # Get market data
    market_data = await adapter.get_market_data("EURUSD")
    print(f"Market data: {market_data}")

    # Get positions
    positions = await adapter.get_positions()
    print(f"Open positions: {positions}")

    # Disconnect
    await adapter.disconnect()


if __name__ == "__main__":
    asyncio.run(main())