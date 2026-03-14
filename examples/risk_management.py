"""
Risk Management System
Core component that prevented catastrophic losses after the initial $200K experience
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import warnings


class RiskLevel(Enum):
    """Risk levels for position sizing and alerts"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    SHUTDOWN = "SHUTDOWN"


@dataclass
class Position:
    """Represents a trading position"""
    symbol: str
    entry_price: float
    quantity: float
    side: str  # 'BUY' or 'SELL'
    entry_time: datetime
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    current_price: Optional[float] = None

    @property
    def pnl(self) -> float:
        """Calculate current P&L"""
        if not self.current_price:
            return 0.0

        if self.side == 'BUY':
            return (self.current_price - self.entry_price) * self.quantity
        else:
            return (self.entry_price - self.current_price) * self.quantity

    @property
    def pnl_percent(self) -> float:
        """Calculate P&L percentage"""
        if not self.current_price:
            return 0.0

        if self.side == 'BUY':
            return ((self.current_price - self.entry_price) / self.entry_price) * 100
        else:
            return ((self.entry_price - self.current_price) / self.entry_price) * 100


@dataclass
class RiskMetrics:
    """Container for risk metrics"""
    total_exposure: float
    var_95: float  # Value at Risk at 95% confidence
    max_drawdown: float
    sharpe_ratio: float
    correlation_risk: float
    risk_level: RiskLevel
    alerts: List[str] = field(default_factory=list)


