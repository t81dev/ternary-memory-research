# ternary-memory-research

**Mission.**  
This repository investigates whether ternary-native memory cells or ternary-oriented memory interfaces can provide measurable density or energy advantages over conventional binary SRAM paired with packed ternary representations.

The goal is not to promote ternary hardware, but to determine—under explicit constraints—whether any form of native ternary memory survives realistic periphery, noise, and energy accounting.

## Non-goals

- Not an accelerator implementation.
- Not a dependency of TFMBS or any ternary execution framework.
- Not a production-ready memory macro.
- Not advocacy for ternary hardware.

## Motivation

Ternary execution systems already exist in software and emulation. The open question addressed here is whether **memory itself** can become ternary-native in a way that survives periphery costs, noise margins, and full-system energy accounting.

This repository assumes that semantic consumers of ternary values may exist elsewhere, but it does **not** assume their presence. Any successful result must stand on its own and remain importable into binary, ternary, or hybrid systems without architectural coupling.

The value of this work comes from transparent, falsifiable modeling rather than optimistic claims.

## Core research questions

1. Can a ternary memory element reduce **energy per delivered trit** relative to binary SRAM plus PT-5 encoding?
2. Does ternary storage reduce **effective memory traffic or density cost** once interfaces and periphery are fully accounted for?
3. Where do apparent density or energy gains collapse when sense amplifiers, decoding, and timing infrastructure are included?

## Screening thresholds (non-binding)

These example thresholds are used to rapidly filter candidates, not to guarantee acceptance:

- ≥1.3× effective density improvement **after** periphery amortization.
- ≥1.5× lower pJ/trit read energy compared to the binary SRAM baseline.
- Worst-case access latency no worse than the binary SRAM reference.

Failure to meet these thresholds does not imply ternary memory is impossible, only that the candidate under evaluation does not justify further work.

## Failure conditions

The following conditions falsify a candidate and are formalized in `docs/kill-criteria.md`:

- The ternary middle state is unstable across PVT corners.
- Sense energy or periphery complexity overwhelms any cell-level savings.
- Area or interface overhead cancels density or energy advantages.

Candidates that trigger these conditions are intentionally terminated early.

## Periphery validation snapshot

The shared sense + encoder path is the make-or-break periphery block for Option B. Our workload log in `spicemodels/option-b-encoder-results.md` now reports leakage‑corrected `Edyn` scaled per slice/word plus the fitted activity model `Eword ≈ Eleak + 0.33 pJ × transitions`, which feeds into the amortized periphery ledger at `models/periphery-cost-model.md`.

The aggregated sense/driver run (`spicemodels/option-b-encoder-with-shared-sense*.spice`) now covers TT and ±10% VDD, and `periphery-cost-model.md` tracks the same energy/headroom tuples (≈0.45 pJ `Edyn`, 4–6 pJ `Eword_est`, headroom ≈43–111 mV). Because the shared driver never reaches 0.5 VDD, the `.meas` thresholds were shifted to `{sense_thresh_low*VDD}`→`{sense_thresh_high*VDD}` to capture retiming/jitter margins before the waveform collapses; the new `sense_headroom_min/max` logs document the resulting low-swing safety window. The Monte Carlo noise sweeps now push every sample into the 895–900 mV range (`logs/mismatch-mc/headroom_histogram.csv`, `logs/mismatch-mc-tt/headroom_histogram.csv`, `logs/mismatch-mc-upsized/mismatch_mc.csv`), so the guard is auditable while the latency story catches up.

These measurements keep the repository’s `periphery dominance (2)` kill-criterion audit trail honest while tying the amortized encoder + shared-sense energy back into the README/ROADMAP narrative (see `models/periphery-cost-model.md` and `experiments/shared-sense-periphery.md` for the full table).

## Remaining validation hookup
After wiring the BSIM/TT parameter list into every shared-sense NFET/PFET (via the 13-parameter block or `process_switch=1`), queue 50–200 Monte Carlo runs at nominal and ±10% VDD, including a small injected noise source (≈5–10 mV) across `sharedsensep/sharedsensen`. Record the resulting `sense_headroom_min/max` histograms, confirm the worst-case headroom stays ≥20 mV even with noise, and copy the energy/headroom tuples (including driver permutations such as `logs/mismatch-mc-upsized/mismatch_mc.csv`) into `models/periphery-cost-model.md` and `STATUS.md` so the kill-criterion ledger stays auditable. Capture `sense_thresh_latency` now that the guard sits in the 895–900 mV bin by tuning the `sense_thresh_high` reference to the actual achievable swing (≈30–50 mV) and log the jitter envelope plus any clock-skew/phase-noise stimuli alongside the energy table so README, ROADMAP, and the ledger all point to the same timing story.

-Refer to `TODO.md` for the remaining stress sweeps (MC + jitter) and the migration checklist before the deck graduates into `spicemodels/`.

The ±10% mismatch Monte Carlo campaign now runs 50 seeds per corner (0.9 V/1.0 V/1.1 V) plus a matched TT sweep, so `logs/mismatch-mc/mismatch_mc.csv` and `logs/mismatch-mc-tt/mismatch_mc_tt.csv` hold the full set of 150 entries and `logs/mismatch-mc/headroom_histogram.csv` / `logs/mismatch-mc-tt/headroom_histogram.csv` document the 895–900 mV / 995–1000 mV guard bins. However, the `sense_thresh_latency` `.meas` statements still report “out of interval” because the shared sense differential never crosses the 30–50 mV window (see `logs/mismatch-mc/mc_0.9V_1.log:235-236`); we still need to retarget the timing probe (falling edge, pre-driving below the low threshold, or a normalized comparator snapshot) before those latency numbers appear in the ledger.

## Encoder periphery tie-in
The “typical workload” (≈3–5 transitions per 128-bit word) now ties directly into the amortized energy model from `spicemodels/option-b-encoder-results.md`: `Eword ≈ Eleak + 0.33 pJ × transitions`. Combining that with the shared-sense guardrail (≈4–6 pJ at typical activity) keeps the total periphery budget near 5–7 pJ/word, which we continue to highlight in `models/periphery-cost-model.md` and `STATUS.md` until the unified encoder+sense deck migrates into `spicemodels/` for the final validation chain.

If the ~70–110 mV window already satisfies downstream detection (e.g., a low-power comparator or inverter sense latch), call it out as a low-swing feature in README/ROADMAP. Otherwise, incrementally upsize the final driver, log that energy vs. swing trade-off in `models/periphery-cost-model.md`, and link the new data back to this validation plan before migrating the deck into `spicemodels/`.

## Repository structure

This repository follows a question-first organization. Directories are intentionally empty until justified by surviving models or measurements.
