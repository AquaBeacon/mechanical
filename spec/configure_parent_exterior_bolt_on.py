"""Idempotent Rev.4 placement update; generator remains prepare_parent_oneplate.py."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assemblies/parent_exterior'
SCREWS = 'parts/common/interior/cots/screw'
LOCATORS = 'parts/parent/exterior/printed/parent_oneplate_box_locator'


def main():
    path = A / 'placement.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    data['items'] = [i for i in data['items'] if not i['label'].startswith('bolt_on_')]
    data['note'] = 'Rev.4: rectangular 232x134x20 plate; bolt-on box locators, flat-seat TD04A bracket and thickened C female adapter. Float rope eyes and all sensor coordinates retained.'
    data['coordinate_system'] = 'Box datums Z=0; plate top -0.8, underside -20; TD bracket unchanged Z=-35; C interface Z=-30; ground -72.'

    def add(label, part, file, xyz=None, rot=None, group='hardware'):
        ops = [] if xyz is None else [{'translate': xyz}]
        if rot:
            ops.append({'rotate': rot})
        data['items'].append(dict(label='bolt_on_'+label, part=part, file=file,
                                  ops=ops, group=group,
                                  color='Silver' if group=='hardware' else 'MediumSeaGreen'))

    for variant in ('side_left', 'side_right', 'end_fixed', 'end_push'):
        add(variant, LOCATORS, 'parent_oneplate_box_locator_'+variant, group='exterior')
    for x in (-110, 110):
        for y in (-8, 8):
            # ef_cut extends blind pockets by 0.1 mm; seat hardware on the
            # exported floors, rather than leave a nominal 0.1 mm air gap.
            add(f'side_bolt_{x}_{y}', SCREWS, 'screw_m4x20_socket', [x,y,1.3])
            add(f'side_nut_{x}_{y}', SCREWS, 'screw_nut_m4', [x,y,-15.5])
    for s in (-1,1):
        for y in (52,62):
            add(f'end_bolt_{s}_{y}', SCREWS, 'screw_m4x20_socket', [s*94,s*y,-22.3], [180,0,0])
            add(f'end_nut_{s}_{y}', SCREWS, 'screw_nut_m4', [s*94,s*y,-7.3])

    for i in data['items']:
        label = i['label']
        if i.get('file')=='nut_M5':
            # Replace the inherited six-sided INNER-hole proxy with the shared
            # ordinary M5 nut (AF8 x 4), maintaining its washer bearing face.
            i.update(part=SCREWS,file='screw_nut_m5_4')
            if label.startswith('nut_') and i['ops'][0]['translate'][2]<0:
                i['ops'][0]['translate'][2]=-35
        if label.startswith('qr_female_nut_'):
            i['ops'][0]['translate'][2] = -6.5
        if label.startswith('qr_female_bolt_'):
            i['ops'][0]['translate'][2] = -27.4
        if label.startswith('carrier_screw_'):
            i.update(part=SCREWS, file='screw_m5x40_flat')
            i['ops'][0]['translate'][2] = -0.8
        if label.startswith('carrier_washer_'):
            i['ops'][0]['translate'][2] = -29
        if label.startswith('carrier_nut_'):
            i['ops'][0]['translate'][2] = -33
        if label.startswith('locating_camera_adjust_bolt_'):
            i['file']='screw_m4x8_socket'
            # Same tip Z=36.5 in mount coordinates; head rises clear of the
            # perpendicular bridge bolt/nut without altering camera contact.
            i['ops'][2]['translate'][2]=28.5
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    config = dict(status='prototype_bolt_on_plate', note=(
        'Rev.4: 平板と別体治具。PETG Basic・X1 Carbon・0.4 mmノズル・8壁・100%充填・3 mmブリム。'
        'QRは0.1 mm層、他0.2 mm層。現行STLは本parts内。変更前のprint_jobs/qr_standing/とrepeatable_mount/は履歴で現行形状に使用しない。'
        '現行の変更部品スライスはprint_jobs/bolt_on_plate/を参照。実締結・嵌合・クリープ・浮力は未認定。'
        '平板下面のロープ耳、TD支持、端面治具の座ぐりは外部から除去可能なサポートを確認。側面治具は脚より先に締結。'))
    config["note"] += ' camera_mountは背板から23 mmの左右受けを設けた改良版を1個。単体検証済み設定はGeneric PETG・0.20 mm・6壁・Gyroid 15%・3 mmブリム・底板下・サポートなし。専用3MFはprint_jobs/camera_mount_rear_support/。'
    (A/'print_config.json').write_text(json.dumps(config, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    variants = ROOT/SCREWS/'variants.txt'
    text = variants.read_text(encoding='utf-8-sig')
    if not any(line.startswith('m5x40_flat ') for line in text.splitlines()):
        text=text.rstrip()+'\n# Rev.4 TD04A support: purchased countersunk screw, overall length includes head\nm5x40_flat kind="flat" d=5 l=40 head_d=10 head_h=2.5\n'
    if not any(line.startswith('m4x8_socket ') for line in text.splitlines()):
        text=text.rstrip()+'\n# Camera angle adjuster: same tip, shorter shaft, standard socket head\nm4x8_socket d=4 l=8 head_d=7 head_h=4\n'
    variants.write_text(text,encoding='utf-8')
    print('Configured Rev.4 bolt-on fixtures and hardware.')


if __name__ == '__main__':
    main()
