# Ternary cell candidates

This file tracks the small set of ternary cell ideas worth modeling. Every entry states the topology outline, the expected benefits, and which kill criteria it risks.

## 1. Voltage-tiered multi-transistor SRAM cell
- Concept: Extend a 6T SRAM cell with two steering transistors that hold the storage node at one of three write voltages (0.25 V, 0.5 V, 0.75 V). A differential sense amp with programmable offset separates those tiers during readback.
- Forecasted numbers:
  - Raw cell area: 90–110 F² → ~0.47–0.58 µm² per trit if the array is tiled similarly to the binary baseline.
  - Write energy: ~18–22 fJ/trit; steering transistors are gated to conduct only during writes.
  - Read energy at the cell: ~25–28 fJ/trit plus the sense amp’s 0.25 pJ/bitline pair (periphery model, most of the cost).
  - Voltage margin between states: tuned to ~90 mV with body bias; the margin collapses below 60 mV under ±10% supply variation, triggering bias trimming.
- Kill criteria triggers:
 1. **Middle state instability** – Under 0.9–1.1 V, the middle state margin drops below the calibration window. Adaptive bias trimming adds ~0.6 pJ/word and must be tracked before advancing.
 2. **Periphery cost dominates** – 85 transistors per sense amp pair plus analog offset calibration raise energy; the sense amp energy must drop below ~0.2 pJ/pair to beat the baseline.
 3. **Interface ambiguity** – Requires controller commands for ternary voltages; document the API to avoid depending on TFMBS.

## 2. Resistive multi-level cell (MRAM/PCM)
- Concept: Use resistive elements with three well-separated resistance states (low/medium/high) and read them via a current-DAC sense amp that outputs ternary voltages without additional encoding.
- Forecasted numbers:
  - Effective cell area: 40–60 F² per trit; the multi-level resistance levels live inside one physical device.
  - Sense energy: ~0.15–0.18 pJ/trit (includes 6-bit DAC biasing and comparators with 35% resistance spacing); write energy ~40 fJ/trit for state-setting pulses.
  - Resistance window: ~35% spacing with ~1.2× read margin. Aging shifts require recalibration every 10⁶ cycles to keep overlap below 5%.
- Kill criteria triggers:
 1. **Middle state instability** – Unless per-chunk recalibration (≈0.5 pJ/word) keeps the medium state separated after 10⁶ cycles, overlap will force a kill.
 2. **Periphery cost dominates** – CurrentDAC + comparator array (~140 transistors) consume another ~0.2 pJ per sense amp, pushing energy toward the failure drive.
 3. **Interface ambiguity** – Must provide explicit retry/backoff semantics for controllers expecting fixed timing; failing to do so violates the criterion.

## 3. Floating-gate charge-trap cell with rotational sense
- Concept: Store −1/0/+1 as discrete charge packets on a floating gate. A capacitive charge pump samples the node against two thresholds; writes use analog pulses whose amplitude encodes the tier.
- Forecasted numbers:
  - Area: ~65 F² per trit after shrink, but charge pump routing increases pad area by ~12%.
  - Sense energy: ~0.30–0.32 pJ/trit (charge pump + comparator settling with 12-bit ADC for margin).
  - Write energy: ~0.45–0.5 pJ/trit due to repeated pulses that settle the charge.
  - Voltage margin: ~140 mV between states, but leakage over hours requires refresh every ~10³ writes, adding ~0.2 pJ/word to the refresh budget.
- Kill criteria triggers:
 1. **Middle state instability** – Charge leakage forces refresh, erasing the assumed density/energy benefit.
 2. **Periphery cost dominates / sense energy fails** – Charge pump + calibration logic add ~50 transistors per row driver, raising sense energy above 0.4 pJ/trit.
 3. **Interface ambiguity** – Requires calibration sequences (±0.05 V steps) that must be codified; failure to do so implies semantics depend on chip-specific behavior.

## 4. Hybrid binary array with ternary interface (Option B)
- Concept: Keep the binary cells but add ternary-aware sensing by combining 3-bit windows into trits (straight mapping from 3 bits → 1 trit) and expose ternary tokens on the interface. The array still stores binary, but the interface presents ternary semantics.
- Forecasted numbers:
  - No additional cell area; area cost only in the column encoder and sense amp adjustments. Encoder logic now uses ~96 transistors per 3-bit slice after LUT pruning, down from ≈120.
  - Converter energy: currently ~0.28 pJ/word for the encoding logic plus 0.1 pJ/word for multi-bit window timing and buffering; total periphery addition ≈0.38 pJ/word (a 0.12 pJ/word drop from the previous design).
  - Effective trits/mm² remains the same as the baseline (0.29 µm² per bit), but the interface reduces system-level traffic by ~20% if workloads consume the ternary tokens directly.
- Kill criteria triggers:
1. **Interface ambiguity** – API must be explicit; relying on TFMBS-specific scheduling fails the criterion.
2. **Periphery cost dominates** – Keep encoder energy below the 1.5 pJ PT-5 decoder cost; otherwise this path is worse than the baseline packer.

Only candidates whose periphery energy falls below the 6.6 pJ/word baseline budget and whose margins withstand ±10% supply variation should advance into `spicemodels/`. This hybrid path is the closest to the budget, so the updated encoder energy is logged before moving forward.
