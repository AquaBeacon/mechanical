"""Render the active t200 variant and newly used M3x16 purchased fastener only."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OSC = Path(r'C:\Program Files\OpenSCAD\openscad.exe')
LOGS = ROOT / 'assemblies/child_interior/_work/logs'
LOGS.mkdir(parents=True, exist_ok=True)
jobs = [
    ('parts/child/interior/printed/child_vtray_deck/child_vtray_deck.scad',
     'parts/child/interior/printed/child_vtray_deck/child_vtray_deck_t200.stl',
     ['-D', 'tube_len=200']),
    ('parts/common/interior/cots/screw/screw.scad',
     'parts/common/interior/cots/screw/screw_m3x16.stl',
     ['-D', 'd=3', '-D', 'l=16', '-D', 'head_d=5.5', '-D', 'head_h=2']),
    ('spec/child_interior_reinforcement/pla_matte_lever/root_dense_modifier.scad',
     'spec/child_interior_reinforcement/pla_matte_lever/root_dense_modifier.stl', []),
]
for name in ['child_vtray_batt_box', 'child_vtray_batt_floor', 'child_flange_brace']:
    relative = 'parts/child/interior/printed/' + name + '/' + name
    jobs.append((relative + '.scad', relative + '.stl', []))
for source, output, defs in jobs:
    with (LOGS / (Path(output).stem + '_bolted_render.log')).open('w', encoding='utf-8') as log:
        subprocess.run([str(OSC), *defs, '-o', str(ROOT / output), str(ROOT / source)],
                       stdout=log, stderr=log, check=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    print(output, flush=True)
