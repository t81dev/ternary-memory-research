# Guard status

- Ledger: `data/canonical_guard_ledger.csv` (2239 rows covering 17 experiments, 2024 failures).
- Headroom range: -296.887 mV to 1281.925 mV.
- Sense threshold latency median: 0.125 ps.

## Top experiments by sample count

| Experiment | Samples |
| --- | --- |
| Noise sweep 10m / driver 2.50× | 497 |
| Noise sweep 10m | 150 |
| Noise sweep 10m / driver 1.50× | 150 |
| Noise sweep 10m / driver 2.00× | 150 |
| Noise sweep 10m / driver 3.50× | 150 |

## Notes

- Run `python3 tools/guard_data.py status` to refresh this summary whenever the ledger changes.
- See `data/comparator_failures.csv` for every `comp_pass=failed` sample that the ledger records.