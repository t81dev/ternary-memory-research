#!/usr/bin/env python3
"""Verify the canonical guard ledger matches the on-disk logs."""
import csv
from collections import Counter
from pathlib import Path
import sys

LEDGER = Path("data/canonical_guard_ledger.csv")


def load_ledger(path: Path):
    if not path.exists():
        raise SystemExit(f"Ledger missing: {path}")
    with path.open() as f:
        return [row for row in csv.DictReader((line for line in f if line.strip()))]


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open() as f:
        reader = csv.reader((line for line in f if line.strip() and not line.lstrip().startswith("#")))
        try:
            next(reader)
        except StopIteration:
            return 0
        return sum(1 for _ in reader)


def main():
    ledger = load_ledger(LEDGER)
    counts = Counter(row["log_path"] for row in ledger)
    errors = []
    for log_path, expected in counts.items():
        csv_path = Path(log_path)
        actual = count_csv_rows(csv_path)
        if actual != expected:
            errors.append(f"{csv_path}: ledger {expected} rows vs {actual} actual rows")
        hist = csv_path.parent / "headroom_histogram.csv"
        if not hist.exists():
            errors.append(f"Missing histogram: {hist}")
    if errors:
        print("Ledger consistency check failed:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    print("Ledger consistency verified.")


if __name__ == "__main__":
    main()
