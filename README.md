# Gavin Berger Senior Project - CSCI 4960

## Designing and Testing Quantitative Trading Algorithms in QuantConnect Using SPY

This repository contains my senior project for **CSCI 4960** at the University of North Georgia. The project focuses on designing, backtesting, and evaluating quantitative trading algorithms using **QuantConnect**, **Python**, and **SPY**, the SPDR S&P 500 ETF Trust.

The purpose of this project was to explore how rule-based trading systems can be built using technical indicators, historical market data, automated execution logic, and risk management rules.

---

## Project Overview

This project compares three SPY-based quantitative trading algorithms. Each algorithm uses a different trading approach to test how signal design, timing, and risk controls affect performance.

The project began with a faster short-term moving average crossover strategy. After testing that baseline model, the project moved toward more selective strategies that used trend filters, pullback signals, recovery triggers, exponential moving averages, ATR-based risk management, and stop-loss protection.

The final project evaluates each algorithm using backtest results and performance metrics such as:

- Net profit
- Drawdown
- Win rate
- Average win
- Average loss
- Sharpe ratio
- Profit-loss ratio
- Total orders
- Trade frequency
- Expectancy

---

## Tools and Technologies

- Python
- QuantConnect
- Lean Algorithmic Trading Engine
- SPY historical market data
- Technical indicators
- Backtesting
- GitHub
- Overleaf / LaTeX
- PowerPoint

---

## Repository Contents

| File | Description |
|---|---|
| `main.py` | Main QuantConnect algorithm file |
| `Creative Yellow-Green Panda.py` | Algorithm 1: 15-minute 9/21 SMA crossover strategy |
| `Fat Orange Chinchilla.py` | Algorithm 2: Trend, RSI pullback, and EMA recovery strategy |
| `Alert Magenta Rat.py` | Algorithm 3: 20/50 EMA strategy with 200 EMA trend filter |
| `.json` files | QuantConnect project/backtest result files |
| `QuantConnect__Gavin_Berger_Senior_ProjectPresentation.pptx` | Final project presentation |
| `README.md` | Project documentation |

---

# Algorithm 1: Creative Yellow-Green Panda

## Strategy Type

**15-minute 9/21 SMA crossover strategy**

## Description

Creative Yellow-Green Panda was the first major strategy developed for the project. It was designed as a medium-speed SPY trading model that uses short-term moving average crossover signals on 15-minute price bars.

Instead of using daily candles, the strategy consolidates minute data into 15-minute bars. This allows the algorithm to react faster to short-term market movement while still avoiding extremely high-frequency trading.

## Indicators Used

- 9-period Simple Moving Average
- 21-period Simple Moving Average
- 15-minute consolidated SPY bars

## Trading Logic

The algorithm enters a long position when the 9-period SMA crosses above the 21-period SMA. It exits when the 9-period SMA crosses below the 21-period SMA.

The strategy also includes stop-loss, take-profit, cooldown, and allocation rules to manage risk.

## Risk Management

- 1% stop loss
- 2% take profit target
- 60-minute cooldown after exits
- Maximum allocation of 95%
- Long-only trading

## Backtest Results

| Metric | Result |
|---|---:|
| Starting Equity | $100,000.00 |
| Ending Equity | $120,771.07 |
| Net Profit | 20.77% |
| Maximum Drawdown | 9.20% |
| Total Orders | 889 |
| Win Rate | 41% |
| Profit-Loss Ratio | 1.72 |
| Sharpe Ratio | -0.081 |
| Trade Frequency | 298.88 trades per year |

## Summary

Algorithm 1 produced a positive return, but it placed a high number of trades. This showed that the strategy was profitable, but also exposed to short-term market noise. The negative Sharpe ratio suggested that the risk-adjusted performance still needed improvement.

---

# Algorithm 2: Fat Orange Chinchilla

## Strategy Type

**Long-only SPY swing trading strategy using trend, pullback, and recovery signals**

## Description

Fat Orange Chinchilla was designed to be more selective than Algorithm 1. Instead of entering trades based only on a crossover, this strategy requires multiple conditions before entering a position.

The strategy uses a broader trend filter, an RSI pullback signal, and an EMA recovery trigger. This makes it a more complete swing trading system.

## Indicators Used

- 50-day Simple Moving Average
- 200-day Simple Moving Average
- Relative Strength Index
- 20-day Exponential Moving Average
- Average True Range

## Trading Logic

The algorithm first checks whether SPY is in a broader uptrend using the 50-day SMA and 200-day SMA. If the 50-day SMA is above the 200-day SMA, the market is treated as being in an uptrend.

The algorithm then looks for an RSI oversold condition to identify a pullback. After the pullback, the strategy waits for price to recover above the 20-day EMA before entering a trade.

## Risk Management

- ATR-based stop loss
- Partial profit taking at 5% gain
- Trailing stop after partial profit
- Maximum 20-day holding period
- 3-day cooldown after exits
- Long-only trading

## Backtest Results

| Metric | Result |
|---|---:|
| Starting Equity | $100,000.00 |
| Ending Equity | $104,926.22 |
| Net Profit | 4.93% |
| Compounding Annual Return | 1.454% |
| Maximum Drawdown | 11.40% |
| Total Orders | 10 |
| Win Rate | 83% |
| Loss Rate | 17% |
| Average Win | 2.77% |
| Average Loss | -8.46% |
| Profit-Loss Ratio | 0.33 |
| Expectancy | 0.106 |
| Sharpe Ratio | -1.084 |
| Sortino Ratio | -0.228 |
| Total Fees | $10.13 |

