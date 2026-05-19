"""Equal-weight basket index from sector leader stocks."""

from __future__ import annotations

import pandas as pd

from src.sectors import MIN_CONSTITUENTS, ALL_SECTORS, SectorDefinition


def available_leaders(stock_prices: pd.DataFrame, leaders: tuple[str, ...]) -> list[str]:
    return [t for t in leaders if t in stock_prices.columns and stock_prices[t].notna().sum() >= 20]


def build_equal_weight_index(stock_prices: pd.DataFrame, tickers: list[str]) -> pd.Series | None:
    if len(tickers) < MIN_CONSTITUENTS:
        return None
    sub = stock_prices[tickers].ffill()
    first_valid = sub.apply(lambda s: s.first_valid_index())
    if first_valid.isna().any():
        return None
    start = max(first_valid.dropna())
    sub = sub.loc[start:]
    if len(sub) < 21:
        return None
    base = sub.iloc[0]
    if (base == 0).any() or base.isna().any():
        return None
    normalized = sub.div(base) * 100.0
    return normalized.mean(axis=1, skipna=True).dropna()


def build_all_basket_prices(stock_prices: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, list[str]]]:
    """
    Returns:
        basket_prices: columns = sector_id
        used_map: sector_id -> list of tickers actually used
    """
    baskets: dict[str, pd.Series] = {}
    used_map: dict[str, list[str]] = {}

    for sector in ALL_SECTORS:
        tickers = available_leaders(stock_prices, sector.leaders)
        idx = build_equal_weight_index(stock_prices, tickers)
        if idx is not None:
            baskets[sector.sector_id] = idx
            used_map[sector.sector_id] = tickers

    if not baskets:
        return pd.DataFrame(), used_map

    df = pd.DataFrame(baskets).sort_index()
    return df, used_map


def constituent_returns(
    stock_prices: pd.DataFrame, tickers: list[str], days: int
) -> pd.DataFrame:
    """Per-stock return over N trading days for a sector's constituents."""
    rows = []
    for t in tickers:
        if t not in stock_prices.columns:
            continue
        s = stock_prices[t].dropna()
        if len(s) < days + 1:
            continue
        ret = (s.iloc[-1] / s.iloc[-(days + 1)] - 1) * 100
        rows.append({"ticker": t, f"ret_{days}d": float(ret)})
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(f"ret_{days}d", ascending=False)
