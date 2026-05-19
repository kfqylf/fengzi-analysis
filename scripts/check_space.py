"""One-off diagnostic for space sector proxies."""
import yfinance as yf
import pandas as pd

tickers = ["ARKX", "ITA", "UFO", "ROKT", "WARP", "SPY", "SMH", "RKLB", "ASTS"]
raw = yf.download(tickers, period="6mo", auto_adjust=True, progress=False)
close = raw["Close"].dropna(how="all").sort_index()


def ret(col, days):
    s = close[col].dropna()
    if len(s) < days + 1:
        return None
    return (s.iloc[-1] / s.iloc[-(days + 1)] - 1) * 100


print("As of:", close.index[-1].date())
spy5 = ret("SPY", 5)
spy20 = ret("SPY", 20)
print(f"SPY 5d={spy5:+.2f}% 20d={ret('SPY', 20):+.2f}%")
print()
for t in tickers:
    if t not in close.columns:
        continue
    r5 = ret(t, 5)
    r20 = ret(t, 20)
    if r5 is None:
        continue
    print(f"{t:5} 5d={r5:+.2f}% 20d={r20:+.2f}%  rs5={r5 - spy5:+.2f}%")
