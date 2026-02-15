# TODO

- [x] Capture shared-sense glimpses with 8–16 slices and OR aggregation to verify the energy/headroom scaling; log any new driver/noise permutations in [`experiments/shared-sense-periphery.md`](experiments/shared-sense-periphery.md) while keeping the histograms aligned with [`models/periphery-cost-model.md`](models/periphery-cost-model.md).
- [x] Stress the sense pair with clock-skew/phase-noise stimuli and the new `sense_thresh_low/high` span to bound retiming/jitter headroom before level restoration, logging both the latency numbers and histograms.
- [x] Continue adding the noise-injected runs and uprated driver sizes to [`models/periphery-cost-model.md`](models/periphery-cost-model.md), emphasizing the energy vs. swing tradeoffs so the periphery ledger remains auditable.
- [ ] Migrate the validated encoder + shared-sense deck into [`spicemodels/`](spicemodels/) once all stress sweeps (MC + jitter) pass so the periphery ledger aligns with the `spicemodels/` experiments.
- [ ] Resolve the Comparator Handoff Failure: the StrongARM comparator still reports `comp_pass=failed` even with boosted devices. Investigate stronger drive or alternative comparator topologies.
- [ ] Flag/Fix the current include-path/config issue where NGspice still complains `can't find model 'sky130_fd_pr__pfet_01v8__ss'` even though `PDK_SPICE_DIR` is provided (Workaround: 13-parameter instantiation used).
