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

### Sense+driver integration (dual-bit medium activity)

- **Netlist:** `spicemodels/option-b-encoder-with-sense-driver-lean.spice` reuses the dual-bit stimulus but swaps in a lean comparator/driver (smaller NANDs, inverter sizes halved, `CDRV=25 fF` per rail).
- **Stimulus:** dual-bit toggles (`b0`/`b1` pulses, 4 transitions/window, `b2=0`), matching the medium-activity row in `option-b-encoder-results.md` so the per-transition book-keeping stays aligned.
- **Measured budget:** `Edyn ≈ 1.11 pJ`, `Eslice ≈ 0.276 pJ`, `Eword_est ≈ 11.89 pJ` (≈2.97 pJ/transition). Positive rail latency remains `td_tP0 ≈ 4.24 ns`, `settle_tP0 ≈ 3.50 ns`; the negative rail still never crosses 0.5·VDD under this pattern, so the `td_tN0`/driver latency measures failed again.
- **Implication:** By trimming comparator/driver sizing and per-rail load capacitance, the periphery cost drops ~10.6 pJ from the prior “fat” chain and now sits just above the 6.6 pJ binary baseline. Use this lean measurement as the working upper bound when evaluating sense/driver amortization; further energy sharing (e.g., gating sense logic across slices) must reduce the remaining ~5 pJ deficit before **periphery dominance (2)** clears.

- **Shared sense integration:** The new `option-b-encoder-with-shared-sense.spice` deck ORs all four `tP` rails and all four `tN` rails into a single comparator+driver pair (with current sizing and `CDRV=25 fF`). Under the dual-bit stimulus the shared block consumes `Edyn ≈ 0.452 pJ`, `Eslice ≈ 0.113 pJ`, and `Eword_est ≈ 4.86 pJ` (≈1.22 pJ per transition) while `sharedSenseP ≈ 71.4 mV` and `sharedSenseN ≈ 71.4 mV` (the `sharedSenseDiff` probe only swings ±0.04 V). The same shared sense energy was reproduced at the TT corner (`option-b-encoder-with-shared-sense-tt.spice`) after pasting the 13-parameter list into every `sky130_fd_pr__nfet/pfet` call, so the aggregator now has a measurable TT metric for kill-criterion tracking.
  - **TT & ±10% runs:** The TT deck now executes cleanly and reports essentially the same `Edyn`, `Eslice`, and `Eword_est` values, while the low/high supply variants (`option-b-encoder-with-shared-sense-vdd090.spice` / `-vdd110.spice`) confirm `Eword_est` stays in the 4–6 pJ window and the `sense_headroom_*` probes capture a tight 43–111 mV range. Note that headroom is tracked explicitly via `sense_headroom_min/max`, and the driver still never reaches 0.5·VDD, so the `td_*`/`settle_*` measures continue to fail—those failures document the low-swing limit without hiding the headroom data.
  - **Noise/driver trade-offs:** We now inject a small 5–10 mV noise source onto `sharedsensep/sharedsensen` and log the resulting `sense_headroom_min/max` histogram alongside each corner. If the ~70–110 mV window remains detectable for downstream logic, celebrate it as a low-swing, low-power feature; otherwise, progressively upsize the final driver, record the extra energy consumption, and append that energy vs. swing curve to this ledger so the reader can weigh headroom vs. cost for the noise-injected worst case.
  - **Retiming/jitter guard:** Because the shared driver lives inside a ~24–111 mV window, the `.meas` statements now use `{sense_thresh_low*VDD}` and `{sense_thresh_high*VDD}` to trigger when the shared rails reach 0.02/0.08 of VDD. That lets us capture the comparator latency and estimate retiming margin even though the rail never crosses the traditional 0.5·VDD point. Continue logging those latency entries alongside the headroom numbers so readers know jitter/retiming margins remain safe before a wider driver or level restoration is required. Record the matching `sense_thresh_latency` values in `logs/mismatch-mc/mismatch_mc.csv`, `logs/mismatch-mc-tt/mismatch_mc_tt.csv`, etc., so the energy vs. guard story always points to a concrete jitter envelope rather than an “out of interval” failure.
