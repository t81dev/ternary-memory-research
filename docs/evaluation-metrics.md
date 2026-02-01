## Evaluation Metrics (Revised, Operational)

<<<<<<< HEAD
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
=======
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
>>>>>>> e8336933d21862cc6ed2d3ad7f441eefee22fae3
