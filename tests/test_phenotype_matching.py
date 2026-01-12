from pathlib import Path

from src.rdgt.phenotype_matching import (
    load_diseases,
    build_tfidf_index,
    rank_diseases_for_phenotypes,
)


def test_phenotype_matching_ranks_diseases():
    diseases_path = Path("data/diseases.csv")
    assert diseases_path.exists(), "data/diseases.csv is missing"

    df_diseases = load_diseases(diseases_path)
    vectorizer, tfidf_matrix = build_tfidf_index(df_diseases)

    phenotypes_text = "short stature, intellectual disability, limb abnormalities"
    ranked = rank_diseases_for_phenotypes(
        phenotypes_text,
        df_diseases,
        vectorizer,
        tfidf_matrix,
        top_k=3,
    )

    # should return at most 3 diseases, with a similarity column
    assert len(ranked) <= 3
    assert "similarity" in ranked.columns
    # similarities are between 0 and 1
    assert ranked["similarity"].between(0, 1).all()

