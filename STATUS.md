# Status Dashboard

## Current health
- **Encoder deck:** deterministic runs cover sync/de-sync/sparse/dense/random patterns; leakage-corrected `Edyn` and per-transition normalization reported in `spicemodels/option-b-encoder-results.md`.
- **Shared periphery:** shared comparator/driver energy and headroom logged at ±10% VDD (0.9 V and 1.1 V) plus the random stimulus (see `experiments/shared-sense-periphery.md`). Headroom monitors (`sharedSenseDiff`) now record min/max even though the comparator never crosses 0.5·VDD.
- **Periphery ledger:** `models/periphery-cost-model.md` tracks energy vs. kill criterion, now citing the ±10% shared-sense runs.

## Work in progress
1. **Mismatch / Monte Carlo:** still pending; run the shared-sense deck with mismatch/MC enabled now that the TT parameter list is in place and capture the energy/headroom comparisons alongside the ±10% corners.  
2. **Driver latency measurements:** the shared driver still rarely clears 0.5·VDD, so `td_*`/`settle_*` `.meas` statements fail. Add 0.1/0.9 threshold probes or level restoration once a larger headroom margin appears so the latency budget can be quantified without repeated failures.

## Blockers
- Remaining kill-criterion (periphery dominance / noise margin) requires the mismatch+MC campaign or a noise-injected sweep to prove the low-swing sense remains robust before classifying the candidate as fully validated.

## Done this sprint
- Added the 13-parameter instantiation for every `sky130_fd_pr__nfet/pfet` call, allowing `option-b-encoder-with-shared-sense-tt.spice` to run and match the 1.0 V measurement energy (`Edyn ≈ 0.45 pJ`, `Eword ≈ 4.86 pJ`).  
- Ran the shared-sense deck at ±10% VDD (0.9 V/1.1 V) and recorded the headroom (`sharedSenseP/N ≈ 44 mV` at 0.9 V, ≈111 mV at 1.1 V) plus the failure notices for the 0.5·VDD probes; documented the ±10% results in `experiments/shared-sense-periphery.md` and `models/periphery-cost-model.md`.  
- Logged the negative `td_*` outputs so it is clear why the comparator never crosses 0.5·VDD under the current stimuli.
