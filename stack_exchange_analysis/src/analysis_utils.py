from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def read_csv_flexible(path: str | Path, **kwargs: Any) -> pd.DataFrame:
    """Read a SEDE CSV export without mutating the source file.

    UTF-8 is attempted first. Latin-1 is used only as a compatibility fallback
    for legacy exports.
    """
    source = Path(path)
    defaults: dict[str, Any] = {"low_memory": False}
    defaults.update(kwargs)
    try:
        return pd.read_csv(source, **defaults)
    except UnicodeDecodeError:
        return pd.read_csv(source, encoding="latin-1", **defaults)


def parse_best_date_column(df: pd.DataFrame) -> tuple[str | None, pd.Series | None]:
    """Return the most plausible date column and its parsed values.

    Candidate columns are ranked by semantic name. A candidate is accepted only
    when at least half of its values can be parsed as datetimes.
    """
    candidates: list[tuple[int, str]] = []
    exact_names = {
        "date",
        "day",
        "month",
        "monthstart",
        "creationmonth",
        "votemonth",
    }

    for column in df.columns:
        column_name = str(column)
        normalized = column_name.lower()
        score = 0
        if normalized in exact_names:
            score += 10
        if any(token in normalized for token in ("date", "month", "day")):
            score += 5
        if score:
            candidates.append((score, column_name))

    for _, column in sorted(candidates, key=lambda item: (-item[0], item[1])):
        parsed = pd.to_datetime(df[column], errors="coerce")
        if parsed.notna().mean() >= 0.5:
            return column, parsed

    return None, None


def drop_incomplete_last_period(
    obj: pd.Series | pd.DataFrame | None,
    freq: str = "M",
) -> pd.Series | pd.DataFrame | None:
    """Drop the current calendar month from a time-indexed object when present."""
    if obj is None or len(obj) == 0:
        return obj

    index = pd.DatetimeIndex(obj.index)
    now = pd.Timestamp.now()
    is_monthly = freq.upper().startswith("M")
    is_current_month = index[-1].year == now.year and index[-1].month == now.month

    if is_monthly and is_current_month:
        return obj.iloc[:-1]
    return obj


def save_figure(fig: Any, path: str | Path, dpi: int = 160) -> None:
    """Save a matplotlib figure to a deterministic output path."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(destination, dpi=dpi, bbox_inches="tight")
