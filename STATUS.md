# Status Dashboard

## Current health
- **Encoder deck:** deterministic runs cover sync/de-sync/sparse/dense/random patterns; leakage-corrected `Edyn` and per-transition normalization reported in `spicemodels/option-b-encoder-results.md`.
- **Shared periphery:** shared comparator/driver energy and headroom logged at ±10% VDD (0.9 V and 1.1 V) plus the random stimulus (see `experiments/shared-sense-periphery.md`). Headroom monitors (`sharedSenseDiff`) now record min/max even though the comparator never crosses 0.5·VDD; the TT deck now runs cleanly with the new parameter block so we have TT/±10% energy, headroom, and noise-margin data. Note the shared driver still doesn’t reach 0.5·VDD, so `td_*`/`settle_*` probes designed for 0.5·VDD continue to fail and are ignored in favor of the `sense_headroom_*` recorded values.
  - **Noise stress plan:** add a controlled 5–10 mV noise source across `sharedsensep/sharedsensen`, log the `sense_headroom_min/max` histogram, and, if required, size up the final driver while capturing the additional energy headroom point; these entries will prove the ~70–110 mV swing survives stress or quantify the extra cost needed to widen it.
  - **Monte Carlo histogram:** enabling the MC switches at 0.9/1.0/1.1 V (and a matched TT sweep) with 50 seeds per corner now logs 0.313/0.452 pJ of `Edyn` and ≈3.37/4.86 pJ of `Eword_est`, while the driver difference headroom stays within only ±0.295 mV for ±10% and only occasionally reaches ≈24.6 mV at TT; these tuples live in `logs/mismatch-mc/mismatch_mc.csv` plus `logs/mismatch-mc-tt/mismatch_mc_tt.csv`, and the upsized 3u/6u deck pushes the driver difference to ≈±0.416 mV (see `logs/mismatch-mc-upsized/mismatch_mc.csv` aggregated by `tools/aggregate_mismatch_logs.py`).
  - **Encoder activity tie-in:** combine the typical 3–5 transitions/window workload with the amortized model `Eword ≈ Eleak + 0.33 pJ × transitions`, keeping the total encoder + shared-sense periphery estimate (~5–7 pJ/word) front-and-center in the ledger until the unified deck migrates to `spicemodels/`.
- **Periphery ledger:** `models/periphery-cost-model.md` tracks energy vs. kill criterion, now citing the ±10% shared-sense runs.

## Work in progress
1. **Driver margin strategy:** With the Monte Carlo sweep complete and the upsized driver now reaching only ≈±0.416 mV, decide whether additional upsizing or a level-restorer is required to reach the 20 mV guard before the `td_*` probes can exit their “out of interval” state.
2. **Latency measurements:** The shared driver still never swings to 0.5·VDD, so the `td_*`/`settle_*` `.meas` statements fail; we continue to plot the `{sense_thresh_low/high}` latency span while we identify a noise margin solution that lets the latency probes exit their “out of interval” state.

## Blockers
- The periphery dominance ledger now logs the ±10%/TT and upsized Monte Carlo histograms, but the worst-case headroom stays near ±0.3 mV (baseline) / ±0.416 mV (upsized) at the ±10% corners and only occasionally hits ≈24.6 mV at TT, so the 20 mV noise margin remains unsettled until driver sizing or level restoration recovers that guard.
- The comparator/driver still never reaches 0.5·VDD, so the `td_*`/`settle_*` `.meas` entries remain “out of interval”; we continue cataloging the `sense_headroom_*` and `{sense_thresh_low/high}` spans while searching for a driver/signal change that brings the latency probes back into range.

## Done this sprint
- Added the 13-parameter instantiation for every `sky130_fd_pr__nfet/pfet` call, allowing `option-b-encoder-with-shared-sense-tt.spice` to run and match the 1.0 V measurement energy (`Edyn ≈ 0.45 pJ`, `Eword ≈ 4.86 pJ`).  
- Ran the shared-sense deck at ±10% VDD (0.9 V/1.1 V) and recorded the headroom (`sharedSenseP/N ≈ 44 mV` at 0.9 V, ≈111 mV at 1.1 V) plus the failure notices for the 0.5·VDD probes; documented the ±10% results in `experiments/shared-sense-periphery.md` and `models/periphery-cost-model.md`.  
- Logged the negative `td_*` outputs so it is clear why the comparator never crosses 0.5·VDD under the current stimuli.
