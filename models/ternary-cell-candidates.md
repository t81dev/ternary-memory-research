# Ternary cell candidates

This file tracks the small set of ternary cell ideas considered worth bounding. Every entry states the topology outline, forecasted benefits, explicit risks, and the kill criteria most likely to terminate it.

Forecasted values are first-order bounds. Logged or measured values supersede forecasts and are authoritative for kill decisions.

## 1. Voltage-tiered multi-transistor SRAM cell

**Status:** Expected to fail (boundary reference)

- **Concept:** Extend a 6T SRAM cell with two steering transistors that hold the storage node at one of three write voltages (0.25 V, 0.5 V, 0.75 V). A differential sense amp with programmable offset separates those tiers during readback.

- **Forecasted numbers:**
  - Raw cell area: 90–110 F² → ~0.47–0.58 µm² per trit if tiled similarly to the binary baseline.
  - Write energy: ~18–22 fJ/trit; steering transistors conduct only during writes.
  - Read energy at the cell: ~25–28 fJ/trit plus ≈0.25 pJ/bitline pair sense energy (dominant cost).
  - Voltage margin: tuned to ~90 mV with body bias; collapses below 60 mV under ±10% supply variation, requiring bias trimming.

- **Kill criteria triggers:**
  1. **Middle state instability** – Margin collapse under 0.9–1.1 V forces adaptive bias trimming (~0.6 pJ/word), which must be included before any advancement.
  2. **Periphery dominance** – ≈85 transistors per sense amp pair plus analog offset calibration push energy beyond the baseline unless sense energy drops below ~0.2 pJ/pair.
  3. **Interface dependency** – Requires controller-visible ternary voltage control; API must be explicit to avoid substrate coupling.

This candidate is retained as a reference failure mode illustrating periphery- and margin-driven collapse.

---

## 2. Resistive multi-level cell (MRAM / PCM)

**Status:** Dead (confirmed)

- **Concept:** Use resistive elements with three resistance states (low/medium/high) read via a current-DAC sense amp that outputs ternary values directly.

- **Forecasted numbers:**
  - Effective cell area: ~40–60 F² per trit.
  - Sense energy: ~0.15–0.18 pJ/trit (6-bit DAC biasing and comparators); write energy ~40 fJ/trit.
  - Resistance window: ~35% spacing with ~1.2× read margin.
  - Aging requires recalibration every ~10⁶ cycles to keep overlap <5%.

- **Kill criteria triggers:**
  1. **Middle state instability** – Drift forces periodic recalibration (~0.5 pJ/word), erasing energy and density gains.
  2. **Periphery dominance** – Current-DAC and comparator array (~140 transistors) push periphery energy beyond viable limits.
  3. **Interface dependency** – Requires retry/backoff semantics incompatible with fixed-latency memory expectations.

This candidate fails due to unavoidable calibration and DAC overhead.

---

## 3. Floating-gate charge-trap cell with rotational sense

**Status:** Dead (immediate)

- **Concept:** Store −1/0/+1 as discrete charge packets on a floating gate. Reads use a capacitive charge pump and threshold comparisons; writes use analog pulses.

- **Forecasted numbers:**
  - Area: ~65 F² per trit, with ~12% pad/routing overhead.
  - Sense energy: ~0.30–0.32 pJ/trit (charge pump + ADC-based margining).
  - Write energy: ~0.45–0.5 pJ/trit.
  - Voltage margin: ~140 mV, but leakage requires refresh every ~10³ writes (~0.2 pJ/word).

- **Kill criteria triggers:**
  1. **Middle state instability** – Leakage-driven refresh negates density and energy benefits.
  2. **Periphery dominance** – ADC, charge pump, and calibration logic exceed any viable periphery budget.
  3. **Interface dependency** – Requires chip-specific calibration sequences, breaking semantic portability.

This candidate is rejected without escalation to physical modeling.

---

## 4. Hybrid binary array with ternary interface (Option B)

**Status:** Surviving (conditional; interface-level only)

- **Concept:** Retain binary storage cells but expose ternary semantics at the interface by combining fixed binary windows into ternary tokens. Storage remains binary; semantics are delivered at the boundary.

- **Forecasted / logged numbers:**
  - No additional cell area; costs are confined to column encoders and minor sense adjustments.
  - Encoder logic: ~96 transistors per 3-bit slice after LUT pruning (down from ≈120).
  - Encoder energy: ≈0.28 pJ/word (logged), plus ≈0.1 pJ/word for buffering and timing.
  - Total added periphery: ≈0.38 pJ/word.
  - Effective trits/mm² unchanged at the array level; potential ~20% system-level traffic reduction if ternary tokens are consumed directly.

- **Kill criteria triggers:**
  1. **Interface dependency** – API must be explicit and substrate-neutral; reliance on TFMBS-specific scheduling violates the criterion.
  2. **Periphery dominance** – Encoder energy must remain below the ≈1.5 pJ/word PT-5 decoder cost; regression invalidates the path.

This candidate does not provide intrinsic density gains and survives only as an interface-level optimization pending strict latency, jitter, and API validation.

---

## Summary

All evaluated **cell-level** ternary storage candidates currently fail due to periphery energy, calibration overhead, or middle-state instability.

The hybrid binary array with a ternary interface (Option B) remains the only candidate not yet falsified, and only under narrow, conditional constraints. Advancement beyond modeling requires surviving full periphery, latency, and interface validation without relaxing the established kill criteria.
