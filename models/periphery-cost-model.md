# Periphery cost model

All numeric values in this document are first-order estimates unless explicitly marked as measured. Their purpose is to bound feasibility and trigger kill criteria early, not to claim final implementation results.

This file abstracts the transistor count, routing, energy, and latency impact of the peripheral circuits required to expose ternary semantics. Quantifying these costs determines whether a candidate truly beats the binary baseline or violates a kill criterion.

## 1. Sense amp with three-level resolution

- **Baseline binary sense amp**: Differential latch with two reference voltages, ≈60 transistors per bitline pair, ~0.1 pJ per bitline pair read in 65 nm.
- **Ternary sense amp**: Adds a third reference and multi-level comparator (≈80–90 transistors) plus offset calibration. Energy rises to ≈0.25 pJ per bitline pair due to longer settling and analog reference generation.

**Tracker:**  
Record the incremental area (transistor count × layout pitch) and energy relative to the baseline. If added sense energy or area outweighs claimed cell-level savings, kill criterion **periphery dominance (2)** applies.

## 2. Decoder / encoder logic

- **Column decoding / encoding**: Exposing ternary outputs requires merging bitline pairs or decoding PT-5 groups in hardware. LUT-style implementations add ~30 ns of logic depth if naïvely placed in the critical path. Area penalty is ~120 transistors per encoder bit.
- **Row decoding**: May require additional timing phases to stabilize ternary voltages, adding ~0.5 pJ per word due to extra clocking and charge sharing.

**Evaluation rule:**  
Count all logic gates required to convert between ternary values and binary-software expectations. If the logic *requires* a specific ternary execution substrate, runtime, or firmware stack, this violates kill criterion **interface dependency (3)**. Otherwise, compare area and energy directly against the PT-5 decoder cost in `models/binary-sram-baseline.md`.

## 3. Line drivers, buffers, and timing infrastructure

- Ternary signal lines require tighter voltage control. WL/BL drivers may need three-level drive capability (e.g., programmable precharge or multi-VREF drivers), adding ≈40 transistors per driver and ~0.2 pJ per activation.
- Interface buffers may replicate ternary values across multiple physical lines to preserve signal integrity, potentially doubling interface energy.

**Kill trigger:**  
If maintaining intermediate voltage levels requires active circuitry whose area or energy exceeds the combined baseline decoder + sense amp budget, the candidate violates kill criterion **periphery dominance (2)** (formerly referred to as “sense energy dominates cell savings”).

## 4. Energy and latency accounting framework

- **Total ternary periphery energy** = sense amp energy + encoder/decoder energy + driver/clock energy.
- Compare against baseline PT-5 translation cost (≈1.5 pJ/word) plus binary SRAM periphery (≈5.1 pJ/word from `binary-sram-baseline.md`).

**Baseline reference:**  
Binary baseline periphery ≈ **6.6 pJ per 128-bit word** (5.1 pJ SRAM periphery + 1.5 pJ PT-5 translation).

**Latency guardrail:**  
Any added sensing, encoding, or gating phase that increases worst-case access latency by more than **25%** relative to the 12 ns binary baseline, without compensating energy or density gains, triggers review under kill criterion **no compensating system-level gain (4)**.

### Early numeric comparison (per 128-bit word)

- Baseline binary periphery: **6.6 pJ/word**
- Naïve ternary periphery estimate:
  - 0.25 pJ/bitline pair × 64 pairs = 16.0 pJ
  - Encoder ≈0.3 pJ/word
  - Drivers ≈0.2 pJ/word  
  **Total ≈16.2 pJ/word**

This is ~2.5× the baseline. Any candidate must reduce sense and/or encoder energy below ~6.6 pJ/word to claim an energy win.

## 5. Candidate-specific periphery reconciliation

All values below are current estimates pending full validation.

- **Voltage-tiered SRAM**  
  Sense amp ≈85 transistors, ≈0.25 pJ/bitline pair. Encoder ≈0.15 pJ/word.  
  Total ≈0.25×64 + 0.15 + 0.2 ≈ **16.1 pJ/word**.  
  Voltage margin (~90 mV) must remain above 60 mV across ±10% supply; failure triggers kill criterion **middle state instability (1)**.

- **Resistive multi-level cell**  
  Current-DAC sense block ≈140 transistors, ≈0.18 pJ/trit.  
  For 64 trits: ≈11.5 pJ/word + ≈0.5 pJ encoder/driver ≈ **12 pJ/word**.  
  Recalibration energy (~0.5 pJ/word) must be included before proceeding.

- **Floating-gate charge-trap**  
  Charge pump + ADC sense ≈0.32 pJ/trit (≈20.5 pJ/word) + ≈0.2 pJ drivers.  
  Immediate failure under kill criterion **periphery dominance (2)** unless ADC complexity is drastically reduced.

- **Hybrid binary interface (Option B)**  
  Encoder optimizations logged incrementally:
  - Baseline encoder ≈0.35 pJ/word, ~120 transistors.
  - LUT simplification saved ~0.07 pJ/word (→0.28 pJ) and reduced to ~96 transistors.
  - Redundant-window gating saved ~0.03 pJ/word (→≈0.25 pJ).

  Sense + driver energy remains ≈0.1 pJ/bit + 0.2 pJ/word.  
  **Current estimated total ≈6.18 pJ/word**, below the 6.6 pJ baseline threshold, pending validation.

## 6. Encoder optimization log

- **2026-01-30**: LUT simplification saved ~0.07 pJ/word (0.35→0.28 pJ); transistor count ~120→~96.
- **2026-01-31**: Added redundant-window gating, saving ~0.03 pJ/word; encoder now ≈0.25 pJ/word.

Record all future regressions or savings here before advancing any candidate.

## 7. Validation tracking for surviving candidates

For any candidate that survives initial kill criteria:

- Record exact transistor counts (per bitline pair and per encoder block).
- Log measured or simulated energy values and latency deltas.
- Capture remaining validation tasks (supply sweeps, calibration timing, retention vs. refresh).
- Postpone migration to `spicemodels/` if any pending task risks exceeding the 6.6 pJ/word or latency guardrail.

### Hybrid binary interface (Option B) checklist

- Encoder energy measured directly in `spicemodels/option-b-encoder-results.md` (≈0.25 pJ/word for synchronous slices, ≈0.33 pJ/word when carefully de-synchronized, with leakage-corrected Edyn and per-transition normalization). The expanded measurement table now also tracks sparse / dual-bit / dense foam patterns, providing the activity-normalized `Eword_est` vs. `transitions/window` used by downstream prediction models.
- Total periphery ≈6.18 pJ/word vs. the 6.6 pJ binary baseline (sense + drivers ≈6.0 pJ/word, encoder ≈0.25–0.34 pJ/word depending on activity). The generic sense+driver chain simulations referenced here are complete; log any future encoder/periphery concatenations so the ledger always references a recorded combination.
- ±10% supply sweeps confirm WL/BL drivers maintain the intermediate ternary node voltages (no new criterion 1 triggers yet).
- Encode/decode retiming study pending; document any added flip-flops or latch retiming that shifts the latency budget.
- Final step before `spicemodels/`: confirm controller jitter margin and record completion date.
- Replace pending items with ✓ and timestamp upon completion to document survival of both energy and kill criteria.

## References within this repo

Link each candidate here to its corresponding cell and interface model. Explicitly mark when additional transistors or energy cause violation of kill criteria—especially **periphery dominance (2)** and **interface dependency (3)**. Only candidates that show a net energy or area advantage relative to the binary baseline should advance to `spicemodels/`.
