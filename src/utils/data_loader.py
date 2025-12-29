"""
Data loading utilities for the Trading Lab project.

This module provides functions to load raw and processed data files
with automatic path resolution and data validation.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
from .paths import resolve_data_path, find_data_file, get_project_root


def load_raw_data(
    filename: Optional[str] = None,
    pattern: str = "SPY*.csv",
    symbol: str = "SPY"
) -> pd.DataFrame:
    """
    Load raw OHLCV data from CSV file.
    
    If filename is not provided, automatically searches for files matching
    the pattern in the data/raw directory.
    
    Args:
        filename: Optional specific filename to load
        pattern: File pattern to search for if filename not provided (default: "SPY*.csv")
        symbol: Trading symbol for auto-detection (default: "SPY")
    
    Returns:
        DataFrame with OHLCV data (columns: time, open, high, low, close, volume)
    
    Raises:
        FileNotFoundError: If no data file is found
        ValueError: If required columns are missing
    
    Example:
        >>> df = load_raw_data()  # Auto-detect SPY CSV
        >>> df = load_raw_data("SPY_D1_20251228_215819.csv")  # Specific file
    """
    if filename:
        csv_path = resolve_data_path(filename, "raw")
        if not csv_path.exists():
            raise FileNotFoundError(f"Raw data file not found: {csv_path}")
    else:
        # Auto-detect file
        csv_path = find_data_file(pattern, "raw")
        if csv_path is None:
            # Try alternative patterns
            csv_path = find_data_file(f"{symbol}*.csv", "raw")
            if csv_path is None:
                project_root = get_project_root()
                raise FileNotFoundError(
                    f"No {symbol} CSV files found in {project_root / 'data' / 'raw'}. "
                    f"Please ensure raw data exists or specify filename directly."
                )
    
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Ensure time column is datetime
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], utc=True)
    elif 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], utc=True)
        df.rename(columns={'date': 'time'}, inplace=True)
    elif 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df.rename(columns={'Date': 'time'}, inplace=True)
    
    # Sort by time to ensure chronological order
    df = df.sort_values('time').reset_index(drop=True)
    
    # Validate required columns
    required_cols = ['time', 'open', 'high', 'low', 'close']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    return df


def load_processed_data(filename: str = "spy_featured.csv") -> pd.DataFrame:
    """
    Load processed feature data from CSV file.
    
    Args:
        filename: Name of processed data file (default: "spy_featured.csv")
    
    Returns:
        DataFrame with features and target
    
    Raises:
        FileNotFoundError: If processed data file is not found
    
    Example:
        >>> df = load_processed_data()
        >>> df = load_processed_data("spy_featured_v2.csv")
    """
    csv_path = resolve_data_path(filename, "processed")
    
    if not csv_path.exists():
        project_root = get_project_root()
        raise FileNotFoundError(
            f"Processed data file not found: {csv_path}\n"
            f"Please ensure processed data exists in {project_root / 'data' / 'processed'}"
        )
    
    df = pd.read_csv(csv_path)
    
    # Ensure time column is datetime
    if 'time' in df.columns:
        df['time'] = pd.to_datetime(df['time'], utc=True)
    
    # Sort by time to ensure chronological order
    df = df.sort_values('time').reset_index(drop=True)
    
    return df

