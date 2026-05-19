"""Advanced Plotly visualizations for sector rotation."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.ui.theme import COLORS

DIVERGING = [
    [0.0, COLORS["down"]],
    [0.5, "#1e293b"],
    [1.0, COLORS["up"]],
]


def _base_layout(title: str = "", height: int | None = 420) -> dict:
    layout = dict(
        title=dict(text=title, font=dict(size=14, color=COLORS["text"]), x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Chivo, sans-serif", color=COLORS["text"], size=12),
        margin=dict(l=12, r=12, t=48 if title else 24, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["muted"])),
        xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"]),
        yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"]),
    )
    if height:
        layout["height"] = height
    return layout


def heatmap_timeframes(
    df: pd.DataFrame,
    name_col: str = "name_zh",
    title: str = "",
    x_labels: list[str] | None = None,
) -> go.Figure:
    """Sectors × (5d, 20d, 60d, YTD) return matrix."""
    cols = ["ret_5d", "ret_20d", "ret_60d", "ret_ytd"]
    labels = x_labels or ["5日", "20日", "60日", "YTD"]
    sub = df.dropna(subset=["ret_ytd"]).sort_values("ret_ytd", ascending=False)
    z = sub[cols].values
    text = [[f"{v:+.1f}%" if pd.notna(v) else "—" for v in row] for row in z]
    y_labels = sub[name_col] if name_col in sub.columns else sub["name_zh"]

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=labels,
            y=y_labels,
            text=text,
            texttemplate="%{text}",
            colorscale=DIVERGING,
            zmid=0,
            colorbar=dict(title="%", tickfont=dict(color=COLORS["muted"])),
            hovertemplate="%{y}<br>%{x}: %{z:+.2f}%<extra></extra>",
        )
    )
    fig.update_layout(**_base_layout(title or "Heatmap", height=max(380, len(sub) * 26)))
    return fig


def treemap_momentum(
    df: pd.DataFrame, metric: str = "ret_ytd", name_col: str = "name_zh", title: str = ""
) -> go.Figure:
    sub = df.dropna(subset=[metric]).copy()
    sub["abs_val"] = sub[metric].abs().clip(lower=0.5)
    if "group_show" in sub.columns:
        sub["group_label"] = sub["group_show"]
    else:
        sub["group_label"] = sub["group"].map({"gics": "GICS", "thematic": "Thematic"}).fillna(sub["group"])
    nm = name_col if name_col in sub.columns else "name_zh"
    root = "US Sectors"
    fig = px.treemap(
        sub,
        path=[px.Constant(root), "group_label", nm],
        values="abs_val",
        color=metric,
        color_continuous_scale=[COLORS["down"], "#334155", COLORS["up"]],
        color_continuous_midpoint=0,
        custom_data=["leader_count", "rotation_tag"],
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>%{color:+.2f}%<br>龙头 %{customdata[0]}只<extra></extra>"
    )
    fig.update_layout(**_base_layout(title or "Treemap", height=440))
    return fig


def rotation_scatter(df: pd.DataFrame, name_col: str = "name_zh", title: str = "") -> go.Figure:
    """Relative strength map: 5d vs 20d, bubble = YTD."""
    sub = df.dropna(subset=["rs_5d", "rs_20d"]).copy()
    fig = px.scatter(
        sub,
        x="rs_5d",
        y="rs_20d",
        size=sub["ret_ytd"].abs().clip(1, 80),
        color="group",
        color_discrete_map={"gics": COLORS["accent"], "thematic": COLORS["accent2"]},
        text=name_col if name_col in sub.columns else "name_zh",
        hover_data=["ret_ytd", "ret_5d", "rotation_tag"],
        labels={"rs_5d": "5日相对强度%", "rs_20d": "20日相对强度%", "group": "类型"},
    )
    fig.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="#fff"), sizemin=8))
    fig.add_hline(y=0, line_dash="dot", line_color=COLORS["muted"], opacity=0.5)
    fig.add_vline(x=0, line_dash="dot", line_color=COLORS["muted"], opacity=0.5)
    fig.add_annotation(
        x=0.98, y=0.98, xref="paper", yref="paper", showarrow=False,
        text="右上 = 短期+中期均强", font=dict(size=10, color=COLORS["muted"]), align="right",
    )
    fig.update_layout(**_base_layout(title or "Rotation scatter", height=460))
    return fig


def performance_lines(
    basket_prices: pd.DataFrame,
    spy: pd.Series,
    sector_ids: list[str] | None = None,
    max_lines: int = 8,
    title: str = "",
    spy_label: str = "SPY",
) -> go.Figure:
    """Normalized indexed performance vs SPY."""
    fig = go.Figure()
    if basket_prices.empty or spy.empty:
        fig.update_layout(**_base_layout("走势对比"))
        return fig

    aligned_spy = spy.dropna()
    if len(aligned_spy) < 2:
        return fig

    norm_spy = aligned_spy / aligned_spy.iloc[0] * 100
    fig.add_trace(
        go.Scatter(
            x=norm_spy.index, y=norm_spy.values, name=spy_label,
            line=dict(color=COLORS["muted"], width=2, dash="dot"),
        )
    )

    cols = sector_ids or list(basket_prices.columns)
    if sector_ids is None and "ret_ytd" not in basket_prices.columns:
        # pick top movers by last value change - use all, limit max_lines
        cols = list(basket_prices.columns)[:max_lines]

    palette = px.colors.qualitative.Set2
    for i, col in enumerate(cols[:max_lines]):
        s = basket_prices[col].dropna()
        if len(s) < 2:
            continue
        norm = s / s.iloc[0] * 100
        fig.add_trace(
            go.Scatter(
                x=norm.index, y=norm.values, name=str(col),
                line=dict(color=palette[i % len(palette)], width=1.8),
            )
        )

    fig.update_layout(**_base_layout(title or "Performance", height=420))
    fig.update_yaxes(title="指数")
    return fig


def ranked_bar(
    df: pd.DataFrame, metric: str, label: str, name_col: str = "name_zh"
) -> go.Figure:
    sub = df.dropna(subset=[metric]).sort_values(metric, ascending=True)
    nm = sub[name_col] if name_col in sub.columns else sub["name_zh"]
    sub["label"] = nm + " · " + sub["leader_count"].astype(int).astype(str) + "/10"
    mid = 0 if metric.startswith("rs_") else sub[metric].median()
    fig = px.bar(
        sub, x=metric, y="label", orientation="h", color=metric,
        color_continuous_scale=[COLORS["down"], COLORS["warn"], COLORS["up"]],
        color_continuous_midpoint=mid,
    )
    fig.update_layout(**_base_layout(label, height=max(360, len(sub) * 28)), showlegend=False)
    return fig


def constituent_ytd_lollipop(tickers: list[str], stock_prices: pd.DataFrame, title: str = "") -> go.Figure:
    year_start = pd.Timestamp(stock_prices.index[-1].year, 1, 1)
    rows = []
    for t in tickers:
        if t not in stock_prices.columns:
            continue
        s = stock_prices[t].dropna()
        y = s[s.index >= year_start]
        if len(y) < 2:
            continue
        rows.append({"ticker": t, "ret": (y.iloc[-1] / y.iloc[0] - 1) * 100})
    if not rows:
        fig = go.Figure()
        fig.update_layout(**_base_layout("成分股 YTD"))
        return fig
    d = pd.DataFrame(rows).sort_values("ret")
    colors = [COLORS["up"] if v >= 0 else COLORS["down"] for v in d["ret"]]
    fig = go.Figure(go.Scatter(x=d["ret"], y=d["ticker"], mode="markers", marker=dict(size=14, color=colors)))
    fig.add_vline(x=0, line_color=COLORS["muted"], line_dash="dot")
    fig.update_layout(**_base_layout(title or "YTD", height=max(280, len(d) * 32)))
    fig.update_xaxes(title="%")
    return fig


def constituent_lollipop(
    tickers: list[str], stock_prices: pd.DataFrame, days: int = 5, title: str = ""
) -> go.Figure:
    rows = []
    for t in tickers:
        if t not in stock_prices.columns:
            continue
        s = stock_prices[t].dropna()
        if len(s) < days + 1:
            continue
        ret = (s.iloc[-1] / s.iloc[-(days + 1)] - 1) * 100
        rows.append({"ticker": t, "ret": ret})
    if not rows:
        fig = go.Figure()
        fig.update_layout(**_base_layout("成分股涨跌"))
        return fig

    d = pd.DataFrame(rows).sort_values("ret")
    colors = [COLORS["up"] if v >= 0 else COLORS["down"] for v in d["ret"]]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=d["ret"], y=d["ticker"], mode="markers",
            marker=dict(size=14, color=colors, line=dict(width=1, color="#fff")),
            hovertemplate="%{y}: %{x:+.2f}%<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_color=COLORS["muted"], line_dash="dot")
    fig.update_layout(**_base_layout(title or f"{days}d", height=max(280, len(d) * 32)))
    fig.update_xaxes(title="%")
    return fig


def sector_radar(row: pd.Series, title: str = "") -> go.Figure:
    categories = ["YTD", "5日", "20日", "60日", "5日RS"]
    keys = ["ret_ytd", "ret_5d", "ret_20d", "ret_60d", "rs_5d"]
    vals = [float(row.get(k, 0) or 0) for k in keys]
    fig = go.Figure(
        data=go.Scatterpolar(
            r=vals + [vals[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(34, 211, 238, 0.15)",
            line=dict(color=COLORS["accent"], width=2),
            name=row.get("name_zh", ""),
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(gridcolor=COLORS["border"], tickfont=dict(color=COLORS["muted"])),
            angularaxis=dict(gridcolor=COLORS["border"], tickfont=dict(color=COLORS["text"])),
        ),
        **_base_layout(title or str(row.get("name_zh", "")), height=380),
    )
    return fig


def top_movers_strip(
    stock_prices: pd.DataFrame, tickers: list[str], n: int = 5, title: str = ""
) -> go.Figure:
    """Mini strip of best/worst constituents by 5d."""
    rows = []
    for t in tickers:
        s = stock_prices[t].dropna() if t in stock_prices.columns else pd.Series(dtype=float)
        if len(s) < 6:
            continue
        rows.append({"ticker": t, "ret_5d": (s.iloc[-1] / s.iloc[-6] - 1) * 100})
    if not rows:
        return go.Figure()
    d = pd.DataFrame(rows).sort_values("ret_5d", ascending=False)
    top = pd.concat([d.head(n), d.tail(n)]).drop_duplicates()
    colors = [COLORS["up"] if v >= 0 else COLORS["down"] for v in top["ret_5d"]]
    fig = go.Figure(go.Bar(x=top["ticker"], y=top["ret_5d"], marker_color=colors))
    fig.update_layout(**_base_layout(title or "Movers", height=280))
    return fig
