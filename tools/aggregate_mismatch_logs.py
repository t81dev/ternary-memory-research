#!/usr/bin/env python3
import csv
import re
import subprocess
import sys
from pathlib import Path

if len(sys.argv) != 3:
    print("Usage: aggregate_mismatch_logs.py <logdir> <outfile>")
    sys.exit(1)

logdir = Path(sys.argv[1])
outfile = Path(sys.argv[2])
pattern = re.compile(r"mc_(?P<vdd>\d+\.\d)V_(?P<seed>\d+)\.log$")

rows = []
for path in sorted(logdir.glob("mc_*V_*.log")):
    m = pattern.search(path.name)
    if not m:
        continue
    vdd = m.group("vdd")
    seed = int(m.group("seed"))
    proc = subprocess.run(["tools/parse_mismatch_log.py", str(path)], text=True, capture_output=True)
    if proc.returncode:
        print(f"Failed to parse {path.name}: {proc.stderr.strip()}", file=sys.stderr)
        sys.exit(proc.returncode)
    tokens = proc.stdout.strip().split()
    if len(tokens) < 5:
        print(f"Unexpected parser output for {path.name}: {proc.stdout.strip()}", file=sys.stderr)
        sys.exit(1)
    edyn, eword, sense_min, sense_max, sense_thresh = tokens[:5]
    rows.append((float(vdd), seed, edyn, eword, sense_min, sense_max, sense_thresh))

rows.sort()
outfile.parent.mkdir(parents=True, exist_ok=True)
with outfile.open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["vdd", "seed", "edyn", "eword", "sense_min", "sense_max", "sense_thresh_latency"])
    for row in rows:
        writer.writerow(row)
