# Monte Carlo Portfolio Optimization – Indian Equity Markets

## Objective
To construct and evaluate an optimal portfolio of 30 Indian equities using Modern Portfolio Theory, Monte Carlo simulation, and advanced risk metrics.

---

## Market Universe
30 Large-Cap Indian Equities (NSE)

Benchmark: ^NSEI (NIFTY 50 Index)

Risk-Free Rate: Indian 10-Year Government Bond  

---

## Methodology

1. Download historical price data (Yahoo Finance)
2. Compute daily returns
3. Annualize returns and covariance matrix
4. Run 50,000 Monte Carlo simulations
5. Identify:
   - Maximum Sharpe Ratio Portfolio
   - Minimum Volatility Portfolio
6. Plot:
   - Efficient Frontier
   - Capital Market Line
7. Backtest optimal portfolio vs equal-weight portfolio
8. Compute advanced risk metrics

---

## Advanced Risk & Performance Metrics

- Sharpe Ratio
- Sortino Ratio
- Portfolio Beta vs NIFTY
- Rolling Volatility (252-day)
- Maximum Drawdown
- Comparison vs NIFTY ETF (NIFTYBEES)

---

## Key Insights

This project demonstrates:
- Risk-adjusted return optimization
- Diversification across Indian equities
- Downside risk measurement
- Market-relative performance evaluation
- Quantitative portfolio construction techniques

---

## Tools Used
- Python
- NumPy
- Pandas
- Matplotlib
- yFinance
