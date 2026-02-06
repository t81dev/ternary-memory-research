# Findings

## Scoreboard
- Candidates 1–3 remain the reference failures while Option B is the only conditional survivor (see the Status/kill table in [`models/ternary-cell-candidates.md`](models/ternary-cell-candidates.md)). The documentation keeps Option B alive only if the headroom/latency ledger proves the shared-sense driver plus encoder energy don't violate periphery dominance (see the same file's guard story near lines 82‑105).
- CNTFET/GNRFET routes (candidates 5–8) are still deferred for tooling/device reasons, so no new cells have graduated from their reference status (see [`models/ternary-cell-candidates.md`](models/ternary-cell-candidates.md) for the detour notes around lines 107‑155).

## Measurements & tests
`./tools/run_shared_mismatch_mc.sh` ran 150 seeds (50 per corner) with the retargeted `sense_thresh_latency` probe. `logs/mismatch-mc/mismatch_mc.csv` now stores (`sense_min`, `sense_max`, `sense_thresh_latency`) for every seed, and all 150 entries report ≈0.125 ps jitter while headroom bins in `logs/mismatch-mc/headroom_histogram.csv` sit at 860–865 mV (max ≈0.900 V). The `Edyn ≈ 0.313 pJ` / `Eword_est ≈ 3.34 pJ` tuples remain stable while the new latency column ties each seed to the 20 mV guard.
`./tools/run_tt_mismatch_mc.sh` completed 50 TT seeds. `logs/mismatch-mc-tt/mismatch_mc_tt.csv` now records ≈4.75 ps per seed, and the histogram (`logs/mismatch-mc-tt/headroom_histogram.csv`) sits in the 960–965 mV bin with maxima near 1.00175 V, so every TT tuple pairs latency, headroom, and the −0.29 pJ energy entry.
`tools/run_noise_mismatch_driver_sweep.sh` extended the noise campaign across driver scales 1.5/2.0/2.5 (for both 5 mV and 10 mV noise). The resulting tuples live in `logs/noise-mismatch-{5m,10m}-driver-{1p5,2,2p5}/mismatch_mc.csv` and keep the guard/jitter data aligned with the energy numbers even as the drive strength changes, reinforcing that the 20 mV headroom cushion holds under the enlarged driver permutations.
`spicemodels/sharedsense_comparator_strongarm.spice` now points at a boosted version with larger WP/WN (and a tiny level-restorer), and rerunning the targeted `NOISE_AMPS=10m DRIVER_SCALES="2.5"` sweep at 0.9 V produced 153 seeds recorded in `logs/noise-mismatch-10m-driver-2p5/mismatch_mc.csv` plus the matching histogram; the energy/jitter tuples remain ≈3.34 pJ/0.125 ps and `comp_pass=failed`, so the comparator handoff still doesn’t flip but the boosted logs are now documented in the ledger.
`tools/run_noise_mismatch_driver_sweep.sh` still hits the 120 s timeout when it tries to run the full 10 mV/driver-scale sweep, so we resumed in smaller batches (VDD=1.0 V, +10 mV noise, seeds 1–4) and then filled VDD=0.9 V seeds 16–50 plus VDD=1.1 V seeds 5–50 with the same chunked approach. These rows now extend `logs/noise-mismatch-10m-driver-1p5/mismatch_mc.csv` to all 150 samples, still reporting `Edyn ≈ 0.311 pJ`, `Eword_est ≈ 3.34 pJ`, `sense_thresh_latency ≈ 0.125 ps`, headroom locked to 860–865 mV (count 150), and `comp_pass=failed`, so the comparator tally still fails even though the guard/jitter tuple now exists for driver scale 1.5; the rest of the sweep (scales 2.0/2.5 and/or the 5 mV noise runs) will continue via the same chunked approach.
We also removed the latest 205 MB carrier logs in `logs/noise-mismatch-5m-driver-1p5-delta-0m/` and its archived copy, then added `.gitignore` entries for `logs/archive/` and `logs/noise-mismatch-5m-driver-1p5-delta-0m/*.log` so those heavyweight runs stay local while the CSVs/metadata stay tracked.
All shared-sense decks still pull the SkyWater models from `/Users/t81dev/Code/pdk/sky130A/libs.ref/sky130_fd_pr/…` (see [`spicemodels/option-b-encoder-with-shared-sense-mismatch.spice`](spicemodels/option-b-encoder-with-shared-sense-mismatch.spice):63-66), so the mismatch switches + zeroed slope knobs must stay synchronized for every run.

## Comparator handoff observation

- Noise/driver sweep at 10 mV / driver scale 2.5 produced 60 seeds per corner (`logs/noise-mismatch-10m-driver-2p5/mismatch_mc.csv`) but **`comp_pass` stayed "failed" for every seed** despite the energy staying ≈3.34 pJ/w (per-word `eword` column). The comparator never toggled under this stress, so the comparator-path fork is not yet resolved.

## Next steps
1. Mirror each ±10%/TT energy+headroom+lat tuple (including noise/clock-skew or driver permutations) into [`models/periphery-cost-model.md`](models/periphery-cost-model.md), [`STATUS.md`](STATUS.md), [`SUMMARY.md`](SUMMARY.md), and [`experiments/shared-sense-periphery.md`](experiments/shared-sense-periphery.md) so the guard story keeps jitter & energy together before migrating the deck back into `spicemodels/`.
2. When rerunning the guard sweep, regenerate `logs/mismatch-mc/mismatch_mc.csv`, `logs/mismatch-mc-tt/mismatch_mc_tt.csv`, and their `headroom_histogram.csv` companions together so the latency column, histograms, and CSV tuples stay in sync; treat that aligned dataset as the canonical ledger for periphery dominance and retiming/jitter margins before migration.
3. After each log regeneration, refresh `data/canonical_guard_ledger.csv` via `python3 tools/export_guard_ledger.py data/canonical_guard_ledger.csv`, rerun `tools/guard_data.py catalog/status/failures`, and update `data/GUARD_LEDGER_MANIFEST.md` so the Findings/STATUS/SUMMARY docs always reference the same machine-readable ledger (including histogram metadata) that AI analyses consume; run `tools/check_guard_consistency.py` afterward to confirm every log/histogram pair still exists.

## Baseline migration
- The validated shared-sense deck now lives in `spicemodels/option-b-encoder-with-shared-sense-baseline.spice` (deterministic, mismatch switches off) and is documented in `spicemodels/README.md`. Treat this file as the canonical baseline before branching into subsequent noise/driver stress runs.

## Open tabs
- FINDINGS.md: FINDINGS.md
- STATUS.md: STATUS.md
- SUMMARY.md: SUMMARY.md
- README.md: README.md
- ternary-cell-candidates.md: models/ternary-cell-candidates.md
