#!/usr/bin/env bash
set -euo pipefail

deck="spicemodels/option-b-encoder-with-shared-sense-mismatch.spice"
repo_root=$(pwd)
deck_path="$repo_root/$deck"
samples=${SAMPLES:-50}
seed_start=${SEED_START:-1}
max_seed=${MAX_SEED:-50}
seed_end=$((seed_start + samples - 1))
if [ "$seed_end" -gt "$max_seed" ]; then
  seed_end=$max_seed
fi
vdd_list=${1:-"0.9 1.0 1.1"}
noise_amps=${NOISE_AMPS:-"5m 10m"}
driver_scales=${DRIVER_SCALES:-"1.5 2.0 2.5 3.0"}
pdk_spice_dir=${PDK_SPICE_DIR:-"/Users/t81dev/Code/pdk/sky130A/libs.ref/sky130_fd_pr/spice"}

if [ ! -d "$pdk_spice_dir" ]; then
  echo "PDK spice directory '$pdk_spice_dir' does not exist; download SkyWater libs.ref or set PDK_SPICE_DIR." >&2
  exit 1
fi

pdk_marker="sky130_fd_pr__nfet_01v8__ss.pm3.spice"
if [ ! -f "$pdk_spice_dir/$pdk_marker" ]; then
  echo "Missing expected model '$pdk_marker' in $pdk_spice_dir; ensure the SkyWater PDK is installed." >&2
  exit 1
fi
force_delta_steps=${COMP_FORCE_DELTA_STEPS:-"0 1 2 3 4 5 6 7 8 9 10"}

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

build_comp_param_block() {
  local delta="$1"
  local names=(COMP_WP COMP_WN COMP_CROSS_SCALE COMP_TAIL_SCALE COMP_LOAD_SCALE COMP_WP_CROSS COMP_WN_TAIL COMP_WN_LOAD COMP_FORCE_DELTA COMP_CLK_DELAY COMP_CLK_TR COMP_CLK_TF COMP_CLK_HIGH COMP_CLK_PERIOD COMP_TOPOLOGY COMP_DT_IN COMP_DT_TAIL_PRE COMP_DT_TAIL_LATCH COMP_DT_LATCH COMP_DT_PMOS COMP_DT_INV_WN COMP_DT_INV_WP)
  local block=""
  for name in "${names[@]}"; do
    local val="${!name:-}"
    if [ "$name" = "COMP_FORCE_DELTA" ] && [ -n "$delta" ]; then
      val="$delta"
    fi
    if [ -n "$val" ]; then
      block+=$(printf ".param %s=%s\n" "$name" "$val")
    fi
  done
  printf "%s" "$block"
}

format_force_delta_param() {
  local raw="$1"
  if [[ "$raw" == *m ]]; then
    printf "%s" "$raw"
  else
    printf "%sm" "$raw"
  fi
}

format_force_delta_tag() {
  local raw="$1"
  if [[ "$raw" == *m ]]; then
    raw="${raw%m}"
  fi
  raw="${raw//./p}"
  printf "%sm" "$raw"
}

for scale in $driver_scales; do
  driver_wn=$(compute_width "$scale" 2)
  driver_wp=$(compute_width "$scale" 4)
  scale_tag=$(normalize_scale_tag "$scale")

  for noise in $noise_amps; do
    for force_delta in $force_delta_steps; do
      delta_param=$(format_force_delta_param "$force_delta")
      delta_tag=$(format_force_delta_tag "$force_delta")
      logdir="logs/noise-mismatch-${noise}-driver-${scale_tag}-delta-${delta_tag}"
      mkdir -p "$logdir"
      datafile="$logdir/mismatch_mc_delta_${delta_tag}.csv"
      if [ ! -f "$datafile" ]; then
        printf "# noise_amp=%s driver_scale=%s comp_force_delta=%s mismatch MC data\n" "$noise" "$scale" "$delta_param" > "$datafile"
        printf "vdd,seed,comp_force_delta,edyn,eword,sense_min,sense_max,sense_thresh_latency,comp_toggle_latency,comp_pass\n" >> "$datafile"
      fi

      comp_param_block=$(build_comp_param_block "$delta_param")

      for vdd in $vdd_list; do
        if [ "$seed_start" -gt "$seed_end" ]; then
          echo "No seeds to run (seed_start=$seed_start, seed_end=$seed_end)."
          continue
        fi

        for seed in $(seq "$seed_start" "$seed_end"); do
          logfile="$logdir/mc_$(printf '%.1f' "$vdd")V_${scale_tag}_${delta_tag}_${seed}.log"
          logfile_path="$repo_root/$logfile"
          (
            cd "$pdk_spice_dir"
            printf ".option gseed=%s\n.param run_vdd=%s\n.param noise_amp=%s\n.param PDK_SPICE_DIR=%s\n.param DRIVER_WN=%s\n.param DRIVER_WP=%s\n%s.run\n.quit\n" \
              "$seed" "$vdd" "$noise" "$pdk_spice_dir" "$driver_wn" "$driver_wp" "$comp_param_block" | ngspice -b "$deck_path" -o "$logfile_path"
          )

          read edyn eword sense_min sense_max sense_thresh comp_toggle comp_pass < <(tools/parse_mismatch_log.py "$logfile_path")
          printf "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" "$vdd" "$seed" "$delta_param" "$edyn" "$eword" "$sense_min" "$sense_max" "$sense_thresh" "$comp_toggle" "$comp_pass" >> "$datafile"
        done
      done

      tools/headroom_histogram.py "$datafile" "$logdir/headroom_histogram.csv"
    done
  done
done
