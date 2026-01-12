from pathlib import Path

import pandas as pd

from src.rdgt.variant_scoring import load_variant_model, score_variants


def main():
    data_path = Path("data/example_variants.csv")
    model_path = Path("models/variant_rf.joblib")

    print(f"Loading variants from {data_path}...")
    df = pd.read_csv(data_path)
    print(df)

    print(f"\nLoading model from {model_path}...")
    model = load_variant_model(model_path)

    print("\nScoring variants...")
    scored = score_variants(df, model)
    print(scored[["variant_id", "gene", "consequence", "impact", "polyphen", "af", "pathogenicity_score"]])

    out_path = Path("data/example_variants_scored.csv")
    scored.to_csv(out_path, index=False)
    print(f"\nSaved scored variants to {out_path}")


if __name__ == "__main__":
    main()

