import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# =========================
# CONFIG
# =========================
STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "HINDUNILVR.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "ITC.NS",
    "AXISBANK.NS",
    "ASIANPAINT.NS",
    "MARUTI.NS",
    "SUNPHARMA.NS",
    "TITAN.NS",
    "ULTRACEMCO.NS",
    "NESTLEIND.NS",
    "BAJFINANCE.NS",
    "HCLTECH.NS",
    "POWERGRID.NS",
    "NTPC.NS",
    "WIPRO.NS",
    "JSWSTEEL.NS",
    "ONGC.NS",
    "COALINDIA.NS",
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "DRREDDY.NS",
    "TECHM.NS",
]

BENCHMARK = "^NSEI"
START_DATE = "2015-01-01"
END_DATE = "2026-01-01"
RISK_FREE_RATE = 0.07
NUM_PORTFOLIOS = 50_000
TRADING_DAYS = 252

# Exclude Tata companies (including TATAMOTORS and common Tata Group tickers)
TATA_EXCLUSIONS = {
    "TATAMOTORS.NS",
    "TCS.NS",
    "TITAN.NS",
    "TATASTEEL.NS",
    "TATAPOWER.NS",
    "TATACONSUM.NS",
    "TATACHEM.NS",
    "TATACOMM.NS",
    "TRENT.NS",
    "INDHOTEL.NS",
    "TATAELXSI.NS",
    "VOLTAS.NS",
}


def extract_close(data: pd.DataFrame) -> pd.DataFrame:
    """
    Return close-price dataframe from yfinance output without relying on 'Adj Close'.
    Handles MultiIndex and single-index outputs safely.
    """
    if isinstance(data, pd.Series):
        return data.to_frame()

    if isinstance(data.columns, pd.MultiIndex):
        top = data.columns.get_level_values(0)
        if "Close" in top:
            close = data.xs("Close", axis=1, level=0, drop_level=True)
        elif "Adj Close" in top:  # fallback only
            close = data.xs("Adj Close", axis=1, level=0, drop_level=True)
        else:
            raise KeyError(
                "Neither 'Close' nor 'Adj Close' found in downloaded data.")
        if isinstance(close, pd.Series):
            close = close.to_frame()
        return close

    if "Close" in data.columns:
        return data[["Close"]]
    if "Adj Close" in data.columns:  # fallback only
        return data[["Adj Close"]]

    return data.copy()


def max_drawdown(cumulative_returns: pd.Series) -> float:
    running_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / running_max - 1.0
    return float(drawdown.min())


