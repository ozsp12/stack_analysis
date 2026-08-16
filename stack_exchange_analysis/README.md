# Stack Exchange Activity Analysis

Investigative data analysis of long-run activity on Stack Overflow and selected Stack Exchange sites. The immediate objective is descriptive and diagnostic: establish what changed, when it changed, and which dimensions of community activity moved together before introducing causal explanations.

## Repository structure

```text
stack_exchange_analysis/
├── database/       # Raw SEDE exports and paired SQL/query text
├── notebooks/      # Reproducible investigative notebooks
├── src/            # Shared analysis utilities
├── analysis/       # Generated figures/tables and legacy analysis artifacts
├── bibliography/   # Research references
└── notes_ideas_stack_exchange_paper.docx
```

Raw exports in `database/` are treated as immutable inputs. Generated tables and figures should be written to `analysis/`.

## Investigative notebooks

| Notebook | Scope |
|---|---|
| `00_data_inventory_and_quality.ipynb` | File inventory, schemas, temporal coverage, missingness, duplicates, provenance flags |
| `01_questions_macro_time_series.ipynb` | Daily/monthly/annual question activity, moving averages, YoY growth, drawdown, seasonality |
| `02_structural_breaks.ipynb` | Rolling slopes and data-driven candidate regime changes |
| `03_cross_site_comparison.ipynb` | Normalized trajectories across Stack Exchange sites, correlations, PCA |
| `04_answers_and_unanswered.ipynb` | Answer volumes, deletion status, answers/questions ratio, unanswered stock |
| `05_user_cohort_dynamics.ipynb` | User registration cohorts and cross-site user metrics |
| `06_tags_and_votes.ipynb` | Tag snapshot, vote trajectories, concentration and entropy |
| `07_legacy_excel_inspection.ipynb` | Inspection of the pre-existing Excel analysis workbook |

## Data caveats

Filename labels are not sufficient provenance. Some exports have temporal labels that do not match their observed coverage, and source endpoints may refer to different Stack Exchange sites. The audit notebook should therefore be run first.

The current user-by-month export is grouped by user account creation month. It measures registration cohorts, not monthly active users. Likewise, the current tag table is a snapshot rather than a historical count of questions by tag.

See [`../docs/data_provenance.md`](../docs/data_provenance.md) and [`../docs/analysis_conventions.md`](../docs/analysis_conventions.md) for the formal project policies.

## Execution

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
jupyter lab
```

Run notebooks in numerical order. They resolve paths from either the repository root or the `notebooks/` directory.

## Automation

The repository has two GitHub Actions workflows:

- `CI` checks Python linting, unit tests, notebook structure, and source-data readability on pull requests and pushes to `main`.
- `Analysis Pipeline` executes all investigative notebooks after relevant changes reach `main`, renders them to HTML, and uploads both executed notebooks and HTML reports as workflow artifacts.

The local equivalent of the CI quality gate is:

```bash
make check
```
