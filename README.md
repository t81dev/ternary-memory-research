# ternary-memory-research

**Mission.**  
This repository investigates whether ternary-native memory cells or ternary-oriented memory interfaces can provide measurable density or energy advantages over conventional binary SRAM paired with packed ternary representations.

The goal is not to promote ternary hardware, but to determine—under explicit constraints—whether any form of native ternary memory survives realistic periphery, noise, and energy accounting.

## Non-goals

- Not an accelerator implementation.
- Not a dependency of TFMBS or any ternary execution framework.
- Not a production-ready memory macro.
- Not advocacy for ternary hardware.

## Motivation

Ternary execution systems already exist in software and emulation. The open question addressed here is whether **memory itself** can become ternary-native in a way that survives periphery costs, noise margins, and full-system energy accounting.

This repository assumes that semantic consumers of ternary values may exist elsewhere, but it does **not** assume their presence. Any successful result must stand on its own and remain importable into binary, ternary, or hybrid systems without architectural coupling.

The value of this work comes from transparent, falsifiable modeling rather than optimistic claims.

## Core research questions

1. Can a ternary memory element reduce **energy per delivered trit** relative to binary SRAM plus PT-5 encoding?
2. Does ternary storage reduce **effective memory traffic or density cost** once interfaces and periphery are fully accounted for?
3. Where do apparent density or energy gains collapse when sense amplifiers, decoding, and timing infrastructure are included?

## Screening thresholds (non-binding)

These example thresholds are used to rapidly filter candidates, not to guarantee acceptance:

- ≥1.3× effective density improvement **after** periphery amortization.
- ≥1.5× lower pJ/trit read energy compared to the binary SRAM baseline.
- Worst-case access latency no worse than the binary SRAM reference.

Failure to meet these thresholds does not imply ternary memory is impossible, only that the candidate under evaluation does not justify further work.

## Failure conditions

The following conditions falsify a candidate and are formalized in `docs/kill-criteria.md`:

- The ternary middle state is unstable across PVT corners.
- Sense energy or periphery complexity overwhelms any cell-level savings.
- Area or interface overhead cancels density or energy advantages.

Candidates that trigger these conditions are intentionally terminated early.

## Repository structure

This repository follows a question-first organization. Directories are intentionally empty until justified by surviving models or measurements.

