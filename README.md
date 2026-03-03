Monte Carlo Portfolio Optimization – Indian Equity Markets
Objective

To construct and evaluate an optimal portfolio of 30 Indian large-cap equities using Modern Portfolio Theory (MPT), Monte Carlo simulation, and risk-adjusted performance metrics.

The objective is to identify the portfolio that maximizes the Sharpe Ratio while controlling volatility, beta exposure, and drawdown risk.

Methodology

Historical adjusted closing price data collected using yfinance

Daily log returns computed

Returns and volatility annualized using 252 trading days

50,000 random portfolios generated using Monte Carlo simulation

For each portfolio, the following were calculated:

Expected Annual Return

Annual Volatility

Sharpe Ratio

Sortino Ratio

Beta vs NIFTY 50

Maximum Drawdown

The Maximum Sharpe Ratio portfolio was selected

Performance backtested against NIFTY 50 (^NSEI)

Key Results

Maximum Sharpe Ratio: approximately 0.87 – 1.00

Expected Annual Return: approximately 21% – 24%

Annual Volatility: approximately 16% – 17%

Beta vs NIFTY 50: approximately 0.95

Maximum Drawdown: approximately 35% – 36%

The optimized portfolio demonstrated superior risk-adjusted performance relative to the benchmark during the evaluation period.

Project Structure

Monte-Carlo-Portfolio-Optimization
│
├── src
│ └── portfolio_optimization.py
│
├── outputs
│ └── efficient_frontier.png
│
├── requirements.txt
└── README.md

Concepts Applied

Modern Portfolio Theory (Markowitz Framework)

Efficient Frontier

Sharpe Ratio Optimization

Monte Carlo Simulation

Risk-Adjusted Performance Measurement

Beta Estimation

Drawdown Analysis

Portfolio Backtesting

Technologies Used

Python

NumPy

Pandas

Matplotlib

yfinance

How to Run

Clone the repository

Install dependencies using:
pip install -r requirements.txt

Run the script using:
python src/portfolio_optimization.py

Benchmark and Assumptions

Benchmark: NIFTY 50 Index (^NSEI)

Risk-Free Rate: Indian 10-Year Government Bond

Trading Days per Year Assumed: 252
