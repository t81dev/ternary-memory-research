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
