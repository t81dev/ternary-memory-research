import math
from pathlib import Path

src = Path('spicemodels/sharedsense_comparator_strongarm.spice')
dst = Path('spicemodels/sharedsense_comparator_strongarm_boosted.spice')
text = src.read_text()
import re

params = {}
for line in text.splitlines():
    if line.strip().startswith('.param'):
        parts = line.split()
        if '=' in parts[1]:
            key, val = parts[1].split('=')
            params[key] = val

scale = 1.75

for key in ['COMP_WP','COMP_WN']:
    val = params[key]
    if val.endswith('u'):
        val_f = float(val[:-1])
        params[key] = f"{val_f*scale:.3f}u"

new_text = text
for key,val in params.items():
    new_text = re.sub(rf'(\.param {key}=)[0-9\.]+u', rf'\1{val}', new_text)

new_text += "\n* Added weak level-restoring stage\n"
new_text += "Xlr sharedDriveP sharedDriveN mid vdd 0 sky130_fd_pr__nfet_01v8  l=0.18u w=1.5u\n"
new_text += "Xlr2 mid comp_out 0 0 sky130_fd_pr__pfet_01v8  l=0.18u w=4u\n"

dst.write_text(new_text)
print('written', dst)