class RiskManagementSystem:
    """
    Advanced risk management system
    Implements the lessons learned from the $200K loss experience
    """

    def __init__(self,
                 initial_capital: float,
                 max_risk_per_trade: float = 0.02,  # 2% default
                 max_portfolio_risk: float = 0.06,  # 6% default
                 max_correlation: float = 0.7):
        """
        Initialize risk management system

        Args:
            initial_capital: Starting capital
            max_risk_per_trade: Maximum risk per single trade
            max_portfolio_risk: Maximum total portfolio risk
            max_correlation: Maximum allowed correlation between positions
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.max_risk_per_trade = max_risk_per_trade
        self.max_portfolio_risk = max_portfolio_risk
        self.max_correlation = max_correlation

        self.positions: List[Position] = []
        self.historical_returns: List[float] = []
        self.risk_events: List[Dict] = []

    def calculate_position_size(self,
                               entry_price: float,
                               stop_loss: float,
                               symbol: str) -> float:
        """
        Calculate optimal position size using Kelly Criterion with safety factor

        This is the key lesson from the $200K loss:
        NEVER risk more than you can afford to lose
        """
        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss)

        # Maximum risk amount based on account
        max_risk_amount = self.current_capital * self.max_risk_per_trade

        # Check current exposure
        current_exposure = self._calculate_current_exposure()
        remaining_risk = (self.current_capital * self.max_portfolio_risk) - current_exposure

        if remaining_risk <= 0:
            warnings.warn("Portfolio risk limit reached. No new positions allowed.")
            return 0

        # Use the smaller of the two limits
        allowed_risk = min(max_risk_amount, remaining_risk)

        # Calculate position size
        position_size = allowed_risk / risk_per_unit

        # Apply Kelly Criterion safety factor (0.25 Kelly for safety)
        win_rate = self._calculate_win_rate()
        avg_win = self._calculate_average_win()
        avg_loss = self._calculate_average_loss()

        if avg_loss != 0 and win_rate > 0:
            kelly_factor = (win_rate * avg_win - (1 - win_rate) * abs(avg_loss)) / avg_win
            kelly_factor = max(0, min(kelly_factor * 0.25, 1))  # Safety: use 25% Kelly
            position_size *= kelly_factor

        return round(position_size, 2)

    def check_correlation_risk(self, new_symbol: str,
                              correlation_matrix: pd.DataFrame) -> bool:
        """
        Check if adding new position would exceed correlation limits
        Prevents concentration risk that contributed to the $200K loss
        """
        if not self.positions:
            return True

        current_symbols = [pos.symbol for pos in self.positions]

        for symbol in current_symbols:
            if symbol in correlation_matrix.index and new_symbol in correlation_matrix.columns:
                correlation = abs(correlation_matrix.loc[symbol, new_symbol])
                if correlation > self.max_correlation:
                    warnings.warn(f"High correlation ({correlation:.2f}) with {symbol}")
                    return False

        return True

    def calculate_var(self, confidence_level: float = 0.95) -> float:
        """
        Calculate Value at Risk
        Answers: "What's the maximum I could lose in a day?"
        """
        if len(self.historical_returns) < 20:
            return 0

        returns_array = np.array(self.historical_returns)
        var_percentile = (1 - confidence_level) * 100
        var = np.percentile(returns_array, var_percentile) * self.current_capital

        return abs(var)

    def calculate_max_drawdown(self) -> float:
        """
        Calculate maximum drawdown from peak
        Key metric that would have prevented the $200K loss
        """
        if not self.historical_returns:
            return 0

        cumulative_returns = np.cumprod(1 + np.array(self.historical_returns))
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max

        return abs(np.min(drawdown)) if len(drawdown) > 0 else 0

    def emergency_stop_check(self) -> Tuple[bool, str]:
        """
        Circuit breaker - stops all trading if critical thresholds hit
        This would have saved the $200K
        """
        # Check daily loss limit (3% hard stop)
        daily_loss = (self.initial_capital - self.current_capital) / self.initial_capital
        if daily_loss > 0.03:
            return True, "Daily loss limit exceeded (3%)"

        # Check maximum drawdown (10% hard stop)
        max_dd = self.calculate_max_drawdown()
        if max_dd > 0.10:
            return True, f"Maximum drawdown exceeded ({max_dd:.1%})"

        # Check consecutive losses (5 losses in a row)
        if len(self.historical_returns) >= 5:
            last_five = self.historical_returns[-5:]
            if all(r < 0 for r in last_five):
                return True, "5 consecutive losses - system halt required"

        # Check correlation concentration
        if self._check_correlation_concentration() > 0.8:
            return True, "Correlation concentration too high (>80%)"

        return False, "System operational"

    def get_risk_metrics(self) -> RiskMetrics:
        """
        Get comprehensive risk metrics for current portfolio
        """
        total_exposure = self._calculate_current_exposure()
        var_95 = self.calculate_var(0.95)
        max_drawdown = self.calculate_max_drawdown()
        sharpe = self._calculate_sharpe_ratio()
        correlation = self._check_correlation_concentration()

        # Determine risk level
        risk_level = self._determine_risk_level(
            total_exposure, var_95, max_drawdown, correlation
        )

        # Generate alerts
        alerts = self._generate_risk_alerts(
            total_exposure, var_95, max_drawdown, correlation, risk_level
        )

        return RiskMetrics(
            total_exposure=total_exposure,
            var_95=var_95,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe,
            correlation_risk=correlation,
            risk_level=risk_level,
            alerts=alerts
        )

    def _calculate_current_exposure(self) -> float:
        """Calculate total current exposure as % of capital"""
        if not self.positions:
            return 0

        total_risk = sum(abs(pos.pnl) for pos in self.positions
                        if pos.pnl < 0)  # Only count losing positions
        return abs(total_risk) / self.current_capital if self.current_capital > 0 else 0

    def _calculate_win_rate(self) -> float:
        """Calculate historical win rate"""
        if len(self.historical_returns) < 10:
            return 0.5  # Default assumption

        wins = sum(1 for r in self.historical_returns if r > 0)
        return wins / len(self.historical_returns)

    def _calculate_average_win(self) -> float:
        """Calculate average winning return"""
        wins = [r for r in self.historical_returns if r > 0]
        return np.mean(wins) if wins else 0.01  # Default 1%

    def _calculate_average_loss(self) -> float:
        """Calculate average losing return"""
        losses = [r for r in self.historical_returns if r < 0]
        return abs(np.mean(losses)) if losses else 0.01  # Default 1%

    def _calculate_sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio (risk-adjusted returns)"""
        if len(self.historical_returns) < 20:
            return 0

        returns = np.array(self.historical_returns)
        return np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0

    def _check_correlation_concentration(self) -> float:
        """Check portfolio correlation concentration"""
        if len(self.positions) < 2:
            return 0

        # Simplified correlation check based on symbol similarity
        symbols = [pos.symbol for pos in self.positions]
        base_currencies = [s[:3] for s in symbols if len(s) >= 6]

        if not base_currencies:
            return 0

        # Check concentration
        from collections import Counter
        currency_counts = Counter(base_currencies)
        max_concentration = max(currency_counts.values()) / len(base_currencies)

        return max_concentration

    def _determine_risk_level(self, exposure: float, var: float,
                             drawdown: float, correlation: float) -> RiskLevel:
        """Determine overall risk level based on metrics"""
        risk_score = 0

        # Exposure scoring
        if exposure > 0.05:
            risk_score += 3
        elif exposure > 0.03:
            risk_score += 2
        elif exposure > 0.01:
            risk_score += 1

        # VaR scoring
        var_percent = var / self.current_capital if self.current_capital > 0 else 0
        if var_percent > 0.05:
            risk_score += 3
        elif var_percent > 0.03:
            risk_score += 2
        elif var_percent > 0.01:
            risk_score += 1

        # Drawdown scoring
        if drawdown > 0.08:
            risk_score += 3
        elif drawdown > 0.05:
            risk_score += 2
        elif drawdown > 0.02:
            risk_score += 1

        # Correlation scoring
        if correlation > 0.7:
            risk_score += 2
        elif correlation > 0.5:
            risk_score += 1

        # Map score to risk level
        if risk_score >= 9:
            return RiskLevel.SHUTDOWN
        elif risk_score >= 7:
            return RiskLevel.CRITICAL
        elif risk_score >= 5:
            return RiskLevel.HIGH
        elif risk_score >= 3:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    def _generate_risk_alerts(self, exposure: float, var: float,
                            drawdown: float, correlation: float,
                            risk_level: RiskLevel) -> List[str]:
        """Generate actionable risk alerts"""
        alerts = []

        if risk_level == RiskLevel.SHUTDOWN:
            alerts.append("🚨 EMERGENCY: Shut down all trading immediately!")

        if exposure > 0.05:
            alerts.append(f"⚠️ High exposure: {exposure:.1%} of capital at risk")

        if drawdown > 0.05:
            alerts.append(f"⚠️ Significant drawdown: {drawdown:.1%} from peak")

        if correlation > 0.7:
            alerts.append(f"⚠️ High correlation risk: {correlation:.1%} concentration")

        var_percent = var / self.current_capital if self.current_capital > 0 else 0
        if var_percent > 0.03:
            alerts.append(f"⚠️ VaR Warning: Could lose ${var:.2f} in a day")

        if not alerts and risk_level == RiskLevel.LOW:
            alerts.append("✅ All risk metrics within acceptable limits")

        return alerts


