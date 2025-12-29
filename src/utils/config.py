"""
Configuration loading utilities for the Trading Lab project.

This module provides functions to load and access configuration values
from YAML configuration files.
"""

from pathlib import Path
from typing import Any, Optional, Dict
import yaml


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Optional path to config file. If None, searches for config.yaml
                     in project root or config/ directory.
    
    Returns:
        Dictionary containing configuration values
    
    Raises:
        FileNotFoundError: If config file cannot be found
        yaml.YAMLError: If config file cannot be parsed
    
    Example:
        >>> config = load_config()
        >>> symbol = config['trading']['symbol']
    """
    if config_path is None:
        # Try to find config file in project root or config/ directory
        from .paths import get_project_root
        
        project_root = get_project_root()
        possible_paths = [
            project_root / "config.yaml",
            project_root / "config" / "config.yaml",
            project_root / "config" / "config.example.yaml",
        ]
        
        for path in possible_paths:
            if path.exists():
                config_path = path
                break
        else:
            # Return default config if no file found
            return _get_default_config()
    
    if not config_path.exists():
        return _get_default_config()
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}
    
    # Merge with defaults to ensure all keys exist
    default_config = _get_default_config()
    return _merge_config(default_config, config)


def get_config_value(config: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get a configuration value using dot-notation path.
    
    Args:
        config: Configuration dictionary
        key_path: Dot-separated path to value (e.g., "trading.symbol")
        default: Default value if key not found
    
    Returns:
        Configuration value or default
    
    Example:
        >>> config = load_config()
        >>> symbol = get_config_value(config, "trading.symbol", "SPY")
        >>> horizon = get_config_value(config, "features.horizon_days", 5)
    """
    keys = key_path.split('.')
    value = config
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value


def _get_default_config() -> Dict[str, Any]:
    """Get default configuration values."""
    return {
        'trading': {
            'symbol': 'SPY',
            'timeframe': 'D1',
            'lookback_days': 5000,
        },
        'features': {
            'horizon_days': 5,
            'rsi_period': 14,
            'ema_short': 20,
            'ema_long': 50,
            'atr_period': 14,
        },
        'model': {
            'n_estimators': 100,
            'learning_rate': 0.05,
            'train_ratio': 0.8,
            'random_state': 42,
        },
        'backtest': {
            'initial_capital': 100.0,
            'commission_rate': 0.001,  # 0.1%
            'slippage': 0.0001,  # 0.01%
        },
    }


def _merge_config(default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    """Merge user config with defaults, recursively."""
    result = default.copy()
    
    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_config(result[key], value)
        else:
            result[key] = value
    
    return result

