# Guard ledger manifest

This manifest describes the canonical guard ledger used by the shared-sense periphery documentation, status table, and downstream AI analysis.

- **Ledger file:** `data/canonical_guard_ledger.csv`
- **Generation script:** `tools/export_guard_ledger.py` (run from the repository root)
- **Purpose:** combine every numeric tuple (energy, headroom, latency, comparator pass/fail, seeds, noise/driver/phase metadata, logs, and matching histogram file) into one machine-readable dataset that mirrors the guard/jitter story in human-facing docs.

## Regeneration steps
1. `python3 tools/export_guard_ledger.py data/canonical_guard_ledger.csv`
2. Review `headroom_histogram.csv` files under each `logs/*` directory; the script stores their relative paths in the ledger.
3. Commit both `data/canonical_guard_ledger.csv` and this manifest when the raw logs or metadata change.

## Column summary
- `experiment`: high-level notes for the log directory (±10% mismatch MC, noise sweep, TT, phase-skew, glimpses, boosted/tuned driver)
- `subset`: detail string for variants such as boosted strong-arm or tuned eval window
- `noise_amp`, `driver_scale`, `phase_ns`: experiment knobs exposed in the logs
- `vdd`, `seed`: corner and sample identifiers
- `edyn_pJ`, `eword_pJ`: energy entries converted to picojoules
- `sense_min_mV`, `sense_max_mV`: guard headroom converted to millivolts
- `sense_thresh_latency_ps`, `comp_toggle_latency_ps`: jitter measurements converted to picoseconds
- `comp_pass`: comparator pass/fail verdict from the logs
- `headroom_histogram`: CSV path (in `logs/<dir>/headroom_histogram.csv`) tied to each tuple

## Tracking notes
Each downstream doc (README, STATUS.md, SUMMARY.md, models/periphery-cost-model.md, experiments/shared-sense-periphery.md, FINDINGS.md) now references this ledger/manifest so the numeric story stays synchronized. Update the ledger + manifest whenever new sweep data or histogram counts are added.
