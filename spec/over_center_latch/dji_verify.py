"""Verify actual final STL geometry, motion and interfaces of the 40 N latch."""
from pathlib import Path
import itertools,json,math
import numpy as np
import trimesh
from shapely.geometry import Polygon,Point,box,LineString
from shapely.affinity import rotate,translate
from shapely.ops import unary_union
from geometry import *

ROOT=Path(__file__).resolve().parents[2];P=ROOT/'parts/common/jigs/over_center_latch'
OUT=ROOT/'assemblies/over_center_latch/_work/analysis/verification'

def section(mesh,y):
    sec=mesh.section(plane_origin=[0,y,0],plane_normal=[0,1,0]);shape=Polygon()
    if sec:
        for loop in sec.discrete:shape=shape.symmetric_difference(Polygon(np.asarray(loop)[:,[0,2]]).buffer(0))
    return shape.buffer(0)

def main():
    v=json.loads((P/'parameters.json').read_text(encoding='utf-8'));OUT.mkdir(parents=True,exist_ok=True)
    items=layout(v);meshes={s:trimesh.load(P/(s+'.stl')) for s in set(i['file'] for i in items)}
    mesh_report={}
    for name,m in meshes.items():
        deg=int(np.count_nonzero(m.area_faces<1e-12))
        valid=m.is_watertight and m.is_volume and len(m.split())==1 and not deg
        mesh_report[name]=dict(watertight=bool(m.is_watertight),positive_volume=bool(m.is_volume),
            components=len(m.split()),zero_faces=deg,volume_mm3=float(m.volume),bounds_mm=m.bounds.tolist())
        assert valid,(name,mesh_report[name])
    planes=[0,1,3.7,3.95,4.45,6,7.85,8.1,8.5,10,12.2,12.5,14,14.85,15.15,15.9,16.2,18,21.7,22.2,24,27,29,30,31,34]
    planes=sorted(set(planes+[-y for y in planes if y]))
    profiles={}
    for y in planes:
        profiles[y]={i['label']:section(meshes[i['file']],y-i['ops'][0]['translate'][1]) for i in items if i['label']!='epdm'}
    samples=[(float(a),0,0) for a in np.linspace(v['open_angle'],closed_angle(v),161)]
    samples += [(v['open_angle'],float(a),0) for a in np.linspace(0,v['release_angle'],81)]
    samples += [(v['open_angle'],v['release_angle'],float(a)) for a in np.linspace(0,20,31)]
    collisions=[];maximum=0.;paircount=0
    for angle,lift,separate in samples:
        poses={i['label']:i for i in layout(v,angle,lift,separate)}
        for y,ps in profiles.items():
            moved={}
            for name,shape in ps.items():
                item=poses[name];xyz=item['ops'][0]['translate'];rot=item['ops'][1]['rotate'][1]
                moved[name]=translate(rotate(shape,-rot,origin=(0,0)),xoff=xyz[0],yoff=xyz[2])
            for a,b in itertools.combinations(moved,2):
                area=moved[a].intersection(moved[b]).area;maximum=max(maximum,area);paircount+=1
                if area>.006:collisions.append(dict(theta=angle,lift=lift,separate=separate,y=y,pair=[a,b],area_mm2=area))
    worst={}
    for c in collisions:
        key='/'.join(c['pair'])
        if key not in worst or c['area_mm2']>worst[key]['area_mm2']:worst[key]=c
    (OUT/'motion_collisions.json').write_text(json.dumps(dict(collisions=collisions[:100],worst_by_pair=worst,total=len(collisions),max_mm2=maximum),indent=2)+'\n',encoding='utf-8')
    assert not collisions,('rigid intersections',collisions[:5],len(collisions))
    mounted={}
    for i in items:
        m=meshes[i['file']].copy();m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(i['ops'][1]['rotate'][1]),[0,1,0]));m.apply_translation(i['ops'][0]['translate']);mounted[i['label']]=m
    # Nominal rear seating area measured from actual coplanar STL triangles.
    hood=mounted['lever'];tri=hood.triangles[np.max(np.abs(hood.triangles[:,:,2]),axis=1)<1e-5]
    contact=unary_union([Polygon(t[:,:2]) for t in tri])
    base=mounted['base'];tri=base.triangles[np.max(np.abs(base.triangles[:,:,2]),axis=1)<1e-5]
    plate=unary_union([Polygon(t[:,:2]) for t in tri])
    assert contact.area>20 and contact.difference(plate.buffer(.001)).area<.005,('direct seating missing',contact.area)
    # No separately raised stop exists behind A's integral bearing root.
    assert base.vertices[base.vertices[:,0]<-9.1,2].max()<.001
    hoodheight=hood.bounds[1,2];assert hoodheight<=v['closed_height_limit']+.001
    # Mounting bores and real straight tool corridors, including axis heads/tips.
    holes=[]
    for name,coords in mounting_holes(v).items():
        local=meshes['over_center_latch_'+name];depth=v['host_fixed_floor'] if name=='base' else v['host_floor']
        sec=local.section(plane_origin=[0,0,-depth/2],plane_normal=[0,0,1]);face=Polygon()
        for loop in sec.discrete:face=face.symmetric_difference(Polygon(np.asarray(loop)[:,:2]).buffer(0))
        for x,y in coords:
            assert face.intersection(Point(x,y).buffer(1.7,resolution=32)).area<.003,(name,x,y,'blocked bore')
            gx=x+(v['catch_distance'] if name=='keeper' else 0)
            for z in np.linspace(.25,hoodheight+4,41):
                for label,m in mounted.items():
                    if label in ['base','keeper','epdm']:continue
                    sec=m.section(plane_origin=[0,0,z],plane_normal=[0,0,1]);shape=Polygon()
                    if sec:
                        for loop in sec.discrete:shape=shape.symmetric_difference(Polygon(np.asarray(loop)[:,:2]).buffer(0))
                    assert shape.intersection(Point(gx,y).buffer(v['tool_diameter']/2,resolution=32)).area<.003,(name,x,y,label,z,'tool corridor')
            holes.append([name,x,y])
    # Support of the entire specified inclined rubber adhesive patch, using STL.
    keeper=meshes['over_center_latch_keeper'];tri=keeper.triangles
    B,C,K,Q,n,u=contact_geometry(v);wall=Q-n*(v['epdm_thickness']-v['preload']);wall[0]-=v['catch_distance']
    distances=(tri[:,:,[0,2]]-wall)@n
    selected=tri[np.max(np.abs(distances),axis=1)<1e-4]
    patch=unary_union([Polygon(np.column_stack((t[:,1],(t[:,[0,2]]-wall)@u))) for t in selected])
    offset=v.get('epdm_tangent_offset',0.)
    requested=box(-v['epdm_width']/2,-v['epdm_height']/2+offset,v['epdm_width']/2,v['epdm_height']/2+offset)
    assert requested.difference(patch.buffer(.001)).area<.001,'rubber face not fully backed'
    assert abs(keeper.bounds[1,2])<.001,'keeper raised above plate'
    assert v['host_floor']+v['pocket_floor']>=2,'insufficient pocket floor'
    # Load sign with declared geometric tolerance, without changing acceptance.
    margins=[]
    for dz,angle in itertools.product([-.15,0,.15],[-2,0,2]):
        trial=dict(v,axis_height=v['axis_height']+dz,closed_angle_deg=v['closed_angle_deg']+angle)
        margins.append(over_center(trial,closed_angle(trial)))
    assert min(margins)>0,'tolerance can reverse closing moment'
    close=load_at(v,closed_angle(v));assert abs(close['clamp_horizontal_N']-40)<.001
    assert close['hand_vertical_N']<0 and close['lip_N']>0
    report=dict(parts=mesh_report,poses=len(samples),sections=planes,pair_checks=paircount,
        max_intersection_mm2=maximum,closed_height_mm=float(hoodheight),mount_holes=holes,
        rear_seating_area_mm2=contact.area,additional_stops=False,groove_angle_deg=v['groove_angle_deg'],
        supported_glue_patch_mm2=requested.area,pocket_floor_thickness_mm=v['host_floor']+v['pocket_floor'],
        base_plate_mm=v['host_fixed_floor'],keeper_plate_mm=v['host_floor'],
        minimum_restoring_lever_margin_mm=min(margins),tolerance_test='A height +/-0.15 mm, closed link angle +/-2 deg',
        limitations=['Rigid STL planar motion; excludes rubber deformation','No physical force, fatigue or strength verification here'])
    (OUT/'transverse_sweep.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: meshes, motion, inclined glue patch, holes/tools, thin floor and direct seating',paircount)

if __name__=='__main__':main()
