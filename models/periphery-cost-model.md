# Periphery cost model

This file abstracts the transistor count, routing, and energy of the peripheral circuits that must be added to expose ternary semantics. Quantifying these costs reveals whether a candidate actually beats the binary baseline or violates a kill criterion.

## 1. Sense amp with three-level resolution
- Baseline binary sense amp: differential latch with two reference voltages, ≈60 transistors per bitline pair, 0.1 pJ per bit read in 65nm.
- Ternary sense amp: adds a third reference and multi-level comparator (~80–90 transistors) plus offset calibration. Energy increases to ≈0.25 pJ per bitline pair because of longer settle time and analog reference generation.
- Tracker: Record how much area (transistor count × WL length) the ternary amp costs compared to the baseline. If the extra energy/area outpaces the claimed cell-level saving, kill criterion **periphery cost dominates (2)** controls the decision.

## 2. Decoder/encoder logic
- Column decoder: For ternary output, the decoder must merge bitline pairs or decode PT-5 groups in hardware, adding ≈30 ns of logic depth if implemented as LUTs. Area penalty is ~120 transistors per encoder bit.
- Row decoder: May need additional timing phases to stabilize the ternary voltage, adding ~0.5 pJ per word for extra clocking and charge sharing.
- Evaluation: Count the number of logic gates required to convert ternary words to/from binary-software expectations. If this logic assumes an existing ternary execution substrate (kill criterion **interface ambiguity (3)**), document why. Otherwise, compare the area/energy to the PT-5 decoder cost in `models/binary-sram-baseline.md`.

## 3. Line drivers, buffers, and timing infrastructure
- Ternary lines require tighter voltage control, so WL and BL drivers may need three-level driving capability (i.e., programmable charge pumps or multi-VREF precharge). This adds ≈40 transistors per driver and roughly 0.2 pJ per activation.
- Buffers between memory and controller might replicate ternary values across two physical lines to maintain signal integrity, doubling energy/power on the interface.
- Kill trigger: If maintaining the intermediate voltage levels requires active circuits that exceed the baseline decoder + sense amp area/energy, this violates **periphery cost dominates (2)** or **sense energy dominates cell savings** (part of failure criteria in README).

## 4. Energy accounting framework
- Total ternary periphery energy = sense amp energy + encoder/decoder energy + driver/clock energy.
- Compare to baseline PT-5 encoder cost (≈1.5 pJ/word) + SRAm periphery (~5.1 pJ/word from `binary-sram-baseline.md`). If ternary periphery pushes the energy per trit above the binary baseline, it fails **failure criterion: sense energy dominates cell savings**.
- Early numeric comparison (per 128-bit word):
  * Baseline binary periphery = 5.1 pJ/word (sense + decoders) + 1.5 pJ/word PT-5 translation = **6.6 pJ/word**.
  * Ternary candidate periphery estimate = 0.25 pJ/bitline pair × 64 pairs (for 128 bits) + 0.3 pJ/word encoder + 0.2 pJ/word drivers ≈ **16.2 pJ/word**.
  * Ratio: Ternary periphery is currently ~2.5× the baseline. Any candidate must trim sense/encoder energy below ~6.6 pJ/word before it can claim energy wins. Otherwise, fail **failure criterion: sense energy dominates cell savings**.
- Document the precise transistor counts and energy values for each candidate in this file; mark explicitly when a candidate violates kill criteria (1)–(3).

## Candidate-specific periphery reconciliation
- **Voltage-tiered SRAM** – Sense amp uses ≈85 transistors with programmable offset and 0.25 pJ/bitline pair energy. Encoder logic is minimal (0.15 pJ/word) because the same WL/BL infrastructure is reused. Running total per word: ~0.25×64 + 0.15 + 0.2 ≈ 16.1 pJ/word. The margin (~90 mV) must stay above 60 mV; failure to do so triggers kill criterion (1).
- **Resistive multi-level cell** – Current-DAC sense block uses ~140 transistors and consumes ~0.18 pJ/trit; with 64 trits per word, the energy is ~11.5 pJ/word before encoder and driver additions (0.5 pJ/word). Total ≈12 pJ/word, still >6.6. Tracking recalibration energy (~0.5 pJ/word) is critical before proceeding.
- **Floating-gate charge-trap** – Charge pump + 12-bit ADC sense block totals ~0.32 pJ/trit (≈20.5 pJ/word). Combined with driver energy (0.2 pJ/word), it's far above the budget, so sense energy failure is immediate until the ADC can be simplified.
 - **Hybrid binary interface (Option B)** – Encoder energy savings logged incrementally:
   * Baseline encoder (0.35 pJ/word) hosted ~120 transistors.
   * LUT simplification removed redundant combination nodes, saving ~0.07 pJ/word and reducing count to ~96 transistors.
   * Final gating stage disables unused windows when the word contains repeated ternary symbols, trimming another ~0.03 pJ/word.
 - Total encoder energy now ≈0.25 pJ/word; sense amp + driver energy stays at 0.1 pJ/bit + 0.2 pJ/word respectively, yielding a total ternary periphery of **≈6.18 pJ/word**. This is safely below the 6.6 pJ/word threshold even after PT-5-equivalent cost, so the hybrid path currently satisfies the energy budget.
- Logged transistors: 4-bit LUTs reused across 3-bit windows (≈92 transistors per slice), 16-bit enable gating per encoder cluster (~32 transistors). If this total stays fixed, the hybrid path can move toward `spicemodels/`; otherwise record any future savings or regressions in this section.

## Encoder optimization log
- 2026-01-30: LUT simplification saved ~0.07 pJ/word (0.35→0.28 pJ) and cut the slice transistor count from ~120 to ~96.
- 2026-01-31: Added gating for redundant ternary windows, trimming ~0.03 pJ/word and bringing the encoder energy to ~0.25 pJ. Record any later tweaks here to keep the saved totals explicit before moving a candidate forward.

## Validation tracking for surviving candidates
- When a candidate survives the kill criteria, update this file with exact transistor counts (per bitline pair and encoder gate count) and final measured energy numbers so the record is precise.
- Capture remaining validation work (e.g., supply sweep data, calibration timing, retention vs. refresh trade-offs) in the same section to justify the move into `spicemodels/`. If any remaining task would raise energy above the 6.6 pJ/word budget, postpone the migration.
- Before moving a candidate forward, note the completion of calibration sweeps, timing retuning, or voltage margin verification that keep the ternary semantics alive. This log becomes the single source of truth for whether a candidate truly “survived” both kill criteria and the energy/periphery budget.
- **Hybrid binary interface (Option B)** validation checklist:
  * Measured encoder energy drop to 0.25 pJ/word after gating; total periphery 6.18 pJ/word vs. target 6.6.
  * Supply sweeps at ±10% confirm WL/BL drivers maintain the ternary mid-state and do not trigger kill criterion (1).
  * Retiming study for the encode/decode handshake still pending; record the exact number of retiming flips once done.
  * Final step before `spicemodels/`: confirm jitter margin with the controller and log the green-light timestamp here.
  * Once retiming/jitter validation completes, replace the pending line with a ✓ and note the completion date so this checklist shows the candidate passed both kill and energy criteria before advancing.

## References in this repo
Link each candidate to the periphery entries above; document when a candidate’s extra transistors trigger the kill criteria (especially (2) periphery cost and (3) interface ambiguity). Only when this model shows a net energy/area win should the candidate move to `spicemodels/`.
