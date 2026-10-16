"""Rotate the vessel/cradle to face A; replace folded returns with straight mounts."""
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
PART=ROOT/'parts/child/exterior/printed/child_exterior_open_frame'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def turn(v): return [-v[1],v[0],v[2]]
if __name__=='__main__':
    p=read(OUT/'placement.json')
    if p['clamp_a_connection'].get('axis')=='X': raise SystemExit('Rotation already applied.')
    hist=OUT/'_work/images/history/before_clamp_rotation'
    hist.mkdir(parents=True,exist_ok=True)
    for src in (OUT/'_work/images').glob('child_exterior_*'):
        if src.is_file(): shutil.copy2(src,hist/src.name)
    for src,name in [(OUT/'placement.json','placement_before_clamp_rotation.json'),
                     (PART/'concept.json','concept_before_clamp_rotation.json'),
                     (OUT/'child_exterior_concept.blend','child_exterior_before_clamp_rotation.blend')]:
        shutil.copy2(src,OUT/'_work/intermediate'/name)
    rotated=['vessel','Integrated clamp cradle','Hinged cable guard','Fixed hinge and pin']
    for row in p['items']:
        if row['group'] in rotated:
            row['ops']=[{'rotate':[0,0,90]}]+row.get('ops',[])
            row['explode_mm']=turn(row.get('explode_mm',[0,0,0]))
        if row['group']=='Frame A':
            row['ops'][0]['translate'][0]=120 if row['ops'][0]['translate'][0]>0 else -120
            row.pop('inward_sign',None)
            row['note']='Flat A with four straight mounting holes per clamp level; no folded returns.'
        if row['group']=='Ballast C':
            row['ops'][0]['translate'][0]=96 if row['ops'][0]['translate'][0]>0 else -96
        if row['label']=='transducer_inner_mount': row['ops'][0]['translate'][0]=94
    for route in p['cable_routes']:
        route['points_mm'][-1 if route['start']!='vessel_bottom' else 0]=turn(route['points_mm'][-1 if route['start']!='vessel_bottom' else 0])
        for point in route['points_mm']+route['ties_mm']:
            if abs(point[0])>=113: point[0]=102 if point[0]>0 else -102
    p['hinge']['pivot_world_mm']=turn(p['hinge']['pivot_world_mm'])
    p['hinge']['axis_world']=[0,1,0]
    connection=p['clamp_a_connection']
    connection.update(axis='X',reference_rotation_deg=[0,0,90],spacer_span_x_mm=[85.35,114],
                      note='Vessel and complete cradle rotate 90 degrees. Each four-hole mounting pad faces one flat A. Straight axial spacers replace all long folded returns.')
    connection.pop('tab_face_y_mm',None)
    for h in connection['holes']:
        h['axis_world_mm']=turn(h['axis_world_mm'])
        x,y,z=h['axis_world_mm']
        h['frame_hole_world_mm']=[120 if x>0 else -120,y,z]
        h.pop('tab_hole_world_mm',None)
    p['notes']=[n for n in p['notes'] if 'returns' not in n]
    p['notes'].append('User correction: rotate vessel and linked clamps 90 degrees about Z; existing mounting faces now point straight at A. No folded returns.')
    write(OUT/'placement.json',p)
    s=read(PART/'concept.json')
    s['variants']['frame_c']['size_mm'][0]=240
    for window in s['variants']['frame_c']['windows']: window['size_mm'][0]=182
    s['variants']['frame_b_bottom']['size_mm'][0]=228
    s['variants']['transducer_inner_mount']['size_mm'][0]=40
    for name,levels in [('frame_a_lower',[35,95]),('frame_a_upper',[-21])]:
        v=s['variants'][name]
        v.pop('inward_tabs',None)
        v['mounting_webs']=dict(local_z_mm=levels,size_mm=[12,196,32],hole_y_mm=[-18,18],hole_z_mm=[-8,8],hole_radius_mm=1.75)
    write(PART/'concept.json',s)
    print('Vessel/cradle/hinge rotated 90 degrees; A mounts directly along existing X-axis hole lines.')
