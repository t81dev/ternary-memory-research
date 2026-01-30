# Kill Criteria

## Purpose

This document defines **explicit termination conditions** for ternary memory research conducted in this repository.

A candidate design that triggers any kill criterion is considered **non-viable** and should not receive further modeling, simulation, or implementation effort unless a *new mechanism* is introduced that directly addresses the failure.

This document exists to prevent:

* confirmation bias,
* sunk-cost continuation,
* and “cell-only wins” that fail at the system level.

---

## Global Kill Rule

> **Any ternary memory design that does not outperform the binary SRAM + PT-5 baseline on at least one primary metric *without losing on the others* is rejected.**

Primary metrics are defined in `docs/evaluation-metrics.md`.

---

## K1 — Energy Non-Competitiveness

**Condition:**
Energy per delivered trit ≥ baseline energy per delivered trit (binary SRAM + PT-5), after all sensing, decoding, and interface costs are included.

**Rationale:**
If ternary memory does not reduce energy, its added complexity is unjustified.

**Notes:**

* Cell-only energy savings do not count.
* Sense amplifiers, reference ladders, and analog biasing are always included.

**Result:**
Terminate candidate.

---

## K2 — Density Collapse After Periphery

**Condition:**
Effective trits/mm² ≤ baseline effective trits/mm² after amortizing:

* sense amps,
* reference generators,
* decoders,
* routing overhead.

**Rationale:**
Density gains that disappear at the macro level are illusory.

**Notes:**

* Peripheral area must be counted even if “shared.”
* Layout realism overrides schematic optimism.

**Result:**
Terminate candidate.

---

## K3 — Unacceptable Access Latency

**Condition:**
Read or write latency > 1.5× baseline SRAM latency **without a compensating energy or density win ≥ 2×**.

**Rationale:**
Inference accelerators are latency-sensitive; moderate penalties may be tolerated only with strong gains elsewhere.

**Notes:**

* Multi-cycle sensing counts as latency unless fully hidden.
* “Could be pipelined” is not an argument without proof.

**Result:**
Terminate candidate.

---

## K4 — Middle-State Instability

**Condition:**
The ternary middle state cannot be reliably distinguished from ±1 across:

* voltage corners,
* temperature corners,
* process variation (Monte Carlo),

without excessive margin tightening or calibration.

**Indicators include:**

* collapsing noise margin,
* read disturb,
* high soft-error probability,
* sensitivity to device mismatch.

**Rationale:**
A ternary memory without a robust middle state is functionally binary with extra failure modes.

**Result:**
Immediate termination.

---

## K5 — Excessive Periphery Complexity

**Condition:**
Periphery transistor count or routing complexity exceeds that of the baseline by >2× **without a proportional system-level win**.

**Rationale:**
Memory arrays scale; periphery does not. Complexity here kills real designs.

**Notes:**

* Comparator count, reference ladders, and bias circuits are included.
* Digital glue logic is not “free.”

**Result:**
Terminate candidate.

---

## K6 — Calibration Dependence

**Condition:**
Correct operation requires:

* per-chip calibration,
* per-bank tuning,
* temperature-tracked reference adjustment,

beyond what is standard for SRAM macros.

**Rationale:**
Inference accelerators must be deterministic and low-maintenance.

**Result:**
Terminate candidate or reclassify as *experimental-only*.

---

## K7 — Baseline Evasion

**Condition:**
The candidate’s evaluation relies on:

* weakening the binary SRAM baseline,
* excluding PT-5 decode costs,
* excluding zero-detect logic,
* or redefining metrics post hoc.

**Rationale:**
A result that only wins by changing the rules is invalid.

**Result:**
Invalidate comparison.

---

## Acceptable Partial Outcomes

The following outcomes are explicitly acceptable and **do not constitute failure**:

* Demonstrating that **binary SRAM + ternary-native interfaces** outperform true ternary cells.
* Showing that ternary cells are viable only in **non-volatile or near-memory** contexts.
* Concluding that ternary memory is unsuitable for high-performance SRAM but viable for **cold weight storage**.

Negative results are first-class outputs of this repository.

---

## Termination Protocol

When a candidate is killed:

1. Document the failure mode clearly.
2. Record which kill criterion was triggered.
3. Do not refactor the candidate to “almost pass.”
4. Move on.

A killed idea is considered **resolved**, not abandoned.

---

## Status

**Status:** Normative
**Applies to:** All candidate memory cells and interfaces
**Change policy:** Kill criteria may only be tightened, never weakened

---
