# TODO

1. Complete mismatch/mc campaign for shared-sense deck once TT/BSIM parameters settle; log energy, headroom histograms, and Monte Carlo variations in `models/periphery-cost-model.md` + `STATUS.md`.
2. Run shared-sense glimpses with 8–16 slices and record OR aggregation energy/headroom impacts in `experiments/shared-sense-periphery.md`.
3. Capture clock-skew/phase-noise stimuli using `sense_thresh_low/high` probes to quantify retiming/jitter until downstream level restoration is needed.
4. Add the shared-sense noise-injected runs and any uprated driver sizes to `models/periphery-cost-model.md` highlighting energy vs. swing tradeoffs.
5. Migrate the validated encoder + shared-sense deck into `spicemodels/` once all stress sweeps pass so the periphery ledger aligns with the `spicemodels/` experiments.
