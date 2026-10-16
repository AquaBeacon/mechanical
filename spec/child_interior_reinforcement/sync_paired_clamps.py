"""Use paired RX clamps without moving existing board or fastener interfaces."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for assembly in ('child_interior', 'child_vertical_assembly'):
    path = ROOT / 'assemblies' / assembly / 'placement.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    items = data['items']
    old = [i for i in items if i['part'].endswith('/child_rx_edge_clamp')]
    if len(old) == 4 and all(i.get('file', '').endswith('_pair') for i in old):
        continue
    assert len(old) == 8, 'Unexpected clamp layout; inspect before migrating'
    for side in (-1, 1):
        for kind in ('base', 'cap'):
            lower = next(i for i in old if i['label'] == f'rx_clamp_{kind}_{side}_140.5')
            upper = next(i for i in old if i['label'] == f'rx_clamp_{kind}_{side}_174.5')
            assert lower['ops'] == [{'translate': [0, 0, 140.5]}, {'scale': [side, 1, -1]}]
            assert upper['ops'] == [{'translate': [0, 0, 174.5]}, {'scale': [side, 1, 1]}]
            lower['file'] = f'child_rx_edge_clamp_{kind}_pair'
            lower['label'] = f'rx_clamp_{kind}_pair_{side}'
            lower['ops'] = [{'translate': [0, 0, 140.5]}, {'scale': [side, 1, 1]}]
            lower['note'] = 'Paired RX clamp: original Z140.5/174.5 contacts and screw axes retained; bridge outside PCB'
            items.remove(upper)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Updated', assembly)
