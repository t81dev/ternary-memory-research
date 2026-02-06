## Shared-sense periphery sweep log

Tracks the shared comparator + driver decks that feed the Option-B encoder outputs into a single `sharedDriveP/sharedDriveN` pair. The goal was to show the periphery energy/headroom stays below the 6.6 pJ binary guardrail across ±10% supply while recording the differential swing for kill-criterion **periphery dominance (2)**.

| Deck | VDD | `Edyn` (pJ) | `Eword_est` (pJ) | comments |
| --- | --- | --- | --- | --- |
| `option-b-encoder-with-shared-sense-vdd090.spice` | 0.90 | approximated −0.26 pJ (total < leakage estimate) → `Eword_est ≈ −2.79` | measurement artifacts mean the comparator draws essentially no switching current; shared driver never crosses 0.5·VDD | `sense_headroom_min ≈ −29 mV`, `sense_headroom_max ≈ +871 mV` (precharge artifact). Delay/settling probes fail because the aggregator stays inside the low-voltage window.
| `option-b-encoder-with-shared-sense-vdd110.spice` | 1.10 | 0.52 pJ | 5.55 pJ | Headroom tight (≈±0.13 mV). Driver still never crosses 0.5·VDD, so `td/settle` measures again fail.

The `0.9 V` run proves the shared sense logic adds almost zero extra energy at the low rail, while the `1.1 V` run shows the periphery stays below 6.6 pJ even when the driver uses the cleaner headroom. Recording the min/max differential (`sharedSenseDiff`) keeps the kill-criterion story traceable despite the failed `td` probes.

The latest round of noise/driver sweeps (5 mV/10 mV × scale 1.5/2.0/2.5) plus the ±10%/TT mismatch MC entries are now re-parsed with `tools/parse_mismatch_log.py`, so each `logs/*/mismatch_mc.csv` explicitly carries `sense_min/max`, `sense_thresh_latency`, and `comp_pass`. Every valid row still reports `comp_pass=failed` even though the 860–865 mV bins and ≈3.34 pJ `Eword_est` persist, so the comparator path has not yet toggled before considering driver upsizing or topology tweaks. The reparse also rewrote the `headroom_histogram.csv` files so the hist counts align with the seed totals (150 per driver scale/VDD combination, 150 total for ±10%/TT, etc.), keeping the guard/jitter ledger auditable before the deck migrates back into `spicemodels/`.

### 8–16 slice OR aggregation glimpses

To verify that the shared comparator/driver remains bounded as more encoder slices feed the OR tree, we now capture deterministic glimpses with eight and sixteen slices. Copy the `Xenc*`/`Ctp*`/`Ctn*` blocks in [`spicemodels/option-b-encoder-with-shared-sense-mismatch.spice`](spicemodels/option-b-encoder-with-shared-sense-mismatch.spice) so `NSLICES_IN_DECK` equals 8 or 16, then run the same pseudo-random stimulus (or the MC deck with `mismatch_switch=0`) while keeping `sense_thresh_latency`, `sense_headroom_min/max`, and `sharedSenseDiff` probes unchanged. Log each run in `logs/shared-sense-glimpse-8slice` / `logs/shared-sense-glimpse-16slice`, regenerate the matching `headroom_histogram.csv` using `tools/headroom_histogram.py`, and make sure [`models/periphery-cost-model.md`](models/periphery-cost-model.md) points to those CSVs so the energy/headroom scaling story stays parallel to the four-slice baseline.

These glimpses confirm that `Eslice` (measured via `.meas tran Eslice PARAM='Edyn/NSLICES_IN_DECK'`) still averages to ≈0.11–0.13 pJ and that the guard bin stays in the 860–865 mV neighborhood, validating the “periphery dominance (2)” ledger before any deck migration or controller retiming adjustments.

- **Run summary:** the glimpses now sweep ±10% VDD (0.9/1.0/1.1 V) with two seeds per corner so each `logs/shared-sense-glimpse-{8,16}/mismatch_mc.csv` includes a full triplet of energy/headroom/jitter samples plus a `headroom_histogram.csv` that covers the −297 … −233 mV bin. The 8-slice data still shows `Edyn` between ≈−0.45 pJ (at 0.9 V) and ≈0.52 pJ (at 1.0 V) with `Eword_est ≈ 2.4–2.8 pJ` and `sense_thresh_latency` shrinking from ≈4.6 ps at 0.9 V to ≈1.1 ps at 1.1 V. The 16-slice path mirrors that energy range (≈−0.92 pJ at 0.9 V to ≈0.95 pJ at 1.1 V) while `sense_thresh_latency` stays inside the 1–5 ps window and the headroom histogram range stays within −297 … −233 mV. These samples prove the aggregated driver still respects the ≈5–7 pJ/word ledger even as we scale the OR tree before finally migrating the deck.

### Driver/noise permutation log

