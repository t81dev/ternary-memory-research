# AGENTS

This file documents instructions for future agents working on ternary-memory-research.

Every agent should:
1. Respect the guard ledger workflow: regenerate `data/canonical_guard_ledger.csv` via `python3 tools/export_guard_ledger.py data/canonical_guard_ledger.csv` whenever any `logs/*/mismatch_mc*.csv` or `logs/*/headroom_histogram.csv` changes.
2. After regenerating the ledger, run `python3 tools/guard_data.py catalog`, `python3 tools/guard_data.py status`, and `python3 tools/guard_data.py failures` so the catalog, status summary, and comparator-failure slice stay current.
3. Ensure `tools/check_guard_consistency.py` exits cleanly before committing; it verifies every ledger row matches existing CSVs and histograms.
4. Update the documentation pointers (`README.md`, `STATUS.md`, `SUMMARY.md`, `FINDINGS.md`, `models/periphery-cost-model.md`, `experiments/shared-sense-periphery.md`) whenever the guard story changes, always referencing `data/canonical_guard_ledger.csv` and the generated status/catalog/failure outputs.
5. Maintain `.gitignore` rules around large logs (e.g., `logs/archive/`, `logs/noise-mismatch-5m-driver-1p5-delta-0m/*.log`) so generated artifacts stay out of Git history.

If any instruction conflicts with higher-level policies (system/developer), follow the higher-level instruction.
