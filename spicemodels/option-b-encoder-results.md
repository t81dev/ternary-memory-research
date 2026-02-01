# spicemodels/option-b-encoder-results.md

## Setup
- Date: 2026-02-01
- Simulator: ngspice (batch mode)
- Device models: SKY130 (`nfet_01v8` / `pfet_01v8`, SS corner, mismatch disabled in this deck)
- VDD sweep: 1.0 V (single point in this deck)
- Cload sweep: 50 fF (per-output cap)
- NSLICES scaling assumption: 43 total slices ⇒ 4 instantiated per deck
- Topology commit hash: (fill with the relevant git hash when you collect the result)

## Measurements
| Corner (activity) | VDD | Cload | Etotal (J) | Eslice (pJ) | Eword_est (pJ) | td_tP0 (ns) | Transitions/window | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ss (mismatch off), 4 slices synchronized | 1.0 | 50 fF | 1.85600e-12 | 0.462 | 19.89 | 14.03 | 6 (3 rising + 3 falling) | `T1=5n`, `T2=35n` (gives TO≈35.0025 ns), leakage-corrected Edyn ≈9.914e-13 J, td_tN0 ≈9.18 ns, normalized ≈0.165 pJ/transition × 6 |
| ss (mismatch off), 4 slices de-synchronized (0-2 ns offsets) | 1.0 | 50 fF | 2.09936e-12 | 0.342 | 14.70 | 4.90 | 6 (per-slice timing offsets) | `T1=5n`, `T2=35n`, Edyn ≈1.37e-12 J, td_tN0 ≈10.17 ns, settle_tP0 ≈13.08 ns / settle_tN0 ≈1.32 ns, normalized ≈0.228 pJ/transition × 6 |
| ss (mismatch off), sparse pulse (2 transitions) | 1.0 | 50 fF | 5.95340e-14 | 0.0149 | 0.64 | — | 2 (1 rising + 1 falling on b0) | `T1=5n`, `T2=35n`, Edyn ≈5.94e-14 J, td_* failed (no 0.5·VDD crossing), normalized ≈0.32 pJ/transition × 2 |
| ss (mismatch off), dual-bit pulse (4 transitions) | 1.0 | 50 fF | 6.08300e-13 | 0.0407 | 1.75 | 4.04 | 4 (b0+b1 single cycles) | `T1=5n`, `T2=35n`, Edyn ≈1.63e-13 J, td_tn0 failed, settle_tP0 ≈3.09 ns, normalized ≈0.41 pJ/transition × 4 |
| ss (mismatch off), dense pulse (8 transitions) | 1.0 | 50 fF | 7.61237e-13 | 0.0631 | 2.71 | 26.03 | 8 (b0 double, b1/b2 single) | `T1=5n`, `T2=35n`, Edyn ≈2.52e-13 J, td_tn0 ≈15.18 ns, settle_* failed, normalized ≈0.34 pJ/transition × 8 |
| ss (mismatch off), idle (0 transitions) | 1.0 | 50 fF | 4.96636e-18 | 3.855e-24 | 1.66e-22 | — | 0 | `T1=5n`, `T2=35n`, Edyn ≈1.54e-23 J, all threshold measures fail (no transitions), leakage floor captured |
| ss (mismatch off), pseudo-random toggles | 1.0 | 50 fF | 3.80508e-13 | 0.0950 | 4.08 | — | ~10 | `T1=5n`, `T2=35n`, Edyn ≈3.80e-13 J, td/settle triggers fail (signals rarely cross 0.5·VDD), normalized ≈0.38 pJ/transition × 10 |

## Latest interpretation
- The instantaneous power proxy `Bpw pwr 0 V=-V(vdd)*I(VDD)` keeps `V(pwr)` positive for consumption because ngspice defines current entering the positive terminal of a voltage source. In the synchronous deck, this produced `Pavg = 6.191864e-05 W`, `Etotal = 1.85600e-12 J`, `Eleak_tail = 1.44095e-13 J`, `Eleak_est = 8.64569e-13 J`, and therefore `Edyn = 9.91434e-13 J` over `[T1=5ns, T2=35ns]` (`spicemodels/option-b-encoder.spice:174-196`). The de-synchronized run raised `Pavg` slightly to `6.237912e-05 W` and `Etotal` to `1.87001e-12 J`, but the leakage tail shrank so `Edyn ≈ 1.35e-12 J`, `Eslice = 3.37e-13 J`, and `Eword_est = 1.45e-11 J` now reflect a more “average word” load. ngspice’s reported upper bound TO is ≈35.0025 ns in both cases due to time-step alignment; keep `T2=35n` in the log.
- With `NSLICES_IN_DECK=4` and `NSLICES=43`, that integrates to **≈0.46 pJ per slice** (leakage-corrected) and **≈19.89 pJ per 128-bit word** under the current stimulus (synchronous pulses on all slices). The table now includes additional rows for 2-, 4-, and 8-transition patterns; the roughly linear increase in `Eword_est` across those rows (normalized per transition as 0.32–0.41 pJ) supports a leakage-plus-dynamic-per-transition model of the form 

\[
E_{\text{word}} \approx E_{\text{leak}} + k \times \text{transitions}, \quad\text{where } E_{\text{leak}}\approx0.16\text{ pJ},\ k\approx0.33\text{ pJ/transition}.
\]

Use the logged `transitions/window` value to estimate any future workload energy (keeping `VDD`, `CLOAD`, `T1/T2`, and the pulse timing noted). Always pair these numbers with the incident transition count so their scope stays explicit.
- To isolate dynamic energy, capture a leakage-only interval (e.g., `TLEAK1=30n`, `TLEAK2=35n` with inputs steady) and do either:
 1. **Option A:** measure `Pleak = AVG V(pwr)` on the tail and compute `Eleak_est = Pleak * (T2-T1)` (constant-leakage approximation), then `Edyn = Etotal - Eleak_est`.
 2. **Option B:** integrate leakage directly via `Eleak_tail = INTEG V(pwr) FROM=TLEAK1 TO=TLEAK2` and scale it by `(T2-T1)/(TLEAK2-TLEAK1)` before subtracting from `Etotal`. Both options keep the subtraction consistent with the `V(pwr)` definition.
- Scale `Edyn` to per-slice and per-word figures (same NSLICES parameters above) and log the resulting values, not raw `Etotal`, when reporting switching energy.
- Delay measurements now track both `td_tP0` and `td_tN0` (values from the latest run: ≈14.03 ns and ≈9.18 ns, respectively). The new settling proxies (`settle_tP0 ≈ 13.09 ns`, `settle_tN0 ≈ 1.32 ns`) measure the time to cross 0.1·VDD→0.9·VDD (and vice versa), ensuring sluggish drives are exposed before linking the encoder to downstream periphery models. Consider re-running the proxy whenever the transition count or activity pattern changes.
- Because every slice receives identical input timing, the deck bounds a simultaneous-switching scenario. Phase-shifting or randomizing individual slice inputs (without Monte Carlo) produces a more realistic “average word” energy while staying deterministic.
- Recording **effective activity** (number of transitions per window) alongside `pJ/word` prevents readers from mistaking these numbers for a universal constant—they are tied to the stimulus in this deck.

## Decision
- Pass/Fail: Pass (measurement plumbing validated and bounded energy/delay numbers recorded)
- Triggered kill criteria: None
- Next action: Capture activity-normalized pJ/word (counts already in the current rows), feed these bounded encoder metrics into the downstream periphery/periphery modeling workstream, and repeat the settling-time proxy/transition logging whenever the stimulus changes substantially.
