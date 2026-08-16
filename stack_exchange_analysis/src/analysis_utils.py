from pathlib import Path

import numpy as np
import pandas as pd


def read_csv_flexible(path, **kwargs):
    """Read common SEDE CSV exports robustly without mutating source data."""
    path = Path(path)
    defaults = dict(low_memory=False)
    defaults.update(kwargs)
    try:
        return pd.read_csv(path, **defaults)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1", **defaults)


def parse_best_date_column(df):
    """Return the most plausible date column and parsed values, or (None, None)."""
    priority = []
    for column in df.columns:
        name = str(column).lower()
        score = 0
        if name in {"date", "day", "month", "monthstart", "creationmonth", "votemonth"}:
            score += 10
        if "date" in name or "month" in name or "day" in name:
            score += 5
        if score:
            priority.append((score, column))
    for _, column in sorted(priority, reverse=True):
        parsed = pd.to_datetime(df[column], errors="coerce")
        if parsed.notna().mean() >= 0.5:
            return column, parsed
    return None, None


def drop_incomplete_last_period(obj, freq="M"):
    """Drop the current calendar month from an aggregated object when present."""
    if obj is None or len(obj) == 0:
        return obj
    index = pd.DatetimeIndex(obj.index)
    now = pd.Timestamp.now()
    if freq.upper().startswith("M") and index[-1].year == now.year and index[-1].month == now.month:
        return obj.iloc[:-1]
    return obj


def save_figure(fig, path, dpi=160):
    """Save a matplotlib figure to the analysis directory."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
