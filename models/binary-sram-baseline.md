# Binary SRAM + PT-5 Baseline

## Purpose

This document defines the **baseline memory system** against which all ternary memory candidates in this repository are evaluated.

The baseline represents a *competent, modern implementation* of ternary storage using:

* conventional binary SRAM cells,
* PT-5 packed ternary encoding (5 trits / byte),
* decode and zero-detect logic placed outside the memory array.

Any ternary-native memory proposal must outperform this baseline **after all peripheral and system costs are included**.

---

## Baseline Assumptions

### Memory Cell

* **Cell type:** Standard 6T binary SRAM
* **Process node:** Assumed modern planar or FinFET (node-agnostic; normalized comparisons only)
* **Stored unit:** 8-bit byte

### Ternary Representation

* **Encoding:** PT-5 (5 trits per byte)
* **Unused codes:** 13/256 (unused for simplicity and decode robustness)
* **Effective utilization:** ≈94.5% of byte space

---

## Memory Organization

* Memory arrays store **PT-5 encoded bytes**, not raw trits.
* Trit extraction occurs in **logic periphery**, not inside the SRAM array.
* SRAM read granularity remains byte-aligned.

This reflects current best practice and avoids exotic memory macros.

---

## Read Path Energy Model

### Components Included

Energy per delivered trit includes:

1. **SRAM bitcell read energy** (byte-level)
2. **Sense amplifier energy**
3. **PT-5 decode logic**
4. **Zero-detect logic**
5. **Register / latch overhead to present trits to consumers**

### Normalization Rule

Energy is amortized as:

[
E_{\text{per trit}} =
\frac{E_{\text{SRAM read (byte)}}
+ E_{\text{sense}}
+ E_{\text{decode}}}
{5}
]

Zero-detect energy is included even if the trit is zero, as this logic must toggle to determine that fact.

---

## Density Model

### Cell Density

* Binary SRAM density is treated as the reference unit.
* No density gain is assumed at the cell level.

### Effective Trit Density

[
\text{Effective trits/mm}^2 =
\frac{5 \times \text{bytes stored}}
{\text{total area (cells + periphery)}}
]

Peripheral logic area (decode, zero-detect) is **explicitly included**.

This avoids overstating density by counting only raw cell area.

---

## Access Latency

### Assumptions

* SRAM access latency is unchanged from baseline binary SRAM.
* PT-5 decode and zero-detect occur **off critical path** where possible.

### Accounting

* If decode latency enters the critical path, it is counted.
* Multi-cycle decode is allowed but penalized in latency comparisons.

This reflects realistic accelerator integration constraints.

---

## Stability

* Binary SRAM is assumed to have **near-zero read instability** across PVT.
* No multi-level sensing is required.
* No mid-level collapse is possible.

This makes the baseline extremely robust and sets a high bar for ternary cells.

---

## Periphery Complexity

### Included

* PT-5 decode logic
* Zero-detect comparators
* Routing to lane interfaces

### Excluded

* Compute-side logic (lanes, accumulators)
* Scheduler or orchestration logic

Only memory-facing costs are counted.

---

## Why This Is a Strong Baseline

This baseline already captures:

* high ternary density (via PT-5),
* simple, robust SRAM cells,
* predictable timing,
* compatibility with existing flows.

Any ternary-native memory design must therefore demonstrate **clear wins** in:

* energy per delivered trit,
* effective density after periphery,
* or semantic utility (e.g., earlier zero suppression).

If a candidate does not beat this baseline, the correct conclusion is that **binary SRAM + smart encoding remains optimal**.

---

## Relationship to TFMBS

TFMBS currently assumes this baseline behavior when modeling:

* PT-5 residency,
* decode cost,
* zero-skip gating.

This document exists independently of TFMBS and may be used by any architecture evaluating ternary storage.

---

## Status

**Status:** Normative baseline
**Change policy:** Changes require explicit justification and must not weaken the baseline

If you want, I can draft **`docs/kill-criteria.md` next**, or help you choose **one** ternary cell family worth modeling first (and several that should be explicitly excluded).
