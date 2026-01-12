from pathlib import Path

import pandas as pd

from src.rdgt.variant_scoring import load_variant_model, score_variants


def test_score_variants_adds_column():
    data_path = Path("data/example_variants.csv")
    model_path = Path("models/variant_rf.joblib")

    assert data_path.exists(), "example_variants.csv is missing"
    assert model_path.exists(), "variant_rf.joblib is missing"

    df = pd.read_csv(data_path)
    model = load_variant_model(model_path)

    scored = score_variants(df, model)

    # should add a pathogenicity_score column
    assert "pathogenicity_score" in scored.columns
    # scores should be between 0 and 1
    assert scored["pathogenicity_score"].between(0, 1).all()

