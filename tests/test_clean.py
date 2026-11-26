import io

import pandas as pd
import pytest

from tsforecast.data.clean import clean_prices, parse_numeric
from tsforecast.data.sources import load_nse_csv, load_yfinance

NSE_CSV = """Date , Open Price , Close Price , Total Traded Quantity , Turnover ₹
05-Jan-2024 , "3,700.00" , "3,710.50" , "1,200" , "4,452,600.00"
02-Jan-2024 , "3,650.00" , "3,660.25" , "1,000" , "3,660,250.00"
03-Jan-2024 , "3,660.00" , "3,670.00" , "1,100" , "4,037,000.00"
03-Jan-2024 , "3,661.00" , "3,671.00" , "1,150" , "4,221,650.00"
"""


@pytest.fixture
def raw():
    return pd.read_csv(io.StringIO(NSE_CSV), dtype=str, skipinitialspace=True)


def test_parse_numeric_handles_commas_and_whitespace():
    s = pd.Series([" 1,234.5 ", "₹2,000", "-", ""])
    out = parse_numeric(s)
    assert out.iloc[0] == 1234.5
    assert out.iloc[1] == 2000.0
    assert out.iloc[2:].isna().all()


def test_clean_prices(raw):
    df = clean_prices(raw, dayfirst=True)
    assert list(df.columns) == ["open", "close", "volume", "turnover"]
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.is_monotonic_increasing and df.index.is_unique
    assert df.index.freqstr == "B"
    # 2024-01-02 .. 2024-01-05 business days; 01-04 missing -> NaN, not filled
    assert list(df.index.strftime("%Y-%m-%d")) == ["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
    assert pd.isna(df.loc["2024-01-04", "close"])
    # duplicate date keeps last row
    assert df.loc["2024-01-03", "close"] == 3671.0
    assert df.loc["2024-01-05", "volume"] == 1200.0
    assert all(pd.api.types.is_float_dtype(df[c]) for c in df.columns)


def test_clean_without_freq(raw):
    df = clean_prices(raw, dayfirst=True, freq=None)
    assert len(df) == 3


def test_load_nse_csv(tmp_path):
    p = tmp_path / "tcs.csv"
    p.write_text(NSE_CSV, encoding="utf-8")
    df = load_nse_csv(p)
    assert df["close"].dropna().iloc[-1] == 3710.50


def test_load_yfinance_uses_cache(tmp_path, monkeypatch):
    import sys

    monkeypatch.setitem(sys.modules, "yfinance", None)  # any import would fail
    (tmp_path / "TCS_NS_2024-01-01_2024-01-10.csv").write_text(
        "Date,Open,High,Low,Close,Adj Close,Volume\n"
        "2024-01-02,3650,3700,3640,3660.25,3600,1000\n"
        "2024-01-03,3660,3690,3650,3670,3610,1100\n",
        encoding="utf-8",
    )
    df = load_yfinance("TCS.NS", "2024-01-01", "2024-01-10", cache_dir=tmp_path)
    assert list(df.columns) == ["open", "high", "low", "close", "adj_close", "volume"]
    assert df["close"].iloc[-1] == 3670.0
