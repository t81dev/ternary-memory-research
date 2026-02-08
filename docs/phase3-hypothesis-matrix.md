# Phase 3 Hypothesis and Kill-Criteria Matrix

Roadmap linkage:
- `t81-roadmap#16`
- `t81-roadmap/PHASE3_MILESTONE_MATRIX.md` (`P3-M3`)
- Implementation tracker: `ternary-memory-research#2`

## Hypothesis Matrix

| Hypothesis ID | Statement | Acceptance Signal | Kill Trigger | Primary Evidence |
| --- | --- | --- | --- | --- |
| H1 | Shared-sense periphery can maintain guard headroom under ±10% and TT sweeps. | Headroom bins remain above minimum guard threshold with reproducible logs. | Headroom collapse below guard threshold across repeated seeds. | `logs/mismatch-mc/headroom_histogram.csv`, `logs/mismatch-mc-tt/headroom_histogram.csv` |
| H2 | Energy + jitter tuple remains stable across noise/driver/phase-skew sweeps. | `sense_thresh_latency` and energy tuples remain within bounded bands. | Unbounded latency/energy growth under targeted stress permutations. | `logs/*/mismatch_mc*.csv`, `data/canonical_guard_ledger.csv` |
| H3 | Candidate decks remain auditable against explicit kill criteria before `spicemodels/` promotion. | Ledger + status docs stay synchronized with experiment outputs. | Inability to map claims to ledger rows and experiment artifacts. | `data/GUARD_LEDGER_MANIFEST.md`, `STATUS.md`, `SUMMARY.md` |

## Reproducible Evidence Path

Core sweep + aggregation path:

```bash
tools/run_noise_mismatch_driver_sweep.sh
python3 tools/aggregate_mismatch_logs.py
python3 tools/headroom_histogram.py
python3 tools/export_guard_ledger.py data/canonical_guard_ledger.csv
python3 tools/check_guard_consistency.py
```

Phase-skew extension path:

```bash
tools/run_shared_sense_phase_skew.sh
python3 tools/aggregate_phase_skew_logs.py
python3 tools/headroom_histogram.py
```

## Software-Hardware Checkpoint Link

The guard ledger and histogram outputs serve as the current checkpoint artifact set for cross-repo Phase 3 reporting in `t81-roadmap`.
