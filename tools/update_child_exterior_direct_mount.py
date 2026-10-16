"""Correct the orientation study: direct A mounts, stationary ballast, guard-only motion."""
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
PART=ROOT/'parts/child/exterior/printed/child_exterior_open_frame'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def turn(v): return [v[1],-v[0],v[2]]
def main():
    history=OUT/'_work/intermediate/before_direct_mount_correction'
    history.mkdir(parents=True,exist_ok=True)
    for source in [OUT/'placement.json',OUT/'child_exterior_concept.blend',OUT/'README.md',PART/'concept.json']:
        if not (history/source.name).exists(): shutil.copy2(source,history/source.name)
    images=OUT/'_work/images/history/before_direct_mount_correction'
    images.mkdir(parents=True,exist_ok=True)
    for source in (OUT/'_work/images').glob('child_exterior_*'):
        if source.is_file() and not (images/source.name).exists(): shutil.copy2(source,images/source.name)
    p,c=read(history/'placement.json'),read(history/'concept.json')
    p['items']=[r for r in p['items'] if r['group']!='Guard B coupling']
    c['variants'].pop('guard_b_link',None)
    con=p['clamp_a_connection']; con.pop('spacer_span_x_mm',None)
    con.update(mode='direct_face_contact',frame_center_x_mm=91.35,frame_thickness_mm=12,
               note='A inner faces X=+/-85.35 touch existing clamp mounting pads; no spacers.')
    for h in con['holes']: h['frame_hole_world_mm'][0]=91.35 if h['axis_world_mm'][0]>0 else -91.35
    for r in p['items']:
        if r['group'] in ['Frame B','Ballast B','Ballast C','Hinged cable guard','Fixed hinge and pin','vessel']:
            r['ops']=[{'rotate':[0,0,-90]}]+r['ops']
            r['explode_mm']=turn(r.get('explode_mm',[0,0,0]))
        if r['group']=='Frame A': r['ops'][0]['translate'][0]=91.35 if 'right' in r['label'] else -91.35
        if r['group'] in ['Transducer','Transducer mount']:
            r['ops'][0]['translate'][0]-=28.65
    p['hinge'].update(pivot_world_mm=turn(p['hinge']['pivot_world_mm']),axis_world=[1,0,0],
                      moving_labels=['guard_integrated'],note='Only guard opens. B and all ballast remain fixed. Orientation changed -90 degrees about vessel Z.')
    p['revision']='Direct A-to-clamp mounting; B/ballast and guard reoriented about Z; only guard animated'
    p['notes']=[n for n in p['notes'] if not n.startswith('User correction: rotate vessel')]
    p['notes'].append('Clamps keep the X-facing pads. Vessel, guard and fixed ballast installation rotate -90 degrees about Z. Only the guard articulates; its sweep intersects fixed B/ballast.')
    c['variants']['frame_c']['size_mm'][0]=182.7
    c['variants']['frame_c']['windows'][0]['size_mm'][0]=124.7
    # Restore the lower A crossrail: the guard now exits through the C side.
    c['variants']['frame_a_lower']['windows'][0].update(center_mm=[0,0,-56],size_mm=[40,214,74])
    c['variants']['frame_b_bottom']['size_mm'][1]=170.7
    # Keep the plate's rim after narrowing its transverse dimension.
    for w in c['variants']['frame_b_bottom']['windows']:
        w['center_mm'][1]=48 if w['center_mm'][1]>0 else -48
        w['size_mm'][1]=38
    # Cradle remains Z90; local -X now supports the new world -Y hinge.
    for s in c['variants']['integrated_clamps']['spines'][2:]:
        s['center_mm']=turn(s['center_mm'])
        s['size_mm'][:2]=s['size_mm'][1::-1]
    for route in p['cable_routes']:
        for pt in route['points_mm']+route['ties_mm']:
            if abs(pt[0])>=70: pt[0]-=28.65 if pt[0]>0 else -28.65
        endpoint=-1 if route['start']!='vessel_bottom' else 0
        route['points_mm'][endpoint]=turn(route['points_mm'][endpoint])
    write(OUT/'placement.json',p); write(PART/'concept.json',c)
if __name__=='__main__': main()
