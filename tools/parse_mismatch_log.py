#!/usr/bin/env python3
import sys
KEYS = ['edyn','eword_est','sense_headroom_min','sense_headroom_max']
vals = {k: '' for k in KEYS}
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        name, value = line.split('=', 1)
        name = name.strip().lower()
        if name in vals and not vals[name]:
            vals[name] = value.strip().split()[0]
print(' '.join(vals[k] for k in KEYS))
