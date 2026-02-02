#!/usr/bin/env bash
set -euo pipefail

deck="spicemodels/option-b-encoder-with-shared-sense-tt.spice"
logdir="logs/mismatch-mc-tt"
samples=50
mkdir -p "$logdir"
datafile="$logdir/mismatch_mc_tt.csv"
printf "# auto-generated TT mismatch MC data\n" > "$datafile"
printf "vdd,seed,edyn,eword,sense_min,sense_max\n" >> "$datafile"

for seed in $(seq 1 "$samples"); do
  logfile="$logdir/tt_mc_${seed}.log"
  printf ".option gseed=%s\n.param run_vdd=1.0\n.param mc_mm_switch=1\n.param mc_pr_switch=1\n.param mc_switch=1\n.param mismatch_switch=1\n.param process_switch=1\n.run\n.quit\n" "$seed" | ngspice -b "$deck" -o "$logfile"

  read edyn eword sense_min sense_max < <(tools/parse_mismatch_log.py "$logfile")

  printf "1.0,%s,%s,%s,%s,%s\n" "$seed" "$edyn" "$eword" "$sense_min" "$sense_max" >> "$datafile"
done
