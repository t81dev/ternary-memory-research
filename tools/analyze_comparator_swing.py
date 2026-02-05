import csv
from pathlib import Path

def get_csvs(root):
    return sorted(Path(root).rglob('mismatch_mc.csv'))

for csv_path in get_csvs('logs'):
    values = []
    with open(csv_path) as f:
        reader = csv.DictReader(line for line in f if not line.startswith('#'))
        for row in reader:
            try:
                sense_min = float(row['sense_min'])
                sense_max = float(row['sense_max'])
            except KeyError:
                continue
            values.append(sense_max - sense_min)
    if not values:
        continue
    avg = sum(values) / len(values)
    print(f"{csv_path.relative_to('.')}: {len(values)} samples, avg swing {avg*1000:.2f} mV, max {max(values)*1000:.2f} mV, min {min(values)*1000:.2f} mV")
