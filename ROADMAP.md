# Roadmap

## Phase 1 – Questions and baselines
- Define native ternary memory, interface boundaries, and evaluation metrics in documentation.
- Codify binary SRAM baseline and periphery reference in `models/`.
- Establish kill criteria that stop work when energy, stability, or area goals cannot be met.

## Phase 2 – Candidate screening
- Populate `models/ternary-cell-candidates.md` with the smallest set of cell families worth modeling.
- Decide whether ternary-isolated or ternary-over-binary interfaces produce measurable gains.
- Document tools and data sources needed for future SPICE/explorations.

-## Phase 3 – Experimentation (conditional)
- Move surviving models into `spicemodels/` and concrete experiments (shared sense, periphery, encoder energy vs activity).  
- Track results under `experiments/` plus the periphery ledger so kill criteria and intermediary failures remain auditable; the new TT/±10% shared-sense sweeps (with headroom/noise logging) live there now.  
- Publish updated conclusions in `README.md`, `SUMMARY.md`, and the docs folder once a verdict emerges.

ternary-memory-research/
├── README.md
├── ROADMAP.md
├── docs/
│ ├── problem-statement.md
│ ├── prior-art.md
│ ├── evaluation-metrics.md
│ ├── kill-criteria.md
│ └── assumptions.md
├── models/
│ ├── binary-sram-baseline.md
│ ├── ternary-cell-candidates.md
│ └── periphery-cost-model.md
├── spicemodels/
│ └── (empty at first)
├── experiments/
│ └── (empty at first)
└── LICENSE


## Next steps

1. Keep the periphery ledger (`models/periphery-cost-model.md` + `experiments/shared-sense-periphery.md`) current with each sweep so the “periphery dominance” story stays traceable.
2. Ship new TT/mismatch sweeps only after the corner parameters align or after confirming that reuse of SS decks with `process_switch=1` is acceptable.
3. Summarize each phase’s outcome in `SUMMARY.md` and cross-link to the `STATUS.md` backlog so every reader can see what’s blocked, what’s passing, and what still needs validation before crossing off the kill criteria.
4. Validate shared sense retiming/jitter margins by logging the low-threshold `td_*`/`settle_*` measurements (with the new `sense_thresh_low/high` knobs) and record their headroom snapshots alongside the energy table; append those numbers to `models/periphery-cost-model.md` so the roadmap explicitly documents the periphery’s timing safety window.
5. Inject a small noise source (~5–10 mV) across `sharedsensep/sharedsensen`, stress the `sense_headroom_*` monitors, and, if needed, uptune the final driver while logging the additional energy vs. swing data so the ledger captures both the low-swing feature and any driver-size trade-offs.
6. Record the `sense_thresh` settling/jitter entries (time from `sense_thresh_low` to `sense_thresh_high`) and any clock-skew/phase-noise stimulus in both this roadmap and `README.md` so the latency story parallels the energy story before migrating to `spicemodels/`.
7. ✅ Run 50-sample Monte Carlo sweeps per corner (0.9 V/1.0 V/1.1 V) with the slope knobs pinned, log the `Edyn`, `Eword_est`, and driver-based `sense_headroom_{min,max}` histograms, and record the tuples in `models/periphery-cost-model.md`, `STATUS.md`, and `SUMMARY.md` (see `logs/mismatch-mc/mismatch_mc.csv`, `logs/mismatch-mc-tt/mismatch_mc_tt.csv`, and the upsized `logs/mismatch-mc-upsized/mismatch_mc.csv`). The headroom histogram still peaks at only ≈±0.3 mV (≈±0.416 mV once the driver is 3u/6u) despite the noise injection—TT occasionally hits ≈24.6 mV—so the 20 mV guard remains the next decision point before declaring the periphery dominance kill criterion resolved.
