"""Backward-compatible exports."""

from dataclasses import dataclass

from src.sectors import (
    ALL_SECTORS,
    BENCHMARK_TICKER,
    GICS_SECTORS,
    THEMATIC_SECTORS,
    SectorDefinition,
    all_leader_tickers,
)


@dataclass(frozen=True)
class Benchmark:
    ticker: str
    name_en: str
    name_zh: str


BENCHMARK = Benchmark(BENCHMARK_TICKER, "S&P 500", "标普500")


def all_tickers() -> list[str]:
    return all_leader_tickers()
