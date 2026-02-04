# Findings

## Scoreboard
- Candidates 1–3 remain the reference failures while Option B is the only conditional survivor (see the Status/kill table in `models/ternary-cell-candidates.md:7-105`). The documentation keeps Option B alive only if the headroom/latency ledger proves the shared-sense driver plus encoder energy don't violate periphery dominance (models/ternary-cell-candidates.md:82-105).
- CNTFET/GNRFET routes (candidates 5–8) are still deferred for tooling/device reasons, so no new cells have graduated from their reference status (models/ternary-cell-candidates.md:107-155).

## Measurements & tests
`./tools/run_shared_mismatch_mc.sh` ran 150 seeds (50 per corner) with the retargeted `sense_thresh_latency` probe. `logs/mismatch-mc/mismatch_mc.csv` now stores (`sense_min`, `sense_max`, `sense_thresh_latency`) for every seed, and all 150 entries report ≈0.125 ps jitter while headroom bins in `logs/mismatch-mc/headroom_histogram.csv` sit at 860–865 mV (max ≈0.900 V). The `Edyn ≈ 0.313 pJ` / `Eword_est ≈ 3.34 pJ` tuples remain stable while the new latency column ties each seed to the 20 mV guard.
`./tools/run_tt_mismatch_mc.sh` completed 50 TT seeds. `logs/mismatch-mc-tt/mismatch_mc_tt.csv` now records ≈4.75 ps per seed, and the histogram (`logs/mismatch-mc-tt/headroom_histogram.csv`) sits in the 960–965 mV bin with maxima near 1.00175 V, so every TT tuple pairs latency, headroom, and the −0.29 pJ energy entry.
`tools/run_noise_mismatch_driver_sweep.sh` extended the noise campaign across driver scales 1.5/2.0/2.5 (for both 5 mV and 10 mV noise). The resulting tuples live in `logs/noise-mismatch-{5m,10m}-driver-{1p5,2,2p5}/mismatch_mc.csv` and keep the guard/jitter data aligned with the energy numbers even as the drive strength changes, reinforcing that the 20 mV headroom cushion holds under the enlarged driver permutations.
All shared-sense decks still pull the SkyWater models from `/Users/t81dev/Code/pdk/sky130A/libs.ref/sky130_fd_pr/…` (`spicemodels/option-b-encoder-with-shared-sense-mismatch.spice:63-66`), so the mismatch switches + zeroed slope knobs must stay synchronized for every run.

## Comparator handoff observation

- Noise/driver sweep at 10 mV / driver scale 2.5 produced 60 seeds per corner (`logs/noise-mismatch-10m-driver-2p5/mismatch_mc.csv`) but **`comp_pass` stayed "failed" for every seed** despite the energy staying ≈3.34 pJ/w (per-word `eword` column). The comparator never toggled under this stress, so the comparator-path fork is not yet resolved.

## Next steps
1. Mirror each ±10%/TT energy+headroom+lat tuple (including noise/clock-skew or driver permutations) into `models/periphery-cost-model.md`, `STATUS.md`, `SUMMARY.md`, and `experiments/shared-sense-periphery.md` so the guard story keeps jitter & energy together before migrating the deck back into `spicemodels/`.
2. When rerunning the guard sweep, regenerate `logs/mismatch-mc/mismatch_mc.csv`, `logs/mismatch-mc-tt/mismatch_mc_tt.csv`, and their `headroom_histogram.csv` companions together so the latency column, histograms, and CSV tuples stay in sync; treat that aligned dataset as the canonical ledger for periphery dominance and retiming/jitter margins before migration.

## Baseline migration
- The validated shared-sense deck now lives in `spicemodels/option-b-encoder-with-shared-sense-baseline.spice` (deterministic, mismatch switches off) and is documented in `spicemodels/README.md`. Treat this file as the canonical baseline before branching into subsequent noise/driver stress runs.

## Open tabs
- FINDINGS.md: FINDINGS.md
- STATUS.md: STATUS.md
- SUMMARY.md: SUMMARY.md
- README.md: README.md
- ternary-cell-candidates.md: models/ternary-cell-candidates.md
