# TODO

1. Round up the ±10% mismatch sweeps with the new `ttime(...)` measurement that quantifies how long the `sharedDriveDiff` guard takes to settle into the 0.898–0.900 V window; once the latency column is populated in `logs/mismatch-mc/mismatch_mc.csv` and `logs/mismatch-mc-tt/mismatch_mc_tt.csv`, copy the tuples into `models/periphery-cost-model.md`, `STATUS.md`, and `SUMMARY.md` so the guard story links energy, headroom, and jitter before the deck graduates.
2. Capture shared-sense glimpses with 8–16 slices and OR aggregation to verify the energy/headroom scaling; log any new driver/noise permutations in `experiments/shared-sense-periphery.md` while keeping the histograms aligned with `models/periphery-cost-model.md`.
3. Stress the sense pair with clock-skew/phase-noise stimuli and the new `sense_thresh_low/high` span to bound retiming/jitter headroom before level restoration, logging both the latency numbers and histograms.
4. Continue adding the noise-injected runs and uprated driver sizes to `models/periphery-cost-model.md`, emphasizing the energy vs. swing tradeoffs so the periphery ledger remains auditable.
5. Migrate the validated encoder + shared-sense deck into `spicemodels/` once all stress sweeps (MC + jitter) pass so the periphery ledger aligns with the `spicemodels/` experiments.
