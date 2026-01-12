from pathlib import Path

import pandas as pd

from src.rdgt.variant_scoring import load_variant_model, score_variants
from src.rdgt.phenotype_matching import (
    load_diseases,
    build_tfidf_index,
    rank_diseases_for_phenotypes,
)
from src.rdgt.prioritization import aggregate_variant_scores_by_gene


def main():
    # --- Paths ---
    variants_path = Path("data/example_variants.csv")
    model_path = Path("models/variant_rf.joblib")
    diseases_path = Path("data/diseases.csv")
    out_variants_scored = Path("data/example_variants_scored.csv")
    out_genes_scored = Path("data/example_genes_scored.csv")
    out_diseases_ranked = Path("data/example_diseases_ranked.csv")

    # --- 1. Load and score variants ---
    print(f"Loading variants from {variants_path}...")
    df_variants = pd.read_csv(variants_path)
    print(df_variants)

    print(f"\nLoading variant model from {model_path}...")
    model = load_variant_model(model_path)

    print("\nScoring variants...")
    df_variants_scored = score_variants(df_variants, model)
    print(df_variants_scored[["variant_id", "gene", "consequence", "impact", "polyphen", "af", "pathogenicity_score"]])

    df_variants_scored.to_csv(out_variants_scored, index=False)
    print(f"\nSaved scored variants to {out_variants_scored}")

    # --- 2. Aggregate scores at gene level ---
    print("\nAggregating variant scores by gene...")
    df_genes = aggregate_variant_scores_by_gene(df_variants_scored)
    print(df_genes)

    df_genes.to_csv(out_genes_scored, index=False)
    print(f"Saved gene-level scores to {out_genes_scored}")

    # --- 3. Phenotype–disease matching ---
    print(f"\nLoading diseases from {diseases_path}...")
    df_diseases = load_diseases(diseases_path)
    print(df_diseases[["disease_id", "name"]])

    print("\nBuilding TF-IDF index over disease descriptions...")
    vectorizer, tfidf_matrix = build_tfidf_index(df_diseases)

    # Example case phenotypes – you can change this string
    phenotypes_text = "short stature, intellectual disability, limb abnormalities, distinctive facial features"
    print(f"\nPhenotypes for this case: {phenotypes_text}")

    df_diseases_ranked = rank_diseases_for_phenotypes(
        phenotypes_text,
        df_diseases,
        vectorizer,
        tfidf_matrix,
        top_k=5,
    )

    print("\nTop ranked diseases:")
    for _, row in df_diseases_ranked.iterrows():
        print(f"- {row['name']} (similarity={row['similarity']:.3f})")

    df_diseases_ranked.to_csv(out_diseases_ranked, index=False)
    print(f"\nSaved ranked diseases to {out_diseases_ranked}")

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()

