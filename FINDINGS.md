# Findings

## Scoreboard
- Candidates 1–3 are still the reference failures while Option B remains the only conditional survivor (see the Status/kill table in `models/ternary-cell-candidates.md:7-105`). The documentation still flags the hybrid binary interface as surviving only once the headroom/latency ledger proves the shared-sense driver and encoder energy do not violate periphery dominance (models/ternary-cell-candidates.md:82-105).
- CNTFET/GNRFET explorations (candidates 5–8) stay deferred for device/tooling reasons, so no additional cells have graduated from their reference status (models/ternary-cell-candidates.md:107-155).

## Measurements & tests
- Ran `./tools/run_shared_mismatch_mc.sh` to resume the ±10% mismatch sweep and regenerate `logs/mismatch-mc/mismatch_mc.csv`; the first 18 entries at 0.9 V are populated but the new `sense_thresh_latency` column still shows `failed` because the guard never crosses the 0.898–0.900 V window (`logs/mismatch-mc/mismatch_mc.csv:1-20`). The driver headroom histogram landed in `logs/mismatch-mc/headroom_histogram.csv:1-2` with the earlier samples clustered at 895–900 mV.
- The per-corner log `logs/mismatch-mc/mc_0.9V_1.log:235-236` still records `sense_thresh_latency  trig(TRIG) ... failed`, confirming the `ttime("v(sharedDriveDiff)",…)` probe is not finding the pair of thresholds yet; the same failure stays in each of the ngspice runs because the shared-drive differential never meets the guard.
- A background launch of `./tools/run_tt_mismatch_mc.sh` was started to capture the TT corner but the process was killed once the Sense circuit log files began accumulating (no completed TT CSV reached disk), so the TT latency histogram still needs to be rebuilt once the guard measurement is solved.
- Manual runs such as `ngspice -b spicemodels/option-b-encoder-with-shared-sense-mismatch.spice -o logs/mismatch-mc/mc_0.9V_1.log` were repeated to exercise the new `ttime` measurement; every single log still terminates early because the guard never triggers the threshold pair.

## Libraries & dependencies
- All shared-sense decks include the SkyWater models from `/Users/t81dev/Code/pdk/sky130A/libs.ref/sky130_fd_pr/…` (`spicemodels/option-b-encoder-with-shared-sense-mismatch.spice:63-66`), so maintenance of the mismatch switches and zeroed slope knobs is still required for every run.

## Next steps
1. Re-target the latency probe so it captures an actual low-to-high swing (either by forcing the sharedDriveDiff node below `sense_latency_low` before measurement, injecting a controlled settling step, or widening the `sense_latency_*` window) and rerun the ±10%/TT sweeps until the `sense_thresh_latency` column populates with numeric jitter values.
2. Once that column and the headroom histogram are stable, append the new tuples to `models/periphery-cost-model.md`, `STATUS.md`, and `SUMMARY.md` and update `FINDINGS.md` with the actual latency numbers so energy + jitter remain bundled before the deck migrates into `spicemodels/`.
