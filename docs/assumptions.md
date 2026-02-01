# Assumptions

This document enumerates the explicit assumptions underlying the ternary memory research project. These assumptions are not claims of correctness; they define the boundary conditions under which models, metrics, and kill criteria are evaluated.

If an assumption is violated, associated results must be reinterpreted or discarded.

## Technology and process assumptions

- Fabrication is assumed to use a mature CMOS process node suitable for SRAM (e.g., ≥28 nm class). No reliance on exotic materials, non-CMOS devices, or post-CMOS fabrication techniques is assumed.
- Device characteristics (leakage, mismatch, threshold variation) are assumed to be comparable to contemporary binary SRAM designs at the same node.
- Voltage and temperature ranges reflect typical commercial or industrial operating envelopes unless otherwise stated.

## Electrical and signaling assumptions

- Ternary states are represented using voltage or current levels that are resolvable by on-chip sensing circuitry without off-chip calibration.
- Reference generation, biasing, and sensing circuits are assumed to be implementable using standard analog CMOS techniques.
- Noise sources (thermal, flicker, supply ripple, coupling) are assumed to scale similarly to binary SRAM periphery at the same process node.

## Memory organization assumptions

- Memory arrays are evaluated as full systems, including cells, sense amplifiers, decoding, reference generation, and control logic.
- No assumption is made that ternary cells can be densely tiled without additional spacing or shielding beyond what is required for stability.
- Refresh, recalibration, or background correction mechanisms—if required—must be explicitly modeled and included in metrics.

## Interface and system assumptions

- The binary host system remains authoritative for addressing, coherence, and I/O.
- Ternary memory is treated as an attached subsystem or fabric rather than a replacement for the binary memory hierarchy.
- Ternary semantics must be exposed at a well-defined memory interface without requiring a custom execution substrate or runtime.

## Baseline assumptions

- The reference baseline is conventional binary SRAM paired with software or firmware-level ternary packing (e.g., PT-5).
- Baseline designs are assumed to be well-optimized and representative of competent industry practice, not strawman implementations.

## Scope and limitation assumptions

- This project does not assume that ternary memory is broadly superior to binary memory.
- The investigation is limited to determining whether narrow, well-bounded advantages exist under realistic constraints.
- Negative or null results are considered valid outcomes.

## Assumption management

- Assumptions may be refined or tightened as models mature, but not relaxed to accommodate failing candidates.
- Any experiment or model that violates one or more assumptions must explicitly document the deviation and its impact on results.
