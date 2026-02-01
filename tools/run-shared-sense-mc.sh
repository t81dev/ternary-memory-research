#!/usr/bin/env bash
set -eu -o pipefail

deck="spicemodels/option-b-encoder-with-shared-sense.spice"
logdir="logs/shared-sense-mc"
seeds=100
corners=(1.0 0.9 1.1)

mkdir -p "$logdir"

for vdd in "${corners[@]}"; do
  for seed in $(seq 1 "$seeds"); do
    logfile="$logdir/vdd${vdd/./p}_seed${seed}.log"
    ngspice -b "$deck" \
      -o "$logfile" \
      +VDD="$vdd" \
      +mismatch_switch=1 \
      +mcseed="$seed" \
      >/dev/null
  done
done
