"""Bilingual UI strings — 峰子分析 / Fengzi Analysis."""

from __future__ import annotations

TAG_EN = {
    "数据不足": "Insufficient data",
    "持续强势": "Sustained strength",
    "新晋强势": "Emerging strength",
    "持续走弱": "Sustained weakness",
    "高位回调": "Pullback from highs",
    "反弹但跑输大盘": "Bounce, lagging SPY",
    "弱势整理": "Weak consolidation",
    "中性": "Neutral",
}

TEXT: dict[str, dict[str, str]] = {
    "zh": {
        "app_title": "峰子分析",
        "app_subtitle": "美股板块轮动 · 每板块 10 只龙头等权合成 · 截至 {as_of}",
        "tag_gics": "GICS + 主题",
        "tag_benchmark": "基准 {ticker}",
        "tag_demo": "研究演示",
        "sidebar_title": "控制面板",
        "lang_label": "界面语言",
        "period": "历史区间",
        "view": "板块视图",
        "view_all": "全部",
        "view_gics": "GICS 板块",
        "view_thematic": "主题板块",
        "rank_metric": "主排序指标",
        "rank_ytd": "年初至今涨幅",
        "rank_5d": "近5日涨幅",
        "rank_60d": "近60日涨幅",
        "rank_rs5": "近5日相对强度",
        "rank_rsytd": "YTD相对强度",
        "ai_insight": "AI 轮动解读",
        "refresh": "↻ 刷新行情",
        "data_source": "数据 · Yahoo Finance · 5 分钟缓存",
        "loading": "合成板块指数中…",
        "load_error": "数据加载失败：{err}",
        "no_data": "暂无板块数据",
        "as_of": "行情截至",
        "as_of_sub": "SPY 最近收盘日",
        "spy_1d": "近 1 日",
        "strongest": "最强板块",
        "weakest": "最弱板块",
        "sectors_covered": "覆盖板块",
        "leader_pool": "龙头池 {n} 只",
        "tab_overview": "◈ 总览仪表盘",
        "tab_rank": "▤ 板块排行",
        "tab_drill": "◎ 成分深挖",
        "tab_insight": "✦ 轮动解读",
        "leaders": "↑ 领先板块",
        "laggards": "↓ 落后板块",
        "col_sector": "板块",
        "col_type": "类型",
        "col_count": "成分",
        "col_tag": "标签",
        "col_leaders": "龙头代码",
        "type_gics": "gics",
        "type_thematic": "thematic",
        "pick_sector": "选择板块",
        "basket_caption": "**{name}** 合成指数 · YTD {ytd:+.2f}% · 5日 {d5:+.2f}% · 等权 {n} 只龙头",
        "generating": "生成解读…",
        "insight_src": "解读来源：{src}",
        "src_ai": "DeepSeek AI",
        "src_tpl": "规则模板",
        "pool_config": "板块龙头池配置",
        "disclaimer": "免责声明：仅供研究与学习，不构成投资建议。每板块为 10 只龙头等权合成指数，与实盘指数存在差异。",
        "chart_heatmap": "板块多周期收益热力矩阵",
        "chart_scatter": "轮动象限 · 相对标普500",
        "chart_treemap": "板块动能树图（面积∝波动幅度）",
        "chart_perf": "龙头等权合成指数 · 归一化走势 (基期=100)",
        "chart_bar": "{metric}",
        "chart_radar": "{name} · 多维画像",
        "chart_movers": "成分股 5日涨跌 Top/Bottom",
        "chart_lollipop_5d": "成分股近 5 日涨跌",
        "chart_lollipop_ytd": "成分股 YTD 涨跌",
    },
    "en": {
        "app_title": "Fengzi Analysis",
        "app_subtitle": "US Sector Rotation · 10 leaders equal-weight per sector · As of {as_of}",
        "tag_gics": "GICS + Thematic",
        "tag_benchmark": "Benchmark {ticker}",
        "tag_demo": "Research Demo",
        "sidebar_title": "Control Panel",
        "lang_label": "Language",
        "period": "History",
        "view": "Sector view",
        "view_all": "All",
        "view_gics": "GICS",
        "view_thematic": "Thematic",
        "rank_metric": "Sort by",
        "rank_ytd": "YTD return",
        "rank_5d": "5-day return",
        "rank_60d": "60-day return",
        "rank_rs5": "5-day rel. strength",
        "rank_rsytd": "YTD rel. strength",
        "ai_insight": "AI rotation insight",
        "refresh": "↻ Refresh data",
        "data_source": "Data · Yahoo Finance · 5 min cache",
        "loading": "Building sector baskets…",
        "load_error": "Failed to load: {err}",
        "no_data": "No sector data",
        "as_of": "Market close",
        "as_of_sub": "Last SPY session",
        "spy_1d": "1 day",
        "strongest": "Strongest",
        "weakest": "Weakest",
        "sectors_covered": "Sectors",
        "leader_pool": "{n} stocks in pool",
        "tab_overview": "◈ Overview",
        "tab_rank": "▤ Rankings",
        "tab_drill": "◎ Constituents",
        "tab_insight": "✦ Insights",
        "leaders": "↑ Leaders",
        "laggards": "↓ Laggards",
        "col_sector": "Sector",
        "col_type": "Type",
        "col_count": "Count",
        "col_tag": "Tag",
        "col_leaders": "Tickers",
        "type_gics": "gics",
        "type_thematic": "thematic",
        "pick_sector": "Select sector",
        "basket_caption": "**{name}** basket · YTD {ytd:+.2f}% · 5d {d5:+.2f}% · {n} leaders EW",
        "generating": "Generating insight…",
        "insight_src": "Source: {src}",
        "src_ai": "DeepSeek AI",
        "src_tpl": "Rule template",
        "pool_config": "Leader pool config",
        "disclaimer": "Disclaimer: For research and education only. Not investment advice. Equal-weight leader baskets may differ from live indices.",
        "chart_heatmap": "Multi-timeframe return heatmap",
        "chart_scatter": "Rotation quadrant vs S&P 500",
        "chart_treemap": "Sector momentum treemap",
        "chart_perf": "Normalized basket performance (base=100)",
        "chart_bar": "{metric}",
        "chart_radar": "{name} · profile",
        "chart_movers": "Constituents 5d top/bottom",
        "chart_lollipop_5d": "Constituents · 5-day %",
        "chart_lollipop_ytd": "Constituents · YTD %",
    },
}

RANK_KEYS = [
    ("ret_ytd", "rank_ytd"),
    ("ret_5d", "rank_5d"),
    ("ret_60d", "rank_60d"),
    ("rs_5d", "rank_rs5"),
    ("rs_ytd", "rank_rsytd"),
]


def t(lang: str, key: str, **kwargs) -> str:
    s = TEXT.get(lang, TEXT["zh"]).get(key, key)
    return s.format(**kwargs) if kwargs else s


def tag_label(lang: str, tag_zh: str) -> str:
    if lang == "en":
        return TAG_EN.get(tag_zh, tag_zh)
    return tag_zh


def apply_display_names(metrics, lang: str):
    m = metrics.copy()
    m["display_name"] = m.apply(lambda r: r["name_en"] if lang == "en" else r["name_zh"], axis=1)
    m["rotation_tag_show"] = m["rotation_tag"].map(lambda x: tag_label(lang, x))
    m["group_show"] = m["group"].map(
        lambda g: ("GICS" if lang == "en" else "GICS行业")
        if g == "gics"
        else ("Thematic" if lang == "en" else "主题板块")
    )
    return m
