"""
Path resolution utilities for the Trading Lab project.

This module provides functions to reliably find project root and resolve
paths to data and model directories, regardless of where code is executed.
"""

from pathlib import Path
from typing import Optional


def get_project_root(start_path: Optional[Path] = None) -> Path:
    """
    Find the project root directory by looking for common markers.
    
    Searches for:
    - requirements.txt file
    - data/raw/ directory
    - models/ directory
    
    Args:
        start_path: Optional starting path for search. Defaults to current working directory.
    
    Returns:
        Path to project root directory
    
    Raises:
        FileNotFoundError: If project root cannot be determined
    """
    if start_path is None:
        start_path = Path.cwd()
    
    # Check current directory and parents for project root
    for check_path in [start_path, start_path.parent, start_path.parent.parent, 
                       start_path.parent.parent.parent, start_path.parent.parent.parent.parent]:
        # Check for common project markers
        if ((check_path / "requirements.txt").exists() or
            (check_path / "data" / "raw").exists() or
            (check_path / "models").exists() or
            (check_path / "src").exists()):
            return check_path.resolve()
    
    # If no project root found, use current directory as fallback
    return start_path.resolve()


def resolve_data_path(relative_path: str, data_type: str = "processed") -> Path:
    """
    Resolve a data file path relative to project root.
    
    Args:
        relative_path: Relative path to data file (e.g., "spy_featured.csv")
        data_type: Type of data directory ("raw" or "processed", default: "processed")
    
    Returns:
        Resolved absolute Path to the data file
    
    Example:
        >>> resolve_data_path("spy_featured.csv", "processed")
        Path('/path/to/project/data/processed/spy_featured.csv')
    """
    project_root = get_project_root()
    data_dir = project_root / "data" / data_type
    return (data_dir / relative_path).resolve()


def resolve_model_path(model_filename: str) -> Path:
    """
    Resolve a model file path relative to project root.
    
    Args:
        model_filename: Name of model file (e.g., "xgboost_spy_v1.pkl")
    
    Returns:
        Resolved absolute Path to the model file
    
    Example:
        >>> resolve_model_path("xgboost_spy_v1.pkl")
        Path('/path/to/project/models/xgboost_spy_v1.pkl')
    """
    project_root = get_project_root()
    models_dir = project_root / "models"
    return (models_dir / model_filename).resolve()


def find_data_file(pattern: str, data_type: str = "raw") -> Optional[Path]:
    """
    Find a data file matching a pattern in the data directory.
    
    Args:
        pattern: File pattern to search for (e.g., "SPY*.csv")
        data_type: Type of data directory ("raw" or "processed", default: "raw")
    
    Returns:
        Path to first matching file, or None if not found
    
    Example:
        >>> find_data_file("SPY*.csv", "raw")
        Path('/path/to/project/data/raw/SPY_D1_20251228_215819.csv')
    """
    project_root = get_project_root()
    data_dir = project_root / "data" / data_type
    
    if not data_dir.exists():
        return None
    
    matches = list(data_dir.glob(pattern))
    return matches[0] if matches else None

