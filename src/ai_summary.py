"""Optional DeepSeek narrative; falls back to template summary."""

from __future__ import annotations

import json
import os
from typing import Any

import pandas as pd
import requests

DISCLAIMER = (
    "以下为基于龙头等权合成指数的研究性摘要，不构成投资建议。"
    "短期板块轮动波动大，请自行核实数据并评估风险。"
)


def _template_summary(df: pd.DataFrame, as_of: str, lang: str = "zh") -> str:
    if df.empty:
        return f"截至 {as_of}：暂无可用板块数据。\n\n{DISCLAIMER}"

    sort_col = "ret_ytd" if "ret_ytd" in df.columns and df["ret_ytd"].notna().any() else "rs_5d"
    top5 = df.nlargest(3, sort_col)
    bot5 = df.nsmallest(3, sort_col)
    thematic = df[df["group"] == "thematic"]

    name_col = "display_name" if "display_name" in df.columns else ("name_en" if lang == "en" else "name_zh")
    if lang == "en":
        lines = [f"**Sector rotation summary** (as of {as_of}, 10-leader EW baskets)\n"]
        lead_h, lag_h, theme_h = "**Leaders:**", "**Laggards:**", "**Thematic:**"
    else:
        lines = [f"**板块轮动摘要**（截至 {as_of}，各板块=10龙头等权合成）\n"]
        lead_h, lag_h, theme_h = "**排行靠前：**", "**排行靠后：**", "**主题板块：**"

    lines.append(lead_h)
    for _, r in top5.iterrows():
        nm = r.get(name_col, r.get("name_zh", ""))
        ytd = r.get("ret_ytd")
        ytd_s = f"YTD {ytd:+.2f}%, " if ytd is not None and not pd.isna(ytd) else ""
        tag = r.get("rotation_tag_show", r.get("rotation_tag", ""))
        lines.append(
            f"- {nm}: {ytd_s}5d {r['ret_5d']:+.2f}%, RS {r['rs_5d']:+.2f}%, {tag}"
        )

    lines.append(f"\n{lag_h}")
    for _, r in bot5.iterrows():
        nm = r.get(name_col, r.get("name_zh", ""))
        ytd = r.get("ret_ytd")
        ytd_s = f"YTD {ytd:+.2f}%, " if ytd is not None and not pd.isna(ytd) else ""
        tag = r.get("rotation_tag_show", r.get("rotation_tag", ""))
        lines.append(
            f"- {nm}: {ytd_s}5d {r['ret_5d']:+.2f}%, RS {r['rs_5d']:+.2f}%, {tag}"
        )

    if not thematic.empty:
        lines.append(f"\n{theme_h}")
        for _, r in thematic.iterrows():
            nm = r.get(name_col, r.get("name_zh", ""))
            lines.append(
                f"- {nm}: YTD {r['ret_ytd']:+.2f}% · 5d {r['ret_5d']:+.2f}%"
            )

    disc = (
        "Disclaimer: Research only, not investment advice."
        if lang == "en"
        else DISCLAIMER
    )
    lines.append(f"\n{disc}")
    return "\n".join(lines)


def _deepseek_chat(prompt: str) -> str | None:
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        return None

    base = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    url = f"{base}/v1/chat/completions"

    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "你是美股板块轮动分析助手。数据为各板块10只龙头等权合成指数。"
                        "写中文摘要150-250字，语气客观，末尾含免责声明：不构成投资建议。"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 500,
        },
        timeout=45,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


def generate_summary(
    df: pd.DataFrame, as_of: str, use_ai: bool = True, lang: str = "zh"
) -> tuple[str, str]:
    cols = [
        "sector_id",
        "display_name",
        "name_zh",
        "name_en",
        "group",
        "leader_count",
        "leaders",
        "ret_1d",
        "ret_5d",
        "ret_20d",
        "ret_60d",
        "ret_ytd",
        "rs_5d",
        "rs_20d",
        "rs_ytd",
        "rotation_tag",
        "rotation_tag_show",
    ]
    payload: list[dict[str, Any]] = df[[c for c in cols if c in df.columns]].round(2).to_dict(orient="records")

    if use_ai:
        try:
            lang_hint = "Write in English." if lang == "en" else "请用中文撰写。"
            prompt = (
                f"As of {as_of}. US sector equal-weight leader basket metrics (JSON):\n"
                f"{json.dumps(payload, ensure_ascii=False)}\n"
                f"{lang_hint} Sector rotation summary."
            )
            text = _deepseek_chat(prompt)
            if text:
                if DISCLAIMER.split("，")[0] not in text:
                    text = text + f"\n\n{DISCLAIMER}"
                return text, "deepseek"
        except Exception:
            pass

    return _template_summary(df, as_of, lang=lang), "template"
