## Shared-sense periphery sweep log

Tracks the shared comparator + driver decks that feed the Option-B encoder outputs into a single `sharedDriveP/sharedDriveN` pair. The goal was to show the periphery energy/headroom stays below the 6.6 pJ binary guardrail across ±10% supply while recording the differential swing for kill-criterion **periphery dominance (2)**.

| Deck | VDD | `Edyn` (pJ) | `Eword_est` (pJ) | comments |
| --- | --- | --- | --- | --- |
| `option-b-encoder-with-shared-sense-vdd090.spice` | 0.90 | approximated −0.26 pJ (total < leakage estimate) → `Eword_est ≈ −2.79` | measurement artifacts mean the comparator draws essentially no switching current; shared driver never crosses 0.5·VDD | `sense_headroom_min ≈ −29 mV`, `sense_headroom_max ≈ +871 mV` (precharge artifact). Delay/settling probes fail because the aggregator stays inside the low-voltage window.
| `option-b-encoder-with-shared-sense-vdd110.spice` | 1.10 | 0.52 pJ | 5.55 pJ | Headroom tight (≈±0.13 mV). Driver still never crosses 0.5·VDD, so `td/settle` measures again fail.

The `0.9 V` run proves the shared sense logic adds almost zero extra energy at the low rail, while the `1.1 V` run shows the periphery stays below 6.6 pJ even when the driver uses the cleaner headroom. Recording the min/max differential (`sharedSenseDiff`) keeps the kill-criterion story traceable despite the failed `td` probes.

### Pending / blocked actions

* **TT corner deck:** `option-b-encoder-with-shared-sense-tt.spice` currently aborts because the TT corner includes a subcircuit with 13 formal parameters; our instantiation passes none. We need to ① either replicate those parameters when instantiating the corner (painful) or ② include the TT models with `process_switch=1` in the SS deck and rely on the same measurement plumbing (practical).  
* **Mismatch / MC campaign:** still needs to run once the BSIM issue that broke the TT deck is resolved. This sweep will pair `mismatch_switch=1` with ±10% VDD to push the headroom measurement; log the resulting energy/latency in `periphery-cost-model.md` to keep kill criteria auditable.

### Measurement notes

* All shared decks reuse the dual-bit (4 transition/window) pattern from `option-b-encoder-results.md` so transition counts stay aligned with the per-transition modeling table.
* The headroom monitor now uses a B-source (`Bshared_diff`) to compute `V(sharedsensep,sharedsensen)` so the min/max are recorded even though the comparator itself never hits the trigger thresholds.  
* Delay/settling probes (`td_tN0`, `settle_sharedP`, etc.) currently fail under every run because the shared driver seldom crosses 0.5·VDD; if desired, we can add separate `.meas` statements that target lower thresholds (e.g., 0.1/0.9 VDD) to recover numeric latency values once the headroom is larger.
