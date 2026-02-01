# Problem statement

## What is native ternary memory?

Native ternary memory stores, communicates, and delivers ternary digits (trits) without remapping them into binary-only representations at every interface. It describes any part of the storage subsystem—cells, sense amps, decode/encode flow, and interfaces—that is explicitly designed for ternary semantics from the voltage/current operating point through the API exposed to the rest of the system.

A design qualifies as *native* if ternary semantics are preserved across the memory interface boundary, regardless of whether the underlying storage primitive is ternary or binary.

We distinguish three layers:

- **Ternary cells** are the physical nodes that encode three metastable states (e.g., –1/0/1 or 0/1/2) and must be measurable, stable, and manufacturable across PVT corners.
- **Ternary interfaces** are the electrical, timing, and protocol boundaries that carry trits between cells and logic (e.g., sense amps that resolve three levels, decoding logic that presents ternary values to the rest of the chip, serialization between binary and ternary domains).
- **Ternary semantics** are the expectations placed on the stored values (e.g., a computation pipeline that consumes trits directly or a memory controller that treats reads/writes as ternary operations).

Option B—ternary-native interfaces backed by binary SRAM—is a first-class outcome, not a fallback. This includes designs where a conventional binary cell array is paired with analog or latched periphery capable of exporting ternary values to an external controller, compiler, or runtime. Such hybrid approaches remain within scope as long as the interface genuinely delivers ternary behavior without relying on pre-existing ternary execution infrastructure.

## Baseline and comparison

All evaluations in this project are performed relative to a conventional binary SRAM baseline with comparable process assumptions, array organization, and peripheral complexity. Comparisons focus on the combined cost of storage arrays *and* their periphery, rather than on isolated cell density or idealized signaling models.

## What this investigation seeks to determine

This project does not assume that ternary memory is superior to binary memory. Instead, it evaluates whether any form of native ternary memory—cell-level or interface-level—can meet the following bar:

- Deliver ternary semantics at the memory interface with measurable advantages (energy, area, bandwidth, or semantic efficiency) relative to a binary SRAM baseline with comparable periphery.
- Avoid disproportionate periphery, control, or error-management overhead that negates any gains from ternary representation.
- Remain stable, manufacturable, and predictable under realistic noise, PVT, and scaling assumptions.

Failure to meet these conditions is considered a valid and valuable outcome, and may result in narrowing scope, isolating viable subcases, or terminating the investigation entirely.
