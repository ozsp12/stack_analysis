from __future__ import annotations

from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "stack_exchange_analysis" / "notebooks"


def main() -> int:
    notebooks = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    if not notebooks:
        raise SystemExit(f"No notebooks found in {NOTEBOOK_DIR}")

    failures: list[str] = []
    for path in notebooks:
        try:
            with path.open("r", encoding="utf-8") as handle:
                notebook = nbformat.read(handle, as_version=4)
            nbformat.validate(notebook)
        except Exception as exc:  # noqa: BLE001 - aggregate validation failures
            failures.append(f"{path.relative_to(ROOT)}: {exc}")

    if failures:
        print("Notebook validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Validated {len(notebooks)} notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
