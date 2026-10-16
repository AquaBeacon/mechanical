"""Read-only clearance probe for the coplanar sensor fixture revision."""
from parent_access_common import *
import sys
sys.path.insert(0, str(R/'scad/lib'))
import parent_gnss as G

d, c = load()
mag = c['magnetometer'].copy()
mag.translate(v(0, 0, -20))
rails = Part.makeBox(5.8, 26.12, 4, v(44.64, 194.64, 51.5))
for y in [197.54, 217.86]:
    rails = rails.fuse(Part.makeBox(27.36, 5.8, 4, v(44.64, y-2.9, 51.5)))
rails = rails.fuse(Part.makeBox(5.8, 26.12, 4, v(57.34, 194.64, 51.5)))
exclude = ['magnetometer', 'gnss_universal_carrier'] + [n for n in c if n.startswith(('mag_bolt_', 'mag_nut_'))]
report = {'sensor_at_Z56': collisions(mag, c, exclude), 'coplanar_rails': collisions(rails, c, exclude)}
out = O/'_work/analysis/sensor_mounts_20261011'
out.mkdir(parents=True, exist_ok=True)
(out/'probe.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report), flush=True)
