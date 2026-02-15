# Roadmap

## Phase 1 – Questions and baselines
- Define native ternary memory, interface boundaries, and evaluation metrics in documentation.
- Codify binary SRAM baseline and periphery reference in `models/`.
- Establish kill criteria that stop work when energy, stability, or area goals cannot be met.

## Phase 2 – Candidate screening
- Populate `models/ternary-cell-candidates.md` with the smallest set of cell families worth modeling.
- Decide whether ternary-isolated or ternary-over-binary interfaces produce measurable gains.
- Document tools and data sources needed for future SPICE/explorations.

## Phase 3 – Experimentation (Active)
- [x] Move surviving models into `spicemodels/` and concrete experiments (shared sense, periphery, encoder energy vs activity).
- [x] Track results under `experiments/` plus the periphery ledger so kill criteria and intermediary failures remain auditable.
- [x] Log noise, mismatch, and phase-skew sweeps in the canonical guard ledger (`data/canonical_guard_ledger.csv`).
- [ ] Finalize comparator topology (resolve handoff failure) and migrate validated deck to `spicemodels/`.
- [ ] Publish updated conclusions in `README.md`, `SUMMARY.md`, and the docs folder once a verdict emerges.

## Directory Structure
```
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
│ └── (option-b-encoder-with-shared-sense-baseline.spice)
├── experiments/
│ └── (shared-sense-periphery.md)
└── LICENSE
```

## Next steps

1. **Maintain Periphery Ledger:** Keep `models/periphery-cost-model.md` and `experiments/shared-sense-periphery.md` current with each sweep.
2. **Resolve Comparator:** Address the `comp_pass=failed` status by investigating stronger drivers or alternative comparator topologies.
3. **Consolidate Documentation:** Ensure `STATUS.md` and `SUMMARY.md` remain synchronized with the canonical ledger.
4. **Complete Migration:** Once the comparator is stable and all stress sweeps (MC + jitter) pass, migrate the final deck to `spicemodels/`.
5. ✅ **Baseline Validation:** 50-sample Monte Carlo sweeps per corner (0.9 V/1.0 V/1.1 V) completed; headroom histogram peaks in the 895–900 mV bin.
6. ✅ **Noise Stress:** 5mV/10mV noise injections completed and logged.
7. ✅ **Phase Skew:** ±0.5 ns phase skew sweeps completed and logged.
