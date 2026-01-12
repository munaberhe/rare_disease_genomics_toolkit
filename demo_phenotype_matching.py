from pathlib import Path

from src.rdgt.phenotype_matching import (
    load_diseases,
    build_tfidf_index,
    rank_diseases_for_phenotypes,
)


def main():
    diseases_path = Path("data/diseases.csv")
    print(f"Loading diseases from {diseases_path}...")
    df_diseases = load_diseases(diseases_path)
    print(df_diseases[["disease_id", "name"]])

    print("\nBuilding TF-IDF index...")
    vectorizer, tfidf_matrix = build_tfidf_index(df_diseases)

    # Example case: you can change this text to test different phenotypes
    phenotypes_text = "short stature, intellectual disability, limb abnormalities, distinctive facial features"
    print(f"\nPhenotypes: {phenotypes_text}")

    ranked = rank_diseases_for_phenotypes(
        phenotypes_text,
        df_diseases,
        vectorizer,
        tfidf_matrix,
        top_k=5,
    )

    print("\nTop ranked diseases:")
    for _, row in ranked.iterrows():
        print(f"- {row['name']} (similarity={row['similarity']:.3f})")

    out_path = Path("data/phenotype_matching_example.csv")
    ranked.to_csv(out_path, index=False)
    print(f"\nSaved ranked diseases to {out_path}")


if __name__ == "__main__":
    main()