## Summary

Algorithm 2 had the highest win rate, but the average loss was much larger than the average win. This showed that win rate alone is not enough to judge a trading strategy. Even though the strategy was profitable, its drawdown and risk-adjusted performance were weaker than expected.

---

# Algorithm 3: Alert Magenta Rat

## Strategy Type

**Daily 20/50 EMA strategy with 200 EMA trend filter**

## Description

Alert Magenta Rat was the strongest overall strategy in the project. It was designed to create a more balanced SPY trading system by using exponential moving averages and a long-term trend filter.

This strategy uses a daily 20/50 EMA signal structure with a 200 EMA trend filter. It also includes ATR-based position sizing and intraday stop-loss monitoring.

## Indicators Used

- 20-day Exponential Moving Average
- 50-day Exponential Moving Average
- 200-day Exponential Moving Average
- Average True Range
- Minute data for intraday risk monitoring

## Trading Logic

The algorithm enters a long position when the 20 EMA crosses above the 50 EMA while SPY is also above the 200 EMA. This confirms both short-term momentum and broader trend strength.

The algorithm exits when the 20 EMA crosses below the 50 EMA or when the stop-loss condition is triggered.

## Risk Management

- 5% stop loss
- ATR-based volatility-adjusted position sizing
- Daily signal check near market close
- Intraday stop-loss monitoring using minute data
- Long-only trading
- 200 EMA trend filter to avoid weaker market conditions

## Backtest Results

| Metric | Result |
|---|---:|
| Starting Equity | $100,000.00 |
| Ending Equity | $131,593.01 |
| Net Profit | 31.593% |
| Compounding Annual Return | 6.545% |
| Drawdown | 7.60% |
| Total Orders | 13 |
| Win Rate | 67% |
| Loss Rate | 33% |
| Average Win | 8.31% |
| Average Loss | -2.45% |
| Profit-Loss Ratio | 3.39 |
| Expectancy | 1.927 |
| Sharpe Ratio | 0.011 |
| Sortino Ratio | 0.010 |
| Total Fees | $13.00 |

## Summary

Algorithm 3 produced the best overall results. It had the highest net profit, the lowest drawdown, and the strongest profit-loss ratio. It was also much more selective than Algorithm 1, placing only 13 orders while still outperforming the other strategies.

---

# Algorithm Comparison

| Metric | Algorithm 1 | Algorithm 2 | Algorithm 3 |
|---|---:|---:|---:|
| Strategy Name | Creative Yellow-Green Panda | Fat Orange Chinchilla | Alert Magenta Rat |
| Strategy Type | 15-minute 9/21 SMA crossover | Trend, RSI pullback, EMA recovery | 20/50 EMA with 200 EMA filter |
| Main Asset | SPY | SPY | SPY |
| Trade Style | Medium-speed long-only | Swing trading long-only | Trend-following long-only |
| Trade Count | 889 orders | 10 orders | 13 orders |
| Win Rate | 41% | 83% | 67% |
| Average Win | Not provided | 2.77% | 8.31% |
| Average Loss | Not provided | -8.46% | -2.45% |
| Max Drawdown | 9.20% | 11.40% | 7.60% |
| Net Profit | 20.77% | 4.93% | 31.593% |
| Sharpe Ratio | -0.081 | -1.084 | 0.011 |
| Profit-Loss Ratio | 1.72 | 0.33 | 3.39 |

---

# Key Findings

The project showed that a profitable trading algorithm is not always the strongest strategy. Each algorithm had different strengths and weaknesses.

Algorithm 1 produced a solid return, but it traded too frequently and had weak risk-adjusted performance.

Algorithm 2 had the highest win rate, but its average loss was much larger than its average win. This made the strategy less reliable even though it was profitable.

Algorithm 3 had the best balance of return, drawdown control, trade quality, and selectivity. It produced the highest net profit while placing far fewer trades than Algorithm 1.

---

# What I Learned

This project helped me better understand how computer science can be applied to financial technology. I learned how to design trading algorithms, work with historical market data, evaluate backtest results, and debug strategy logic.

The project also showed that algorithmic trading is not only about writing code that buys and sells assets. A strong strategy must also manage risk, control losses, avoid misleading backtest results, and be evaluated using multiple performance metrics.

Important lessons from the project include:

- Total profit does not tell the full story
- Win rate can be misleading
- Drawdown is important for understanding risk
- Small implementation issues can change backtest results
- Risk management is just as important as entry logic
- A strategy needs enough trades to judge reliability
- Backtesting is useful, but results must be interpreted carefully

---

# Future Improvements

Possible future improvements include:

- Testing the strategies on more assets besides SPY
- Comparing each strategy directly against buy-and-hold SPY
- Improving stop-loss and position sizing logic
- Testing the strategies in bull, bear, and sideways markets
- Running longer live paper trading tests
- Building a dashboard to compare backtest results
- Adding stronger benchmark analysis
- Collecting more trades to improve reliability

---

# Disclaimer

This project was created for educational purposes only. The algorithms in this repository are not financial advice and should not be used for live trading without additional testing, validation, and risk review.

---

# Author

**Gavin Berger**  
Computer Science Student  
University of North Georgia  
CSCI 4960 Senior Project  
May 2026
