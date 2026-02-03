# SPICE models — scope and gatekeeping rules

This directory contains transistor-level and analog simulations used to validate **only those candidates that have already survived** the modeling, metrics, and kill criteria defined elsewhere in this repository.

SPICE work is not exploratory. It is confirmatory.

## Authority and precedence

The following documents are authoritative and must not be overridden by SPICE results:

- `docs/problem-statement.md`
- `docs/evaluation-metrics.md`
- `docs/kill-criteria.md`
- `docs/assumptions.md`
- `models/binary-sram-baseline.md`
- `models/periphery-cost-model.md`

SPICE simulations exist to test feasibility *within* these constraints, not to redefine them.

## Admissible questions for SPICE

SPICE models may be used to answer the following questions only:

- Does the proposed sensing or encoding circuitry maintain required noise margins across ±10% supply variation and stated temperature corners?
- What is the settling time of sense, encode, and buffer stages under worst-case conditions?
- Does jitter, coupling, or analog variation force additional buffering, calibration, or timing phases?
- Are first-order energy estimates directionally correct once device-level effects are included?

SPICE may refine numbers. It may not introduce new degrees of freedom.

## Prohibited outcomes and techniques

The following are **explicitly disallowed** in SPICE work:

- Introducing exotic devices, materials, or process assumptions not listed in `docs/assumptions.md`.
- Adding hidden calibration loops, background refresh, or adaptive biasing unless their energy, latency, and area are fully modeled and charged to the candidate.
- Optimizing one corner case at the expense of violating worst-case latency, energy, or stability constraints.
- Assuming special controller behavior, firmware assistance, or execution substrates not required by the binary baseline.

If a candidate requires any of the above to survive, it fails.

## Fixed budgets and guardrails

All SPICE validation must respect the following frozen constraints:

- **Energy ceiling:**  
  Total periphery energy must remain below **6.6 pJ per 128-bit word**, matching the binary SRAM + PT-5 baseline.

- **Latency guardrail:**  
  Worst-case access latency must not exceed the binary baseline (~12 ns) by more than **25%** unless compensated by a clear energy or density advantage.

- **Stability requirement:**  
  Ternary semantics (if present) must remain resolvable across ±10% supply variation without requiring undocumented compensation.

These limits are inputs, not tuning targets.

## Kill switches during SPICE validation

Any of the following outcomes immediately terminate the candidate:

- Required buffering, calibration, or retiming pushes energy above the 6.6 pJ/word ceiling.
- Sense or encode settling time exceeds the latency guardrail without compensating gains.
- Noise, mismatch, or drift collapses the ternary middle state or forces periodic refresh.
- Interface behavior becomes ambiguous or timing-dependent in a way that cannot be expressed as a simple, substrate-neutral API.

SPICE confirmation of failure is considered success of the research process.

## Scope of current SPICE eligibility

At present, **only one candidate is eligible** for SPICE validation:

- **Hybrid binary array with ternary interface (Option B)**

All cell-level ternary storage candidates have already failed under periphery and stability modeling and must not be reintroduced here without explicit revision of upstream documents.

## Documentation requirements

For each SPICE model added:

- State which question from *Admissible questions* it addresses.
- Log measured vs. estimated energy and latency deltas.
- Record any assumption violations explicitly.
- Update `models/periphery-cost-model.md` with authoritative numbers if they change.

## Baseline migration

The validated hybrid shared-sense deck now lives in `option-b-encoder-with-shared-sense-baseline.spice`. This deterministic, mismatch-free configuration captures the calibrated guard/jitter metrics (sense_thresh latency ≈0.125 ps at ±10%, ≈4.75 ps at TT, 860–865 mV / 960–965 mV headroom bins) and the amortized energy numbers reported in `logs/mismatch-mc/*.csv`. Use it as the canonical artifact for future investigations before branching into noise, driver, or clock-skew permutations.
Do not delete failed SPICE results. Negative outcomes are part of the record.

## Exit conditions

A candidate may advance beyond SPICE only if:

- All kill criteria remain untriggered.
- Energy, latency, and stability remain within frozen budgets.
- No additional assumptions are required beyond those already documented.

Failure to meet these conditions concludes the investigation for that candidate.
