#!/usr/bin/env bash
set -euo pipefail

deck="spicemodels/option-b-encoder-with-shared-sense-mismatch-upsized.spice"
logdir="logs/mismatch-mc-upsized"
samples=50
mkdir -p "$logdir"

vdd_list=${1:-"0.9 1.0 1.1"}

for vdd in $vdd_list; do
  for seed in $(seq 1 "$samples"); do
    logfile="$logdir/mc_$(printf '%.1f' "$vdd")V_${seed}.log"
    printf ".option gseed=%s\n.param run_vdd=%s\n.run\n.quit\n" "$seed" "$vdd" | ngspice -b "$deck" -o "$logfile"

    read edyn eword sense_min sense_max < <(tools/parse_mismatch_log.py "$logfile")

  done
done
