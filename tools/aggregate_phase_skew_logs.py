#!/usr/bin/env python3
import csv
import re
import subprocess
import sys
from pathlib import Path


def decode_phase_label(label: str) -> float:
    # convert label like "m0p5n" to numeric nanoseconds (-0.5)
    text = label.replace("m", "-").replace("p", ".")
    if text.endswith("n"):
        return float(text[:-1])
    return float(text)


def main():
    if len(sys.argv) != 3:
        print("Usage: aggregate_phase_skew_logs.py <logdir> <outfile>")
        sys.exit(1)

    logdir = Path(sys.argv[1])
    outfile = Path(sys.argv[2])
    pattern = re.compile(r"mc_ps(?P<phase>[a-z0-9]+)(?:_seed(?P<seed>\d+))?\.log$")

    rows = []
    for path in sorted(logdir.glob("mc_ps*.log")):
        m = pattern.search(path.name)
        if not m:
            continue
        phase_label = m.group("phase")
        seed = int(m.group("seed") or 1)
        proc = subprocess.run(
            ["tools/parse_mismatch_log.py", str(path)],
            text=True,
            capture_output=True,
        )
        if proc.returncode:
            print(f"Failed to parse {path.name}: {proc.stderr.strip()}", file=sys.stderr)
            sys.exit(proc.returncode)
        tokens = proc.stdout.strip().split()
        if len(tokens) < 5:
            print(f"Unexpected parser output for {path.name}: {proc.stdout.strip()}", file=sys.stderr)
            sys.exit(1)
        edyn, eword, sense_min, sense_max, sense_thresh = tokens[:5]
        phase_ns = decode_phase_label(phase_label)
        rows.append((phase_ns, seed, edyn, eword, sense_min, sense_max, sense_thresh))

    rows.sort()
    outfile.parent.mkdir(parents=True, exist_ok=True)
    with outfile.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "phase_ns",
                "seed",
                "edyn",
                "eword",
                "sense_min",
                "sense_max",
                "sense_thresh_latency",
            ]
        )
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    main()
