#!/usr/bin/env python3
from pathlib import Path
import csv
import math
import sys


def load_sense_min(csv_path):
    values = []
    with open(csv_path) as f:
        filtered = (line for line in f if not line.lstrip().startswith("#"))
        reader = csv.DictReader(filtered)
        for row in reader:
            try:
                values.append(float(row["sense_min"]) * 1000.0)
            except (KeyError, ValueError):
                continue
    return values


def make_bins(data, bin_width=5):
    if not data:
        raise SystemExit("No headroom data to histogram.")
    min_val = math.floor(min(data) / bin_width) * bin_width
    max_val = math.ceil(max(data) / bin_width) * bin_width
    if max_val == min_val:
        max_val += bin_width
    bins = list(range(int(min_val), int(max_val) + bin_width, bin_width))
    return bins


def bucket_counts(data, bins):
    counts = [0] * (len(bins) - 1)
    for val in data:
        for idx in range(len(bins) - 1):
            low = bins[idx]
            high = bins[idx + 1]
            if idx == len(bins) - 2:
                if low <= val <= high:
                    counts[idx] += 1
                    break
            elif low <= val < high:
                counts[idx] += 1
                break
    return counts


def write_histogram(bins, counts, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["bin_lower_mV", "bin_upper_mV", "count"])
        for idx, count in enumerate(counts):
            writer.writerow([bins[idx], bins[idx + 1], count])


def main():
    if len(sys.argv) != 3:
        print("Usage: headroom_histogram.py <data.csv> <out.csv>")
        sys.exit(1)
    data_csv = Path(sys.argv[1])
    out_csv = Path(sys.argv[2])

    values = load_sense_min(data_csv)
    if not values:
        raise SystemExit("No sense_min entries found.")

    bins = make_bins(values)
    counts = bucket_counts(values, bins)
    write_histogram(bins, counts, out_csv)

    print(f"{len(values)} samples -> min {min(values):.2f} mV, max {max(values):.2f} mV")
    print(f"Histogram written to {out_csv}")


if __name__ == "__main__":
    main()
