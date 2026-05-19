"""Fetch adjusted close prices via yfinance."""

from __future__ import annotations

import pandas as pd
import yfinance as yf

from src.sectors import all_leader_tickers


def fetch_prices(tickers: list[str] | None = None, period: str = "1y") -> pd.DataFrame:
    """Return wide DataFrame of adjusted close (columns = tickers)."""
    tickers = tickers or all_leader_tickers()
    raw = yf.download(
        tickers,
        period=period,
        interval="1d",
        group_by="column",
        auto_adjust=True,
        progress=False,
        threads=True,
    )
    if raw.empty:
        raise RuntimeError("No price data returned. Check network or tickers.")

    if isinstance(raw.columns, pd.MultiIndex):
        if "Close" in raw.columns.get_level_values(0):
            prices = raw["Close"]
        elif "Adj Close" in raw.columns.get_level_values(0):
            prices = raw["Adj Close"]
        else:
            prices = raw.iloc[:, 0]
    else:
        prices = raw["Close"] if "Close" in raw.columns else raw.iloc[:, 0]

    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    prices = prices.dropna(how="all").sort_index()
    return prices.ffill()
