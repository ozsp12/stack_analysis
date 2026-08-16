# Data Provenance

This document defines the minimum provenance standard for datasets used in this repository.

## Source hierarchy

The primary source is the Stack Exchange Data Explorer (SEDE) or another explicitly documented Stack Exchange export. Every analytical dataset should be traceable to:

1. the Stack Exchange site or database queried;
2. the SQL/query used to create the export;
3. the date on which the export was obtained;
4. the temporal coverage observed in the exported data;
5. the unit of observation and aggregation frequency;
6. relevant limitations such as deletion visibility, current-state scores, or incomplete periods.

## Legacy data

Files already present in `stack_exchange_analysis/database/` predate the formal provenance policy. Their file names are descriptive labels, not authoritative metadata. Several files require explicit verification before they are combined in an analysis.

Known classes of risk include:

- a file name claiming a longer time interval than the SQL query actually requests;
- exports originating from a localized Stack Overflow site rather than the English Stack Overflow database;
- use of `Posts` when deleted posts would be relevant to the research question;
- use of current answer scores to reconstruct historical answer status;
- a final daily or monthly period that is incomplete at extraction time;
- user metrics grouped by account creation date being mistaken for monthly active-user metrics;
- tag snapshots being mistaken for historical tag activity.

## Required metadata for new exports

New data additions should be accompanied by a query file or metadata record containing at least:

```text
dataset_name:
source_platform: Stack Exchange Data Explorer
source_site:
query_url:
query_file:
extracted_at_utc:
unit_of_observation:
frequency:
minimum_date:
maximum_date:
uses_deleted_posts:
known_limitations:
```

## Raw-data policy

Files in `stack_exchange_analysis/database/` are immutable inputs. Do not silently edit source exports to repair missing values, dates, headers, encodings, or classifications. Corrections and transformations belong in analysis code and must remain reproducible.

## Validation workflow

Notebook `00_data_inventory_and_quality.ipynb` is the entry point for analytical work. It should be run before combining datasets. CI also performs a lightweight smoke check to confirm that committed CSV files are non-empty and readable.

A successful smoke check does not establish substantive validity. It establishes only that the repository can parse the file. Provenance and semantic validity remain analytical responsibilities.
