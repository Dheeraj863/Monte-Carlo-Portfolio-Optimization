# Monte Carlo Portfolio Optimization – Indian Equity Markets

## Objective

To construct and evaluate an optimal portfolio of 30 Indian large-cap equities using Modern Portfolio Theory (MPT) and Monte Carlo simulation.

The goal is to identify the portfolio that maximizes the Sharpe Ratio while controlling volatility, beta exposure, and drawdown risk.

---

## Methodology

1. Collected historical adjusted close prices using `yfinance`
2. Computed daily returns
3. Annualized return and volatility using 252 trading days
4. Generated 50,000 random portfolios (Monte Carlo simulation)
5. Calculated for each portfolio:
   - Expected Annual Return
   - Annual Volatility
   - Sharpe Ratio
   - Sortino Ratio
   - Beta vs NIFTY 50
   - Maximum Drawdown
6. Selected portfolio with highest Sharpe Ratio
7. Backtested performance vs benchmark (^NSEI)

---

## Key Results

| Metric                     | Approximate Value |
|----------------------------|------------------|
| Maximum Sharpe Ratio       | 0.87 – 1.00      |
| Expected Annual Return     | 21% – 24%        |
| Annual Volatility          | 16% – 17%        |
| Beta vs NIFTY 50           | ~0.95            |
| Maximum Drawdown           | 35% – 36%        |

The optimized portfolio demonstrated superior risk-adjusted performance relative to the benchmark during the evaluation period.

---


---

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- yfinance

---

## How to Run

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/Monte-Carlo-Portfolio-Optimization.git

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the script
python src/portfolio_optimization.py

---

## Benchmark and Assumptions

- Benchmark: NIFTY 50 Index (^NSEI)
- Risk-Free Rate: Indian 10-Year Government Bond
- Trading Days per Year: 252
- Number of Portfolios Simulated: 50,000
