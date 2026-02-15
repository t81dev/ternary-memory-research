# Project Summary

## What we have measured
- **Encoder energy:** [`spicemodels/option-b-encoder-results.md`](spicemodels/option-b-encoder-results.md) lists sync/de-synced patterns and activity-based energy models (`Eword ≈ Eleak + 0.33 pJ × transitions`).
- **Shared sense periphery:** `spicemodels/option-b-encoder-with-shared-sense*.spice` runs across TT and ±10% VDD. Headroom histograms confirm operation outside the 20 mV guard window.
- **Noise/driver notes:** Injecting ~5–10 mV of noise stresses the headroom, but samples remain robust (860–900 mV). Driver sweeps (1.5–2.5×) confirm stability of the guard.
- **Phase-skew:** `tools/run_shared_sense_phase_skew.sh` confirms latency stability (≈1.95 ps) under ±0.5 ns skew.
- **Guard ledger aggregation:** `data/canonical_guard_ledger.csv` is the single source of truth for energy/headroom/latency tuples.

For the full detailed status table and guard/jitter ledger, see [`STATUS.md`](STATUS.md).

## Validation gaps
- **Comparator Handoff:** The StrongARM comparator still reports `comp_pass=failed` for every valid seed, even with boosted devices. The differential swing is insufficient (~40mV) to flip the latch.
- **Upsized Mismatch Logs:** While `logs/mismatch-mc-upsized/` contains data, earlier runs reported warnings about model names. Ensure these are fully resolved before relying on them for final signoff.

## What’s next
1. **Resolve Comparator:** Prioritize fixing the `comp_pass=failed` issue. This is the primary blocker for migrating the deck to `spicemodels/`.
2. **Maintain Documentation:** Keep `STATUS.md` and `models/periphery-cost-model.md` updated with the latest sweep data.
3. **Log Permutations:** Continue to log every noise/driver permutation to the canonical ledger.
