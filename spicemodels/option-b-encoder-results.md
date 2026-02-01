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
| Corner (activity) | VDD | Cload | Etotal (J) | Eslice (pJ) | Eword_est (pJ) | td_tP0 (ns) | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| ss (mismatch off), 4 slices synchronized | 1.0 | 50 fF | 1.85600e-12 | 0.462 | 19.89 | 14.03 | `T1=5n`, `T2=35n` (gives TO≈35.0025 ns), leakage-corrected Edyn ≈9.914e-13 J, td_tN0 ≈9.18 ns |

## Latest interpretation
- The instantaneous power proxy `Bpw pwr 0 V=-V(vdd)*I(VDD)` keeps `V(pwr)` positive for consumption because ngspice defines current entering the positive terminal of a voltage source. The deck now reports `Pavg = 6.191864e-05 W`, `Etotal = 1.85600e-12 J`, `Eleak_tail = 1.44095e-13 J`, `Eleak_est = 8.64569e-13 J`, and therefore `Edyn = 9.91434e-13 J` over `[T1=5ns, T2=35ns]` (`spicemodels/option-b-encoder.spice:174-196`). `Eslice = 2.47859e-13 J` and `Eword_est = 1.06579e-11 J` follow from scaling by `NSLICES_IN_DECK=4` and `NSLICES=43`. ngspice’s reported upper bound TO is ≈35.0025 ns due to time-step alignment; keep `T2=35n` in the log.
- With `NSLICES_IN_DECK=4` and `NSLICES=43`, that integrates to **≈0.46 pJ per slice** (leakage-corrected) and **≈19.89 pJ per 128-bit word** under the current stimulus (synchronous pulses on all slices). Always pair these numbers with `VDD`, `CLOAD`, `T1/T2`, and the pulse timing so their scope is clear.
- To isolate dynamic energy, capture a leakage-only interval (e.g., `TLEAK1=30n`, `TLEAK2=35n` with inputs steady) and do either:
 1. **Option A:** measure `Pleak = AVG V(pwr)` on the tail and compute `Eleak_est = Pleak * (T2-T1)` (constant-leakage approximation), then `Edyn = Etotal - Eleak_est`.
 2. **Option B:** integrate leakage directly via `Eleak_tail = INTEG V(pwr) FROM=TLEAK1 TO=TLEAK2` and scale it by `(T2-T1)/(TLEAK2-TLEAK1)` before subtracting from `Etotal`. Both options keep the subtraction consistent with the `V(pwr)` definition.
- Scale `Edyn` to per-slice and per-word figures (same NSLICES parameters above) and log the resulting values, not raw `Etotal`, when reporting switching energy.
- Delay measurements now track both `td_tP0` and `td_tN0` (values from the latest run: ≈14.03 ns and ≈9.18 ns, respectively). Consider adding a settling proxy (e.g., how long before `V(tP0)` leaves `[0, 0.1·VDD]` or enters `[0.9·VDD, VDD]`) to catch long tails.
- Because every slice receives identical input timing, the deck bounds a simultaneous-switching scenario. Phase-shifting or randomizing individual slice inputs (without Monte Carlo) produces a more realistic “average word” energy while staying deterministic.
- Recording **effective activity** (number of transitions per window) alongside `pJ/word` prevents readers from mistaking these numbers for a universal constant—they are tied to the stimulus in this deck.

## Decision
- Pass/Fail: Pass (measurement plumbing validated and bounded energy/delay numbers recorded)
- Triggered kill criteria: None
- Next action: Rerun with de-synchronized slice timing to bound “average word” energy (leakage + delay metrics already captured)
