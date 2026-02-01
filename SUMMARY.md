# Project Summary

## What we have measured
- **Encoder energy:** `spicemodels/option-b-encoder-results.md` now lists sync/de-synced patterns plus low-, medium-, and high-activity decks. `Edyn` is leakage-corrected and scaled to slices/word (with per-transition normalization). The latest scaling model is `Eword ≈ Eleak + 0.33 pJ × transitions`.
- **Shared sense periphery:** `spicemodels/option-b-encoder-with-shared-sense*.spice` now runs across TT and ±10% VDD, aggregating four encoder outputs into a single comparator/driver. The TT deck reproduces `Edyn ≈ 0.45 pJ`, `Eslice ≈ 0.11 pJ`, and `Eword_est ≈ 4.86 pJ` while the ±10% corners report `Eword_est` between ≈4–6 pJ and sense headroom between ≈43–111 mV. The driver still never crosses 0.5·VDD, so `td_*`/`settle_*` probes targeted at that threshold fail, but `sense_headroom_min/max` capture the low-swing window and keep the periphery ledger (`experiments/shared-sense-periphery.md` / `models/periphery-cost-model.md`) auditable.
  - **Noise/driver notes:** Injecting ~5–10 mV of noise onto the shared rails lets us stress the headroom histogram; if the ~70–110 mV swing remains detectable by downstream logic we log it as a feature, otherwise we ramp up the driver sizing and plot the extra energy vs. swing so the periphery ledger shows the cost of regaining margin.

-## Validation gaps
- The TT corner deck now runs after the per-device parameter block was added, but the mismatch/Monte Carlo sweep is still pending; record its energy/headroom so **periphery dominance (2)** stays validated.
- Measurement probes that expect 0.5·VDD (e.g., `td_tN0`, `td_sharedP`) keep failing because the shared driver never swings that far under the current stimuli; consider additional `.meas` statements at 0.1/0.9 thresholds once the headroom grows (e.g., when we add level restoration).
- The mismatch/Monte Carlo sweep is pending until the BSIM parameter list issue for TT is resolved. That run must record energy/headroom to fully close kill criterion **periphery dominance (2)**.

## What’s next
1. Rerun the shared-sense deck with mismatch/Monte Carlo now that the TT parameters are there, and capture Edyn/headroom for the ledger.  
2. Keep the ±10% + TT results documented in `models/periphery-cost-model.md` plus `STATUS.md`, and roll the new measurements into the roadmap before prototyping.
3. Continue logging every amortized/shared-sense experiment (energy + headroom + stimulus metadata) under `experiments/shared-sense-periphery.md` so the repository keeps a single source of truth for kill-criterion tracking before migrating a candidate to production.
