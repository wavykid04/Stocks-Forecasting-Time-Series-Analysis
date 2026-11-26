"""Raw data loaders: NSE CSV export and yfinance (with local cache)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .clean import clean_prices


def load_nse_csv(path: str | Path, freq: str | None = "B") -> pd.DataFrame:
    """Load an NSE historical-data CSV (e.g. 'compiled security TCS.csv')."""
    raw = pd.read_csv(path, dtype=str, skipinitialspace=True)
    return clean_prices(raw, date_col="date", freq=freq, dayfirst=True)


def _cache_path(cache_dir: Path, symbol: str, start: str | None, end: str | None) -> Path:
    safe = symbol.replace(".", "_").replace("^", "")
    return cache_dir / f"{safe}_{start or 'min'}_{end or 'latest'}.csv"


def load_yfinance(
    symbol: str = "TCS.NS",
    start: str | None = None,
    end: str | None = None,
    cache_dir: str | Path = "data/raw",
    refresh: bool = False,
    freq: str | None = "B",
) -> pd.DataFrame:
    """Download daily OHLCV from Yahoo Finance, caching the raw table as CSV.

    The cached file is reused unless ``refresh`` is True. Note that an
    open-ended ``end`` (None) is cached too; pass ``refresh=True`` to update.
    """
    cache_dir = Path(cache_dir)
    path = _cache_path(cache_dir, symbol, start, end)
    if path.exists() and not refresh:
        raw = pd.read_csv(path)
    else:
        import yfinance as yf  # imported lazily so tests need no network/package

        raw = yf.download(symbol, start=start, end=end, auto_adjust=False, progress=False)
        if raw is None or raw.empty:
            raise RuntimeError(f"yfinance returned no data for {symbol!r}")
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        raw = raw.reset_index()
        cache_dir.mkdir(parents=True, exist_ok=True)
        raw.to_csv(path, index=False)
    return clean_prices(raw, date_col="date", freq=freq)


def load_from_config(cfg: dict) -> pd.DataFrame:
    src = cfg["source"]
    if src["kind"] == "nse_csv":
        return load_nse_csv(src["nse_csv_path"])
    if src["kind"] == "yfinance":
        return load_yfinance(src["symbol"], src.get("start"), src.get("end"), src.get("cache_dir", "data/raw"))
    raise ValueError(f"unknown source kind: {src['kind']!r}")
