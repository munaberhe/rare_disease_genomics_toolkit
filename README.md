# Rare Disease Genomics Toolkit (RDGT)

## Overview

The Rare Disease Genomics Toolkit (RDGT) is an experimental, end-to-end framework for rare disease case prioritisation. The goal is to tie together three key components:

1. **Variant-level evidence** – filtering and scoring of variants from VCF files.  
2. **Phenotype–disease similarity** – ranking candidate diseases based on patient phenotypes (free text or HPO-style descriptions).  
3. **Case-level prioritisation** – combining variant and phenotype evidence into a ranked set of candidate genes and diseases.

This repository is intended as a larger, more realistic bioinformatics project that builds on smaller modules I have already developed (variant pathogenicity prediction, phenotype–disease matching, scRNA/RNA-seq analysis) and moves towards the kind of tooling used in rare disease diagnostics and pharma/biotech settings.

**Note:** RDGT is currently a work in progress and is not intended for clinical use.

---

## Repository Structure

    rare_disease_genomics_toolkit/
    ├── data/                # example VCFs, phenotype files, disease knowledge base (to be added)
    ├── notebooks/           # exploratory analyses, prototypes, and demos (to be added)
    ├── src/
    │   └── rdgt/
    │       ├── __init__.py
    │       ├── cli.py                # command-line entry point (argument parsing)
    │       ├── vcf_filter.py         # utilities for loading and filtering VCF files
    │       ├── variant_scoring.py    # integration with variant pathogenicity models
    │       ├── phenotype_matching.py # TF-IDF/BM25-style phenotype–disease matching utilities
    │       └── prioritization.py     # logic to combine variant and phenotype evidence
    └── tests/              # unit tests (to be added)

---

## Core Components

### 1. VCF Loading and Filtering (`vcf_filter.py`)

This module is responsible for:

- Loading small VCF files into a pandas DataFrame.  
- Applying simple filters, such as:  
  - maximum allele frequency (`AF`) threshold,  
  - allowed variant consequences (e.g. missense, stop_gained, splice, etc.).

In a production setting this logic would be replaced or extended with robust VCF tools (e.g. cyvcf2/pysam, annotation with VEP/ANNOVAR), but here it acts as a clean, testable abstraction for variant-level data and downstream scoring.

---

### 2. Variant Pathogenicity Scoring (`variant_scoring.py`)

This module is designed to interface with a trained model that predicts variant pathogenicity, such as the RandomForest classifier developed in a separate ClinVar-style project. The idea is to:

- Map variant records to the feature set expected by the model (gene, consequence, impact, PolyPhen-like score, allele frequency, etc.).  
- Apply the model to compute a pathogenicity probability per variant.  
- Add a `pathogenicity_score` column to the variant table.

This creates a standard interface for downstream aggregation at gene or case level and can later be extended to support multiple models or ensemble approaches.

---

### 3. Phenotype–Disease Matching (`phenotype_matching.py`)

This module wraps a simple text-based approach to phenotype–disease matching, building on a previous benchmark project:

- Uses TF-IDF to represent disease descriptions from a small knowledge base.  
- Computes similarity (e.g. cosine similarity) between a patient’s phenotype description and each disease description.  
- Returns a ranked list of candidate diseases with similarity scores.

The design is intentionally flexible so it can later support:

- BM25-based ranking,  
- LLM-style scoring of phenotype–disease matches,  
- Integration with HPO-based ontological methods and structured phenotype data.

---

### 4. Case-Level Prioritisation (`prioritization.py`)

This module combines variant-level and phenotype-level evidence to provide case-level scores:

- Aggregates variant pathogenicity scores at the gene level (e.g. mean or maximum pathogenicity per gene).  
- In future iterations, will map genes to diseases and combine:  
  - gene-level scores,  
  - disease similarity scores,  
  - and optional prior knowledge (inheritance patterns, gene–disease databases).

The long-term goal is to output a ranked report per case with candidate genes and diseases sorted by combined evidence.

---

### 5. Command-Line Interface (`cli.py`)

The CLI is the main entry point for running the toolkit from the command line.

Planned usage (future):

    rdgt run-case \
      --vcf data/example_case.vcf \
      --phenotypes "short stature, developmental delay, seizures" \
      --model models/variant_rf.joblib \
      --diseases data/diseases.csv \
      --out reports/case_001_summary.csv

The CLI will eventually:

- Load and filter the VCF.  
- Apply the variant pathogenicity model.  
- Rank diseases based on phenotype similarity.  
- Aggregate and combine evidence.  
- Write a human-readable summary of candidate genes/diseases.

At present, `cli.py` contains a skeleton for argument parsing and will be wired up as the modules mature.

---

## Installation

This project is in active development and currently intended for local use only.

### 1. Clone the repository

    git clone <this-repo-url>
    cd rare_disease_genomics_toolkit

### 2. Create and activate a virtual environment

    python -m venv .venv
    source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1

### 3. Install Python dependencies

For early development:

    pip install pandas numpy scikit-learn matplotlib

Additional dependencies (e.g. joblib, cyvcf2, rich-click) can be added as the project grows.

---

## Usage (Work in Progress)

Right now, the project is at an early stage with modules being designed and wired together. As a rough starting point:

### 1. Experiment in notebooks

Use the `notebooks/` folder to prototype:

- Loading and filtering VCFs using `vcf_filter.py`.  
- Loading a pre-trained variant classifier and applying it via `variant_scoring.py`.  
- Running simple TF-IDF-based phenotype–disease matching with `phenotype_matching.py`.  
- Combining gene-level scores with disease similarity in `prioritization.py`.

### 2. Run the CLI skeleton

The CLI currently only parses arguments and prints them, but can be invoked as:

    python -m rdgt.cli \
      --vcf data/example_case.vcf \
      --phenotypes "short stature, developmental delay" \
      --model models/variant_rf.joblib \
      --diseases data/diseases.csv \
      --out reports/case_001_summary.csv

As functionality is implemented, this entry point will drive the full case analysis.

### 3. End-to-end demo case pipeline

An end-to-end toy pipeline is provided in `demo_case_pipeline.py`. It shows how the toolkit can already run a simple rare disease case:

```bash
python demo_case_pipeline.py

---

## Roadmap

Planned next steps include:

1. **Variant module integration**  
   - Define a minimal schema to map from VCF columns to model features.  
   - Load and apply the existing RandomForest variant pathogenicity model.  
   - Add example data in `data/` and a small demonstration notebook.

2. **Phenotype–disease integration**  
   - Import and reuse code from the phenotype–disease matching project.  
   - Create a small example diseases table (`data/diseases.csv`).  
   - Add a notebook demonstrating phenotype ranking for a few toy cases.

3. **Case-level report**  
   - Implement gene-level aggregation of variant scores.  
   - Combine gene-level and disease-level scores into a simple ranking scheme.  
   - Output a summary table per case under `reports/`.

4. **Testing and robustness**  
   - Add unit tests in `tests/` for each module (`vcf_filter`, `variant_scoring`, `phenotype_matching`, `prioritization`).  
   - Improve error handling, input validation and logging.

5. **Workflow and scaling**  
   - Optionally wrap key steps into a Nextflow pipeline for larger datasets.  
   - Explore deployment to a cloud environment (e.g. AWS) for scalable execution.

---

## Results & Discussion

At this stage, RDGT is primarily an architectural and software design project: the core package structure (`src/rdgt/`), CLI skeleton and major conceptual modules are in place, but the full end-to-end workflow is still under active development.

### Current “results”

- A modular Python package layout suitable for extension and testing.  
- Clean separation between:  
  - VCF handling and filtering,  
  - variant pathogenicity scoring,  
  - text-based phenotype–disease matching,  
  - case-level aggregation and prioritisation,  
  - and a future command-line interface.  
- A clear roadmap for integrating existing models (variant classifier, phenotype matching) from smaller prior projects into a single toolkit.

Although there are no biological benchmark metrics yet (e.g. top-1 gene recall on a cohort), the current state already demonstrates the ability to move beyond single scripts to a more realistic, multi-module bioinformatics project.

### Discussion and motivation

This project is part of a broader effort to build skills in:

- **Bioinformatics and human genetics** – focusing on rare disease genomics.  
- **Software engineering for biology** – designing modular, testable, reusable code rather than one-off scripts.  
- **Machine learning for genomics** – applying models to variant-level and phenotype-level data.  
- **Translational and pharma-relevant workflows** – moving towards tools that could support target discovery, patient stratification and diagnostic pipelines.

Future work will focus on:

- Wiring up real models and example datasets,  
- Adding tests and continuous integration for reliability,  
- Prototyping a simple Nextflow wrapper and/or cloud deployment,  
- And, eventually, evaluating the toolkit on curated rare disease cases (e.g. simulated or public example datasets).
