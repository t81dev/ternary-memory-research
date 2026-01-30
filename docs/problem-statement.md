# Problem statement

## What is native ternary memory?
Native ternary memory stores, communicates, and delivers ternary digits (trits) without remapping them into binary-only representations at every interface. It describes any part of the storage subsystem—cells, sense amps, decode/encode flow, and interfaces—that is explicitly designed for ternary semantics from the voltage/current operating point through the API exposed to the rest of the system.

We distinguish three layers:

- **Ternary cells** are the physical nodes that encode three metastable states (e.g., –1/0/1 or 0/1/2) and must be measurable, stable, and manufacturable across PVT corners.
- **Ternary interfaces** are the electrical, timing, and protocol boundaries that carry trits between cells and logic (e.g., sense amps that resolve three levels, decoding logic that presents ternary values to the rest of the chip, serialization between binary and ternary domains).
- **Ternary semantics** are the expectations placed on the stored values (e.g., a computation pipeline that consumes trits directly or a memory controller that treats reads/writes as ternary operations).

Option B—ternary-native interfaces backed by binary SRAM—is a first-class outcome, not a fallback. This could mean a binary cell array with an analog/latched periphery capable of delivering ternary semantics to an external controller or compiler while keeping the storage primitive binary. That hybrid pathway remains within scope as long as the interface genuinely delivers ternary behavior without relying on pre-existing ternary execution infrastructure.
