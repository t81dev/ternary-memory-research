# Evaluation metrics

To keep the research falsifiable, every candidate is scored by:

- **Energy per delivered trit** – includes sense amp/decoder energy and any analog interface charging overhead. Compare to binary SRAM + PT-5.
- **Density (cells per mm²)** – cast as effective trits/mm² after peripheral area is amortized.
- **Access latency** – measured in nanoseconds to assess whether ternary handling adds unacceptable delay.
- **Stability** – probability that the middle ternary state collapses across voltage, temperature, and process corners.
- **Periphery complexity** – quantifies the transistor count and routing impact of sense amps, decoders, and interfaces needed to expose ternary semantics.

Metrics reference the binary SRAM baseline defined in `models/binary-sram-baseline.md`.
