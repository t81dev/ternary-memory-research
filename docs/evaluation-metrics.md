## Evaluation Metrics (Revised, Operational)

To keep the research falsifiable, every candidate is evaluated against a conventional binary SRAM baseline using the following metrics. All metrics are measured at the memory *interface*, not at the isolated cell level.

## Primary metrics

- **Energy per delivered trit**  
  Total energy required to successfully deliver a single ternary value at the memory interface, including sense amplifiers, reference generation, decoding, interface charging, and any required re-sensing or retry behavior. Measured separately for reads and writes where applicable. Compared against binary SRAM delivering ternary values via PT-5 encoding.

- **Effective density (trits/mm²)**  
  Usable ternary storage density after amortizing all required peripheral circuitry, including sense amps, decoders, reference ladders, and routing. Raw cell density alone is non-authoritative.

- **Access latency**  
  Worst-case first-trit read latency, measured in nanoseconds across PVT corners, including all sensing and decoding stages required to present a stable ternary value at the interface.

- **Stability**  
  Probability of incorrect ternary state resolution at the interface due to noise, drift, or PVT variation, with particular emphasis on collapse or misclassification of the middle state. Stability is evaluated using measurable voltage or current margin thresholds rather than idealized state models.

- **Periphery complexity**  
  Relative increase in transistor count, routing congestion, and control logic required to expose ternary semantics at the interface, normalized against the binary SRAM baseline.

## Evaluation principle

A candidate is considered viable only if it meets or exceeds the binary baseline on at least one primary metric *without* incurring disproportionate losses in the others. Failure on any primary metric without compensating advantage is grounds for rejection.
