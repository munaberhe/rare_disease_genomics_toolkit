"""
Command-line entry point for the rare disease genomics toolkit.

Example (future):

    rdgt run-case \
        --vcf data/example.vcf \
        --phenotypes "short stature, developmental delay" \
        --model models/variant_rf.joblib \
        --diseases data/diseases.csv \
        --out reports/case_001_summary.csv
"""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Rare disease genomics toolkit - case prioritisation"
    )
    parser.add_argument("--vcf", type=Path, required=True, help="Path to VCF file.")
    parser.add_argument(
        "--phenotypes",
        type=str,
        required=True,
        help="Free-text phenotypes or HPO-style description.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        required=True,
        help="Path to trained variant pathogenicity model (joblib).",
    )
    parser.add_argument(
        "--diseases",
        type=Path,
        required=True,
        help="Path to diseases CSV (id, name, description, etc.).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Path to save the summary/report CSV.",
    )

    args = parser.parse_args()

    # TODO: wire together:
    # - load VCF, filter variants
    # - load model, score variants
    # - phenotype–disease ranking
    # - combine into a final report

    print("CLI skeleton parsed arguments:")
    print(args)


if __name__ == "__main__":
    main()

