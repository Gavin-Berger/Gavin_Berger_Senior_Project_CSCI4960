# Gavin Berger Senior Project - CSCI 4960

## QuantConnect Algorithmic Trading Senior Project

This repository contains my senior project for **CSCI 4960** at the University of North Georgia. The project focuses on designing, testing, and comparing quantitative trading algorithms using **QuantConnect** and Python.

The goal of this project was to explore how rule-based trading strategies can be developed, backtested, and evaluated using historical market data. Each algorithm uses a different trading approach and risk management style to test how technical indicators can guide automated trading decisions.

---

## Project Overview

This senior project focuses on algorithmic trading with SPY, the SPDR S&P 500 ETF Trust. SPY was used because it tracks the S&P 500 and provides a strong market benchmark for testing trading strategies.

The project includes:

- Multiple QuantConnect trading algorithms
- Python-based strategy logic
- Backtesting results
- Risk management rules
- Performance comparison between strategies
- Final presentation materials

---

## Tools and Technologies

- **Python**
- **QuantConnect**
- **LEAN Algorithmic Trading Engine**
- **SPY ETF historical market data**
- **Technical indicators**
  - Simple Moving Average
  - Exponential Moving Average
  - Relative Strength Index
  - Average True Range
- **Backtesting**
- **GitHub**

---

## Repository Contents

| File | Description |
|---|---|
| `main.py` | Main QuantConnect algorithm file |
| `Alert Magenta Rat.py` | Moving average crossover strategy with trend filtering and ATR-based position sizing |
| `Creative Yellow-Green Panda.py` | Medium-speed SPY trend strategy using 15-minute bars and SMA crossovers |
| `Fat Orange Chinchilla.py` | SPY swing trading strategy using RSI pullbacks, moving averages, ATR stops, partial profit taking, and trailing stops |
| `Measured Violet Rhinoceros.json` | QuantConnect project/backtest data file |
| `Muscular Brown Jellyfish.json` | QuantConnect project/backtest data file |
| `Swimming Light Brown Sheep.json` | QuantConnect project/backtest data file |
| `QuantConnect__Gavin_Berger_Senior_ProjectPresentation.pptx` | Final project presentation |
| `README.md` | Project documentation |

---

## Algorithm 1: Moving Average Crossover Strategy

This strategy uses SPY and focuses on trend-following behavior. It compares a fast moving average against a slower moving average to detect bullish and bearish crossover signals.

### Main Features

- Trades SPY
- Uses moving average crossover logic
- Uses a long-term trend filter
- Uses ATR for volatility-based position sizing
- Includes stop-loss risk management
- Checks signals near market close

### Strategy Logic

The algorithm enters a long position when the fast moving average crosses above the slow moving average while the price is also above the long-term trend moving average. It exits when the fast moving average crosses below the slow moving average or when the stop-loss condition is triggered.

---

## Algorithm 2: Medium-Speed SPY Trend Strategy

This strategy uses 15-minute bars to create a faster trend-following system. Instead of using daily data only, it consolidates minute data into 15-minute candles and uses short-term SMA crossovers.

### Main Features

- Trades SPY
- Uses 15-minute consolidated bars
- Uses a 9-period Simple Moving Average
- Uses a 21-period Simple Moving Average
- Includes stop-loss and take-profit rules
- Uses a cooldown period to prevent overtrading

### Strategy Logic

The algorithm buys SPY when the fast SMA crosses above the slow SMA. It exits when the fast SMA crosses below the slow SMA, when the stop-loss is reached, or when the take-profit target is reached.

---

## Algorithm 3: SPY Swing Trading Strategy

This strategy uses daily data and combines multiple technical indicators to identify pullback opportunities during longer-term uptrends.

### Main Features

- Trades SPY
- Uses daily market data
- Uses 50-day SMA and 200-day SMA trend filters
- Uses RSI to detect oversold pullbacks
- Uses 20-day EMA as a recovery trigger
- Uses ATR-based stop losses
- Includes partial profit taking
- Includes trailing stop logic
- Includes maximum holding period and cooldown rules

### Strategy Logic

The algorithm looks for SPY to be in an uptrend based on the 50-day SMA being above the 200-day SMA. It then waits for RSI to become oversold and only enters after the price recovers above the 20-day EMA. The strategy manages risk using ATR-based stops, partial profit taking, and trailing stops.

---

## Backtesting

Each strategy was tested using QuantConnect’s backtesting environment. The backtests helped evaluate how each algorithm performed under historical market conditions.

Important performance metrics reviewed included:

- Total return
- Net profit
- Drawdown
- Win rate
- Sharpe ratio
- Sortino ratio
- Number of trades
- Profit-loss ratio
- Portfolio turnover

---

## What I Learned

Through this project, I learned how quantitative trading systems are built, tested, and improved. I also gained experience working with financial data, technical indicators, automated trading logic, and performance metrics.

This project helped connect computer science concepts with finance by applying:

- Automation
- Data analysis
- Object-oriented programming
- Algorithm design
- Risk management
- Testing and evaluation

---

## Future Improvements

Possible improvements for this project include:

- Testing the algorithms on more assets besides SPY
- Adding benchmark comparisons
- Improving position sizing logic
- Testing different market conditions
- Adding machine learning or statistical models
- Building a dashboard to compare strategy performance
- Improving file organization for each algorithm and result set

---

## Disclaimer

This project was created for educational purposes only. The algorithms in this repository are not financial advice and should not be used for live trading without further testing, validation, and risk review.

---

## Author

**Gavin Berger**  
Computer Science Student  
University of North Georgia  
CSCI 4960 Senior Project
