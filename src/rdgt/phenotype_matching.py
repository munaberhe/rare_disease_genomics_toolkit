"""
Phenotype–disease matching utilities.

This module provides:
- a simple TF-IDF index over disease descriptions,
- a function to rank diseases for a given phenotype description.

It is intentionally lightweight and can later be extended to:
- BM25 ranking,
- LLM-based scoring,
- HPO / ontology-aware methods.
"""

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_diseases(diseases_path: str | Path) -> pd.DataFrame:
    """
    Load a small disease knowledge base from CSV.

    Expected columns:
    - disease_id
    - name
    - description
    """
    diseases_path = Path(diseases_path)
    df = pd.read_csv(diseases_path)
    required = {"disease_id", "name", "description"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in diseases CSV: {missing}")
    return df


def build_tfidf_index(
    df_diseases: pd.DataFrame,
    text_col: str = "description",
) -> Tuple[TfidfVectorizer, any]:
    """
    Build a TF-IDF index over disease descriptions.

    Returns:
    - fitted TfidfVectorizer
    - TF-IDF matrix (sparse)
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df_diseases[text_col])
    return vectorizer, tfidf_matrix


def rank_diseases_for_phenotypes(
    phenotypes_text: str,
    df_diseases: pd.DataFrame,
    vectorizer: TfidfVectorizer,
    tfidf_matrix,
    text_col: str = "description",
    top_k: int = 5,
) -> pd.DataFrame:
    """
    Rank diseases based on cosine similarity between the case phenotype text
    and disease descriptions.

    Returns a copy of df_diseases with an extra 'similarity' column, sorted
    descending by similarity, limited to top_k.
    """
    query_vec = vectorizer.transform([phenotypes_text])
    sims = cosine_similarity(query_vec, tfidf_matrix)[0]
    out = df_diseases.copy()
    out["similarity"] = sims
    out = out.sort_values("similarity", ascending=False).head(top_k)
    return out

