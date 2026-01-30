## Evaluation Metrics (Revised, Operational)

To keep the research falsifiable, every candidate ternary memory design is evaluated against a **binary SRAM + PT-5 baseline** using the following metrics.

### 1. Energy per Delivered Trit

**Definition:**
Total dynamic energy consumed to deliver one logical trit to a compute lane, including:

* bitcell read energy,
* sense amplifier(s),
* decode / threshold comparison logic,
* any analog interface charging or discharge overhead.

**Unit:** pJ/trit (read), pJ/trit (write, if applicable)

**Normalization:**
Reported relative to binary SRAM delivering PT-5 packed data and performing unpack + zero-detect in logic.

> This is the primary success metric. A ternary cell that does not win here is considered non-viable regardless of density.

---

### 2. Effective Density

**Definition:**
Usable trit storage per unit silicon area, amortizing all required periphery.

[
\text{Effective Density} = \frac{\text{Total stored trits}}{\text{Total area (cells + periphery)}}
]

**Unit:** trits/mm²

**Notes:**

* Peripheral area includes sense amps, reference generators, decoders, and routing overhead.
* Density is compared against binary SRAM storing PT-5 bytes, not raw bits.

---

### 3. Access Latency

**Definition:**
Time from address valid to stable trit value available at the memory interface.

**Unit:** ns (read), ns (write)

**Interpretation:**
Latency is not required to beat binary SRAM, but:

* > 1.5× latency penalty is considered unacceptable for inference workloads,
* excessive latency invalidates energy wins by stalling pipelines.

---

### 4. Stability (Middle-State Robustness)

**Definition:**
Probability that the ternary middle state remains distinguishable from ±1 across:

* voltage corners,
* temperature corners,
* process variation (Monte Carlo).

**Metric:**

* Error probability per access, or
* minimum noise margin (mV) across PVT.

**Kill Criterion:**
If the middle state cannot be reliably sensed without tightening margins beyond practical limits, the design is rejected.

---

### 5. Periphery Complexity

**Definition:**
Overhead required to expose ternary semantics at the array edge.

Measured as:

* additional transistors per bitcell (amortized),
* number of sense thresholds / comparators,
* routing complexity (qualitative, but documented).

**Purpose:**
Prevents “cell-only wins” that disappear once real memory macros are built.

---

### 6. Composite Metric: System-Relevant Efficiency (Optional but Recommended)

To avoid cherry-picking, candidates may also be ranked by a composite score:

[
\text{System Efficiency} =
\frac{\text{trits delivered per second}}{\text{energy} \times \text{area}}
]

This metric reflects **what actually matters at the accelerator level**, not isolated circuit cleverness.

---

## Baseline Reference

All metrics are evaluated relative to the binary SRAM baseline defined in:

```
models/binary-sram-baseline.md
```

This baseline includes:

* PT-5 packing overhead,
* unpack + zero-detect logic,
* standard SRAM periphery.

A ternary design must beat this baseline **after all costs are included** to be considered successful.

---

## Why This Version Works

* Every metric is **measurable**, not aspirational.
* Density and energy are explicitly **effective**, not cell-only.
* Stability has an explicit **kill switch**.
* The baseline comparison prevents unfair framing.
* The optional composite metric helps reason at the **system scale**, which aligns with TFMBS.