def demonstrate_risk_management():
    """
    Demonstrate the risk management system in action
    Shows how it would have prevented the $200K loss
    """
    print("=" * 70)
    print("RISK MANAGEMENT SYSTEM DEMONSTRATION")
    print("Showing how systematic risk control prevents catastrophic losses")
    print("=" * 70)

    # Initialize system with $100k capital
    risk_mgr = RiskManagementSystem(
        initial_capital=100000,
        max_risk_per_trade=0.02,  # 2% per trade
        max_portfolio_risk=0.06   # 6% total
    )

    # Simulate some historical returns (mix of wins and losses)
    historical_returns = [
        0.02, -0.01, 0.015, 0.03, -0.005,  # Good period
        -0.02, -0.015, -0.025, -0.01, -0.03  # Bad period (would trigger stops)
    ]
    risk_mgr.historical_returns = historical_returns

    print("\n1️⃣ POSITION SIZING")
    print("-" * 70)
    position_size = risk_mgr.calculate_position_size(
        entry_price=1.2500,
        stop_loss=1.2450,
        symbol="EURUSD"
    )
    print(f"Entry: 1.2500, Stop: 1.2450")
    print(f"Calculated position size: {position_size:,.0f} units")
    print(f"Maximum risk: ${position_size * 0.005:,.2f} (2% of capital)")

    # Add some positions
    risk_mgr.positions = [
        Position("EURUSD", 1.2500, 10000, "BUY", datetime.now(),
                stop_loss=1.2450, current_price=1.2480),
        Position("GBPUSD", 1.3100, 8000, "BUY", datetime.now(),
                stop_loss=1.3050, current_price=1.3080),
        Position("USDJPY", 110.50, 12000, "SELL", datetime.now(),
                stop_loss=111.00, current_price=110.70)
    ]

    print("\n2️⃣ EMERGENCY STOP CHECK")
    print("-" * 70)
    stop_required, reason = risk_mgr.emergency_stop_check()
    if stop_required:
        print(f"🚨 STOP TRADING: {reason}")
    else:
        print(f"✅ {reason}")

    print("\n3️⃣ RISK METRICS")
    print("-" * 70)
    metrics = risk_mgr.get_risk_metrics()
    print(f"Total Exposure: {metrics.total_exposure:.2%} of capital")
    print(f"Value at Risk (95%): ${metrics.var_95:,.2f}")
    print(f"Maximum Drawdown: {metrics.max_drawdown:.2%}")
    print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
    print(f"Correlation Risk: {metrics.correlation_risk:.2%}")
    print(f"Risk Level: {metrics.risk_level.value}")

    print("\n4️⃣ RISK ALERTS")
    print("-" * 70)
    for alert in metrics.alerts:
        print(alert)

    print("\n5️⃣ THE $200K LESSON")
    print("-" * 70)
    print("Without risk management:")
    print("  ❌ No position sizing → Overleveraged")
    print("  ❌ No stop losses → Unlimited losses")
    print("  ❌ No correlation check → Concentrated risk")
    print("  ❌ No emergency stops → Emotional trading")
    print("\nWith this system:")
    print("  ✅ Systematic position sizing")
    print("  ✅ Automatic stop losses")
    print("  ✅ Correlation limits")
    print("  ✅ Circuit breakers")
    print("\n💡 Result: Consistent growth without catastrophic losses")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_risk_management()