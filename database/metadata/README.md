# Database metadata

The database is divided into three layers:

- `raw/`: original Stack Exchange Data Explorer (SEDE) CSV exports, kept unchanged.
- `refined/`: datasets prepared for direct analytical use.
- `metadata/queries/`: SQL and query metadata associated with the exports.

Primary source: [Stack Exchange Data Explorer](https://data.stackexchange.com/).

Schema reference: [Database schema documentation for the public data dump and SEDE](https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede).

## cumulative-answers-questions-stackexchange

The legacy workbook `cumulative-answers-questions-stackexchange.xlsx` contains one worksheet, `QueryResults`, with 118 monthly observations from August 2016 through May 2026 and nine fields.

| Column | Meaning |
|---|---|
| `MonthStart` | First calendar day of the reference month. |
| `Month Year` | Reference month used on the x-axis of the original Excel chart. |
| `Cumulative Unanswered Questions` | Running number of questions with neither an accepted answer nor a currently positive-scored answer. |
| `Cumulative No Answers At All` | Running number of questions that have never received an answer. |
| `New Questions` | Questions created in the reference month. |
| `Newly Answered Questions` | Questions leaving the unanswered state in the reference month. |
| `NewlyGotFirstAnswer` | Questions receiving their first answer in the reference month. |
| `NetChangeInUnanswered` | New questions minus questions leaving the unanswered state. |
| `NetChangeInNoAnswersAtAll` | New questions minus questions receiving their first answer. |

The Excel workbook contains one line chart. It uses `Month Year` as the time axis and plots `Cumulative Unanswered Questions` and `Cumulative No Answers At All`. The same chart is reproduced by `StackExchangeDescriptiveAnalysis.plot_cumulative_unanswered()`.

The corresponding reproducible SEDE query is stored at `metadata/queries/cumulative-answers-questions-stackexchange.sql`.