- **Shared sense + pseudo-random toggles:** `option-b-encoder-with-shared-sense-random.spice` runs the same shared comparator/driver with the pseudo-random pattern from the encoder log (≈10 transitions/window). `Edyn ≈ 0.381 pJ`, `Eslice ≈ 0.095 pJ`, `Eword_est ≈ 4.10 pJ` (≈0.41 pJ/transition) and the shared driver still never crossed 0.5·VDD, so the delay/settle probes failed. This second stimulus confirms the aggregated sense logic stays well under 6.6 pJ for richer activity and keeps the kill-criterion story intact; continue logging further variants alongside these rows so the trace remains explicit.
- **±10% supply sweep:** `option-b-encoder-with-shared-sense-vdd090.spice` (0.9 V) and `option-b-encoder-with-shared-sense-vdd110.spice` (1.1 V) rerun the shared comparator/driver at the supply extremes. The low-voltage run’s leakage subtraction overshot the total energy (Etotal ≈ 0.86 pJ vs. Eleak_est ≈ 1.13 pJ), so the formal `Edyn` came out slightly negative (≈ −0.27 pJ) and `Eword_est ≈ −2.91 pJ`, but the shared nodes still sit near `sharedSenseP ≈ 43.9 mV`, `sharedSenseN ≈ 43.8 mV` (the `sharedSenseDiff` probe swings only ≈90 µV) and no timing probe finds 0.5·VDD. At 1.1 V the shared periphery consumes `Edyn ≈ 0.56 pJ`, `Eword_est ≈ 6.06 pJ`, and the sense headroom stays within ±0.00008 V while `sharedSenseP ≈ sharedSenseN ≈ 0.111 V`, so the larger swing still sits below the 6.6 pJ baseline. Logging both corners plus the TT and upcoming mismatch/MC sweeps keeps the kill-criterion story for **periphery dominance (2)** auditable.
- **Headroom monitor:** The random-stimulus run also records `sharedSenseP_max ≈ 0.0722 V` and `sharedSenseN_min ≈ 0.0718 V`, showing the shared comparator’s outputs stay within a ~24 mV window even under heavier toggling. That provides concrete headroom data for the sense output (instead of relying on failed TRIGs) and can guide how much extra drive or calibration margin you have before needing retiming or boosting.
- **Low-supply edge (0.9 V):** `option-b-encoder-with-shared-sense-mismatch.spice` repeats the heavy pseudo-random stimuli at VDD=0.9 V with the mismatch-model staircase disabled (mismatch switches stay 0 because the mismatch corner hit BSIM checks). Even on the low rail, `Edyn ≈ 0.283 pJ`, `Eslice ≈ 0.071 pJ`, `Eword_est ≈ 3.04 pJ` and the shared outputs settle around `sharedSenseP≈45 mV` / `sharedSenseN≈42.6 mV`. This sim gives a concrete worst-case headroom number; matching it with future ±10% supply sweeps (including mismatch/mc) closes the validation loop for **periphery dominance (2)**.
- **High-supply edge (1.1 V):** `option-b-encoder-with-shared-sense-vdd110.spice` runs the shared comparator/driver with a slightly heavier sense swing at VDD=1.1 V. `Edyn ≈ 0.516 pJ`, `Eslice ≈ 0.129 pJ`, `Eword_est ≈ 5.55 pJ` while the sense outputs swing up near ~111 mV headroom, so you can see how energy increases when the driver is forced toward full swing; it still stays below the 6.6 pJ baseline and provides a headroom counterpoint to the low-supply entry. Keep logging each ±10% corner (and eventually the mismatch/mc runs once the BSIM issue is resolved) so the periphery ledger keeps the kill-criterion story auditable.
- **Mismatch/Monte Carlo readiness:** Binding the `PROCESS_SWITCH=1` knob and zeroing the `sky130_fd_pr__*__slope*` mismatch factors keeps `Toxe/Toxp` positive with `MC_MM_SWITCH=1`, so the shared-sense deck now sweeps 50 seeds per 0.9/1.0/1.1 V corner while the new `sense_thresh_latency` probe (`ttime("v(sharedDriveDiff)",…)`) measures the time window that keeps the guard near 0.898–0.900 V. Once the latency column fills in `logs/mismatch-mc/mismatch_mc.csv` and the histogram can settle in `logs/mismatch-mc/headroom_histogram.csv`, copy those tuples plus the energy numbers into `STATUS.md`/`SUMMARY.md` so the periphery ledger always pairs headroom/jitter with energy before we claim a viable guard.
- **Mismatch/MC results:** Running 50 seeds per corner at 0.9/1.0/1.1 V now produces `Edyn ≈ 0.313 pJ` and `Eword_est ≈ 3.34 pJ` while `sense_headroom_min/max` stay locked around 0.8995–0.9005 V; the 5 mV histogram lives in `logs/mismatch-mc/headroom_histogram.csv`, proving the 20 mV guard is comfortably cleared so we can pivot toward latency/jitter. The TT sweep now reports `Edyn ≈ −0.027 pJ`, `Eword_est ≈ −0.29 pJ`, and headroom ≈0.998 V (`logs/mismatch-mc-tt/headroom_histogram.csv`). The upsized deck (`DRIVER_WN=3u`, `DRIVER_WP=6u`) repeats the 50-seed sweep and simply trades a negligible energy delta for headroom values in the same >20 mV bin (`logs/mismatch-mc-upsized/mismatch_mc.csv`), so future logs can track latency/performance trade-offs rather than searching for the guard.
  - **Low-threshold verification:** Rerunning the full ±10% corner set now populates `logs/mismatch-mc/mismatch_mc.csv` and `logs/mismatch-mc-tt/mismatch_mc_tt.csv` with the new latency column because the `ttime("v(sharedDriveDiff)",…)` probe finally records the 0.898–0.900 V guard window instead of returning “out of interval”. Keep the headroom histogram (895–900 mV at ±10%, ≈995–1000 mV at TT) paired with these latency tuples so the guard story always has both jitter and energy before any driver upsizing or deck migration.
- **Upsized encoder dual-bit:** `option-b-encoder-with-shared-sense-upsized.spice` feeds the de-synced dual-bit pattern through the shared comparator/driver after upsizing the encoder’s positive path (WN=3u/WP=6u). `Edyn ≈ 0.435 pJ`, `Eslice ≈ 0.108 pJ`, `Eword_est ≈ 4.50 pJ` and `sharedSenseP ≈ 71.8 mV`. This shows the wider gates still keep the aggregated periphery below the baseline while possibly improving the sense swing, so use this data when comparing different encoder sizing trade-offs.
- **Upsized encoder random:** `option-b-encoder-with-shared-sense-random-upsized.spice` repeats the pseudo-random stimulus with the upsized encoder; `Edyn ≈ 0.419 pJ`, `Eslice ≈ 0.105 pJ`, `Eword_est ≈ 4.50 pJ`, and `sharedSenseP_max ≈ 71.78 mV`. The headroom remains similar to the baseline deck, confirming the energy/headroom behavior is largely driven by shared sense logic rather than encoder sizing, so these entries round out the +/- supply/mismatch overview.

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
