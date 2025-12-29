# Trading Lab

A robust, modular stock forecasting system using Python, MetaTrader 5, and machine learning.

## Project Structure

```
trading-lab/
├── data/               # Storage for raw and processed market data
│   ├── raw/            # Untouched CSVs or JSONs from MT5/APIs
│   └── processed/      # Cleaned data with features added
├── notebooks/          # Jupyter notebooks for EDA (Exploratory Data Analysis)
├── src/                # The core Python "engine"
│   ├── ingestion/      # Scripts to pull data from MT5 or yfinance
│   ├── features/       # Signal processing (calculating indicators, FFTs, etc.)
│   ├── models/         # AI model definitions (XGBoost, LSTMs, etc.)
│   └── backtest/       # The "Simulator" to check performance
├── models/             # Saved model files (.pkl, .h5) after training
├── config/             # YAML/JSON files for API keys and hyperparameters
└── requirements.txt    # Python dependencies
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your settings in `config/` directory (see `config.example.yaml` for template)

## Usage

- Use Jupyter notebooks in `notebooks/` for exploratory data analysis
- Run ingestion scripts from `src/ingestion/` to pull market data
- Build features in `src/features/` for signal processing
- Train models in `src/models/`
- Backtest strategies in `src/backtest/`

## Coding Standards

- Type hinting for all Python functions
- Modular classes over long scripts
- Pandas DataFrames for all data handling
- Document mathematical logic of financial indicators
- Avoid look-ahead bias in backtesting
