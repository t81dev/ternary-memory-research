# Prior art

The literature covers several attempts at ternary storage and computing:

- Charge-based ternary SRAM macros that trade increased periphery for a third voltage level.
- Sense-amp and decoder designs that differentiate three states using offset references or multi-threshold devices.
- Emulated ternary systems that rely on binary memory plus software packing.
- Analog/tristate memories that revisit multiple-valued logic for dense memories.

This repo does not attempt to rehash every prior work; it focuses on distilling the core assumptions and failure modes of existing ternary memory proposals and then evaluating them against our falsification criteria.
