# src/utils/prices.py
from __future__ import annotations

import time
from typing import Dict, Iterable, List, Tuple

import pandas as pd
import yfinance as yf


def _download_prices(
    symbols: List[str],
    period: str = "5d",
    interval: str = "1d",
    timeout: int = 30,
) -> pd.DataFrame:
    """
    Download recent close prices from yfinance.
    Uses group_by='ticker' so we can handle per-symbol failures.
    """
    if not symbols:
        return pd.DataFrame()

    df = yf.download(
        tickers=" ".join(symbols),
        period=period,
        interval=interval,
        group_by="ticker",
        auto_adjust=True,
        threads=True,
        progress=False,
        timeout=timeout,
    )
    return df


def latest_prices(
    symbols: Iterable[str],
    retries: int = 3,
    sleep_seconds: float = 2.0,
    timeout: int = 30,
    allow_partial: bool = True,
) -> Dict[str, float]:
    """
    Returns {symbol: last_close_price}.

    - Retries on transient yfinance/network issues.
    - If allow_partial=True, symbols with missing prices are skipped instead of raising.
    """
    syms = [s.strip().upper() for s in symbols if s and str(s).strip()]
    if not syms:
        return {}

    last_exc = None
    df = None

    for attempt in range(1, retries + 1):
        try:
            df = _download_prices(syms, timeout=timeout)
            break
        except Exception as e:
            last_exc = e
            if attempt < retries:
                time.sleep(sleep_seconds * attempt)

    if df is None:
        raise RuntimeError(f"Price download failed after {retries} retries: {last_exc}")

    prices: Dict[str, float] = {}

    # Case 1: multiple tickers => columns often become a MultiIndex (Ticker, OHLCV)
    # Case 2: single ticker => columns are flat ('Open','High','Low','Close',...)
    if isinstance(df.columns, pd.MultiIndex):
        for sym in syms:
            if sym in df.columns.get_level_values(0):
                try:
                    close_series = df[sym]["Close"].dropna()
                    if len(close_series) > 0:
                        prices[sym] = float(close_series.iloc[-1])
                except Exception:
                    pass
    else:
        # single symbol
        try:
            close_series = df["Close"].dropna()
            if len(close_series) > 0:
                prices[syms[0]] = float(close_series.iloc[-1])
        except Exception:
            pass

    missing = [s for s in syms if s not in prices]
    if missing and not allow_partial:
        raise RuntimeError(f"No price data for: {missing}")

    return prices
