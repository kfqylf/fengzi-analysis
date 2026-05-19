"""Resolve display date from actual benchmark price bars (not wall clock)."""

from __future__ import annotations

import pandas as pd

BENCHMARK = "SPY"


def market_as_of(stock_prices: pd.DataFrame, benchmark: str = BENCHMARK) -> tuple[str, pd.Timestamp | None]:
    """
    Last trading session date on the benchmark series.
    Returns (YYYY-MM-DD string, timestamp).
    """
    if benchmark not in stock_prices.columns:
        series = stock_prices.dropna(how="all").iloc[:, 0] if len(stock_prices.columns) else None
    else:
        series = stock_prices[benchmark].dropna()

    if series is None or series.empty:
        return "N/A", None

    ts = pd.Timestamp(series.index[-1])
    if ts.tzinfo is not None:
        try:
            ts = ts.tz_convert("America/New_York")
        except Exception:
            ts = ts.tz_localize(None)
    ts = ts.normalize()

    today = pd.Timestamp.now(tz="America/New_York").normalize().tz_localize(None)
    if ts > today:
        ts = today

    return ts.strftime("%Y-%m-%d"), ts
