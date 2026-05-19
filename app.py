"""
峰子分析 · Fengzi Analysis
US sector rotation — 10 leaders equal-weight per sector
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "logo.png"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

load_dotenv(ROOT / ".env")

from src.ai_summary import generate_summary
from src.basket import build_all_basket_prices
from src.data import fetch_prices
from src.i18n import RANK_KEYS, apply_display_names, t, tag_label
from src.rotation import build_metrics, leaders_laggards
from src.sectors import ALL_SECTORS, BENCHMARK_TICKER, all_leader_tickers
from src.ui.charts import (
    constituent_lollipop,
    constituent_ytd_lollipop,
    heatmap_timeframes,
    performance_lines,
    ranked_bar,
    rotation_scatter,
    sector_radar,
    top_movers_strip,
    treemap_momentum,
)
from src.market_date import market_as_of
from src.ui.theme import hero, inject_theme, kpi_row
from src.universe import BENCHMARK

st.set_page_config(
    page_title="峰子分析 Fengzi Analysis",
    page_icon=str(LOGO) if LOGO.exists() else "◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

VIEW_OPTS = [("all", "view_all"), ("gics", "view_gics"), ("thematic", "view_thematic")]
HEAT_LABELS = {"zh": ["5日", "20日", "60日", "YTD"], "en": ["5d", "20d", "60d", "YTD"]}


@st.cache_data(ttl=300, show_spinner=False)
def load_market_data(period: str):
    stock_prices = fetch_prices(all_leader_tickers(), period=period)
    basket_prices, used_map = build_all_basket_prices(stock_prices)
    spy = stock_prices[BENCHMARK_TICKER].dropna()
    metrics = build_metrics(basket_prices, used_map, spy)
    as_of, _ = market_as_of(stock_prices)
    return stock_prices, basket_prices, metrics, used_map, as_of


def filter_metrics(metrics: pd.DataFrame, view_key: str) -> pd.DataFrame:
    if view_key == "gics":
        return metrics[metrics["group"] == "gics"].copy()
    if view_key == "thematic":
        return metrics[metrics["group"] == "thematic"].copy()
    return metrics.copy()


def color_pct(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "color: #94a3b8"
    if val > 0:
        return "color: #34d399; font-weight: 600"
    if val < 0:
        return "color: #f87171; font-weight: 600"
    return "color: #94a3b8"


def rank_label(lang: str, col: str) -> str:
    for k, tk in RANK_KEYS:
        if k == col:
            return t(lang, tk)
    return col


def main() -> None:
    inject_theme()

    if "lang" not in st.session_state:
        st.session_state.lang = "zh"

    with st.sidebar:
        if LOGO.exists():
            st.image(str(LOGO), width=72)
        st.markdown(f"### {t(st.session_state.lang, 'sidebar_title')}")
        lang = st.radio(
            t(st.session_state.lang, "lang_label"),
            ["zh", "en"],
            format_func=lambda x: "中文" if x == "zh" else "English",
            horizontal=True,
            key="lang_radio",
        )
        st.session_state.lang = lang
        period = st.selectbox(t(lang, "period"), ["3mo", "6mo", "1y"], index=2)
        view_key = st.radio(
            t(lang, "view"),
            VIEW_OPTS,
            format_func=lambda x: t(lang, x[1]),
        )[0]
        rank_col = st.selectbox(
            t(lang, "rank_metric"),
            RANK_KEYS,
            format_func=lambda x: t(lang, x[1]),
        )[0]
        use_ai = st.checkbox(t(lang, "ai_insight"), value=bool(os.getenv("DEEPSEEK_API_KEY")))
        st.markdown("---")
        if st.button(t(lang, "refresh"), use_container_width=True):
            load_market_data.clear()
            st.rerun()
        st.caption(t(lang, "data_source"))

    try:
        with st.spinner(t(lang, "loading")):
            stock_prices, basket_prices, metrics, used_map, as_of = load_market_data(period)
    except Exception as e:
        st.error(t(lang, "load_error", err=e))
        return

    if metrics.empty:
        st.warning(t(lang, "no_data"))
        return

    metrics = apply_display_names(metrics, lang)
    metrics_view = filter_metrics(metrics, view_key)
    sector_names = {
        s.sector_id: (s.name_en if lang == "en" else s.name_zh) for s in ALL_SECTORS
    }
    id_name = dict(zip(metrics["sector_id"], metrics["display_name"]))

    hero(
        t(lang, "app_title"),
        t(lang, "app_subtitle", as_of=as_of),
        tags=[
            t(lang, "tag_gics"),
            t(lang, "tag_benchmark", ticker=BENCHMARK.ticker),
            t(lang, "tag_demo"),
        ],
        logo_path=str(LOGO) if LOGO.exists() else None,
    )

    spy_1d = None
    if BENCHMARK.ticker in stock_prices.columns:
        sp = stock_prices[BENCHMARK.ticker].dropna()
        if len(sp) >= 2:
            spy_1d = (sp.iloc[-1] / sp.iloc[-2] - 1) * 100

    top1, bot1 = leaders_laggards(metrics, rank_col, 1)
    kpi_cards = [
        {
            "label": t(lang, "as_of"),
            "value": as_of,
            "sub": t(lang, "as_of_sub"),
            "is_date": True,
        },
        {
            "label": BENCHMARK.ticker,
            "value": f"{spy_1d:+.2f}%" if spy_1d is not None else "—",
            "sub": t(lang, "spy_1d"),
            "sub_class": "kpi-sub-up" if spy_1d and spy_1d > 0 else ("kpi-sub-down" if spy_1d and spy_1d < 0 else ""),
        },
    ]
    if len(top1):
        v = top1.iloc[0][rank_col]
        kpi_cards.append(
            {
                "label": t(lang, "strongest"),
                "value": top1.iloc[0]["display_name"],
                "sub": f"{rank_label(lang, rank_col)} {v:+.2f}%",
                "sub_class": "kpi-sub-up" if v and v > 0 else "kpi-sub-down",
                "small": True,
            }
        )
    else:
        kpi_cards.append({"label": t(lang, "strongest"), "value": "—", "sub": ""})
    if len(bot1):
        v = bot1.iloc[0][rank_col]
        kpi_cards.append(
            {
                "label": t(lang, "weakest"),
                "value": bot1.iloc[0]["display_name"],
                "sub": f"{rank_label(lang, rank_col)} {v:+.2f}%",
                "sub_class": "kpi-sub-up" if v and v > 0 else "kpi-sub-down",
                "small": True,
            }
        )
    else:
        kpi_cards.append({"label": t(lang, "weakest"), "value": "—", "sub": ""})
    kpi_cards.append(
        {
            "label": t(lang, "sectors_covered"),
            "value": str(len(metrics)),
            "sub": t(lang, "leader_pool", n=len(all_leader_tickers()) - 1),
        }
    )
    kpi_row(kpi_cards)

    tab_overview, tab_rank, tab_drill, tab_insight = st.tabs(
        [
            t(lang, "tab_overview"),
            t(lang, "tab_rank"),
            t(lang, "tab_drill"),
            t(lang, "tab_insight"),
        ]
    )

    ncol = "display_name"
    hl = HEAT_LABELS[lang]

    with tab_overview:
        left, right = st.columns([1.1, 0.9])
        with left:
            st.plotly_chart(
                heatmap_timeframes(
                    metrics_view, name_col=ncol, title=t(lang, "chart_heatmap"), x_labels=hl
                ),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with right:
            st.plotly_chart(
                rotation_scatter(metrics, name_col=ncol, title=t(lang, "chart_scatter")),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        st.plotly_chart(
            treemap_momentum(metrics_view, rank_col, ncol, t(lang, "chart_treemap")),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        top_ids = metrics.nlargest(6, "ret_ytd")["sector_id"].tolist()
        renamed = basket_prices.rename(columns=id_name)
        cols_show = [id_name.get(i, i) for i in top_ids if i in basket_prices.columns]
        st.plotly_chart(
            performance_lines(
                renamed[[c for c in cols_show if c in renamed.columns]],
                stock_prices[BENCHMARK_TICKER],
                max_lines=7,
                title=t(lang, "chart_perf"),
                spy_label=BENCHMARK.ticker,
            ),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with tab_rank:
        st.plotly_chart(
            ranked_bar(metrics_view, rank_col, rank_label(lang, rank_col), ncol),
            use_container_width=True,
            config={"displayModeBar": False},
        )
        top3, bot3 = leaders_laggards(metrics, rank_col, 3)
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"#### {t(lang, 'leaders')}")
            for _, row in top3.iterrows():
                st.markdown(
                    f"**{row['display_name']}** `{row['rotation_tag_show']}`  \n"
                    f"YTD **{row['ret_ytd']:+.2f}%** · 5d {row['ret_5d']:+.2f}% · "
                    f"RS {row['rs_5d']:+.2f}%"
                )
        with r2:
            st.markdown(f"#### {t(lang, 'laggards')}")
            for _, row in bot3.iterrows():
                st.markdown(
                    f"**{row['display_name']}** `{row['rotation_tag_show']}`  \n"
                    f"YTD **{row['ret_ytd']:+.2f}%** · 5d {row['ret_5d']:+.2f}% · "
                    f"RS {row['rs_5d']:+.2f}%"
                )

        display = metrics_view[
            [
                "display_name", "group_show", "leader_count", "ret_ytd", "ret_5d",
                "ret_20d", "ret_60d", "rs_ytd", "rs_5d", "rotation_tag_show", "leaders",
            ]
        ].copy()
        pct_cols = ["YTD%", "5d%", "20d%", "60d%", "YTD RS%", "5d RS%"]
        display.columns = [
            t(lang, "col_sector"),
            t(lang, "col_type"),
            t(lang, "col_count"),
            *pct_cols,
            t(lang, "col_tag"),
            t(lang, "col_leaders"),
        ]
        st.dataframe(
            display.style.format({c: "{:+.2f}" for c in pct_cols}, na_rep="—").map(
                lambda v: color_pct(v) if isinstance(v, (int, float)) else "",
                subset=pct_cols,
            ),
            use_container_width=True,
            height=360,
        )

    with tab_drill:
        pick = st.selectbox(
            t(lang, "pick_sector"),
            metrics["sector_id"].tolist(),
            format_func=lambda sid: f"{sector_names.get(sid, sid)}  ({', '.join(used_map.get(sid, []))})",
        )
        if not pick:
            st.stop()
        row = metrics[metrics["sector_id"] == pick].iloc[0]
        tickers = used_map.get(pick, [])
        d1, d2 = st.columns(2)
        with d1:
            st.plotly_chart(
                sector_radar(row, t(lang, "chart_radar", name=row["display_name"])),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with d2:
            st.plotly_chart(
                top_movers_strip(stock_prices, tickers, title=t(lang, "chart_movers")),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        d3, d4 = st.columns(2)
        with d3:
            st.plotly_chart(
                constituent_lollipop(tickers, stock_prices, 5, t(lang, "chart_lollipop_5d")),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with d4:
            st.plotly_chart(
                constituent_ytd_lollipop(tickers, stock_prices, t(lang, "chart_lollipop_ytd")),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        st.caption(
            t(
                lang,
                "basket_caption",
                name=row["display_name"],
                ytd=row["ret_ytd"],
                d5=row["ret_5d"],
                n=int(row["leader_count"]),
            )
        )

    with tab_insight:
        with st.spinner(t(lang, "generating")):
            summary, source = generate_summary(metrics, as_of, use_ai=use_ai, lang=lang)
        st.markdown(summary)
        src = t(lang, "src_ai") if source == "deepseek" else t(lang, "src_tpl")
        st.caption(t(lang, "insight_src", src=src))
        with st.expander(t(lang, "pool_config")):
            for s in ALL_SECTORS:
                nm = s.name_en if lang == "en" else s.name_zh
                st.markdown(f"**{nm}** — `{', '.join(s.leaders)}`")

    st.markdown(f'<p class="disclaimer-box">{t(lang, "disclaimer")}</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
