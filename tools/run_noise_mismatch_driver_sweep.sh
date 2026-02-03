#!/usr/bin/env bash
set -euo pipefail

deck="spicemodels/option-b-encoder-with-shared-sense-mismatch.spice"
samples=50
vdd_list=${1:-"0.9 1.0 1.1"}
noise_amps=${NOISE_AMPS:-"5m 10m"}
driver_scales=${DRIVER_SCALES:-"1.5 2.0 2.5 3.0"}

compute_width() {
  python3 - "$1" "$2" <<'PY'
import sys
scale = float(sys.argv[1])
factor = float(sys.argv[2])
print(f"{scale * factor:g}u")
PY
}

normalize_scale_tag() {
  python3 - "$1" <<'PY'
import sys
tag = sys.argv[1].replace(".", "p")
if tag.endswith("p0"):
    tag = tag[:-2]
print(tag)
PY
}

for scale in $driver_scales; do
  driver_wn=$(compute_width "$scale" 2)
  driver_wp=$(compute_width "$scale" 4)
  scale_tag=$(normalize_scale_tag "$scale")

  for noise in $noise_amps; do
    logdir="logs/noise-mismatch-${noise}-driver-${scale_tag}"
    mkdir -p "$logdir"
    datafile="$logdir/mismatch_mc.csv"
    printf "# noise_amp=%s driver_scale=%s mismatch MC data\n" "$noise" "$scale" > "$datafile"
    printf "vdd,seed,edyn,eword,sense_min,sense_max,sense_thresh_latency\n" >> "$datafile"

    for vdd in $vdd_list; do
      for seed in $(seq 1 "$samples"); do
        logfile="$logdir/mc_$(printf '%.1f' "$vdd")V_${scale_tag}_${seed}.log"
        printf ".option gseed=%s\n.param run_vdd=%s\n.param noise_amp=%s\n.param DRIVER_WN=%s\n.param DRIVER_WP=%s\n.run\n.quit\n" \
          "$seed" "$vdd" "$noise" "$driver_wn" "$driver_wp" | ngspice -b "$deck" -o "$logfile"

        read edyn eword sense_min sense_max sense_thresh < <(tools/parse_mismatch_log.py "$logfile")
        printf "%s,%s,%s,%s,%s,%s,%s\n" "$vdd" "$seed" "$edyn" "$eword" "$sense_min" "$sense_max" "$sense_thresh" >> "$datafile"
      done
    done

    tools/headroom_histogram.py "$datafile" "$logdir/headroom_histogram.csv"
  done
done
