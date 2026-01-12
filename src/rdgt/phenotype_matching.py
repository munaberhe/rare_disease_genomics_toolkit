"""
Phenotype–disease matching utilities.

This will wrap the BM25 / TF-IDF / LLM approaches from your
phenotype_disease_matching project into reusable functions.
"""

from typing import List, Tuple
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_tfidf_disease_index(df_diseases: pd.DataFrame, text_col: str = "description"):
    """
    Build a simple TF-IDF index over disease descriptions.

    Returns:
    - fitted vectorizer
    - TF-IDF matrix
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df_diseases[text_col])
    return vectorizer, tfidf_matrix


def rank_diseases_for_case(
    phenotypes_text: str,
    df_diseases: pd.DataFrame,
    vectorizer,
    tfidf_matrix,
    text_col: str = "description",
    top_k: int = 10,
) -> pd.DataFrame:
    """
    Rank diseases based on cosine similarity between the case phenotypes
    and disease descriptions.
    """
    query_vec = vectorizer.transform([phenotypes_text])
    sims = cosine_similarity(query_vec, tfidf_matrix)[0]
    df = df_diseases.copy()
    df["similarity"] = sims
    df = df.sort_values("similarity", ascending=False).head(top_k)
    return df

