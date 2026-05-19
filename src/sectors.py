"""
板块定义：每个板块由 10 只美股龙头等权汇总（非单只 ETF）。
龙头池按市值与行业代表性人工维护，正式版可接指数成分 API 自动更新。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SectorDefinition:
    sector_id: str
    name_en: str
    name_zh: str
    group: str  # gics | thematic
    leaders: tuple[str, ...]  # 10 tickers


BENCHMARK_TICKER = "SPY"

# --- GICS 11 板块龙头（美股大型市值代表）---
GICS_SECTORS: list[SectorDefinition] = [
    SectorDefinition(
        "materials",
        "Materials",
        "原材料",
        "gics",
        ("LIN", "APD", "SHW", "ECL", "NEM", "FCX", "NUE", "DOW", "VMC", "MLM"),
    ),
    SectorDefinition(
        "communication",
        "Communication Services",
        "通信服务",
        "gics",
        ("META", "GOOGL", "GOOG", "NFLX", "DIS", "CMCSA", "TMUS", "T", "VZ", "CHTR"),
    ),
    SectorDefinition(
        "energy",
        "Energy",
        "能源",
        "gics",
        ("XOM", "CVX", "COP", "WMB", "MPC", "SLB", "EOG", "PSX", "VLO", "OXY"),
    ),
    SectorDefinition(
        "financials",
        "Financials",
        "金融",
        "gics",
        ("BRK-B", "JPM", "V", "MA", "BAC", "WFC", "GS", "MS", "SPGI", "BLK"),
    ),
    SectorDefinition(
        "industrials",
        "Industrials",
        "工业",
        "gics",
        ("GE", "CAT", "RTX", "HON", "UPS", "BA", "DE", "LMT", "UNP", "ETN"),
    ),
    SectorDefinition(
        "technology",
        "Technology",
        "科技",
        "gics",
        ("AAPL", "MSFT", "NVDA", "AVGO", "ORCL", "CRM", "CSCO", "AMD", "ADBE", "INTC"),
    ),
    SectorDefinition(
        "consumer_staples",
        "Consumer Staples",
        "必需消费",
        "gics",
        ("PG", "COST", "WMT", "KO", "PEP", "PM", "MO", "CL", "MDLZ", "KMB"),
    ),
    SectorDefinition(
        "real_estate",
        "Real Estate",
        "房地产",
        "gics",
        ("PLD", "AMT", "EQIX", "SPG", "O", "PSA", "WELL", "DLR", "AVB", "CCI"),
    ),
    SectorDefinition(
        "utilities",
        "Utilities",
        "公用事业",
        "gics",
        ("NEE", "SO", "DUK", "CEG", "SRE", "AEP", "VST", "D", "EXC", "XEL"),
    ),
    SectorDefinition(
        "health_care",
        "Health Care",
        "医疗保健",
        "gics",
        ("LLY", "JNJ", "ABBV", "UNH", "MRK", "TMO", "ABT", "ISRG", "PFE", "AMGN"),
    ),
    SectorDefinition(
        "consumer_disc",
        "Consumer Discretionary",
        "可选消费",
        "gics",
        ("AMZN", "TSLA", "HD", "MCD", "LOW", "BKNG", "TJX", "NKE", "SBUX", "ORLY"),
    ),
]

THEMATIC_SECTORS: list[SectorDefinition] = [
    SectorDefinition(
        "semiconductors",
        "Semiconductors",
        "半导体",
        "thematic",
        ("NVDA", "AVGO", "AMD", "QCOM", "TXN", "MU", "AMAT", "LRCX", "KLAC", "MRVL"),
    ),
    SectorDefinition(
        "space",
        "Commercial Space",
        "商业航天/太空",
        "thematic",
        ("RKLB", "ASTS", "PLTR", "IRDM", "LUNR", "ACHR", "SPIR", "BA", "LMT", "RTX"),
    ),
    SectorDefinition(
        "aerospace_defense",
        "Aerospace & Defense",
        "航空航天国防",
        "thematic",
        ("LMT", "RTX", "NOC", "GD", "BA", "LHX", "TDG", "HWM", "HEI", "TXT"),
    ),
    SectorDefinition(
        "software",
        "Software",
        "软件",
        "thematic",
        ("MSFT", "ORCL", "CRM", "NOW", "ADBE", "INTU", "PANW", "SNOW", "WDAY", "CRWD"),
    ),
    SectorDefinition(
        "biotech",
        "Biotechnology",
        "生物科技",
        "thematic",
        ("VRTX", "REGN", "GILD", "AMGN", "BIIB", "MRNA", "ILMN", "ALNY", "BMRN", "EXAS"),
    ),
    SectorDefinition(
        "nuclear",
        "Nuclear Power",
        "核电",
        "thematic",
        ("CEG", "VST", "CCJ", "OKLO", "SMR", "BWXT", "GEV", "LEU", "UEC", "NNE"),
    ),
]

ALL_SECTORS: list[SectorDefinition] = GICS_SECTORS + THEMATIC_SECTORS

MIN_CONSTITUENTS = 5  # 至少 5 只有效成分才计算板块指数


def all_leader_tickers() -> list[str]:
    tickers: set[str] = {BENCHMARK_TICKER}
    for s in ALL_SECTORS:
        tickers.update(s.leaders)
    return sorted(tickers)


def sector_by_id(sector_id: str) -> SectorDefinition | None:
    for s in ALL_SECTORS:
        if s.sector_id == sector_id:
            return s
    return None
