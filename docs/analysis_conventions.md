# Analysis Conventions

## Notebook order

Investigative notebooks use two-digit numeric prefixes. Earlier notebooks establish data validity and broad descriptive structure; later notebooks add more specialized diagnostics. A notebook should not silently depend on out-of-order execution of another notebook.

## Time-series conventions

- Daily data are the least aggregated representation when available.
- Weekly and monthly series should be derived reproducibly from daily observations.
- Incomplete terminal periods must be identified and excluded from comparisons that assume complete periods.
- Calendar effects and seasonality should be inspected before interpreting short-run changes as structural changes.
- Structural-break analyses are exploratory unless a formal identification strategy is explicitly introduced.

## Cross-site comparisons

Raw question counts from different Stack Exchange sites are not directly comparable because site scale differs by orders of magnitude. Comparative plots should therefore include normalized indices, rates, shares, or standardized trajectories when scale is not the object of interest.

## Missing observations

A missing row is not automatically equivalent to zero activity. Zero-filling is allowed only when the data-generating query guarantees that absence of a row means a zero count for that period.

## Deleted content

Analyses must state whether they use `Posts`, `PostsWithDeleted`, or another table. Counts of currently visible posts and counts of posts originally created are different estimands.

## User metrics

Account-creation cohorts must not be described as monthly active users. Active-user analyses require activity-based definitions derived from questions, answers, votes, or other events during the period of interest.

## Generated outputs

Generated figures and tables belong under `stack_exchange_analysis/analysis/`. Executed notebooks and rendered HTML produced by CI/CD are GitHub Actions artifacts and should not normally be committed.

## Interpretation

Exploratory correlation, temporal coincidence, and change-point detection do not establish causality. Notebooks should distinguish observations, statistical associations, and causal claims explicitly.
