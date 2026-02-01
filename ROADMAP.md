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
- Track results under `experiments/` plus the periphery ledger so kill criteria and intermediary failures remain auditable.  
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
