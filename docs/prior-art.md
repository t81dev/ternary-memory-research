# Prior art

Prior work in ternary and multi-valued memory broadly falls into a small number of recurring approaches:

- **Charge-based ternary SRAM macros**, which introduce a third voltage level at the cost of additional reference generation, sensing complexity, and reduced noise margins.
- **Multi-threshold or offset sense-amp designs**, which attempt to resolve three states using analog discrimination, often with increased sensitivity to PVT variation.
- **Emulated ternary systems**, which store ternary values in conventional binary memory using software or firmware-level packing schemes.
- **Analog or multi-valued logic memories**, which revisit dense or non-binary storage concepts but frequently struggle with scaling, stability, and peripheral overhead.

Across this literature, several common failure modes recur:

- Peripheral circuitry (sense amps, reference ladders, decoders) dominates area and energy, erasing cell-level density gains.
- The ternary middle state exhibits poor stability under realistic noise and PVT conditions.
- Designs rely on tightly coupled execution substrates or custom logic, limiting generality and system-level adoption.
- Reported gains focus on isolated cells or idealized models rather than full array-plus-periphery implementations.

Binary memory with software-level ternary packing already provides a robust and scalable baseline. Any native ternary memory proposal must therefore demonstrate clear advantages beyond what is achievable with conventional SRAM and encoding alone.

This project does not attempt to exhaustively reproduce prior designs. Instead, it treats the historical record as a source of constraints and failure patterns, using them to inform evaluation metrics and kill criteria. Novelty is claimed only where a proposal survives these known failure modes under explicit measurement.
