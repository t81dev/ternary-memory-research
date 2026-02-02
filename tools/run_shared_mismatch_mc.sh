#!/usr/bin/env bash
set -euo pipefail

deck="spicemodels/option-b-encoder-with-shared-sense-mismatch.spice"
logdir="logs/mismatch-mc"
samples=50
mkdir -p "$logdir"
datafile="$logdir/mismatch_mc.csv"
printf "# auto-generated mismatch MC data\n" > "$datafile"
printf "vdd,seed,edyn,eword,sense_min,sense_max,sense_thresh_latency\n" >> "$datafile"

vdd_list=${1:-"0.9 1.0 1.1"}

for vdd in $vdd_list; do
  for seed in $(seq 1 "$samples"); do
    logfile="$logdir/mc_$(printf '%.1f' "$vdd")V_${seed}.log"
    printf ".option gseed=%s\n.param run_vdd=%s\n.run\n.quit\n" "$seed" "$vdd" | ngspice -b "$deck" -o "$logfile"

    read edyn eword sense_min sense_max sense_thresh < <(tools/parse_mismatch_log.py "$logfile")

    printf "%s,%s,%s,%s,%s,%s,%s\n" "$vdd" "$seed" "$edyn" "$eword" "$sense_min" "$sense_max" "$sense_thresh" >> "$datafile"
done

tools/headroom_histogram.py "$datafile" "$logdir/headroom_histogram.csv"
done
