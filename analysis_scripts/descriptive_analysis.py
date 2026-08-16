from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


class StackExchangeDescriptiveAnalysis:
    """Basic descriptive inspection of the datasets stored in this repository."""

    REFINED_DATASET = "cumulative-answers-questions-stackexchange.csv"

    EXACT_DESCRIPTIONS = {
        "MonthStart": "First calendar day of the reference month.",
        "Month Year": "Reference month used as the time axis in the original Excel chart.",
        "Cumulative Unanswered Questions": (
            "Running number of questions that have neither an accepted answer nor a "
            "currently positive-scored answer."
        ),
        "Cumulative No Answers At All": "Running number of questions that have never received any answer.",
        "New Questions": "Questions created during the reference month.",
        "Newly Answered Questions": (
            "Questions that leave the unanswered state during the reference month."
        ),
        "NewlyGotFirstAnswer": "Questions receiving their first answer during the reference month.",
        "NetChangeInUnanswered": (
            "Monthly change in the unanswered-question stock: new questions minus newly answered questions."
        ),
        "NetChangeInNoAnswersAtAll": (
            "Monthly change in the no-answer stock: new questions minus questions receiving a first answer."
        ),
    }

    def __init__(self, database_dir: str | Path | None = None) -> None:
        root = Path(__file__).resolve().parents[1]
        self.database_dir = Path(database_dir) if database_dir else root / "database"
        self.raw_dir = self.database_dir / "raw"
        self.refined_dir = self.database_dir / "refined"

    def datasets(self, include_excel: bool = False) -> pd.DataFrame:
        """Return an inventory of analytical datasets."""
        rows: list[dict[str, Any]] = []
        for layer, directory in (("raw", self.raw_dir), ("refined", self.refined_dir)):
            patterns = ("*.csv", "*.xlsx") if include_excel else ("*.csv",)
            for pattern in patterns:
                for path in sorted(directory.glob(pattern)):
                    rows.append(
                        {
                            "dataset": path.name,
                            "layer": layer,
                            "format": path.suffix.lower().lstrip("."),
                            "size_mb": round(path.stat().st_size / 1024**2, 3),
                        }
                    )
        return pd.DataFrame(rows)

    def raw_datasets(self) -> list[str]:
        return [path.name for path in sorted(self.raw_dir.glob("*.csv"))]

    def refined_datasets(self) -> list[str]:
        return [path.name for path in sorted(self.refined_dir.glob("*.csv"))]

    def _resolve(self, dataset: str | Path) -> Path:
        path = Path(dataset)
        if path.exists():
            return path

        for directory in (self.raw_dir, self.refined_dir):
            candidate = directory / path
            if candidate.exists():
                return candidate
        raise FileNotFoundError(f"Dataset not found: {dataset}")

    def load(self, dataset: str | Path) -> pd.DataFrame:
        """Load CSV or Excel data without modifying the source file."""
        path = self._resolve(dataset)
        if path.suffix.lower() == ".xlsx":
            return pd.read_excel(path)

        try:
            return pd.read_csv(path, low_memory=False)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin-1", low_memory=False)

    @staticmethod
    def _date_candidates(df: pd.DataFrame) -> dict[str, pd.Series]:
        result: dict[str, pd.Series] = {}
        date_tokens = ("date", "day", "month", "year", "time")
        for column in df.columns:
            name = str(column)
            if any(token in name.lower() for token in date_tokens):
                parsed = pd.to_datetime(df[column], errors="coerce")
                if len(parsed) and parsed.notna().mean() >= 0.60:
                    result[name] = parsed
        return result

    def explain_column(self, column: str) -> str:
        if column in self.EXACT_DESCRIPTIONS:
            return self.EXACT_DESCRIPTIONS[column]

        name = column.lower()
        rules = (
            ("tag", "Tag or tag-related attribute from Stack Exchange."),
            ("vote", "Vote count or vote-related attribute."),
            ("score", "Stack Exchange score or score-derived metric."),
            ("answer", "Answer count, answer status, or answer-related metric."),
            ("question", "Question count, question status, or question-related metric."),
            ("user", "User identifier, count, cohort, or user-related metric."),
            ("site", "Stack Exchange site or site-level identifier."),
            ("database", "SEDE database or database-level identifier."),
            ("db", "SEDE database or database-level identifier."),
            ("count", "Number of records satisfying the corresponding condition."),
            ("total", "Aggregate total for the corresponding measure."),
            ("cumulative", "Running cumulative value over the ordered time dimension."),
            ("netchange", "Net change over the reference period."),
            ("month", "Monthly time field or month-level aggregation."),
            ("year", "Calendar year or year-level aggregation."),
            ("day", "Daily time field or day-level aggregation."),
            ("date", "Date or datetime field."),
            ("id", "Identifier used by the underlying Stack Exchange data model."),
        )
        for token, description in rules:
            if token in name:
                return description
        return "Dataset-specific field; inspect the paired SQL query in database/metadata/queries."

    def overview(self, dataset: str | Path) -> pd.DataFrame:
        """Return one-row structural and quality metadata for a dataset."""
        path = self._resolve(dataset)
        df = self.load(path)
        dates = self._date_candidates(df)

        date_column = next(iter(dates), None)
        date_min = dates[date_column].min() if date_column else pd.NaT
        date_max = dates[date_column].max() if date_column else pd.NaT

        return pd.DataFrame(
            [
                {
                    "dataset": path.name,
                    "rows": len(df),
                    "columns": df.shape[1],
                    "missing_cells": int(df.isna().sum().sum()),
                    "duplicated_rows": int(df.duplicated().sum()),
                    "memory_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 3),
                    "date_column": date_column,
                    "date_min": date_min,
                    "date_max": date_max,
                }
            ]
        )

    def columns(self, dataset: str | Path) -> pd.DataFrame:
        """Describe every column in a dataframe."""
        df = self.load(dataset)
        rows = []
        for column in df.columns:
            series = df[column]
            rows.append(
                {
                    "column": column,
                    "dtype": str(series.dtype),
                    "non_null": int(series.notna().sum()),
                    "missing": int(series.isna().sum()),
                    "unique": int(series.nunique(dropna=True)),
                    "description": self.explain_column(str(column)),
                }
            )
        return pd.DataFrame(rows)

    def numeric_summary(self, dataset: str | Path) -> pd.DataFrame:
        """Return standard descriptive statistics for numeric columns."""
        df = self.load(dataset)
        numeric = df.select_dtypes(include="number")
        if numeric.empty:
            return pd.DataFrame()
        return numeric.describe().T

    def overview_all(self, layer: str = "raw") -> pd.DataFrame:
        """Inspect all CSV dataframes in one database layer."""
        names = self.raw_datasets() if layer == "raw" else self.refined_datasets()
        if not names:
            return pd.DataFrame()
        return pd.concat([self.overview(name) for name in names], ignore_index=True)

    def plot_cumulative_unanswered(self) -> tuple[Any, Any]:
        """Reproduce the line chart embedded in the legacy Excel workbook."""
        df = self.load(self.REFINED_DATASET).copy()
        df["Month Year"] = pd.to_datetime(df["Month Year"], errors="coerce")

        fig, ax = plt.subplots(figsize=(11, 5))
        ax.plot(
            df["Month Year"],
            df["Cumulative Unanswered Questions"],
            label="Cumulative Unanswered Questions",
        )
        ax.plot(
            df["Month Year"],
            df["Cumulative No Answers At All"],
            label="Cumulative No Answers At All",
        )
        ax.set(
            title="Cumulative unanswered questions",
            xlabel="Month",
            ylabel="Questions",
        )
        ax.legend()
        ax.grid(alpha=0.2)
        fig.tight_layout()
        return fig, ax
