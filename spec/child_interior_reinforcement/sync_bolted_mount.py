"""Apply the 2026-10-01 bolted interfaces to existing authoritative placements.

Idempotent; preserves other items and the current retired-LCD configuration.
Never run the older sync_child_interior.py to restore this revision.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCREW = 'parts/common/interior/cots/screw'


def nut(label, xyz, angle):
    return dict(label=label, part=SCREW, file='screw_nut_m3',
                group='interior', color='Silver', alpha=1.0,
                note='Purchased plain M3 nut AF5.5/t2.4; insert before cable rails',
                ops=[{'translate': xyz}, {'rotate': [angle, 0, 0]},
                     {'rotate': [0, 0, 30]}])


for name in ('child_interior', 'child_vertical_assembly'):
    path = ROOT / 'assemblies' / name / 'placement.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    summary = '2026-10-01 bolted revision: battery M3x12/nut x4, floor M3x10 flat/nut, printed broader roots, front flange M3x16. Earlier notes below are history.'
    if not data.get('note', '').startswith(summary):
        data['note'] = summary + '\n' + data.get('note', '')
    data['note'] = data['note'].replace('scad/lib/sync_child_interior.py', 'spec/child_interior_reinforcement/sync_bolted_mount.py')
    items = [i for i in data['items'] if not i['label'].startswith('bolted_nut_')]
    additions = []
    for i in items:
        label = i['label']
        if label.startswith('batt_box_screw_'):
            i['file'] = 'screw_m3x12'
            i['note'] = 'M3x12 through deck 4 mm and bay pad 8 mm; captive nut, no plastic thread'
            pos = i['ops'][0]['translate']
            additions.append(nut('bolted_nut_' + label, [pos[0], -15.5, pos[2]], 90))
        elif label == 'batt_floor_screw':
            i['file'] = 'screw_m3x10_flat'
            i['note'] = 'M3x10 flat: reinforced service tab and captive M3 nut; 1.1 mm nominal tip projection'
            additions.append(nut('bolted_nut_floor', [22.5, -36.5, 36], -90))
        elif label == 'flange_screw_y':
            i['file'] = 'screw_m3x16'
            i['note'] = 'M3x16 through 12 mm printed seat; flange engagement 4 mm, blind-hole depth respected'
        elif label == 'vtray_batt_box':
            i['note'] = 'Reinforced battery bay: four 8 mm pads, M3x12 through bolts and plain captive M3 nuts'
        elif label == 'vtray_batt_floor':
            i['note'] = '3 mm removable floor with 14 mm service tab, M3x10 flat and captive nut; slide -Z2 then withdraw -Y'
        elif label == 'vtray_deck':
            i['note'] = 't200 deck: broadened printed flange roots X28..48.7, Z20..100, bed Y-10; confirmed battery hole locations'
        elif label == 'flange_brace':
            i['note'] = 'Printed brace: 12 mm beams, 24 mm webs, 20 mm tangential flange seat, existing M3 spacers'
    data['items'] = items + additions
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(name, len(data['items']), 'items')
