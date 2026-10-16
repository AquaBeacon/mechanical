"""Migrate the visual concept to a shared guard / ballast opening assembly."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assemblies/child_exterior_concept'
PART = ROOT / 'parts/child/exterior/printed/child_exterior_open_frame'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def write(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    history = OUT / '_work/intermediate/before_shared_guard_motion'
    history.mkdir(parents=True, exist_ok=True)
    for p in [OUT/'placement.json', OUT/'child_exterior_concept.blend', PART/'concept.json']:
        if not (history/p.name).exists():
            shutil.copy2(p, history/p.name)
    p, c = read(history/'placement.json'), read(history/'concept.json')
    params = read(ROOT/'parts/child/exterior/printed/child_endcap_guard/parameters.json')
    p['hinge']['pivot_world_mm'] = [params['hinge_y'], 0, -14-params['hinge_z']]
    p['hinge']['moving_labels'] = [r['label'] for r in p['items'] if r['group'] in
                                  ['Hinged cable guard', 'Frame B', 'Ballast B', 'Ballast C']]
    p['hinge']['preview_frames'] = [1,8,15,22,29,36,43,50]
    p['revision'] = 'Guard, bottom frame B and all ballast rotate together; wider A and upper-half C'
    for key in ['frame_a_lower', 'frame_a_upper']:
        s = c['variants'][key]
        s['size_mm'][1] = 260
        s['lap_cut']['size_mm'][1] = 280
        s['mounting_webs']['size_mm'][1] = 236
        for w in s['windows']:
            w['size_mm'][1] = 214
    # An open-bottom service slot lets the hinged assembly sweep through A.
    c['variants']['frame_a_lower']['windows'][0].update(
        center_mm=[0,0,-74], size_mm=[40,214,178])
    c['variants']['frame_c']['size_mm'][2] = 188
    c['variants']['frame_c']['windows'] = [dict(center_mm=[0,0,6], size_mm=[182,40,136])]
    # Extend the existing fixed cradle neck to the current reference hinge.
    c['variants']['integrated_clamps']['spines'][3].update(
        center_mm=[0,-108.5,9], size_mm=[36,61,14])
    c['variants']['guard_b_link'] = dict(kind='bar', size_mm=[14,12,24], bevel_mm=1,
        note='Visual coupling only; fixing holes and load path unverified')
    for sign in [-1,1]:
        label='guard_b_link_'+str(sign)
        p['items'].append(dict(label=label,
            part='parts/child/exterior/printed/child_exterior_open_frame', file='guard_b_link',
            group='Guard B coupling', material='guard', geometry='concept', print=False,
            ops=[{'translate':[0,sign*65,-103]}], explode_mm=[0,0,-60]))
        p['hinge']['moving_labels'].append(label)
    for r in p['items']:
        if r['group'] == 'Frame C':
            r['ops'][0]['translate'] = [0,130 if r['label']=='C_front' else -130,166]
        elif r['group'] in ['Cameras','Equipment mounts','Upward lights','Transducer','Transducer mount']:
            xyz=r['ops'][0]['translate']
            xyz[1] += 20 if xyz[1]>0 else -20
            if r['group'] in ['Cameras','Equipment mounts']:
                xyz[2] += 28
        if r['group']=='Fixed hinge and pin' and r['label']!='hinge_reference':
            r['ops'][3]['translate'][1] = params['hinge_y']
    for route in p['cable_routes']:
        for xyz in route['points_mm']:
            if abs(xyz[1])>=57.5:
                xyz[1] += 20 if xyz[1]>0 else -20
        route['ties_mm'] = [[x,y+(20 if y>0 else -20),z] for x,y,z in route['ties_mm'] if z>=78]
    p['hinge']['note'] = 'Visual rigid linkage; guard-to-B brackets and load-bearing hinge are not fabrication designs.'
    write(OUT/'placement.json',p)
    write(PART/'concept.json',c)

if __name__ == '__main__':
    main()
