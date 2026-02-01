# Project Summary

## What we have measured
- **Encoder energy:** `spicemodels/option-b-encoder-results.md` now lists sync/de-synced patterns plus low-, medium-, and high-activity decks. `Edyn` is leakage-corrected and scaled to slices/word (with per-transition normalization). The latest scaling model is `Eword ≈ Eleak + 0.33 pJ × transitions`.
- **Shared sense periphery:** `spicemodels/option-b-encoder-with-shared-sense*.spice` (plus the ±10% variants) aggregates four encoder outputs into one driver. At 0.9 V the comparator draws nearly zero extra dynamic energy, and at 1.1 V the periphery is still ≈5.55 pJ/word with headroom ≈±0.13 mV. The periphery ledger (see `experiments/shared-sense-periphery.md` and `models/periphery-cost-model.md`) now says the shared-sense path sits below the 6.6 pJ binary guardrail provided the TT/mismatch validations succeed.

## Validation gaps
- The TT corner deck (`option-b-encoder-with-shared-sense-tt.spice`) still aborts because the TT subcircuit requires parameter passing; decide whether to duplicate that parameter list or reuse the SS deck with `process_switch=1`.  
- Measurement probes that expect 0.5·VDD (e.g., `td_tN0`, `td_sharedP`) keep failing because the shared driver never swings that far under the current stimuli; consider additional `.meas` statements at 0.1/0.9 thresholds once the headroom grows (e.g., when we add level restoration).
- The mismatch/Monte Carlo sweep is pending until the BSIM parameter list issue for TT is resolved. That run must record energy/headroom to fully close kill criterion **periphery dominance (2)**.

## What’s next
1. Decide how to run the TT corner (pass parameters vs. set `process_switch=1`).  
2. Once TT/mismatch parameters are settled, execute the shared-sense ±10% + mismatch sweep and append those results to the periphery ledger.  
3. Continue logging every amortized/shared-sense experiment (energy + headroom + stimulus metadata) under `experiments/shared-sense-periphery.md` so the repository keeps a single source of truth for kill-criterion tracking before migrating a candidate to production.
