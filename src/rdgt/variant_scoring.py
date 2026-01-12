"""
Variant-level scoring and pathogenicity prediction.

This module:
- loads a pre-trained RandomForest (or similar) model saved with joblib,
- assumes a ClinVar-style feature set,
- returns per-variant pathogenicity scores.
"""

from pathlib import Path
from typing import Any, Sequence

import joblib
import pandas as pd


FEATURE_COLS: Sequence[str] = ["gene", "consequence", "impact", "polyphen", "af"]


def load_variant_model(model_path: str | Path) -> Any:
    """
    Load a pre-trained variant pathogenicity model (e.g. RandomForest pipeline).

    The model is expected to be a scikit-learn Pipeline that:
    - takes a DataFrame with columns FEATURE_COLS
    - exposes predict_proba(X)[:, 1] for pathogenicity scores
    """
    model_path = Path(model_path)
    model = joblib.load(model_path)
    return model


def prepare_features(df_variants: pd.DataFrame) -> pd.DataFrame:
    """
    Select and return the feature columns expected by the model.

    This assumes df_variants has columns matching FEATURE_COLS.
    """
    missing = [c for c in FEATURE_COLS if c not in df_variants.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")
    return df_variants[FEATURE_COLS].copy()


def score_variants(df_variants: pd.DataFrame, model: Any) -> pd.DataFrame:
    """
    Apply the model to a variants DataFrame and return a copy with an extra
    'pathogenicity_score' column.

    Parameters
    ----------
    df_variants : DataFrame
        Must contain at least FEATURE_COLS.
    model : Any
        A fitted model/pipeline with predict_proba.

    Returns
    -------
    DataFrame
        Original variants plus 'pathogenicity_score' between 0 and 1.
    """
    X = prepare_features(df_variants)
    proba = model.predict_proba(X)[:, 1]
    out = df_variants.copy()
    out["pathogenicity_score"] = proba
    return out

