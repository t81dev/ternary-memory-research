# Kill criteria

This project prioritizes early falsification. A candidate pathway is rejected immediately if any of the following conditions are met when evaluated against the binary SRAM baseline.

## Candidate-level kill conditions

1. **Middle state instability**  
   The ternary middle state cannot be reliably resolved across ±10% supply variation or specified temperature extremes *after accounting for all required compensation circuitry*. Any compensation must be explicitly modeled and included in energy, area, and latency metrics.

2. **Periphery dominance**  
   The area or energy cost of sense amplifiers, reference generation, decoding, buffering, or control exceeds the binary baseline by a margin that negates claimed cell-level savings. Periphery cost is evaluated as a first-class contributor, not amortized away.

3. **Interface dependency**  
   The design cannot expose ternary semantics at the memory interface without requiring a specific ternary execution substrate, firmware stack, or runtime. Compatibility with ternary systems is allowed; dependency is disqualifying.

4. **No compensating system-level gain**  
   After amortizing latency, energy, density, and stability costs, the candidate fails to exceed the binary SRAM + packing baseline in at least one primary evaluation metric *without* incurring disproportionate losses in the others.

## Project-level implications

- Rejection of a candidate does not imply rejection of ternary memory as a whole.
- Repeated failure of all candidates within a category (e.g., cell-level ternary storage) may trigger narrowing of scope or termination of that category.
- Failure across all investigated categories is considered a valid outcome and grounds for concluding the project.

Kill criteria may be refined only to improve measurement fidelity, not to rescue failing designs.
