# 📈 TCS Stock Portfolio Forecasting
### End-to-End Time-Series Analysis on NIFTY50 TCS Data

> A decade of Tata Consultancy Services NIFTY50 stock data, analysed with ARIMA-family models, with a SARIMA model fitted for price forecasting.
>
> **Status:** work in progress. There is no out-of-sample evaluation yet (a walk-forward backtest is coming), so no forecast-accuracy claims are made below.

---

## Overview

This project performs rigorous time-series analysis and forecasting on real-world TCS (Tata Consultancy Services) NIFTY50 stock closing prices. Starting from raw NSE data, it covers data cleaning, stationarity testing, seasonality analysis, and in-sample model fitting with AIC/BIC comparison. Rolling (walk-forward) forecast evaluation is planned but not yet implemented.

---

## Models

| # | Model | Status |
|---|-------|--------|
| 1 | Naive Baseline | Planned (backtest phase) |
| 2 | Exponential Smoothing / ETS | **Not yet implemented** |
| 3 | AR / MA / ARMA / ARIMA | Fitted in-sample in `TCS_TSA.ipynb` |
| 4 | SARIMA | Fitted in-sample in `Arima.ipynb` |
| 5 | ARIMAX | **Not yet implemented** |
| 6 | Auto-ARIMA (grid search) | **Not yet implemented** |

---

## Key Results

| Model | Configuration | Result |
|-------|--------------|--------|
| **Selected ARIMA** | (2, 1, 2) | Best AIC/BIC score |
| **Fitted SARIMA** (`Arima.ipynb`) | (2,1,3)×(2,1,3,10) | In-sample fit only; residual diagnostics, not forecast accuracy |
| **Out-of-sample accuracy** | — | Not yet measured (backtest coming) |

---

## Pipeline

```
Raw NSE CSV Data
      │
      ▼
Data Cleaning & Type Conversion
(strip whitespace, remove commas, parse ₹ columns)
      │
      ▼
EDA & Visualisation
(price history, volume, moving averages, seasonality decomposition)
      │
      ▼
Stationarity Testing
(Augmented Dickey-Fuller test → first differencing applied)
      │
      ▼
ACF / PACF Analysis
(lag identification for p, q parameters)
      │
      ▼
Model Training & AIC/BIC Selection
(in-sample; walk-forward backtest planned)
      │
      ▼
SARIMA Deployment & Diagnostic Checks
(Ljung-Box, residual analysis)
      │
      ▼
10-Step Ahead Forecast
```

---

## Data

**Source:** NSE historical data for TCS (NIFTY50 constituent)  
**File:** `compiled security TCS.csv` (not included — download from NSE or your broker)

**Columns used:**
- `Date` — Trading date
- `Close Price` — Primary forecasting target
- `Open Price`, `High Price`, `Low Price`, `Prev Close`
- `Total Traded Quantity`, `Turnover ₹`, `No. of Trades`

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/TCS-StockForecasting.git
cd TCS-StockForecasting
pip install -r requirements.txt
```

### Package (Python 3.11)
```bash
pip install -e ".[dev]"   # pinned deps from pyproject.toml
pytest -q
```

```python
from tsforecast.data.sources import load_yfinance, load_nse_csv
df = load_yfinance("TCS.NS", start="2014-01-01")   # cached under data/raw/
# or: df = load_nse_csv("data/compiled security TCS.csv")
```
See `configs/tcs.yaml` for the data source settings.

---

## Usage

### Step 1 — Add your data
Place `compiled security TCS.csv` in the project root.

### Step 2 — Run EDA notebook
```
TCS_TSA.ipynb   # Data cleaning, EDA, stationarity tests, visualisations
```

### Step 3 — Run ARIMA/SARIMA notebook
```
Arima.ipynb     # Model selection, SARIMA deployment, forecast plot
```

---

## Project Structure

```
TCS-StockForecasting/
├── TCS_TSA.ipynb               # EDA and data analysis
├── Arima.ipynb                 # ARIMA/SARIMA modelling and forecasting
├── pyproject.toml
├── configs/tcs.yaml
├── src/tsforecast/data/     # sources.py (loaders), clean.py (cleaning)
├── tests/
├── requirements.txt
├── README.md
└── data/
    └── compiled security TCS.csv   # Add your NSE data here
```

---

## Diagnostics

The SARIMA actually fitted in `Arima.ipynb` is (2,1,3)×(2,1,3,10). Residual diagnostics (e.g. Ljung-Box) describe in-sample fit only and are not a measure of forecast accuracy. The seasonal period s=10 on daily trading data is not yet justified (a trading week is 5 days) and will be revisited in the backtest phase.
- **ADF test** on differenced series — stationarity checked before model fit

---

## Author
**Pragna Das** · B.E. Civil Engineering, BITS Pilani (2027)  
`F20230252@pilani.bits-pilani.ac.in`
