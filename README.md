# Algorithmic Trading System - From Manual to Machine Learning 🚀

> A complete trading system evolution: From emotional manual trading to cloud-based ML-powered algorithmic execution

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org)
[![Oracle](https://img.shields.io/badge/Oracle-ADB-red.svg)](https://www.oracle.com/cloud/)
[![Performance](https://img.shields.io/badge/Performance-25x_Optimized-green.svg)](https://github.com)
[![ML](https://img.shields.io/badge/ML-LSTM_Geometry-purple.svg)](https://github.com)

## 🎯 Project Overview

This repository showcases a 5-year journey building a production algorithmic trading system that evolved through 7 major architectural iterations, from manual trading on BM&F Bovespa to a cloud-based ML-powered platform processing multiple markets simultaneously.

### The Evolution at a Glance

```
Manual Trading (2019) → MQL5 Expert Advisors (2020) → Excel/VBA Hybrid (2021)
→ Python Integration (2022) → Local MySQL (2023) → Oracle Cloud (2024) → ML/LSTM (Current)
```

### Current System Capabilities

- **Markets**: Forex, Futures, Multiple Brokers (MT5)
- **Scale**: 750K+ historical records ETL, 50-100 candles/second real-time
- **Intelligence**: LSTM models with geometry pattern extraction
- **Infrastructure**: Oracle Autonomous Database on OCI
- **Performance**: 25x faster processing, sub-100ms execution
- **Capital Managed**: From $6K to peak $200K, current $40K systematic

## 📈 The Complete Evolution Story

### Stage 1: Manual Trading (2019)
**Platform**: BM&F Bovespa futures mini contracts
**Strategy**: Smart Money Concepts (SMC) with Price Action

**Challenges Faced**:
- Extremely time and emotion consuming
- Scalable in position size but impossible to manage multiple symbols
- Required constant screen time and expertise in execution
- **Result**: Reached $200K but lost it all to emotions

**Key Learning**: "Trading is viable without emotions. Emotion moves me, but shouldn't move the operator."

### Stage 2: MQL5 Expert Advisors (2020)
**Technology**: MetaQuotes Language 5 (MQL5)
**Purpose**: Automate strategy and remove emotions

**Architecture**:
```
[MT5 Terminal] → [Expert Advisor] → [Trade Execution]
```

**Limitations Discovered**:
- No history of calculations for each entry
- Couldn't directly model time series
- Hard to scale across brokers
- Black box - no visibility into decision process

### Stage 3: Excel/VBA + MQL5 Hybrid (2021)
**Innovation**: Blended MQL5 for execution with Excel for calculations

**Architecture**:
```
[MT5 Data] → [Excel Calculations] → [VBA Logic] → [MQL5 Execution]
         ↓
    [Limited History Window]
```

**Improvements**:
- Gained insights into dataset windows
- Fast parameter testing without recompiling MQL5
- More flexibility in modeling

**Remaining Issues**:
- Excel limited to window snapshots
- Not scalable to multiple symbols/brokers
- Calculation time bottlenecks

### Stage 4: Python + Excel Transition (2022)
**Breakthrough**: Dropped Expert Advisors, used Python with MQL5 library

**Architecture**:
```
[MT5 API] → [Python (RAM)] → [Excel Parameters] → [Execution]
```

**Advances**:
- All calculations in RAM (faster)
- More sophisticated parameter modeling
- Better integration possibilities

**Missing Pieces**:
- No structured data lake
- Limited support for data science
- No capability for neural networks

### Stage 5: Local MySQL Database (2023)
**Major Upgrade**: Implemented local database for full history

**Architecture**:
```
[MT5 Feed] → [Python ETL] → [MySQL Local] → [Analysis]
                    ↓              ↓
            [Bulk Historical]  [Runtime Data]
```

**Achievements**:
- Full historical data storage (750K+ records)
- Bulk load functions for backtesting
- Data modeling capabilities unlocked
- Foundation for data science

**Constraints**:
- Local machine limitations
- Availability issues (downtime)
- Scaling bottlenecks

### Stage 6: Oracle Cloud Migration (2024 - Current)
**Cloud Native**: Moved to Oracle Autonomous Database on OCI

**Current Architecture**:
```
┌─────────────────────────────────────────────────────────────────────┐
│                     CLOUD-BASED ALGORITHMIC TRADING                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📊 DATA SOURCES          🧠 PROCESSING           📈 EXECUTION       │
│  ┌──────────────┐      ┌──────────────┐       ┌──────────────┐     │
│  │ MT5 Brokers  │      │ Strategy     │       │ Order Mgmt   │     │
│  │ - XM         │──────│ Engine       │───────│ System       │     │
│  │ - Exness     │      │ - SMC        │       │              │     │
│  │ - IC Markets │      │ - Geometry   │       └──────────────┘     │
│  └──────────────┘      └──────────────┘              ↓             │
│         ↓                     ↓                ┌──────────────┐     │
│  ┌──────────────┐      ┌──────────────┐       │ Multi-Broker │     │
│  │ Oracle ADB   │      │ ML/LSTM      │       │ Execution    │     │
│  │ - Historical │◄─────│ - Pattern    │       │ Layer        │     │
│  │ - Real-time  │      │ - Prediction │       └──────────────┘     │
│  │ - DBeaver    │      └──────────────┘                            │
│  └──────────────┘                                                   │
│         ↓                                                            │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                    Oracle APEX Dashboard                    │    │
│  │  • Performance Metrics  • P&L Tracking  • Risk Monitoring   │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

**Current Capabilities**:
- Full cloud scalability
- SMC strategy running at full scale
- Data science at the core
- Geometry Extraction paper implementation
- LSTM feature engineering deployed

### Stage 7: Vision - Continuous Strategy Evolution
**Target Architecture**:

```
[New Strategy] → [Validation Pipeline] → [Backtesting] → [Approval]
                                                              ↓
                                                    [Strategy Library]
                                                              ↓
                                                    [Symbol Matrix]
                                                              ↓
                                              [Continuous Recalibration]
```

**Planned Features**:
- Multiple strategies running simultaneously
- Automatic strategy validation and backtesting
- Continuous recalibration based on performance
- Market expansion (Futures, Forex, Crypto)
- Oracle APEX user interface for monitoring

## 🔬 Technical Deep Dive

### Geometry Extraction Innovation

Based on academic research, implementing pattern recognition through:
- **Geometric Analysis**: Identifying price action patterns mathematically
- **Feature Engineering**: Converting patterns to LSTM-ready features
- **ML Pipeline**: Training models on historical geometry patterns
- **Real-time Application**: Applying predictions to live market data

### Performance Optimizations Achieved

| Phase | Metric | Before | After | Improvement |
|-------|--------|--------|-------|-------------|
| Historical ETL | Data Load Time | 4+ hours | <10 minutes | **25x faster** |
| Historical ETL | Records/Hour | 30K | 4.5M (750K/10min) | **150x faster** |
| Live Trading | Order Execution | 2-3 seconds | <100ms | **25x faster** |
| Live Trading | Candle Processing | 1-2/second | 50-100/second | **50x faster** |
| Risk Management | Emotion Factor | Lost $200K | Systematic | **∞ better** |
| Infrastructure | Availability | 8 hours/day | 23.5 hours/day | **3x better** |
| Database | Local MySQL | Limited | Oracle ADB Cloud | **∞ scalability** |

## 🛠️ Technology Stack

### Core Technologies
- **Language**: Python 3.12 (asyncio, threading, multiprocessing)
- **Database**: Oracle Autonomous Database (ADB) on OCI
- **Database Tools**: DBeaver, Oracle SQL Developer, Wallet Authentication
- **Trading Platform**: MetaTrader 5 (MT5)

### Libraries & Frameworks
- **Trading**: MetaTrader5 Python API, Custom MQL5 integration
- **Data Processing**: Pandas, NumPy, Custom calculation packs
- **Machine Learning**: TensorFlow/Keras (LSTM), scikit-learn
- **Visualization**: Oracle APEX (planned), Plotly
- **Cloud**: Oracle Cloud Infrastructure (OCI)

### Development Environment
- **IDE**: VS Code with Python extensions
- **Notebooks**: Jupyter for strategy research
- **Version Control**: Git/GitHub
- **Testing**: Local → Staging (paper trading) → Production

## 📁 Repository Structure

```
algorithmic-trading-system/
├── 00_vsCode/                      # Core system files
│   ├── MainBoard.py               # Main execution engine
│   ├── CalculationsPack.py        # Trading calculations
│   └── Watchdog.py                # System monitoring
├── 03_Research_Paper_Geometry/     # Academic research implementation
│   ├── geometry_extraction.py     # Pattern recognition
│   ├── lstm_trading_model.py      # LSTM implementation
│   └── mt5_pattern_detector.py    # Real-time pattern detection
├── brokers/                        # Multi-broker integration
│   ├── base.py                    # Abstract broker interface
│   ├── mt5_broker.py              # MT5 implementation
│   ├── factory.py                 # Broker factory pattern
│   └── etl_pipeline.py            # Historical data ETL
├── database/                       # Database layer
│   ├── oracle_config.json         # ADB configuration
│   └── wallet_algotrading/        # Oracle wallet auth
├── strategies/                     # Trading strategies
│   ├── smc_strategy.py            # Smart Money Concepts
│   └── geometry_patterns.py       # Geometry-based signals
└── risk_management/                # Risk control systems
    ├── position_sizing.py          # Kelly criterion implementation
    └── drawdown_control.py        # Maximum drawdown limits
```

## 🎓 Key Lessons from the Journey

### 1. Evolution is Necessary
Each stage taught critical lessons that informed the next architecture. Starting simple (Excel/VBA) and evolving to cloud/ML was the right path.

### 2. Emotion Removal is Paramount
The $200K loss was the best tuition I ever paid. It forced the creation of a systematic approach.

### 3. Data is Everything
Moving from "no history" in MQL5 to full Oracle ADB was transformational. You can't improve what you don't measure.

### 4. Cloud Changes Everything
Local limitations (MySQL on laptop) vs cloud scalability (Oracle ADB) - night and day difference.

### 5. Continuous Learning
From Price Action theory to LSTM implementation - the learning never stops.

## 🚀 Current Status & Next Steps

### ✅ Completed
- Full cloud migration to Oracle ADB
- SMC strategy running in production
- Geometry extraction paper implemented
- LSTM models deployed
- Multi-broker support active

### 🔄 In Progress
- Oracle APEX dashboard development
- Additional strategy implementations
- Performance optimization for 100+ symbols
- Risk management refinements

### 📅 Future Roadmap
- Expand to cryptocurrency markets
- Implement portfolio-level risk management
- Build strategy marketplace
- API for third-party integrations
- Mobile monitoring app

## ⚠️ Risk Disclaimer

This repository demonstrates architectural patterns and technical implementation of an algorithmic trading system. Actual trading strategies and profit-generating logic are proprietary and not included. Past performance does not guarantee future results.

## 💡 Unique Value Proposition

What makes this system stand out:
1. **Complete Evolution Story**: Shows the full journey from manual to ML
2. **Real Money Experience**: Managed up to $200K, learned from real losses
3. **Academic Foundation**: Implementing research papers (Geometry Extraction)
4. **Cloud Native**: Built on Oracle Cloud, not just local scripts
5. **Production Ready**: Actually running with real capital, not just backtests

## 🤝 Connect

Interested in discussing:
- Algorithmic trading architecture
- Cloud migration strategies
- ML in trading systems
- Risk management approaches
- The journey from manual to algorithmic

Connect via [LinkedIn](https://www.linkedin.com/in/felipe-costa) for technical discussions.

---

*"From losing $200K manually to managing $40K systematically - the most expensive and valuable education in algorithmic trading"*