"""
VCF filtering utilities for rare disease analysis.

This module will:
- parse small VCF files,
- filter variants by allele frequency, consequence, gene list, etc.
"""

from pathlib import Path
from typing import Optional, List

import pandas as pd


def load_vcf_as_df(vcf_path: str | Path) -> pd.DataFrame:
    """
    Load a (reasonably small) VCF file into a pandas DataFrame.

    Assumes a standard, tab-delimited VCF with header lines starting with '##'
    and a single '#CHROM' header line.

    For bigger data this would need to be replaced with cyvcf2 / pysam.
    """
    vcf_path = Path(vcf_path)
    with vcf_path.open() as f:
        header_lines = [line for line in f if line.startswith("#")]
    colnames = header_lines[-1].strip().lstrip("#").split("\t")
    df = pd.read_csv(vcf_path, comment="#", sep="\t", names=colnames)
    return df


def basic_filter(
    df: pd.DataFrame,
    max_af: float = 0.01,
    allowed_consequences: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Apply simple filters:
    - keep variants with allele frequency <= max_af (if AF column exists),
    - keep consequences in allowed_consequences (if CONSEQUENCE column exists).

    This is a simplified placeholder for more realistic filtering logic.
    """
    filtered = df.copy()

    if "AF" in filtered.columns:
        filtered = filtered[filtered["AF"] <= max_af]

    if allowed_consequences is not None and "CONSEQUENCE" in filtered.columns:
        filtered = filtered[filtered["CONSEQUENCE"].isin(allowed_consequences)]

    return filtered

