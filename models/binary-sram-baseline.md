# Binary SRAM + PT-5 Baseline

This document records the binary SRAM assumptions used as the comparative baseline for all ternary memory candidates.

## Technology assumptions

- Process node: 65-nm CMOS, representative of academic and industrial SRAM macros (6-metal stack, 1.0 V nominal).
- Minimum cell pitch: 0.80 µm × 0.36 µm → ~0.29 µm² (≈55 F²) per bit, including bitline spacing.
- Banking strategy: 16 kbit sub-arrays with 128-bit wordlines and differential sense amplifiers per bitline pair.

Cell density figures refer to raw array area only. Peripheral circuitry (sense amps, decoders, drivers, control) is accounted for separately in energy, latency, and periphery-cost comparisons.

## Energy and latency assumptions

Unless otherwise stated, energy and latency figures assume read-dominated workloads and worst-case timing.

- Bitline energy per access (read or write): ~3.2 pJ per 128-bit word (≈25 fJ per bit), including precharge, bitline discharge, and sense loading.
- Sense amplifier energy (differential latch with reference half-cell), amortized across the word: ~1.1 pJ per 128-bit word.
- Decoder and row driver energy: ~0.8 pJ per 128-bit word.
- Access latency: row activation plus sensing ≈10 ns; column multiplexing and data-out add ≈2 ns. Worst-case read/write latency ≈12 ns.

## PT-5 packing scheme

PT-5 maps five ternary digits (trits) onto eight binary bits using a pre-computed translation table that preserves balanced ternary semantics (−1/0/1).

- Effective density: 5 trits / 8 bits → 0.625 trits per bit. With a 0.29 µm² binary cell, this corresponds to ~0.18 trits/µm² at the array level.
- Translation overhead: PT-5 encode/decode logic adds approximately 1.5 pJ per 128-bit word, modeled as LUT lookups and simple combinational logic (e.g., XOR trees).

PT-5 overhead is included in all baseline energy and latency comparisons.

## Referencing this baseline

All ternary proposals are evaluated relative to this baseline after including equivalent translation, buffering, and control overheads. Binary SRAM metrics defined here serve as the denominator for comparative figures (e.g., pJ/trit, trits/mm², worst-case access latency).
