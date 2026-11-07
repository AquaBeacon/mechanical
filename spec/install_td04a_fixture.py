"""Install the shared TD04A fixture in the two current exterior placements.

Does not use the rejected sensor body. Sensor hardware assumes a 3 mm ear.
Run after rebuilding the common bracket; regenerate assembly outputs afterwards.
"""
from pathlib import Path
import copy
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]

def main():
    fixture = json.loads((ROOT/'assemblies/td04a_fixture/placement.json').read_text(encoding='utf8'))
    for unit, name, origin, rotation in [
        ('parent', 'parent_exterior', [53, -55, -20], [0, 0, -90]),
        ('child', 'child_horizontal_plate_frame', [122, -74, 108], [0, 0, 0]),
    ]:
        folder = ROOT/'assemblies'/name
        history = folder/'_work/analysis/td04a_cable_r6/history'
        history.mkdir(parents=True, exist_ok=True)
        for rel in ['placement.json', 'README.md', 'print_config.json', 'parts/manifest.json', 'parts/PRINT.md']:
            src = folder/rel
            dst = history/rel
            if src.exists() and not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        path = folder/'placement.json'
        data = json.loads(path.read_text(encoding='utf8'))
        removed = {'sensor_carrier', 'td_bracket_jaw', 'td04a_actual_shape_reference', 'td_screw_37', 'td_screw_73'} if unit == 'parent' else set()
        data['items'] = [row for row in data['items'] if row['label'] not in removed and not row['label'].startswith('td04a_r6_')]
        for row in data['items']:
            if unit == 'parent' and row['label'].startswith('carrier_washer_'):
                row['ops'][0]['translate'][2] = -26
            if unit == 'parent' and row['label'].startswith('carrier_nut_'):
                row['ops'][0]['translate'][2] = -30
        variant = next(v for v in fixture['fixture_variants'] if v['unit'] == unit)
        for source in fixture['items']:
            if source['group'] != unit:
                continue
            row = copy.deepcopy(source)
            row['label'] = 'td04a_r6_' + row['label']
            row['group'] = 'exterior' if source['label'].endswith('_strap') else 'hardware'
            row['ops'] = [{'translate': origin}, {'rotate': rotation},
                          {'translate': [-n for n in variant['origin_mm']]}] + row['ops']
            row['note'] = 'Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.'
            data['items'].append(row)
        data['td04a_revision'] = 'cable_clearance_r6'
        data['td04a_limits'] = 'Nominal 12 mm approximate hole pitch; real body/cable/ear fit and strength unverified.'
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf8')

if __name__ == '__main__':
    main()
