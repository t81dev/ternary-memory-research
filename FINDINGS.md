# Findings

## Scoreboard
- Candidates 1–3 remain the reference failures while Option B is the only conditional survivor (see the Status/kill table in [`models/ternary-cell-candidates.md`](models/ternary-cell-candidates.md)). The documentation keeps Option B alive only if the headroom/latency ledger proves the shared-sense driver plus encoder energy don't violate periphery dominance.
- CNTFET/GNRFET routes (candidates 5–8) are still deferred for tooling/device reasons.

## Measurements & tests
- **Mismatch MC:** `./tools/run_shared_mismatch_mc.sh` ran 150 seeds (50 per corner). `sense_thresh_latency` is ≈0.125 ps, and headroom bins in `logs/mismatch-mc/headroom_histogram.csv` sit at 860–865 mV.
- **TT Mismatch MC:** `./tools/run_tt_mismatch_mc.sh` completed 50 TT seeds. `sense_thresh_latency` is ≈4.75 ps, headroom ≈960–965 mV.
- **Noise Stress:** `tools/run_noise_mismatch_driver_sweep.sh` extended the noise campaign across driver scales 1.5/2.0/2.5. The guard stayed above ≈860–865 mV.
- **Phase Skew:** `tools/run_shared_sense_phase_skew.sh` confirms that even with ±0.5 ns skew, the latency remains stable at ≈1.95 ps and headroom at ≈−271 mV.
- **Boosted Comparator:** The StrongARM comparator with boosted devices still reports `comp_pass=failed` for all seeds in `logs/noise-mismatch-10m-driver-2p5/mismatch_mc.csv`.

## Comparator handoff observation

- Noise/driver sweep at 10 mV / driver scale 2.5 produced 60 seeds per corner (`logs/noise-mismatch-10m-driver-2p5/mismatch_mc.csv`) but **`comp_pass` stayed "failed" for every seed** despite the energy staying ≈3.34 pJ/w. The comparator never toggled under this stress, so the comparator-path fork is not yet resolved. This remains the primary blocker.

## Next steps
1. Mirror each ±10%/TT energy+headroom+lat tuple into [`models/periphery-cost-model.md`](models/periphery-cost-model.md) and [`STATUS.md`](STATUS.md).
2. When rerunning the guard sweep, regenerate CSVs and histograms together.
3. Refresh `data/canonical_guard_ledger.csv` after each batch.

## Baseline migration
- The validated shared-sense deck now lives in `spicemodels/option-b-encoder-with-shared-sense-baseline.spice`. Treat this file as the canonical baseline before branching into subsequent noise/driver stress runs.