def main() -> None:
    stocks = [s for s in STOCKS if s not in TATA_EXCLUSIONS]
    if len(stocks) < 2:
        raise ValueError("Not enough non-Tata stocks after exclusions.")

    # -------------------------
    # DATA DOWNLOAD
    # -------------------------
    stock_raw = yf.download(
        tickers=stocks,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,
        progress=False,
        group_by="column",
        threads=True,
    )
    stock_prices = extract_close(stock_raw)
    stock_prices = stock_prices.dropna(axis=1, how="all")

    if stock_prices.empty or stock_prices.shape[1] < 2:
        raise ValueError("Insufficient stock price data after cleaning.")

    benchmark_raw = yf.download(
        tickers=BENCHMARK,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,
        progress=False,
        group_by="column",
        threads=True,
    )
    benchmark_df = extract_close(benchmark_raw)

    # Ensure benchmark is a Series
    if BENCHMARK in benchmark_df.columns:
        benchmark_prices = benchmark_df[BENCHMARK]
    else:
        benchmark_prices = benchmark_df.iloc[:, 0]
    benchmark_prices = benchmark_prices.squeeze()
    benchmark_prices.name = BENCHMARK
    if not isinstance(benchmark_prices, pd.Series):
        benchmark_prices = pd.Series(
            benchmark_prices, index=benchmark_df.index, name=BENCHMARK)

    # -------------------------
    # RETURNS
    # -------------------------
    stock_returns = stock_prices.pct_change(fill_method=None).dropna(how="any")
    benchmark_returns = benchmark_prices.pct_change(fill_method=None).dropna()

    if stock_returns.empty:
        raise ValueError("Stock returns are empty after preprocessing.")
    if benchmark_returns.empty:
        raise ValueError("Benchmark returns are empty after preprocessing.")

    mean_returns_annual = stock_returns.mean() * TRADING_DAYS
    cov_matrix_annual = stock_returns.cov() * TRADING_DAYS

    asset_names = stock_returns.columns.tolist()
    n_assets = len(asset_names)

    # -------------------------
    # MONTE CARLO SIMULATION
    # -------------------------
    results = np.zeros((3, NUM_PORTFOLIOS))
    weights_matrix = np.zeros((NUM_PORTFOLIOS, n_assets))

    mean_vec = mean_returns_annual.values
    cov_mat = cov_matrix_annual.values

    for i in range(NUM_PORTFOLIOS):
        weights = np.random.random(n_assets)
        weights /= weights.sum()

        port_return = float(weights @ mean_vec)
        port_vol = float(np.sqrt(weights @ cov_mat @ weights))
        sharpe = (port_return - RISK_FREE_RATE) / \
            port_vol if port_vol > 0 else np.nan

        weights_matrix[i, :] = weights
        results[0, i] = port_return
        results[1, i] = port_vol
        results[2, i] = sharpe

    max_sharpe_idx = int(np.nanargmax(results[2]))
    optimal_weights = pd.Series(
        weights_matrix[max_sharpe_idx], index=asset_names, name="Weight")

    # Ensure portfolio_daily_returns is a Series with correct index
    portfolio_daily_returns = stock_returns.mul(
        optimal_weights, axis=1).sum(axis=1)
    portfolio_daily_returns.name = "Portfolio"

    equal_weights = pd.Series(1.0 / n_assets, index=asset_names)
    equal_daily_returns = stock_returns.mul(equal_weights, axis=1).sum(axis=1)
    equal_daily_returns.name = "EqualWeight"

    # -------------------------
    # METRICS
    # -------------------------
    annual_return_opt = portfolio_daily_returns.mean() * TRADING_DAYS
    annual_vol_opt = portfolio_daily_returns.std() * np.sqrt(TRADING_DAYS)
    sharpe_opt = (annual_return_opt - RISK_FREE_RATE) / \
        annual_vol_opt if annual_vol_opt > 0 else np.nan

    downside = portfolio_daily_returns[portfolio_daily_returns < 0]
    downside_std_annual = downside.std() * np.sqrt(TRADING_DAYS)
    sortino_opt = (annual_return_opt - RISK_FREE_RATE) / \
        downside_std_annual if downside_std_annual > 0 else np.nan

    # Align for beta using inner join (required)
    beta_aligned = pd.concat(
        [portfolio_daily_returns.rename(
            "Portfolio"), benchmark_returns.rename("Market")],
        axis=1,
        join="inner",
    ).dropna()

    market_var = beta_aligned["Market"].var()
    beta_opt = beta_aligned["Portfolio"].cov(
        beta_aligned["Market"]) / market_var if market_var > 0 else np.nan

    cumulative_opt = (1 + portfolio_daily_returns).cumprod()
    mdd_opt = max_drawdown(cumulative_opt)

    rolling_vol_252 = portfolio_daily_returns.rolling(
        252, min_periods=252).std() * np.sqrt(TRADING_DAYS)

    # Align backtest series properly with inner join to avoid shape mismatch
    comparison_returns = pd.concat(
        [
            portfolio_daily_returns.rename("Optimal Portfolio"),
            equal_daily_returns.rename("Equal Weight Portfolio"),
            benchmark_returns.rename(BENCHMARK),
        ],
        axis=1,
        join="inner",
    ).dropna()

    cumulative_comparison = (1 + comparison_returns).cumprod()

    # -------------------------
    # OUTPUT
    # -------------------------
    print("\n===== MONTE CARLO PORTFOLIO OPTIMIZATION (INDIA) =====")
    print(f"Universe size (after Tata exclusion): {n_assets}")
    print(f"Portfolios simulated: {NUM_PORTFOLIOS:,}")
    print(f"Benchmark: {BENCHMARK}")
    print("\n===== OPTIMAL PORTFOLIO METRICS =====")
    print(f"Expected Annual Return : {annual_return_opt:.2%}")
    print(f"Annual Volatility      : {annual_vol_opt:.2%}")
    print(f"Sharpe Ratio           : {sharpe_opt:.4f}")
    print(f"Sortino Ratio          : {sortino_opt:.4f}")
    print(f"Beta vs NIFTYBEES      : {beta_opt:.4f}")
    print(f"Maximum Drawdown       : {mdd_opt:.2%}")

    print("\n===== OPTIMAL WEIGHTS =====")
    for ticker, w in optimal_weights.sort_values(ascending=False).items():
        print(f"{ticker:15s} {w:7.2%}")

    # -------------------------
    # PLOTS
    # -------------------------
    plt.style.use("seaborn-v0_8")
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # Efficient Frontier
    sc = axes[0].scatter(
        results[1, :],
        results[0, :],
        c=results[2, :],
        cmap="viridis",
        s=8,
        alpha=0.65,
    )
    axes[0].scatter(
        results[1, max_sharpe_idx],
        results[0, max_sharpe_idx],
        color="red",
        marker="*",
        s=280,
        label="Max Sharpe",
    )
    axes[0].set_title("Efficient Frontier (Monte Carlo)")
    axes[0].set_xlabel("Annualized Volatility")
    axes[0].set_ylabel("Annualized Return")
    axes[0].legend(loc="best")
    fig.colorbar(sc, ax=axes[0], label="Sharpe Ratio")

    # Backtest comparison
    axes[1].plot(cumulative_comparison.index,
                 cumulative_comparison["Optimal Portfolio"], label="Optimal Portfolio")
    axes[1].plot(cumulative_comparison.index,
                 cumulative_comparison["Equal Weight Portfolio"], label="Equal Weight")
    axes[1].plot(cumulative_comparison.index,
                 cumulative_comparison[BENCHMARK], label=BENCHMARK)
    axes[1].set_title("Backtest Comparison (Cumulative Growth)")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Growth of 1 INR")
    axes[1].legend(loc="best")

    # Rolling volatility
    axes[2].plot(rolling_vol_252.index, rolling_vol_252, color="tab:orange")
    axes[2].set_title(
        "Rolling 252-Day Annualized Volatility (Optimal Portfolio)")
    axes[2].set_xlabel("Date")
    axes[2].set_ylabel("Volatility")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
