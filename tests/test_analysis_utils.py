from __future__ import annotations

from pathlib import Path

import pandas as pd

from stack_exchange_analysis.src.analysis_utils import (
    drop_incomplete_last_period,
    parse_best_date_column,
    read_csv_flexible,
)


def test_read_csv_flexible_reads_utf8(tmp_path: Path) -> None:
    path = tmp_path / "sample.csv"
    path.write_text("Date,Value\n2024-01-01,1\n", encoding="utf-8")

    frame = read_csv_flexible(path)

    assert list(frame.columns) == ["Date", "Value"]
    assert frame.loc[0, "Value"] == 1


def test_parse_best_date_column_prefers_semantic_date_name() -> None:
    frame = pd.DataFrame(
        {
            "Value": [1, 2],
            "CreationMonth": ["2024-01-01", "2024-02-01"],
        }
    )

    column, parsed = parse_best_date_column(frame)

    assert column == "CreationMonth"
    assert parsed is not None
    assert parsed.notna().all()


def test_parse_best_date_column_returns_none_when_no_candidate_exists() -> None:
    frame = pd.DataFrame({"Value": [1, 2]})

    column, parsed = parse_best_date_column(frame)

    assert column is None
    assert parsed is None


def test_drop_incomplete_last_period_removes_current_month() -> None:
    now = pd.Timestamp.now().normalize().replace(day=1)
    previous = now - pd.offsets.MonthBegin(1)
    series = pd.Series([10, 20], index=pd.DatetimeIndex([previous, now]))

    result = drop_incomplete_last_period(series)

    assert result is not None
    assert len(result) == 1
    assert result.index[-1] == previous
