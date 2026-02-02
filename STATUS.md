## Current health
- **Encoder deck:** deterministic runs cover sync/de-sync/sparse/dense/random patterns; leakage-corrected `Edyn` and per-transition normalization reported in `spicemodels/option-b-encoder-results.md`.
- **Shared periphery:** shared comparator/driver energy and headroom logged at ±10% VDD (0.9 V and 1.1 V) plus the random stimulus (see `experiments/shared-sense-periphery.md`). Headroom monitors (`sharedSenseDiff`) now register 0.8995–0.9005 V at ±10% and ≈0.998 V at TT, so the 20 mV guard is satisfied even though the comparator still never crosses 0.5·VDD (the `td_*`/`settle_*` probes remain “out of interval”). The TT deck runs cleanly with the new parameter block, giving us energy, headroom, and noise-margin data that tie into `logs/mismatch-mc/headroom_histogram.csv` and `logs/mismatch-mc-tt/headroom_histogram.csv`.
  - **Noise stress plan:** add a controlled 5–10 mV noise source across `sharedsensep/sharedsensen`, log the `sense_headroom_min/max` histogram, and, if required, size up the final driver while logging the additional energy vs. swing data so the ledger captures both the low-swing feature and any driver-size trade-offs.
  - **Monte Carlo histogram:** enabling the MC switches at 0.9/1.0/1.1 V (and a matched TT sweep) with 50 seeds per corner now logs 0.313/0.452 pJ of `Edyn` and ≈3.34/−0.29 pJ of `Eword_est`, while the driver headroom stays around 0.8995–0.9005 V for ±10% and ≈0.998 V at TT (see `logs/mismatch-mc/mismatch_mc.csv` and `logs/mismatch-mc-tt/mismatch_mc_tt.csv`). The kill-criterion ledger now references a satisfied 20 mV guard instead of hunting for one.
  - **Encoder activity tie-in:** combine the typical 3–5 transitions/window workload with the amortized model `Eword ≈ Eleak + 0.33 pJ × transitions`, keeping the total encoder + shared-sense periphery estimate (~5–7 pJ/word) front-and-center in the ledger until the unified deck migrates to `spicemodels/`.
- **Periphery ledger:** `models/periphery-cost-model.md` tracks energy vs. kill criterion, now citing the ±10% shared-sense runs.

## Work in progress
1. **Latency/jitter validation:** With the Monte Carlo sweep (and histogram) now clearing the 20 mV guard, log the `sense_thresh_low/high` latency window plus any jitter/noise spreads so the periphery ledger can tie the guard to concrete timing envelopes before the candidate graduates.
2. **Controller APIs:** Confirm the ternary tokens remain substrate-neutral and the shared-sense driver keeps its jitter/latency headroom under the more aggressive noise/stress patterns before moving the deck into `spicemodels/` and tight timing budgets.

## Blockers
- The comparator/driver still never reaches 0.5·VDD, so the `td_*`/`settle_*` `.meas` entries remain “out of interval”; until we can correlate the high headroom with the latency span triggered by `{sense_thresh_low/high}`, those latency probes stay a caution rather than a pass/fail gate.
- Logging the `sense_thresh_latency` entries plus the new histograms (`logs/mismatch-mc/headroom_histogram.csv`, `logs/mismatch-mc-tt/headroom_histogram.csv`) remains critical so the periphery ledger explains exactly how much jitter the 0.9 V/1.1 V combos can tolerate before moving to production-level `spicemodels/`.

## Done this sprint
- Added the 13-parameter instantiation for every `sky130_fd_pr__nfet/pfet` call, allowing `option-b-encoder-with-shared-sense-tt.spice` to run and match the 1.0 V measurement energy (`Edyn ≈ 0.45 pJ`, `Eword ≈ 4.86 pJ`).  
- Ran the shared-sense deck at ±10% VDD (0.9 V/1.1 V) and recorded the headroom (`sharedSenseP/N ≈ 44 mV` at 0.9 V, ≈111 mV at 1.1 V) plus the failure notices for the 0.5·VDD probes; documented the ±10% results in `experiments/shared-sense-periphery.md` and `models/periphery-cost-model.md`.  
- Logged the negative `td_*` outputs so it is clear why the comparator never crosses 0.5·VDD under the current stimuli.
