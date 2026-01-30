# Binary SRAM baseline

This document records the binary SRAM assumptions used to compare against ternary candidates.

## Technology assumptions
- Process node: 65-nm foundry flavor typical for academic memory macros (6-metal, 1.0 V nominal). 
- Minimum cell pitch: 0.80 µm × 0.36 µm → roughly 0.29 µm² (≈55 F²) per bit (including bitline spacing).  
- Banking strategy: 16 kbit sub-array with 128-bit wordline and differential sense amps per bitline pair.

## Energy and latency assumptions
- Bitline energy per access (read or write): ~3.2 pJ per 128-bit word (≈25 fJ per bit) including precharge, sense amp loading, and bitline discharge.  
- Sense amp energy (differential latch, reference half-cell) amortized across the word: ~1.1 pJ/word.  
- Decoder/row driver energy: ~0.8 pJ/word (driving long WL).  
- Access latency: Row activation + sense = ~10 ns; column multiplex + data-out adds ~2 ns. Worst-case read/write latency ≈12 ns.

## PT-5 packing scheme
PT-5 maps 5 ternary digits (trits) onto 8 binary bits with a pre-computed translation table to keep the canonical ternary sequence (−1/0/1) balanced. Each logical ternary symbol is stored in one byte but only uses five bits. 
- Effective density: 5 trits/8 bits → 0.625 trits per bit. For the baseline cell area, this means an effective ternary density of 0.625 × (1 cell/bit) → ~0.18 trits/µm², assuming the 0.29 µm² cell.  
- Reads/Writes require PT-5 encoder/decoder logic, which adds ≈1.5 pJ per word for translation (measured as simple LUT lookups plus XOR trees). 

## Referencing this baseline
Any ternary proposal must show gains in density, energy, or latency *after* including equivalent translation periphery and the PT-5 overhead. Binary SRAM numbers above serve as the denominator in all comparative equations (e.g., pJ/trit = binary energy / (5 × word length)).
