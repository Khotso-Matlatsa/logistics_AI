"""Lightweight model loader and inference helpers.

This module attempts to load scikit-learn style models saved as .pkl
from the project's `models/` directory and exposes simple prediction
wrappers used by `utils.analytics`.

Functions accept either a mapping (dict) of features or an iterable
of numeric feature values. For dict input, the helper now preserves the
pipeline's expected feature order via `feature_names_in_` when available.
Returned values are floats or None when no model is present.
"""
from __future__ import annotations

import os
import pickle
from typing import Any, Optional

try:
    import joblib  # type: ignore
except Exception:
    joblib = None  # type: ignore

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT, "models")


def _load_model(path: str) -> Optional[Any]:
    if not os.path.exists(path):
        return None
    try:
        if joblib:
            return joblib.load(path)
    except Exception:
        pass
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None


def _prepare_model_input(features: Any, model: Any):
    if features is None:
        return None

    try:
        import pandas as pd
    except Exception:
        pd = None  # type: ignore

    if pd is not None and isinstance(features, (pd.DataFrame, pd.Series)):
        return features

    if isinstance(features, dict):
        if pd is None:
            return None

        if hasattr(model, "feature_names_in_"):
            feature_names = list(model.feature_names_in_)
            missing = [name for name in feature_names if name not in features]
            if missing:
                return None
            return pd.DataFrame([{name: features[name] for name in feature_names}])

        return pd.DataFrame([features])

    if isinstance(features, (list, tuple)):
        return [list(features)]

    try:
        return [list(features)]
    except Exception:
        return None


def predict_shipping_days(features: Any) -> Optional[float]:
    """Predict shipping days using Days_of_shipping_linear.pkl if available."""
    path = os.path.join(MODELS_DIR, "Days_of_shipping_linear.pkl")
    model = _load_model(path)
    model_input = _prepare_model_input(features, model)
    if model is None or model_input is None:
        return None
    try:
        pred = model.predict(model_input)
        return float(pred[0])
    except Exception:
        return None


def predict_risk_probability(features: Any) -> Optional[float]:
    """Predict late-delivery probability using Latedelivery_logistic.pkl if available.

    Returns probability in 0-100 (percent) to match existing analytics expectations.
    """
    path = os.path.join(MODELS_DIR, "Latedelivery_logistic.pkl")
    model = _load_model(path)
    model_input = _prepare_model_input(features, model)
    if model is None or model_input is None:
        return None
    try:
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(model_input)
            p = float(proba[0][1])
            return p * 100.0
        else:
            pred = model.predict(model_input)
            return float(pred[0]) * 100.0
    except Exception:
        return None


def predict_profit(features: Any) -> Optional[float]:
    """Predict expected profit using Saleslinear.pkl (fallback) if available."""
    path = os.path.join(MODELS_DIR, "Saleslinear.pkl")
    if not os.path.exists(path):
        path = os.path.join(MODELS_DIR, "OPPOlinear.pkl")
    model = _load_model(path)
    model_input = _prepare_model_input(features, model)
    if model is None or model_input is None:
        return None
    try:
        pred = model.predict(model_input)
        return float(pred[0])
    except Exception:
        return None
