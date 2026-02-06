#!/usr/bin/env bash
set -eu -o pipefail

deck="spicemodels/option-b-encoder-with-shared-sense.spice"
logdir="logs/shared-sense-phase-skew"
phase_skews=(-0.5n 0 0.5n)
base_start="2n"

mkdir -p "$logdir"

for phase in "${phase_skews[@]}"; do
  phase_label="${phase//./p}"
  phase_label="${phase_label//-/m}"
  tmpfile="$(mktemp)"
  start_value="$(python3 - <<PY
from decimal import Decimal

def parse(value):
    if value.endswith('n'):
        return Decimal(value[:-1]) * Decimal('1e-9')
    return Decimal(value)

base = parse('$base_start')
offset = parse('$phase')
result = (base + offset) * Decimal('1e9')
print(f"{result:.12f}n")
PY
)"
  perl -pe "s/\\.param B1_START=.*/.param B1_START=${start_value}/" "$deck" > "$tmpfile"
  logfile="$logdir/mc_ps${phase_label}.log"
  ngspice -b "$tmpfile" \
    -o "$logfile" \
    >/dev/null
  rm "$tmpfile"
done
