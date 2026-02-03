# TODO

1. Capture shared-sense glimpses with 8–16 slices and OR aggregation to verify the energy/headroom scaling; log any new driver/noise permutations in `experiments/shared-sense-periphery.md` while keeping the histograms aligned with `models/periphery-cost-model.md`.
2. Stress the sense pair with clock-skew/phase-noise stimuli and the new `sense_thresh_low/high` span to bound retiming/jitter headroom before level restoration, logging both the latency numbers and histograms.
3. Continue adding the noise-injected runs and uprated driver sizes to `models/periphery-cost-model.md`, emphasizing the energy vs. swing tradeoffs so the periphery ledger remains auditable.
4. Migrate the validated encoder + shared-sense deck into `spicemodels/` once all stress sweeps (MC + jitter) pass so the periphery ledger aligns with the `spicemodels/` experiments.
