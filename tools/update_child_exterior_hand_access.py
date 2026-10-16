"""Upper A-supported front/rear ballast, lower plate ballast and open service windows."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
PART=ROOT/'parts/child/exterior/printed/child_exterior_open_frame'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def hole(x,y,z,r=2.2,depth=32):return dict(center_mm=[x,y,z],radius_mm=r,depth_mm=depth,axis='X')
def main():
    p,c=read(OUT/'placement.json'),read(PART/'concept.json')
    if p.get('ballast_mount',{}).get('type')=='integrated_c_internal_ballast':
        raise SystemExit('Historical migration: C integration already supersedes this layout. Rebuild from current placement/concept instead.')
    p['items']=[r for r in p['items'] if r['group'] not in ['Ballast support','Fixed cable guides']]
    for r in p['items']:
        if r['group']=='Frame C':
            r['ops'][0]['translate'][1]=170 if r['label']=='C_front' else -170
        for label,y in {'action_camera_front':213,'camera_saddle_front':187,
                        'dive_light_rear':-202,'transducer_inside_c':-158,'transducer_inner_mount':-163}.items():
            if r['label']==label:r['ops'][0]['translate'][1]=y
        if r['label']=='action_camera_front':
            r['ops'][0]['translate'][2]=133
        if r['label']=='camera_saddle_front':
            r['ops'][0]['translate'][2]=85
            r['file']='equipment_saddle'
        if r['group']=='Ballast C':
            sign=-1 if r['label'].endswith(('left','rear')) else 1
            r['label']='ballast_C_rear' if sign<0 else 'ballast_C_front'
            r['ops']=[{'translate':[0,sign*132,40]}]
        if r['group']=='Ballast B':
            index=int(r['label'].split('_')[-1])-1;sign=-1 if index<2 else 1
            z=-118 if index%2==0 else -98
            r['ops']=[{'translate':[sign*97.35,0,z]},{'rotate':[90,0,sign*90]}]
    for variant in ['frame_a_lower','frame_a_upper']:
        a=c['variants'][variant];a['size_mm'][1]=340
        for window in a['windows']:window['size_mm'][1]=294
        a['mounting_webs']['size_mm'][1]=316
        a['lap_cut']['size_mm'][1]=360
    s=c['variants']['frame_a_lower']
    s['windows'][0].update(center_mm=[0,0,-37],size_mm=[40,294,112])
    s['add_boxes']=[dict(center_mm=[0,0,-115],size_mm=[12,340,44])]
    s['post_holes']=[hole(0,y,z-5) for y in [-158,158] for z in [30,50]]
    s['post_holes'] += [hole(0,y,z-5,2.75) for y in [-61.75,-24.25,24.25,61.75] for z in [-118,-98]]
    c['variants'].pop('ballast_b_a_backing',None)
    c['variants'].pop('ballast_c_a_cradle',None)
    c['variants'].pop('fixed_cable_guide',None)
    c['variants'].pop('camera_raised_saddle',None)
    c['variants']['ballast_upper_crossframe']={
        'kind':'composite',
        'boxes':[
            *[dict(center_mm=[x,156,40],size_mm=[8,28,36]) for x in [-81.35,81.35]],
            *[dict(center_mm=[x,144,36],size_mm=[8,32,8]) for x in [-81.35,81.35]],
            dict(center_mm=[0,132,36],size_mm=[170.7,12,8]),
            dict(center_mm=[0,132,36],size_mm=[66,54,8]),
            dict(center_mm=[0,160.5,82],size_mm=[60,8,92])],
        'rings':[dict(center_mm=[0,132,z],outer_radius_mm=28.5,inner_radius_mm=r,height_mm=h,**extra)
                 for z,r,h,extra in [(51,24.75,10,{}),(82,24.75,10,{}),(101,18.5,6,{'split_gap_mm':1.2})]],
        'post_holes':[hole(x,158,z) for x in [-81.35,81.35] for z in [30,50]],
        'note':'Open support extending from both A sides. Concept only; joints, gussets and strength unqualified.'}
    for sign in [-1,1]:
        p['items'].append(dict(label='ballast_upper_frame_rear' if sign<0 else 'ballast_upper_frame_front',
            part='parts/child/exterior/printed/child_exterior_open_frame',file='ballast_upper_crossframe',
            group='Ballast support',geometry='concept',material='frame_a',print=False,
            ops=[{'rotate':[0,0,180 if sign<0 else 0]}],explode_mm=[0,sign*120,0]))
    p['ballast_mount']={'type':'upper_internal_front_rear_crossframes','c_centers_xy_mm':[[0,-132],[0,132]],
        'c_bottom_z_mm':40,'declared_total_mass_g':2240,
        'frame_mount_holes_yz_mm':[[y,z] for y in [-158,158] for z in [30,50]],
        'frame_a_width_y_mm':340,'frame_c_center_y_mm':170,'support_on_a_inner_face':True,
        'plate_centers_z_mm':[-118,-98], 'plate_holes_y_mm':[-61.75,-24.25,24.25,61.75],
        'note':'1000 g front/rear at equal height; 2 x 60 g on each lower A. Ballast CG rises; hydrostatic stability unverified.'}
    p['hand_access']={'opening_yz_mm':[[-147,147],[-88,24]],
        'provisional_hand_corridor_yz_mm':[[10,100],[-80,-20]],'check_frame':50,
        'note':'90 x 60 mm straight corridor at each A, with guard open. Provisional hand envelope, not an ergonomic certification.'}
    for route in p['cable_routes']:
        sign=1 if 'transducer' in route['label'] else -1
        for q in route['points_mm']:
            if abs(q[0]) in [80,72.8]:q[0]=sign*72.8;q[1]=-158
            if abs(q[0])==65 and q[2]==20:q[0]=sign*72.8;q[1]=-158
        if sign>0:
            route['points_mm'][0][1]=-117.5
            route['points_mm'][1][1]=-140
        route['a_ties_mm']=[[sign*72.8,-158,z] for z in ([80,110,140] if sign>0 else [90,150,210,240])]
    p['revision']='1kg ballast inside purple C; A widened to 340 mm; open lower A; lower plate ballast; A cable ties'
    write(OUT/'placement.json',p);write(PART/'concept.json',c)
if __name__=='__main__':main()
