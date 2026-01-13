from typing import Dict, Iterable
import yfinance as yf


def latest_prices(symbols: Iterable[str]) -> Dict[str, float]:
    symbols = list(symbols)

    data = yf.download(
        tickers=" ".join(symbols),
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=True,
        group_by="ticker",
        threads=True,
    )

    prices = {}
    for sym in symbols:
        if len(symbols) == 1:
            close_series = data["Close"].dropna()
        else:
            close_series = data[sym]["Close"].dropna()

        if close_series.empty:
            raise RuntimeError(f"No price data for {sym}")
        prices[sym] = float(close_series.iloc[-1])

    return prices
