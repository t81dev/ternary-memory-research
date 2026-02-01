# Roadmap

## Phase 1 – Questions and baselines
- Define native ternary memory, interface boundaries, and evaluation metrics in documentation.
- Codify binary SRAM baseline and periphery reference in `models/`.
- Establish kill criteria that stop work when energy, stability, or area goals cannot be met.

## Phase 2 – Candidate screening
- Populate `models/ternary-cell-candidates.md` with the smallest set of cell families worth modeling.
- Decide whether ternary-isolated or ternary-over-binary interfaces produce measurable gains.
- Document tools and data sources needed for future SPICE/explorations.

## Phase 3 – Experimentation (conditional)
- Move surviving models into `spicemodels/` and concrete experiments.
- Track results under `experiments/` to show when the repository’s own failure criteria are met.
- Publish updated conclusions in `README.md` and the docs folder once a verdict emerges.

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

1. Establish and review baselines, assumptions, and cost models before introducing physical simulation.
2. Advance only candidates that survive explicit kill criteria into SPICE or experimental modeling.
3. Preserve negative results and terminate ideas early when they fail to beat the defined baseline.