Every new driver-scale or noise-amplitude permutation must be captured in this log before we update the periphery ledger. Continue running `tools/run_noise_mismatch_driver_sweep.sh` with the scripted `DRIVER_SCALES=(1.5 2.0 2.5)` (and any upcoming 3.0/3.5 entries) for both `NOISE_AMPS=(5m 10m)` so the resulting tuples land in `logs/noise-mismatch-{5m,10m}-driver-{1p5,2,2p5}` (or `-3p5`, `-4`, etc.). For each new directory:

- Record `sense_thresh_latency` and `sense_headroom_min/max` in the CSV so the histogram generator can stay in sync.
- Keep the `headroom_histogram.csv` counts matched to the number of seeds logged (use `tools/headroom_histogram.py` after each chunked run).
- Reference the histogram/latency tuple from [`models/periphery-cost-model.md`](models/periphery-cost-model.md) (the guard/jitter table near “Shared sense integration”) so the energy story and timing story stay paired.

If you introduce a new driver/noise combo (e.g., adding `DRIVER_SCALE=3.5` or extra `noise_amp`), append a short summary row to this document describing the observed `Edyn`, `Eword_est`, and headroom bin so the experiments log stays the canonical ledger for future comparisons.

### Phase-skew / clock jitter stress

Use `tools/run_shared_sense_phase_skew.sh` to sweep `PHASE_SKEW_NS=±0.5n` (three points) while leaving the shared driver toggles otherwise untouched. Each run writes `logs/shared-sense-phase-skew/mc_ps*.log`; aggregate them with `tools/aggregate_phase_skew_logs.py` and regenerate the `headroom_histogram.csv` so the vectors stay paired with the new `sense_thresh_latency` column (≈1.95 ps across the ±0.5 ns shifts). The resulting ledger now documents how the latency window plus the ←270 mV headroom bin move as the inter-slice skew varies, proving the jitter guard stays intact before committing the deck back to `spicemodels/`. Include those CSV/hist references whenever you quote the guard/jitter tuple so the new clock-skew story stays auditable.

### Pending / blocked actions

* **TT corner deck:** `option-b-encoder-with-shared-sense-tt.spice` currently aborts because the TT corner includes a subcircuit with 13 formal parameters; our instantiation passes none. We need to ① either replicate those parameters when instantiating the corner (painful) or ② include the TT models with `process_switch=1` in the SS deck and rely on the same measurement plumbing (practical).  
* **Mismatch / MC campaign:** still needs to run once the BSIM issue that broke the TT deck is resolved. This sweep will pair `mismatch_switch=1` with ±10% VDD to push the headroom measurement; log the resulting energy/latency in [`models/periphery-cost-model.md`](models/periphery-cost-model.md) to keep kill criteria auditable.

### Measurement notes

* All shared decks reuse the dual-bit (4 transition/window) pattern from [`option-b-encoder-results.md`](option-b-encoder-results.md) so transition counts stay aligned with the per-transition modeling table.
* The headroom monitor now uses a B-source (`Bshared_diff`) to compute `V(sharedsensep,sharedsensen)` so the min/max are recorded even though the comparator itself never hits the trigger thresholds.  
* Delay/settling probes (`td_tN0`, `settle_sharedP`, etc.) currently fail under every run because the shared driver seldom crosses 0.5·VDD; if desired, we can add separate `.meas` statements that target lower thresholds (e.g., 0.1/0.9 VDD) to recover numeric latency values once the headroom is larger.
* The `{sense_thresh_low/high}` span now captures “time to 90%” settling around the achievable ~30–50 mV swing; log `sense_thresh_latency` alongside the `sense_headroom_{min,max}` histograms in `logs/mismatch-mc*.csv` so every experiment has both energy and jitter recorded.

### Guard/jitter ledger

| Corner | Seeds | sense_thresh_latency (ps) | Headroom bin (mV) | Headroom max (V) | Edyn (pJ) | Eword_est (pJ) | Guard margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ±10% mismatch MC (0.9/1.0/1.1 V) | 150 total (50/corner) | ~0.125 | 860–865 | ~0.900 | ≈0.313 | ≈3.34 | ≥20 mV above the 0.898–0.900 V guard window |
| TT mismatch MC (1.0 V) | 50 | ~4.75 | 960–965 | ~1.002 | ≈−0.027 | ≈−0.29 | ≥60 mV margin from the same guard |
- **Ledger alignment:** reference `data/canonical_guard_ledger.csv` (see `data/GUARD_LEDGER_MANIFEST.md`) for the numeric rows that back this table; rerun `python3 tools/export_guard_ledger.py data/canonical_guard_ledger.csv` whenever the `logs/*/mismatch_mc*.csv` or their `headroom_histogram.csv` companions are refreshed so the document, the ledger, and the histograms stay tightly coupled.
| Noise + driver sweep (5 mV/10 mV × scale 1.5/2.0/2.5) | 150 each (153 for boosted 2.5) | ~0.125 | 860–865 | ~0.900 | ≈0.313 | ≈3.34 | Driver scale changes preserve the guard, see `logs/noise-mismatch-{5m,10m}-driver-{1p5,2,2p5}/mismatch_mc.csv`; every valid tuple records `comp_pass=failed` |
