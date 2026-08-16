from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "stack_exchange_analysis" / "database"


def main() -> int:
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    if not csv_files:
        raise SystemExit(f"No CSV source files found in {DATA_DIR}")

    failures: list[str] = []
    checked = 0

    for path in csv_files:
        if path.stat().st_size == 0:
            failures.append(f"{path.name}: empty file")
            continue

        try:
            frame = pd.read_csv(path, nrows=25, low_memory=False)
        except UnicodeDecodeError:
            try:
                frame = pd.read_csv(path, nrows=25, encoding="latin-1", low_memory=False)
            except Exception as exc:  # noqa: BLE001 - aggregate validation failures
                failures.append(f"{path.name}: {exc}")
                continue
        except Exception as exc:  # noqa: BLE001 - aggregate validation failures
            failures.append(f"{path.name}: {exc}")
            continue

        if len(frame.columns) == 0:
            failures.append(f"{path.name}: no columns detected")
            continue

        checked += 1

    if failures:
        print("Source data checks failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Read headers/sample rows from {checked} CSV source files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
