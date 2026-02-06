#!/usr/bin/env python3
"""Manage guard-leger data exports (catalog, status, failures)."""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Iterable, Sequence

DEFAULT_LEDGER = Path("data/canonical_guard_ledger.csv")


def load_ledger(path: Path) -> list[dict]:
    with path.open() as f:
        reader = csv.DictReader((line for line in f if line.strip()))
        return [row for row in reader]


def catalog(ledger: Sequence[dict], outfile: Path) -> None:
    groups: dict[str, dict] = {}
    for row in ledger:
        log_path = Path(row["log_path"])
        key = log_path.parent.as_posix()
        entry = groups.setdefault(key, {
            "experiment": row.get("experiment"),
            "subset": row.get("subset"),
            "log_dir": key,
            "headroom_histogram": row.get("headroom_histogram"),
            "noise_amp": row.get("noise_amp"),
            "driver_scale": row.get("driver_scale"),
            "phase_ns": row.get("phase_ns"),
            "rows": 0,
            "vdd_counts": Counter(),
            "seed_range": [None, None],
            "sense_min_mV": [],
        })
        entry["rows"] += 1
        entry["vdd_counts"][row.get("vdd")] += 1
        try:
            seed = float(row["seed"]) if row.get("seed") else None
        except ValueError:
            seed = None
        if seed is not None:
            low, high = entry["seed_range"]
            if low is None or seed < low:
                entry["seed_range"][0] = seed
            if high is None or seed > high:
                entry["seed_range"][1] = seed
        entry["sense_min_mV"].append(_to_float(row.get("sense_min_mV")))
    catalog_data = []
    for entry in groups.values():
        mins = [v for v in entry["sense_min_mV"] if v is not None]
        entry["sense_min_mV"] = min(mins) if mins else None
        entry["histogram_exists"] = bool(entry["headroom_histogram"] and Path(entry["headroom_histogram"]).exists())
        entry["vdd_counts"] = dict(entry["vdd_counts"])
        catalog_data.append(entry)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with outfile.open("w") as f:
        json.dump(sorted(catalog_data, key=lambda item: item["log_dir"]), f, indent=2)
    print(f"Catalog written to {outfile} ({len(catalog_data)} directories)")


def status(ledger: Sequence[dict], outfile: Path) -> None:
    headroom_min = min_float([row.get("sense_min_mV") for row in ledger])
    headroom_max = max_float([row.get("sense_max_mV") for row in ledger])
    latency_values = [to_float(row.get("sense_thresh_latency_ps")) for row in ledger if row.get("sense_thresh_latency_ps")]
    experiments = Counter(row.get("experiment") for row in ledger)
    rows = len(ledger)
    top_exps = experiments.most_common(5)
    failures = sum(1 for row in ledger if row.get("comp_pass") and row.get("comp_pass").lower() != "pass")
    lines = [
        "# Guard status",
        "",
        f"- Ledger: `{DEFAULT_LEDGER}` ({rows} rows covering {len(experiments)} experiments, {failures} failures).",
        f"- Headroom range: {format_mv(headroom_min)} to {format_mv(headroom_max)}." if headroom_min is not None and headroom_max is not None else "- Headroom range: n/a.",
        f"- Sense threshold latency median: {format_ps(median(latency_values))}." if latency_values else "- Sense threshold latency median: n/a.",
        "",
        "## Top experiments by sample count",
        "",
        "| Experiment | Samples |",
        "| --- | --- |",
    ]
    for name, count in top_exps:
        lines.append(f"| {name} | {count} |")
    lines.extend([
        "",
        "## Notes",
        "",
        "- Run `python3 tools/guard_data.py status` to refresh this summary whenever the ledger changes.",
        "- See `data/comparator_failures.csv` for every `comp_pass=failed` sample that the ledger records.",
    ])
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text("\n".join(lines))
    print(f"Status written to {outfile}")


def failures(ledger: Sequence[dict], outfile: Path) -> None:
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with outfile.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["log_path", "experiment", "vdd", "seed", "sense_min_mV", "sense_max_mV", "sense_thresh_latency_ps", "noise_amp", "driver_scale", "phase_ns"])
        for row in ledger:
            comp = row.get("comp_pass")
            if comp and comp.lower() == "pass":
                continue
            writer.writerow([
                row.get("log_path"),
                row.get("experiment"),
                row.get("vdd"),
                row.get("seed"),
                row.get("sense_min_mV"),
                row.get("sense_max_mV"),
                row.get("sense_thresh_latency_ps"),
                row.get("noise_amp"),
                row.get("driver_scale"),
                row.get("phase_ns"),
            ])
    print(f"Failure summary written to {outfile}")


def to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _to_float(value: str | None) -> float | None:
    return to_float(value)


def min_float(values: Iterable[str | None]) -> float | None:
    cleaned = [to_float(v) for v in values if v is not None]
    return min(cleaned) if cleaned else None


def max_float(values: Iterable[str | None]) -> float | None:
    cleaned = [to_float(v) for v in values if v is not None]
    return max(cleaned) if cleaned else None


def format_mv(value: float | None) -> str:
    return f"{value:.3f} mV" if value is not None else "n/a"


def format_ps(value: float | None) -> str:
    return f"{value:.3f} ps" if value is not None else "n/a"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["catalog", "status", "failures"], help="action to perform")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER, help="ledger CSV path")
    parser.add_argument("--output", type=Path, help="output path (default derived) ")
    args = parser.parse_args()
    ledger = load_ledger(args.ledger)
    if args.command == "catalog":
        out = args.output or Path("data/guard_experiment_catalog.json")
        catalog(ledger, out)
    elif args.command == "status":
        out = args.output or Path("data/guard_status.md")
        status(ledger, out)
    elif args.command == "failures":
        out = args.output or Path("data/comparator_failures.csv")
        failures(ledger, out)


if __name__ == "__main__":
    main()
