#!/usr/bin/env python3
import re
import statistics
from pathlib import Path

logdir = Path("logs/shared-sense-mc")
records = []

for logpath in sorted(logdir.glob("*.log")):
    text = logpath.read_text()
    try:
        headroom_min = float(re.search(r"sense_headroom_min\s*=\s*([0-9Ee.+-]+)", text).group(1))
        headroom_max = float(re.search(r"sense_headroom_max\s*=\s*([0-9Ee.+-]+)", text).group(1))
        edyn = float(re.search(r"Edyn\s*=\s*([0-9Ee.+-]+)", text).group(1))
        eword = float(re.search(r"Eword_est\s*=\s*([0-9Ee.+-]+)", text).group(1))
    except AttributeError:
        continue
    records.append((headroom_min, headroom_max, edyn, eword, logpath.name))

if not records:
    raise SystemExit("No measurement records found.")

mins = [r[0] for r in records]
maxs = [r[1] for r in records]
dyns = [r[2] for r in records]
words = [r[3] for r in records]

print(f"runs: {len(records)}")
print(f"worst-case headroom min: {min(mins)*1000:.1f} mV")
print(f"best-case headroom max: {max(maxs)*1000:.1f} mV")
print(f"avg Edyn: {statistics.mean(dyns):.3f} pJ")
print(f"avg Eword_est: {statistics.mean(words):.3f} pJ")
