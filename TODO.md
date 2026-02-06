# TODO

-1. Capture shared-sense glimpses with 8–16 slices and OR aggregation to verify the energy/headroom scaling; log any new driver/noise permutations in [`experiments/shared-sense-periphery.md`](experiments/shared-sense-periphery.md) while keeping the histograms aligned with [`models/periphery-cost-model.md`](models/periphery-cost-model.md).
2. Stress the sense pair with clock-skew/phase-noise stimuli and the new `sense_thresh_low/high` span to bound retiming/jitter headroom before level restoration, logging both the latency numbers and histograms.
-3. Continue adding the noise-injected runs and uprated driver sizes to [`models/periphery-cost-model.md`](models/periphery-cost-model.md), emphasizing the energy vs. swing tradeoffs so the periphery ledger remains auditable.
-4. Migrate the validated encoder + shared-sense deck into [`spicemodels/`](spicemodels/) once all stress sweeps (MC + jitter) pass so the periphery ledger aligns with the `spicemodels/` experiments.
5. Resolve the StrongARM comparator build: ensure the strongarm latch uses the SS corner devices (no PM3 substitutions) or predefines the parameters (`l`, `w`, `mult`) before the SkyWater models load, then re-run the 10 mV/4.5× sweep so the comparator pass rate/Energy/guard histogram can be logged.
6. Flag the current include-path/config issue where NGspice still complains `can't find model 'sky130_fd_pr__pfet_01v8__ss'` even though `PDK_SPICE_DIR` is provided; document the interim workaround before rerunning `tools/run_noise_mismatch_driver_sweep.sh` so the delta sweep can complete.
