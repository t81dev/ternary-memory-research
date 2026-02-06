#!/usr/bin/env python3
from pathlib import Path

import matplotlib.pyplot as plt


def read_histogram(csv_path: Path):
    bins = []
    counts = []
    with csv_path.open() as f:
        next(f)
        for line in f:
            lower, upper, count = line.strip().split(",")
            bins.append((float(lower), float(upper)))
            counts.append(int(count))
    return bins, counts


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Plot a headroom histogram.")
    parser.add_argument(
        "csv_path", type=Path, help="Headroom histogram CSV (bin_lower, bin_upper, count)"
    )
    parser.add_argument(
        "out_path", type=Path, help="Output PNG path for the plotted histogram"
    )
    args = parser.parse_args()

    bins, counts = read_histogram(args.csv_path)
    if not bins:
        raise SystemExit("No histogram data found.")

    bin_edges = [b[0] for b in bins] + [bins[-1][1]]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(
        [(b[0] + b[1]) / 2 for b in bins],
        counts,
        width=[b[1] - b[0] for b in bins],
        edgecolor="black",
        align="center",
    )
    ax.set_xlabel("Headroom (mV)")
    ax.set_ylabel("Sample count")
    ax.set_title("Shared-sense headroom distribution (8-slice glimpse)")
    ax.grid(axis="y", alpha=0.6)
    fig.tight_layout()
    args.out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out_path)


if __name__ == "__main__":
    main()
