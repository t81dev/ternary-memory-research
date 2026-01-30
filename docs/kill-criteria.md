# Kill criteria

This project dies fast if any of the following are true for a candidate pathway:

1. **Middle state instability** – The ternary middle voltage collapses under ±10% supply variation or temperature extremes unless expensive compensation is added.
2. **Periphery cost dominates** – Sense amps, differential decoders, or buffering require more area/energy than the claimed cell-level savings.
3. **Interface ambiguity** – The design cannot expose ternary semantics without assuming a specific execution substrate (e.g., TFMBS) or firmware stack.
4. **No measurable system gain** – After amortizing latency and energy, the ternary path performs worse than binary SRAM + packing in at least one primary metric.

Kill criteria should be revisited as models mature so that only well-justified ideas move to the `spicemodels/` or `experiments/` phase.
