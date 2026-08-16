# Stack Analysis

[![CI](https://github.com/ozsp12/stack_analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/ozsp12/stack_analysis/actions/workflows/ci.yml)
[![Analysis Pipeline](https://github.com/ozsp12/stack_analysis/actions/workflows/analysis.yml/badge.svg)](https://github.com/ozsp12/stack_analysis/actions/workflows/analysis.yml)

A reproducible data-analysis project for investigating long-run activity on Stack Overflow and selected Stack Exchange communities.

The project currently focuses on descriptive and diagnostic analysis: establishing what changed, when it changed, where the decline is concentrated, and which dimensions of community activity moved together. Causal interpretation is intentionally deferred until the data provenance and descriptive evidence are sufficiently robust.

## Research questions

The current investigative program is organized around five questions:

1. How has Stack Overflow question activity evolved since 2008?
2. Which structural breaks and persistent regime changes are visible in the time series?
3. Is the decline specific to Stack Overflow, common to technical communities, or visible across the broader Stack Exchange network?
4. How did answers, unanswered questions, users, tags, and voting activity evolve alongside question volume?
5. Which apparent changes are genuine behavioral changes, and which may reflect moderation, deletion, source coverage, or data-extraction effects?

## Repository structure

```text
.
├── .github/workflows/                  # Continuous integration and analysis delivery
├── docs/                               # Methodological and provenance documentation
├── scripts/                            # Repository and notebook validation utilities
├── tests/                              # Unit tests for reusable Python code
├── stack_exchange_analysis/
│   ├── database/                       # Raw SEDE exports and paired SQL/query files
│   ├── notebooks/                      # Numbered investigative Jupyter notebooks
│   ├── src/                            # Shared analysis utilities
│   ├── analysis/                       # Generated figures/tables and legacy artifacts
│   ├── bibliography/                   # Research references
│   └── README.md                       # Analysis-workspace documentation
├── pyproject.toml                      # Tooling configuration
├── requirements.txt                    # Runtime dependencies
├── requirements-dev.txt                # Development and CI dependencies
└── Makefile                            # Common development commands
```

Raw exports under `stack_exchange_analysis/database/` are treated as immutable source material. Analytical transformations belong in notebooks or reusable source modules; generated outputs belong in `stack_exchange_analysis/analysis/`.

## Notebooks

The notebooks are designed to be run in numerical order:

| Notebook | Purpose |
|---|---|
| `00_data_inventory_and_quality.ipynb` | Inventory, schemas, temporal coverage, missingness, duplicates, and provenance checks |
| `01_questions_macro_time_series.ipynb` | Long-run question activity, aggregation, trends, seasonality, YoY growth, and drawdown |
| `02_structural_breaks.ipynb` | Rolling trends and exploratory structural-break detection |
| `03_cross_site_comparison.ipynb` | Normalized trajectories, correlations, and PCA across Stack Exchange sites |
| `04_answers_and_unanswered.ipynb` | Answer volume, deletion status, answer/question ratios, and unanswered-question dynamics |
| `05_user_cohort_dynamics.ipynb` | User-registration cohorts and cross-site user metrics |
| `06_tags_and_votes.ipynb` | Tag composition, voting trajectories, concentration, and entropy |
| `07_legacy_excel_inspection.ipynb` | Audit of the pre-existing Excel analysis workbook |

## Environment

Python 3.11 is the reference runtime.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
```

Then start Jupyter:

```bash
jupyter lab
```

## Quality checks

The same checks used by CI can be run locally:

```bash
make check
```

Individual commands are also available:

```bash
make lint
make test
make notebooks-check
make data-check
```

## Continuous integration and delivery

`CI` runs on pushes and pull requests. It validates Python code, unit tests, notebook structure, and the readability of source data files without modifying them.

`Analysis Pipeline` runs on `main` and can also be triggered manually. It executes the investigative notebooks, renders them as HTML, and uploads the rendered analysis as a GitHub Actions artifact. This provides a reproducible delivery path for analytical outputs without committing generated notebook state to the repository.

## Data provenance

Stack Exchange Data Explorer exports require explicit provenance. File names alone must not be treated as authoritative metadata. Some legacy exports have labels that do not match their actual date coverage or source site. See [`docs/data_provenance.md`](docs/data_provenance.md) and always run notebook `00_data_inventory_and_quality.ipynb` before combining datasets.

## Reproducibility policy

- Raw exports are immutable inputs.
- SQL/query files are retained beside their corresponding exports whenever available.
- Generated figures, tables, and rendered notebooks are build artifacts.
- Analysis code should be deterministic unless randomness is explicitly required and seeded.
- Claims should be traceable to a source file, transformation, and notebook cell.
- Data-quality limitations should be reported, not silently repaired.

## Status

This repository is under active development. The current milestone is a robust investigative analysis layer; causal modeling and manuscript preparation are deliberately out of scope until the descriptive evidence and provenance audit are stable.
