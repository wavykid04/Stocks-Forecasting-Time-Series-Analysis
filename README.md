# 📈 TCS Stock Portfolio Forecasting
### End-to-End Time-Series Analysis on NIFTY50 TCS Data

> A decade of Tata Consultancy Services NIFTY50 stock data, stress-tested across **6 time-series models**, with SARIMA deployed for price forecasting.

---

## Overview

This project performs rigorous time-series analysis and forecasting on real-world TCS (Tata Consultancy Services) NIFTY50 stock closing prices. Starting from raw NSE data, it covers data cleaning, stationarity testing, seasonality analysis, model selection via AIC/BIC, and rolling forecast evaluation across 6 model variants.

---

## Models Evaluated

| # | Model | Notes |
|---|-------|-------|
| 1 | Naive Baseline | Last-value carry-forward |
| 2 | Exponential Smoothing | Single, double, triple |
| 3 | ARIMA | Order selection via AIC/BIC |
| 4 | SARIMA | Seasonal variant |
| 5 | ARIMAX | With exogenous features |
| 6 | Auto-ARIMA (grid search) | Exhaustive parameter search |

---

## Key Results

| Model | Configuration | Result |
|-------|--------------|--------|
| **Selected ARIMA** | (2, 1, 2) | Best AIC/BIC score |
| **Deployed SARIMA** | (0,1,3)×(0,1,3,10) | Ljung-Box p = **0.99** (residuals white noise) |
| **Forecast trend** | — | Upward trend in TCS closing prices |

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
(6 models stress-tested)
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

### Requirements
```
pandas
numpy
matplotlib
statsmodels
scipy
scikit-learn
```

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
├── requirements.txt
├── README.md
└── data/
    └── compiled security TCS.csv   # Add your NSE data here
```

---

## Diagnostics

The deployed SARIMA (0,1,3)×(0,1,3,10) passes:
- **Ljung-Box test** (p = 0.99) — residuals are white noise, no autocorrelation remaining
- **ADF test** on differenced series — stationary confirmed before model fit

---

## Author
**Pragna Das** · B.E. Civil Engineering, BITS Pilani (2027)  
`F20230252@pilani.bits-pilani.ac.in`
