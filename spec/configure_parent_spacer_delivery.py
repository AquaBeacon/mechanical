"""Expose all twelve existing parent spacers as counted, individual print parts.

Run after historical CAD/metadata generators, before assembly_parts.py sync.
Only delivery metadata changes; the canonical STEP/STL solids and poses stay put.
"""
from collections import Counter
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSEMBLY = ROOT / 'assemblies/parent_hand_service'
SPACERS = {'main_corner_column': 4, 'sony_column_left': 2,
           'sony_column_right': 2, 'gnss_column_front': 2, 'gnss_column_rear': 2}
REVISION = '2026-10-22 individual spacer delivery'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def configure():
    for filename in ('placement.json', 'service_placement.json'):
        path = ASSEMBLY / filename
        data = read(path)
        members = [i for i in data['items'] if i.get('file') in SPACERS]
        assert Counter(i['file'] for i in members) == Counter(SPACERS)
        for item in members:
            item['print'] = True
            item.pop('print_set', None)
            item['note'] = ('Individual printed slip spacer; quantity comes from placement. '
                            'Metal through screw retained; do not print an additional runner set.')
        data['spacer_delivery'] = dict(revision=REVISION, mode='individual',
                                       quantities=SPACERS, separate_spacers=12)
        write(path, data)

    path = ASSEMBLY / 'print_config.json'
    config = read(path)
    config['extra_parts'] = [i for i in config.get('extra_parts', [])
                             if i['file'] != 'parent_stack_spacer_set']
    config['spacer_delivery'] = 'individual'
    note = ('2026-10-22：スペーサは種類別STLを表の個数だけ印刷する。'
            'MAIN main_corner_column（高さ14.3 mm）×4、Sony左／右各2、GNSS前／後各2、計12本。'
            '内装全体は13種類20個。旧parent_stack_spacer_setと重複印刷しない。Sony右2本は下端付きの新版へ交換する。'
            'MAIN柱の上にはmain_mount_plate（基板座一体）を載せる。'
            'PWR・TX・電池・アンテナとセンサの一体支持は既存の印刷部品に含まれる。'
            '柱は平らな下面をベッドへ、穴とキーを上向き。PETG／0.4 mmノズル／0.2 mm積層／壁4周／100%充填。'
            'Sony右の下端だけ5×9×高さ1.2 mmへ広げ、軸外径・キー・組立高さ・金属ねじは維持。'
            '12本入り設定済み3MFはprint_jobs/spacers_20261022/parent_spacers.3mf。'
            '嵌合と締付けは実印刷で確認する。')
    previous = config.get('note', '').split('\n\n2026-10-13 全長側溝版：')[-1]
    # Retain the current battery instructions without repeating previous revisions.
    if '2026-10-13 全長側溝版：' in config.get('note', ''):
        previous = '2026-10-13 全長側溝版：' + previous.split('2026-10-13 全長側溝版：')[-1]
        previous = previous.replace('9種類各1個、', '')
        config['note'] = note + '\n\n' + previous
    else:
        config['note'] = note
    reference = 'assemblies/parent_hand_service/spacer_delivery_report.md'
    config['notes'] = list(dict.fromkeys(config.get('notes', []) + [reference]))
    write(path, config)

    path = ASSEMBLY / 'manufacturing_parts.json'
    data = read(path)
    for item in data.get('additional_printed_parts', []):
        if item['file'] in SPACERS:
            item.pop('print_set', None)
    data['print_sets'] = [i for i in data.get('print_sets', [])
                          if i['file'] != 'parent_stack_spacer_set']
    data['spacer_delivery'] = dict(revision=REVISION, mode='individual', quantities=SPACERS)
    write(path, data)
    print('Configured five spacer STL types / twelve pieces from canonical CAD sources.')


if __name__ == '__main__':
    configure()
