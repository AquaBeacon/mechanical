"""Check the actual gate mesh's flat bearing faces and latch clearance.

Run from the Body_Models root: python scad/lib/verify_child_frame2_latch.py
The nominal head is an envelope, not a confirmed purchased fastener.
"""
import json
import re
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[2]
PART = ROOT / "parts/child/exterior/printed/child_jaw_gate/child_jaw_gate"
source = PART.with_suffix(".scad").read_text(encoding="utf-8")


def value(name):
    return float(re.search(rf"^\s*{name}\s*=\s*([-\d.]+)\s*;", source, re.M)[1])


x, y, radius = value("latch_hx"), value("boss_y1"), value("knob_head_d") / 2
tube_r = value("tube_od") / 2
eva_r = tube_r + value("eva_t") - value("eva_comp")
clearance = float(np.hypot(x - radius, y) - eva_r)
assert clearance >= value("knob_clearance"), clearance
core = (ROOT / "parts/child/exterior/printed/child_core_frame/child_core_frame.scad").read_text(encoding="utf-8")
assert float(re.search(r"latch_hx\s*=\s*([\d.]+)", core)[1]) == x
zs = json.loads(re.search(r"latch_z\s*=\s*(\[[^;]+\])", source)[1])
assert zs == json.loads(re.search(r"latch_z\s*=\s*(\[[^;]+\])", core)[1])
mesh = trimesh.load(PART.with_suffix(".stl"), force="mesh")
assert mesh.is_watertight and mesh.is_volume
assert len(mesh.split()) == 1
theta = np.linspace(0, 2 * np.pi, 180, endpoint=False)
# Probe the bearing annulus immediately behind and in front of each face.
# Radial lower bound clears the nominal shaft hole including tessellation.
for z in zs:
    probes = np.array([[x + r*np.cos(t), y - 0.05, z + r*np.sin(t)]
                       for r in np.linspace(value("m5_d")/2 + 0.2, radius, 12)
                       for t in theta])
    assert mesh.contains(probes).all(), f"Incomplete flat bearing face at z={z}"
    probes[:, 1] = y + 0.05
    assert not mesh.contains(probes).any(), f"Obstructed head seat at z={z}"
    shaft = np.array([[x, yy, z] for yy in np.linspace(0.05, y + 1, 100)])
    assert not mesh.contains(shaft).any(), f"Blocked screw bore at z={z}"
report = dict(watertight=True, solids=1, volume_cm3=mesh.volume/1000,
              bounds_mm=mesh.bounds.tolist(), head_to_eva_mm=clearance,
              head_to_tube_mm=float(np.hypot(x-radius, y)-tube_r),
              bearing_probe_count_per_seat=len(probes), latch_axes_match=True,
              note="Nominal diameter 16 mm; hardware dimensions and strength require validation")
out = ROOT / "assemblies/child_frame2_assembly/review_20260909/latch_check.json"
out.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
