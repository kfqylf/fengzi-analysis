"""Sector rotation metrics from equal-weight leader baskets."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.sectors import ALL_SECTORS, BENCHMARK_TICKER, SectorDefinition


def _pct_return(series: pd.Series, days: int) -> float | None:
    if len(series) < days + 1:
        return None
    start = series.iloc[-(days + 1)]
    end = series.iloc[-1]
    if start == 0 or np.isnan(start) or np.isnan(end):
        return None
    return float((end / start - 1.0) * 100.0)


def _ytd_return(series: pd.Series) -> float | None:
    if series.empty:
        return None
    year_start = pd.Timestamp(series.index[-1].year, 1, 1)
    ytd = series[series.index >= year_start]
    if len(ytd) < 2:
        return None
    start, end = ytd.iloc[0], ytd.iloc[-1]
    if start == 0 or np.isnan(start) or np.isnan(end):
        return None
    return float((end / start - 1.0) * 100.0)


def build_metrics(
    basket_prices: pd.DataFrame,
    used_map: dict[str, list[str]],
    spy_series: pd.Series,
) -> pd.DataFrame:
    rows: list[dict] = []

    for sector in ALL_SECTORS:
        if sector.sector_id not in basket_prices.columns:
            continue
        s = basket_prices[sector.sector_id].dropna()
        aligned = pd.concat([s, spy_series], axis=1, join="inner").dropna()
        if aligned.empty:
            continue
        s_aligned = aligned.iloc[:, 0]
        spy_aligned = aligned.iloc[:, 1]

        r1 = _pct_return(s_aligned, 1)
        r5 = _pct_return(s_aligned, 5)
        r20 = _pct_return(s_aligned, 20)
        r60 = _pct_return(s_aligned, 60)
        ytd = _ytd_return(s_aligned)
        rs5 = None if r5 is None else r5 - (_pct_return(spy_aligned, 5) or 0.0)
        rs20 = None if r20 is None else r20 - (_pct_return(spy_aligned, 20) or 0.0)
        rs_ytd = None
        if ytd is not None:
            spy_ytd = _ytd_return(spy_aligned)
            if spy_ytd is not None:
                rs_ytd = ytd - spy_ytd

        used = used_map.get(sector.sector_id, [])
        rows.append(
            {
                "sector_id": sector.sector_id,
                "name_en": sector.name_en,
                "name_zh": sector.name_zh,
                "group": sector.group,
                "leaders": ", ".join(used),
                "leader_count": len(used),
                "ret_1d": r1,
                "ret_5d": r5,
                "ret_20d": r20,
                "ret_60d": r60,
                "ret_ytd": ytd,
                "rs_5d": rs5,
                "rs_20d": rs20,
                "rs_ytd": rs_ytd,
            }
        )

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    for col in ("ret_5d", "ret_20d", "ret_ytd", "rs_5d", "rs_20d", "rs_ytd"):
        df[f"rank_{col}"] = df[col].rank(ascending=False, method="min")

    df["rotation_tag"] = df.apply(_classify_rotation, axis=1)
    return df.sort_values("ret_ytd", ascending=False, na_position="last")


def _classify_rotation(row: pd.Series) -> str:
    r5 = row.get("ret_5d")
    r20 = row.get("ret_20d")
    rs5 = row.get("rs_5d")
    rs20 = row.get("rs_20d")

    if any(v is None or (isinstance(v, float) and np.isnan(v)) for v in (r5, r20, rs5, rs20)):
        return "数据不足"

    if rs5 > 1.5 and rs20 > 2.0 and r5 > 0:
        return "持续强势"
    if rs5 > 1.0 and r20 < 0:
        return "新晋强势"
    if rs5 < -1.0 and r20 < -2.0:
        return "持续走弱"
    if rs5 < -0.5 and r20 > 2.0:
        return "高位回调"
    if r5 > 0 and r20 > 0 and rs5 < 0:
        return "反弹但跑输大盘"
    if r5 < 0 and r20 < 0:
        return "弱势整理"
    return "中性"


def leaders_laggards(df: pd.DataFrame, col: str = "rs_5d", n: int = 3) -> tuple[pd.DataFrame, pd.DataFrame]:
    valid = df.dropna(subset=[col])
    top = valid.nlargest(n, col)
    bottom = valid.nsmallest(n, col)
    return top, bottom
