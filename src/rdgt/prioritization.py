"""
Case-level prioritization: combine variant scores and phenotype–disease scores.

In the future, this can:
- aggregate variant pathogenicity per gene,
- combine gene-level scores with disease similarity scores,
- output a ranked list of candidate genes/diseases for a case.
"""

import pandas as pd


def aggregate_variant_scores_by_gene(df_variants: pd.DataFrame) -> pd.DataFrame:
    """
    Simple gene-level aggregation: mean pathogenicity_score per gene.

    Requires columns: 'gene', 'pathogenicity_score'.
    """
    if not {"gene", "pathogenicity_score"}.issubset(df_variants.columns):
        raise ValueError("df_variants must have 'gene' and 'pathogenicity_score' columns.")

    df_gene = (
        df_variants.groupby("gene")["pathogenicity_score"]
        .mean()
        .reset_index()
        .rename(columns={"pathogenicity_score": "gene_score"})
    )
    return df_gene

