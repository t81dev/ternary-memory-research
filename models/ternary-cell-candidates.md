# Ternary cell candidates

This file tracks the small set of ternary cell ideas considered worth bounding. Every entry states the topology outline, forecasted benefits, explicit risks, and the kill criteria most likely to terminate it.

Forecasted values are first-order bounds. Logged or measured values supersede forecasts and are authoritative for kill decisions.

| # | Candidate | Status | Core kill trigger(s) | Intrinsic density gain? | Periphery overhead | Verdict |
|---|-----------|--------|----------------------|--------------------------|--------------------|---------|
| 1 | Voltage-tiered multi-transistor SRAM | Expected fail (boundary reference) | Middle-state instability / periphery dominance / interface dependency | ~1.5× | High (analog sense amp + offset calibration) | Reference failure |
| 2 | Resistive multi-level cell (MRAM/PCM) | Dead | Drift calibration + DAC energy | ~1.5–2× | Very high (DAC/comparator array) | Rejected |
| 3 | Floating-gate charge-trap | Dead | Leakage refresh + ADC periphery | ~1.3–1.5× | Extreme (charge pump + ADC) | Rejected |
| 4 | Hybrid binary array w/ ternary interface (Option B) | Surviving (conditional; interface-level) | Periphery dominance / interface dependency | None at cell; system ~20% traffic reduction | ~0.38 pJ/word extra | Conditional survivor |
| 5 | CNTFET multi-threshold ternary buffer/cycle operator | Deferred (reference) | Device dependency + interface/headroom | ~1.4–1.5× | Medium (if local shared sense) | Literature optimistic (30–98% lower energy vs. binary/prior ternary, unstable under PVT) |
| 6 | Standard ternary inverter 8T SRAM | Deferred (marginal) | Middle-state instability / periphery dominance | ~1.0× (pending) | High (low-swing sense amp) | Deferred reference (CNTFET variants show SNM gains; CMOS middle state remains leakage/variation vulnerable) |
| 7 | Hybrid memristor-transistor ternary cell | Deferred (emerging/non-volatile) | Calibration + endurance + interface dependency | ~1.2–1.6× | High (DAC/calibration) | Deferred reference |
| 8 | CNT-SGT ternary SRAM | Deferred (reference) | Device dependency + headroom | ~1.3× (speculative) | High (differential read losses) | Reference comparison |

*CNTFET/GNRFET entries (5–8) are literature references only; no Sky130/PDK support is assumed.*
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
- **Validations needed (periphery ledger / shared-sense logs):**
  1. **Headroom guard:** Mismatch/Monte Carlo sweeps now pin `sense_headroom_min/max` near 0.8995–0.9005 V at ±10% and ≈0.998 V at TT, so the 20 mV guard is satisfied; the aggregated histogram is saved in `logs/mismatch-mc/headroom_histogram.csv` (TT histogram in `logs/mismatch-mc-tt/headroom_histogram.csv`) and referenced in `experiments/shared-sense-periphery.md` and `models/periphery-cost-model.md`.
 2. **Latency/jitter probes:** `td_*`/`settle_*` instrumentation must succeed once the driver headroom is close to the 20 mV guard before committing to final encoder latency numbers; in the meantime capture `sense_thresh_low/high` delays and write the `sense_thresh_latency` entries into the mismatch CSVs alongside the headroom histograms (`logs/mismatch-mc/headroom_histogram.csv`, etc.) so every tuple documents both energy and jitter.
  3. **API neutrality:** Ensure the ternary tokens expose a substrate-neutral interface (no TFMBS-only scheduling or bias tweaks) before claiming the hybrid interface satisfies the periphery dominance/interface dependency kill criteria.
  4. **Driver permutations:** Log any driver sizing/noise variations (upsized decks, level-restorers) and register the tuples + headroom histograms in `models/periphery-cost-model.md`, `STATUS.md`, and `SUMMARY.md` so the ledger stays complete.
  5. **Noise/variation realism:** If sense-pair input offset (σ ≈5–8 mV typical in low-power sense amps) collapses headroom further in MC runs, either deploy weak local regeneration on the shared nodes or accept a relaxed headroom guard (e.g., <1% failure at 5 mV differential) with a documented BER/yield tradeoff.

## 5. CNTFET-based cycle-operator or buffer ternary SRAM (8T–10T class)

**Status:** Deferred (non-CMOS baseline; optimistic reference)

- **Concept:** Use multi-threshold CNTFETs with cycle-operator or buffer structures to hold ternary states; combinations aim to rotate or latch −1/0/+1 robustly.
- **Forecasted numbers:** ~30–50% lower read/write energy vs. binary in CNTFET sims; area ≈1.2–1.5× binary; favourable noise margins if Vth tuning holds.
- **Kill criteria triggers:**  
  1. **Device dependency** – Requires CNTFET/GNRFET tooling, so the reference fails portability tests.  
  2. **Middle state instability** – Variation in multi-Vt stack can still collapse the middle hold unless biasing is near perfect.  
 3. **Periphery dominance** – Shared sense or offset calibration reintroduces the same headroom guard workload as Option B.

## 6. Standard ternary inverter 8T SRAM (PTI/NTI cross-coupled)

**Status:** Deferred (marginal)

- **Concept:** Pair ternary inverters with access transistors; the middle state is held via ratioed transconductance or subthreshold bias.
- **Forecasted numbers:** ~8–10T per cell; energy ~0.4–0.7× binary per trit; still requires aggressive refresh or assist for the middle state.
- **Kill criteria triggers:**  
  1. **Middle state instability** – Leakage and variation still demand refresh or assist, undoing energy gains.  
  2. **Periphery dominance** – Differential read still needs low-swing sense amps with calibration risk, so headroom and Monte Carlo guard issues persist.

## 7. Hybrid memristor-transistor ternary cell (ReRAM/PCM pivot)

**Status:** Deferred (emerging / non-volatile angle)

- **Concept:** Combine memristor multi-level elements with transistor access for ternary states; target high density at the cost of write energy and calibration logic.
- **Forecasted numbers:** Area ~40–60 F²/trit; read energy extremely low; write energy high; drift/biasing requires periodic recalibration.
- **Kill criteria triggers:**  
  1. **Calibration / interface dependency** – Active recalibration ties into host-level handshake semantics, so interface dependency kill remains.  
  2. **Endurance / periphery dominance** – DAC/comparator arrays plus calibration logic reintroduce high periphery cost similar to the resistive candidate.

---
## 8. CNT-SGT ternary SRAM

**Status:** Deferred (reference)

- **Concept:** Cross-coupled source-gated transistors hold ternary values (−1/0/+1) with SNM ≈0.37 V in recent 2024–2025 CNT publications; simplifies fabrication compared to multi-threshold CNTFET stacks.
- **Forecasted numbers:** ~6T-style cell with high SNM and speculated 1.3× density gain, assuming the differential read periphery scales.
- **Kill criteria triggers:**  
  1. **Device dependency** – Still tied to CNT/CNTFET tooling; no Sky130 process support.  
  2. **Headroom/periphery** – Differential read likely hits the shared-sense headroom guard again, so this entry remains a periphery reference.

---

## Summary

Cell-level ternary stores remain falsified across CMOS-compatible approaches because middle-state instability, calibration overhead, and periphery dominance consistently trip the kill criteria.

The hybrid binary array with a ternary interface (Option B) survives narrowly as an encoding optimization; the decisive path is to prove shared-sense robustness (headroom, latency/jitter, API neutrality) plus documented driver/log permutations before claiming ternary semantics without changing the cell fabric.
