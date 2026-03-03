Monte Carlo Portfolio Optimization – Indian Equity Markets
Objective

To construct and evaluate an optimal portfolio of 30 Indian large-cap equities using Modern Portfolio Theory (MPT), Monte Carlo simulation, and advanced risk metrics.

The objective is to identify the portfolio that maximizes the Sharpe Ratio while managing volatility, beta exposure, and drawdown risk.

Methodology

Collected historical adjusted closing price data using yfinance

Computed daily log returns

Annualized returns and volatility using 252 trading days

Generated 50,000 random portfolios via Monte Carlo simulation

Calculated the following metrics for each portfolio:

Expected Annual Return

Annual Volatility

Sharpe Ratio

Sortino Ratio

Beta vs NIFTY 50

Maximum Drawdown

Identified the Maximum Sharpe Ratio portfolio

Backtested cumulative performance against NIFTY 50 (^NSEI)

Key Results

Maximum Sharpe Ratio: approximately 0.87–1.00

Expected Annual Return: approximately 21–24%

Annual Volatility: approximately 16–17%

Beta vs NIFTY 50: approximately 0.95

Maximum Drawdown: approximately 35–36%

The optimized portfolio demonstrated superior risk-adjusted performance relative to the benchmark over the evaluation period.

Project Structure
Monte-Carlo-Portfolio-Optimization/
│
├── src/
│   └── portfolio_optimization.py
│
├── outputs/
│   └── efficient_frontier.png
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

Clone the repository:

git clone https://github.com/your-username/Monte-Carlo-Portfolio-Optimization.git

Install dependencies:

pip install -r requirements.txt

Run the script:

python src/portfolio_optimization.py
Benchmark and Assumptions

Benchmark: NIFTY 50 Index (^NSEI)

Risk-Free Rate: Indian 10-Year Government Bond

Trading Days Assumed per Year: 252

Outcome

This project demonstrates practical implementation of quantitative portfolio optimization techniques using real-world Indian equity market data. It reflects applied understanding of financial risk modeling, asset allocation, and performance evaluation.
