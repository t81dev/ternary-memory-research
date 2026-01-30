# ternary-memory-research

**Mission.** This repository investigates whether ternary-native memory cells or ternary-oriented memory interfaces can provide measurable density or energy advantages over binary SRAM plus packed ternary representations.

**Non-goals.**
- Not an accelerator implementation.
- Not a dependency of TFMBS.
- Not aiming for a production-ready memory macro.
- Not advocacy for ternary hardware.

### Motivation
Ternary execution systems already exist in software and emulation. The open question is whether **memory itself** can become ternary-native in a way that survives periphery costs, noise margins, and real energy accounting. This work assumes the broader ternary landscape supplies semantic targets, but the value of this repository comes from transparent, falsifiable experiments rather than hype.

### Core research questions
1. Can a ternary memory element reduce **energy per delivered trit** versus binary SRAM plus PT-5 encoding?
2. Does ternary storage reduce **effective memory traffic** at the system level once interfaces are accounted for?
3. Where do density or energy gains disappear once sense amps, decoding, and peripheral infrastructure are included?

### Success criteria (example thresholds)
- ≥1.3× effective density gain **after** accounting for periphery.
- ≥1.5× lower pJ/trit read compared to the binary SRAM baseline.
- Access latency no worse than the binary SRAM reference.

### Failure criteria (a record of what would falsify this work)
- The ternary middle state is unstable across PVT corners.
- Sense energy or periphery complexity overwhelms cell-level savings.
- Area/periphery overhead cancels any density improvement.

TFMBS assumes ternary values as a semantic execution substrate. This repository does not assume TFMBS exists. Any successful result here must stand on its own merits and be importable into binary, ternary, or hybrid systems without architectural coupling.

### Structure
We adopt a lightweight, question-first organization. Directories start empty to force justification: add models, docs, or experiments only when they help answer a falsifiable question.

```
ternary-memory-research/
├── README.md
├── ROADMAP.md
├── docs/
│   ├── problem-statement.md
│   ├── prior-art.md
│   ├── evaluation-metrics.md
│   └── kill-criteria.md
├── models/
│   ├── binary-sram-baseline.md
│   ├── ternary-cell-candidates.md
│   └── periphery-cost-model.md
├── spicemodels/
│   └── (empty at first)
├── experiments/
│   └── (empty at first)
└── LICENSE
```

### Next steps
1. Document the baseline questions and modeling assumptions before touching Verilog or SPICE.
2. Keep experiments descriptive and falsifiable; add physical models only once a candidate survives the kill criteria.
3. Kill ideas early when they fail to beat the failure criteria above.
