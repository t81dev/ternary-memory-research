#!/usr/bin/env python3
"""Export a canonical guard ledger from each mismatch/phase log directory."""
import argparse
import csv
from pathlib import Path
from typing import Iterable

OUTPUT_COLUMNS = [
    "experiment",
    "subset",
    "log_path",
    "noise_amp",
    "driver_scale",
    "phase_ns",
    "vdd",
    "seed",
    "edyn_pJ",
    "eword_pJ",
    "sense_min_mV",
    "sense_max_mV",
    "sense_thresh_latency_ps",
    "comp_toggle_latency_ps",
    "comp_pass",
    "headroom_histogram",
]

EXPERIMENT_ALIASES = {
    "mismatch-mc": "±10% mismatch MC",
    "mismatch-mc-tt": "TT mismatch MC",
    "shared-sense-phase-skew": "Shared-sense phase-skew sweep",
    "shared-sense-glimpse-8slice": "Shared-sense glimpse (8 slices)",
    "shared-sense-glimpse-16slice": "Shared-sense glimpse (16 slices)",
    "mismatch-mc-upsized": "Shared-sense mismatch (upsized driver)",
}

EXTRA_SUBSETS = {
    "noise-mismatch-10m-driver-2p5": "boosted strong-arm",
    "noise-mismatch-10m-driver-2p5-tuned": "tuned eval window",
    "noise-mismatch-10m-driver-2p5-tuned-early": "tuned eval (early)",
    "shared-sense-glimpse-8slice": "8-slice capture",
    "shared-sense-glimpse-16slice": "16-slice capture",
    "shared-sense-phase-skew": "±0.5 ns skew",
    "mismatch-mc-upsized": "upsized sense/driver",
}

LOG_PATTERN = "*/mismatch_mc*.csv"
NOISE_DIR_PREFIX = "noise-mismatch-"
DRIVER_PART = "-driver-"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outfile", nargs="?", default="data/canonical_guard_ledger.csv", help="path to write the ledger CSV")
    return parser.parse_args()


def clean_lines(file: Iterable[str]) -> Iterable[str]:
    return (line for line in file if line.strip() and not line.lstrip().startswith("#"))


def to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def scaled(value: str | None, scale: float) -> float | None:
    result = to_float(value)
    if result is None:
        return None
    return result * scale


def parse_noise_driver(dir_name: str) -> tuple[str | None, float | None, str | None]:
    noise_amp = None
    driver_scale = None
    tag = None
    if dir_name.startswith(NOISE_DIR_PREFIX):
        remainder = dir_name[len(NOISE_DIR_PREFIX):]
        if DRIVER_PART in remainder:
            noise_part, driver_part = remainder.split(DRIVER_PART, 1)
            noise_amp = noise_part or None
            driver_value = driver_part
            if "-" in driver_value:
                driver_scale_str, tag = driver_value.split("-", 1)
            else:
                driver_scale_str, tag = driver_value, None
            driver_scale = parse_scale(driver_scale_str)
        else:
            noise_amp = remainder or None
    return noise_amp, driver_scale, tag.replace("-", " ") if tag else None


def parse_scale(text: str | None) -> float | None:
    if not text:
        return None
    normalized = text.replace("p", ".")
    try:
        return float(normalized)
    except ValueError:
        return None


def describe_experiment(dir_name: str, noise_amp: str | None, driver_scale: float | None) -> str:
    if dir_name in EXPERIMENT_ALIASES:
        return EXPERIMENT_ALIASES[dir_name]
    if dir_name.startswith(NOISE_DIR_PREFIX):
        if driver_scale:
            return f"Noise sweep {noise_amp} / driver {driver_scale:.2f}×"
        if noise_amp:
            return f"Noise sweep {noise_amp}"
    if dir_name.startswith("shared-sense-glimpse"):
        return EXPERIMENT_ALIASES.get(dir_name, dir_name.replace("-", " "))
    return dir_name.replace("-", " ")


def _parse_seed(value: str | None) -> float | None:
    parsed = to_float(value)
    if parsed is None:
        return None
    if parsed.is_integer():
        return int(parsed)
    return parsed


def build_record(csv_path: Path, row: dict, metadata: dict) -> dict:
    hist_path = csv_path.parent / "headroom_histogram.csv"
    return {
        "experiment": metadata["experiment"],
        "subset": metadata.get("subset"),
        "log_path": csv_path.as_posix(),
        "noise_amp": metadata.get("noise_amp"),
        "driver_scale": metadata.get("driver_scale"),
        "phase_ns": to_float(row.get("phase_ns")),
        "vdd": to_float(row.get("vdd")),
        "seed": _parse_seed(row.get("seed")),
        "edyn_pJ": scaled(row.get("edyn"), 1e12),
        "eword_pJ": scaled(row.get("eword"), 1e12),
        "sense_min_mV": scaled(row.get("sense_min"), 1e3),
        "sense_max_mV": scaled(row.get("sense_max"), 1e3),
        "sense_thresh_latency_ps": scaled(row.get("sense_thresh_latency"), 1e12),
        "comp_toggle_latency_ps": scaled(row.get("comp_toggle_latency"), 1e12),
        "comp_pass": row.get("comp_pass"),
        "headroom_histogram": hist_path.as_posix() if hist_path.exists() else None,
    }


def gather_rows(root: Path) -> Iterable[tuple[Path, dict, dict]]:
    for csv_path in sorted(root.glob(LOG_PATTERN)):
        dir_name = csv_path.parent.name
        noise_amp, driver_scale, tag = parse_noise_driver(dir_name)
        metadata = {
            "noise_amp": noise_amp,
            "driver_scale": driver_scale,
            "subset": tag or EXTRA_SUBSETS.get(dir_name),
        }
        metadata["experiment"] = describe_experiment(dir_name, noise_amp, driver_scale)
        if metadata["subset"] is None and dir_name in EXTRA_SUBSETS:
            metadata["subset"] = EXTRA_SUBSETS[dir_name]
        with csv_path.open() as f:
            reader = csv.DictReader(clean_lines(f))
            for row in reader:
                yield csv_path, metadata.copy(), row


def write_ledger(outfile: Path, records: list[dict]) -> None:
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with outfile.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for record in sorted(records, key=lambda r: (r["experiment"], r["log_path"], r.get("seed", 0) or 0)):
            writer.writerow(record)


def main() -> None:
    args = parse_args()
    root = Path("logs")
    ledger = []
    for csv_path, metadata, row in gather_rows(root):
        ledger.append(build_record(csv_path, row, metadata))
    if not ledger:
        raise SystemExit("No ledger rows were created.")
    write_ledger(Path(args.outfile), ledger)
    print(f"Ledger exported to {args.outfile} ({len(ledger)} rows)")


if __name__ == "__main__":
    main()
