"""Replace the four current MF bodies; preserve canonical placement transforms.

The SCAD is the design source. This script only updates placement/manufacturing
references and is idempotent. Never run historical sync_child_interior.py.
"""
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PART = 'parts/child/interior/printed/child_spacer_set'
STUD = 'parts/common/interior/cots/threaded_stud'
SPEC = {'flange_spacer_p': (10, 26, 4), 'flange_spacer_n': (10, 26, 4),
        'brace_spacer_l': (30, 45, 6), 'brace_spacer_r': (12, 30, 6)}
SUMMARY = '2026-10-21 clearance revision: AF5.5 hex spacers, inscribed 3.5 mm through-bores; flange M3x26 pan x2, brace M3x30/M3x45 studs and two M3 nuts; no spacer tapping.'


def apply(data):
    retired={'flange_screw_p','flange_screw_n','brace_screw_l','brace_screw_r'}
    data['items'] = [i for i in data['items'] if not i['label'].startswith(('spacer_stud_','spacer_nut_')) and i['label'] not in retired]
    studs = []
    for item in data['items']:
        label = item['label']
        if label in SPEC:
            length, stud_length, protrusion = SPEC[label]
            item.update(part=PART, file=f'child_spacer_set_body{length}', color='Orange',
                        print=False, note=f'AF5.5 printed hex slip spacer {length} mm; inscribed 3.5 mm bore, no tapping. Print with child_spacer_set_set; through-stud projects {protrusion} mm below seat.')
            if label.startswith('flange_'):
                item['note']='AF5.5 hex slip spacer 10 mm, inscribed 3.5 mm bore; M3x26 pan screw passes through 12 mm seat and body into flange 4 mm. No tapping.'
                studs.append(dict(label='flange_screw_'+label[-1],part='parts/common/interior/cots/screw',
                    file='screw_m3x26',group='interior',color='Silver',alpha=1,
                    ops=copy.deepcopy(item['ops'])+[{'translate':[0,0,length+12]}],
                    skip_envelope=True,note='M3 pan screw under-head length 26 mm: seat12 + spacer10 + flange engagement4. Cut M3x30 to 26 mm and deburr if needed.'))
                continue
            # +Z cylinder, lower end protrudes below body Z0; transformations are nested.
            studs.append(dict(label='spacer_stud_'+label, part=STUD,
                file=f'threaded_stud_m3x{stud_length}', group='interior', color='Silver', alpha=1,
                ops=copy.deepcopy(item['ops'])+[{'translate':[0,0,-protrusion]}],
                note=f'Metal M3x{stud_length} through-stud; lower projection {protrusion} mm, slides through spacer; upper M3 nut, do not print.',
                skip_envelope=item.get('skip_envelope',False)))
            seat=12 if label.startswith('flange_') else 5.5
            studs.append(dict(label='spacer_nut_'+label,part='parts/common/interior/cots/screw',
                file='screw_nut_m3',group='interior',color='Silver',alpha=1,
                ops=copy.deepcopy(item['ops'])+[{'translate':[0,0,length+seat]}],
                note='Plain metal M3 nut AF5.5/t2.4 on the through-stud. Spacer is a slip sleeve; no printed thread.'))
        elif label=='flange_brace':
            item['note']='Printed brace; existing seating planes retained, hex slip spacers, metal through-studs and M3 nuts.'
    assert {i['label'] for i in data['items']} >= set(SPEC)
    data['items'] += studs
    if not data.get('note','').startswith(SUMMARY):
        data['note']=SUMMARY+'\n'+data.get('note','')
    return data


def main():
    for name in ('child_interior','child_vertical_assembly'):
        path=ROOT/'assemblies'/name/'placement.json'
        data=apply(json.loads(path.read_text(encoding='utf-8')))
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        config_path=path.parent/'print_config.json'
        config=json.loads(config_path.read_text(encoding='utf-8'))
        config['extra_parts']=[i for i in config.get('extra_parts',[]) if i['part']!=PART]+[
            dict(part=PART,file='child_spacer_set_set',quantity=1,labels=['spacer_bodies_10x2_12x1_30x1'])]
        doc=PART+'/child_spacer_set.md'
        if doc not in config.setdefault('notes',[]):config['notes'].append(doc)
        if not config.get('note','').startswith(SUMMARY):
            previous=config.get('note','')
            battery=previous[previous.index('電池ナット締結'):] if '電池ナット締結' in previous else ''
            config['note']=SUMMARY+'\n\nスペーサは child_spacer_set_set.stl を1セット印刷（10 mm×2、12 mm×1、30 mm×1）。外側AF5.5の六角、内接径3.5 mmのM3滑り穴、タップ不要。PETG／0.4 mmノズル／0.2 mm積層／壁4周／100%充填。幅0.8×厚0.4 mmのつなぎを冷却後に折り、跡を除く。左右フランジは首下26 mmのM3なべねじ2本（必要ならM3×30を26 mmに切断・面取り）。ブレースは金属M3×30／×45通しスタッド各1本と普通M3ナット2個で固定。旧短スタッドと旧上ねじ4本は使わない。実物の嵌合・締結強度は未検証。\n\n'+battery
        config_path.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(name,len(data['items']),'items; one connected spacer set')
        if name=='child_interior':
            # Refresh the existing Fusion import manifest from the same placement.
            sys.path.insert(0,str(ROOT/'scad/lib'))
            from verify_child_interior import matrix
            import numpy as np
            fusion_items=[]
            for item in data['items']:
                stem=item.get('file') or Path(item['part']).name
                geometry=ROOT/item['part']/(stem+'.step')
                if not geometry.exists():geometry=geometry.with_suffix('.stl')
                if not geometry.exists():raise FileNotFoundError(geometry)
                m=matrix(item.get('ops'))
                fusion_items.append({**{k:item[k] for k in ('label','part','group','color','alpha','note') if k in item},
                    'geometry':geometry.relative_to(ROOT).as_posix(),'geometry_abs':str(geometry.resolve()),
                    'matrix_mm':m.flatten().tolist(),'translation_mm':m[:3,3].tolist(),
                    'mirrored':bool(np.linalg.det(m[:3,:3])<0)})
            fusion=dict(assembly=data['name'],coordinate_system=data['coordinate_system'],note=data['note'],
                units='mm',source=path.relative_to(ROOT).as_posix(),items=fusion_items)
            (path.parent/'child_interior_fusion.json').write_text(json.dumps(fusion,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__': main()
