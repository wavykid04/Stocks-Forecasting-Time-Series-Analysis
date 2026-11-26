"""Cleaning for raw NSE / yfinance price tables."""
from __future__ import annotations

import re

import pandas as pd

# Map raw NSE column names (after stripping) to canonical snake_case names.
NSE_COLUMN_MAP = {
    "Date": "date",
    "Open Price": "open",
    "High Price": "high",
    "Low Price": "low",
    "Close Price": "close",
    "Prev Close": "prev_close",
    "Total Traded Quantity": "volume",
    "Turnover ₹": "turnover",
    "No. of Trades": "trades",
}


def _canonical(col: str) -> str:
    col = str(col).strip()
    if col in NSE_COLUMN_MAP:
        return NSE_COLUMN_MAP[col]
    return re.sub(r"[^0-9a-z]+", "_", col.lower()).strip("_")


def parse_numeric(s: pd.Series) -> pd.Series:
    """Parse strings like ' 1,234.50 ' or '₹1,234' to float; invalid -> NaN."""
    if pd.api.types.is_numeric_dtype(s):
        return s.astype(float)
    cleaned = (
        s.astype(str)
        .str.strip()
        .str.replace(r"[,₹\s]", "", regex=True)
        .replace({"": None, "-": None, "nan": None, "None": None})
    )
    return pd.to_numeric(cleaned, errors="coerce")


def clean_prices(
    df: pd.DataFrame,
    date_col: str = "date",
    freq: str | None = "B",
    dayfirst: bool | None = None,
) -> pd.DataFrame:
    """Return a cleaned price frame.

    Steps: strip column names/values, canonicalise names, parse numerics
    (commas, currency), build a sorted DatetimeIndex, drop duplicate dates
    (keep last), and optionally reindex to business-day frequency (missing
    days are left as NaN, not filled).
    """
    out = df.copy()
    out.columns = [_canonical(c) for c in out.columns]
    if date_col not in out.columns:
        raise KeyError(f"date column {date_col!r} not found in {list(out.columns)}")

    for c in out.columns:
        if out[c].dtype == object:
            out[c] = out[c].astype(str).str.strip()

    dates = out.pop(date_col)
    if not pd.api.types.is_datetime64_any_dtype(dates):
        dates = pd.to_datetime(dates, dayfirst=bool(dayfirst), errors="coerce", format="mixed")
    dates = pd.DatetimeIndex(dates)
    if dates.tz is not None:
        dates = dates.tz_localize(None)
    out.index = dates.normalize()
    out.index.name = "date"
    out = out[out.index.notna()]

    for c in out.columns:
        parsed = parse_numeric(out[c])
        # keep non-numeric columns (e.g. symbol/series) untouched
        if parsed.notna().any() or out[c].isna().all():
            out[c] = parsed

    out = out[~out.index.duplicated(keep="last")].sort_index()
    if freq is not None and len(out):
        out = out.asfreq(freq)
    return out
