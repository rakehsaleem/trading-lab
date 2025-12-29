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

### Workflow

1. **Data Ingestion**: Run `src/ingestion/mt5_fetch.ipynb` to fetch historical market data
2. **Feature Engineering**: Run `src/features/build_features.ipynb` to calculate technical indicators
3. **Model Training**: Run `src/models/train_xgboost.ipynb` to train the prediction model
4. **Backtesting**: Run `src/backtest/simple_backtest.ipynb` to evaluate strategy performance
5. **Inference**: Run `src/models/predict_tomorrow.ipynb` to predict next day's price direction

### Making Predictions (Inference)

To predict whether SPY price will go **UP** or **DOWN** tomorrow:

1. **Run the prediction notebook**:
   ```bash
   jupyter notebook src/models/predict_tomorrow.ipynb
   ```

2. **Execute all cells** - The notebook will:
   - Fetch the latest 100 bars of SPY data from yfinance
   - Calculate technical indicators (RSI, EMA, ATR) for the most recent bar
   - Load the trained model from `models/xgboost_spy_v1.pkl` (or `.json`)
   - Generate a prediction with confidence score

3. **Expected Output**:
   ```
   ============================================================
   TOMORROW'S PREDICTION
   ============================================================
   Symbol: SPY
   Current Close: $690.31
   Prediction Date: 2025-12-26
   
   Tomorrow's Prediction: UP
   Confidence: 68.3%
   
   Probability Breakdown:
     UP:   68.3%
     DOWN: 31.7%
   ```

   The output includes:
   - **Symbol**: Trading symbol (default: SPY)
   - **Current Close**: Today's closing price
   - **Prediction Date**: Date of the prediction
   - **Tomorrow's Prediction**: UP or DOWN (price direction for tomorrow)
   - **Confidence**: Probability score (0-100%) for the predicted direction
   - **Probability Breakdown**: Full probability distribution (UP/DOWN percentages)

**Prerequisites**:
- A trained model must exist in `models/xgboost_spy_v1.pkl` (or `.json`)
- Internet connection for fetching latest market data
- All dependencies installed (`pip install -r requirements.txt`)

## Coding Standards

- Type hinting for all Python functions
- Modular classes over long scripts
- Pandas DataFrames for all data handling
- Document mathematical logic of financial indicators
- Avoid look-ahead bias in backtesting

## Utilities

The project includes a shared utilities module (`src/utils/`) for common operations:

- **Path Resolution**: `get_project_root()`, `resolve_data_path()`, `resolve_model_path()`
- **Data Loading**: `load_raw_data()`, `load_processed_data()`
- **Model Loading**: `load_trained_model()` (auto-detects .pkl/.json)
- **Configuration**: `load_config()`, `get_config_value()`
