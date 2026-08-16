# Stack Analysis

Exploratory analysis of Stack Overflow and Stack Exchange public data.

## Data source

The datasets in this repository come primarily from the [Stack Exchange Data Explorer (SEDE)](https://data.stackexchange.com/), which provides SQL access to public Stack Exchange data.

Useful references:

- [Stack Exchange Data Explorer](https://data.stackexchange.com/)
- [SEDE and public data dump schema](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede)
- [Stack Overflow content licensing](https://stackoverflow.com/help/licensing)

## Repository structure

```text
database/
├── raw/          # Original SEDE exports
├── refined/      # Prepared datasets used directly in analyses
└── metadata/
    └── queries/  # SQL used to generate the datasets

analysis_scripts/          # Reusable Python analysis classes
bibliography/              # References
descriptive_analysis.ipynb # Descriptive analysis notebook
```

The raw data are kept unchanged. Transformations and reusable analytical logic belong in `analysis_scripts/`.

## Current analysis

The first analysis is a basic descriptive inspection of every dataframe: dimensions, columns, data types, missing values, duplicated rows, date coverage, cardinality, and simple numerical summaries.

The notebook `descriptive_analysis.ipynb` calls the class defined in `analysis_scripts/descriptive_analysis.py`. Each analytical code cell contains one function call and produces one output, with a Markdown cell immediately before it explaining the function and its result.

The refined dataset `cumulative-answers-questions-stackexchange` is available both as Excel and CSV. Its original Excel chart is reproduced in Python as two cumulative time series:

- cumulative unanswered questions;
- cumulative questions with no answers at all.

## Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```
