"""
Model loading utilities for the Trading Lab project.

This module provides functions to load trained models with automatic
format detection (XGBoost .json or sklearn .pkl).
"""

from pathlib import Path
from typing import Tuple, Any, Optional
import joblib
from .paths import resolve_model_path, get_project_root


def load_trained_model(
    model_name: str = "xgboost_spy_v1",
    model_path: Optional[Path] = None
) -> Tuple[Any, str]:
    """
    Load trained model from file with automatic format detection.
    
    Supports both XGBoost (.json) and scikit-learn (.pkl) formats.
    Automatically detects which format is available.
    
    Args:
        model_name: Base name of model file without extension (default: "xgboost_spy_v1")
        model_path: Optional direct path to model file. If None, searches for model.
    
    Returns:
        Tuple of (model, model_type) where model_type is 'xgboost' or 'sklearn'
    
    Raises:
        FileNotFoundError: If model file cannot be found
        ImportError: If XGBoost is required but not available
    
    Example:
        >>> model, model_type = load_trained_model()
        >>> model, model_type = load_trained_model("xgboost_spy_v2")
    """
    # Try to import xgboost (may fail on macOS without libomp)
    xgb = None
    xgboost_available = False
    try:
        import xgboost as xgb
        xgboost_available = True
    except Exception:
        pass
    
    if model_path:
        possible_paths = [Path(model_path)]
    else:
        # Try multiple possible locations and formats
        from .paths import get_project_root, resolve_model_path
        
        project_root = get_project_root()
        possible_paths = [
            resolve_model_path(f"{model_name}.pkl"),
            resolve_model_path(f"{model_name}.json"),
            project_root / "models" / f"{model_name}.pkl",
            project_root / "models" / f"{model_name}.json",
            Path(f"models/{model_name}.pkl"),
            Path(f"models/{model_name}.json"),
            Path(f"../models/{model_name}.pkl"),
            Path(f"../models/{model_name}.json"),
        ]
    
    model = None
    model_type = None
    
    for path in possible_paths:
        if not path.exists():
            continue
        
        if path.suffix == '.json':
            if not xgboost_available:
                continue
            try:
                model_booster = xgb.Booster()
                model_booster.load_model(str(path))
                xgb_classifier = xgb.XGBClassifier()
                xgb_classifier._Booster = model_booster
                model = xgb_classifier
                model_type = 'xgboost'
                break
            except Exception:
                continue
        elif path.suffix == '.pkl':
            try:
                model = joblib.load(path)
                model_type = 'sklearn'
                break
            except Exception:
                continue
    
    if model is None:
        project_root = get_project_root()
        raise FileNotFoundError(
            f"Could not find model file '{model_name}'. Tried:\n"
            f"  - {project_root / 'models' / f'{model_name}.pkl'}\n"
            f"  - {project_root / 'models' / f'{model_name}.json'}\n"
            f"Please ensure model file exists in {project_root / 'models'}"
        )
    
    return model, model_type

