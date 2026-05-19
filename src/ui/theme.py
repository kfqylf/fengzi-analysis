"""Streamlit custom theme — terminal-grade dark dashboard."""

from __future__ import annotations

import streamlit as st

# Design context (impeccable): audience = US equity traders/researchers;
# tone = precise, institutional, calm authority; memorable = cyan signal on deep navy.

COLORS = {
    "bg": "#0a0e17",
    "surface": "#111827",
    "surface2": "#1a2234",
    "border": "#2a3548",
    "text": "#e2e8f0",
    "muted": "#94a3b8",
    "accent": "#22d3ee",
    "accent2": "#a78bfa",
    "up": "#34d399",
    "down": "#f87171",
    "warn": "#fbbf24",
}


def inject_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Chivo:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap');

        .stApp {{
            background: linear-gradient(165deg, {COLORS["bg"]} 0%, #0d1321 45%, #0a0e17 100%);
        }}
        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            font-family: 'Chivo', sans-serif !important;
            letter-spacing: -0.02em;
        }}
        p, label, .stMarkdown, .stCaption, div[data-testid="stMetricValue"] {{
            font-family: 'Chivo', sans-serif;
        }}
        code, .stMetric label, div[data-testid="stMetricDelta"] {{
            font-family: 'JetBrains Mono', monospace !important;
        }}

        /* Equal-size KPI row (replaces default st.metric layout) */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 12px;
            margin: 0 0 1rem 0;
            width: 100%;
        }}
        .kpi-card {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            padding: 14px 16px;
            min-height: 112px;
            height: 100%;
            box-shadow: 0 4px 24px rgba(0,0,0,0.25);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
        }}
        .kpi-label {{
            color: {COLORS["muted"]};
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            line-height: 1.3;
        }}
        .kpi-value {{
            color: {COLORS["accent"]};
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.15rem;
            font-weight: 600;
            line-height: 1.35;
            margin: 6px 0 4px 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .kpi-value-date {{
            font-size: 1rem;
            letter-spacing: 0.02em;
            overflow: visible;
            text-overflow: clip;
        }}
        .kpi-value-sm {{
            font-size: 0.95rem;
        }}
        .kpi-sub {{
            color: {COLORS["muted"]};
            font-size: 0.72rem;
            line-height: 1.35;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .kpi-sub-up {{ color: {COLORS["up"]}; }}
        .kpi-sub-down {{ color: {COLORS["down"]}; }}

        .hero-banner {{
            background: linear-gradient(120deg, {COLORS["surface2"]} 0%, {COLORS["surface"]} 60%);
            border: 1px solid {COLORS["border"]};
            border-left: 4px solid {COLORS["accent"]};
            border-radius: 16px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1rem;
        }}
        .hero-banner h1 {{
            margin: 0;
            font-size: 1.75rem;
            background: linear-gradient(90deg, #f8fafc, {COLORS["accent"]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-sub {{
            color: {COLORS["muted"]};
            font-size: 0.92rem;
            margin-top: 0.35rem;
        }}
        .tag-pill {{
            display: inline-block;
            padding: 0.15rem 0.55rem;
            border-radius: 999px;
            font-size: 0.72rem;
            font-family: 'JetBrains Mono', monospace;
            background: rgba(34, 211, 238, 0.12);
            color: {COLORS["accent"]};
            border: 1px solid rgba(34, 211, 238, 0.35);
            margin-right: 0.35rem;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: transparent;
        }}
        .stTabs [data-baseweb="tab"] {{
            background: {COLORS["surface"]};
            border-radius: 10px;
            border: 1px solid {COLORS["border"]};
            padding: 8px 20px;
            font-family: 'Chivo', sans-serif;
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(167,139,250,0.1));
            border-color: {COLORS["accent"]};
        }}

        div[data-testid="stSidebar"] {{
            background: {COLORS["surface"]};
            border-right: 1px solid {COLORS["border"]};
        }}

        .disclaimer-box {{
            font-size: 0.8rem;
            color: {COLORS["muted"]};
            border-top: 1px dashed {COLORS["border"]};
            padding-top: 0.75rem;
            margin-top: 1.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_row(items: list[dict]) -> None:
    """Render equal-width KPI cards."""
    import html

    parts: list[str] = []
    for it in items:
        sub = it.get("sub") or ""
        sub_cls = it.get("sub_class", "")
        sub_html = (
            f'<div class="kpi-sub {sub_cls}">{html.escape(str(sub))}</div>' if sub else ""
        )
        val_cls = "kpi-value"
        if it.get("is_date"):
            val_cls += " kpi-value-date"
        if it.get("small"):
            val_cls += " kpi-value-sm"
        parts.append(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">{html.escape(str(it["label"]))}</div>'
            f'<div class="{val_cls}">{html.escape(str(it["value"]))}</div>'
            f"{sub_html}"
            f"</div>"
        )

    st.markdown(f'<div class="kpi-row">{"".join(parts)}</div>', unsafe_allow_html=True)


def hero(
    title: str,
    subtitle: str,
    tags: list[str] | None = None,
    logo_path: str | None = None,
) -> None:
    tags_html = "".join(f'<span class="tag-pill">{t}</span>' for t in (tags or []))
    logo_html = ""
    if logo_path:
        import base64
        from pathlib import Path

        p = Path(logo_path)
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()
            logo_html = (
                f'<img src="data:image/png;base64,{b64}" '
                f'style="width:56px;height:56px;border-radius:12px;margin-right:14px;'
                f'vertical-align:middle;box-shadow:0 4px 16px rgba(34,211,238,0.25)" />'
            )
    st.markdown(
        f"""
        <div class="hero-banner">
            <div style="display:flex;align-items:center">
                {logo_html}
                <div>
                    <h1 style="margin:0">{title}</h1>
                    <p class="hero-sub">{subtitle}</p>
                    <div style="margin-top:0.5rem">{tags_html}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
