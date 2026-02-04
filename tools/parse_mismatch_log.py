#!/usr/bin/env python3
import sys
KEYS = ['edyn','eword_est','sense_headroom_min','sense_headroom_max','sense_thresh_latency','comp_toggle_latency','comp_pass']
vals = {k: '' for k in KEYS}
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        name, value = line.split('=', 1)
        name = name.strip().lower()
        if name in vals and not vals[name]:
            token = value.strip().split()[0]
            if name == 'comp_pass':
                continue
            vals[name] = token
    comp_toggle = vals.get('comp_toggle_latency','')
    if comp_toggle and not comp_toggle.lower().startswith('failed'):
        vals['comp_pass'] = 'pass'
    else:
        vals['comp_pass'] = 'failed'
    tokens = []
    for k in KEYS:
        if k == 'comp_toggle_latency':
            tokens.append(vals[k] if vals[k] else 'failed')
        else:
            tokens.append(vals[k])
    print(' '.join(tokens))
