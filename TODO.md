# TODO

1. Capture shared-sense glimpses with 8–16 slices and OR aggregation to verify the energy/headroom scaling; log any new driver/noise permutations in `experiments/shared-sense-periphery.md` while keeping the histograms aligned with `models/periphery-cost-model.md`.
2. Stress the sense pair with clock-skew/phase-noise stimuli and the new `sense_thresh_low/high` span to bound retiming/jitter headroom before level restoration, logging both the latency numbers and histograms.
3. Continue adding the noise-injected runs and uprated driver sizes to `models/periphery-cost-model.md`, emphasizing the energy vs. swing tradeoffs so the periphery ledger remains auditable.
4. Migrate the validated encoder + shared-sense deck into `spicemodels/` once all stress sweeps (MC + jitter) pass so the periphery ledger aligns with the `spicemodels/` experiments.
5. Resolve the StrongARM comparator build: ensure the strongarm latch uses the SS corner devices (no PM3 substitutions) or predefines the parameters (`l`, `w`, `mult`) before the SkyWater models load, then re-run the 10 mV/4.5× sweep so the comparator pass rate/Energy/guard histogram can be logged.
