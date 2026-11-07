"""Actual-mesh checks for Rev.2, including camera release and ground contact."""
from pathlib import Path
import json,sys,hashlib,itertools
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scad/lib'))
from check_asm_contacts import matrix
OUT=ROOT/'assemblies/parent_exterior/_work/analysis/qr_standing'

def intersection(a,b):
    if np.any(np.minimum(a.bounds[1],b.bounds[1])-np.maximum(a.bounds[0],b.bounds[0])<1e-6):return 0.
    c=trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
    return 0. if c is None else float(abs(c.volume))
def probe(a,b,d):return trimesh.creation.cylinder(radius=d/2,sections=48,segment=[a,b])

def main(out=None, bolt_on=False, fixture_checker=None):
    output=OUT if out is None else Path(out)
    p=json.loads((ROOT/'assemblies/parent_exterior/placement.json').read_text(encoding='utf-8'))
    rows={i['label']:i for i in p['items']};meshes={};checks=[]
    for name,i in rows.items():
        f=ROOT/i['part']/((i.get('file') or Path(i['part']).name)+'.stl')
        m=trimesh.load(f,force='mesh')
        if 'printed' in i['part'] or 'jigs' in i['part']:
            checks.append(dict(label=name,source=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),closed=bool(m.is_watertight),winding=bool(m.is_winding_consistent),components=len(m.split(only_watertight=False)),volume_mm3=float(m.volume),bounds_mm=m.bounds.tolist()))
        m.apply_transform(matrix(i.get('ops',[])));meshes[name]=m
    collisions=[]
    for a,b in itertools.combinations(meshes,2):
        if not any(rows[k]['group']=='exterior' or k=='camera_mount' for k in (a,b)):continue
        v=intersection(meshes[a],meshes[b])
        if v>0.04:collisions.append(dict(a=a,b=b,mm3=v))
    # Actual body contact faces and passage cylinders, not nominal hole tables.
    bores=[]
    for x in (-60,-20):
        for y in (-20,20):
            for host,z0,z1 in [('open_frame',-24,0),('camera_qr_female',-34,-24),('camera_qr_male',-60.5,-50)]:
                if host=='camera_qr_male' and p.get('camera_twist_mount'):continue # integral male has no adapter fasteners
                v=intersection(meshes[host],probe([x,y,z0],[x,y,z1],3.4))
                bores.append(dict(host=host,xy=[x,y],obstruction_mm3=v,passed=v<0.02))
    for s in (-1,1):
        for y in (-55,55):
            for host in ['open_frame',f'stand_{s}']:
                v=intersection(meshes[host],probe([s*110,y,-30],[s*110,y,0],5.4))
                bores.append(dict(host=host,xy=[s*110,y],obstruction_mm3=v,passed=v<0.02))
    # Integrated top clamp: all rod passages and the four original pad seats.
    for x in (-110,110):
        for y in (-55,55):
            v=intersection(meshes['upper_clamp_frame'],probe([x,y,102],[x,y,123],5.4))
            bores.append(dict(host='upper_clamp_frame',xy=[x,y],obstruction_mm3=v,passed=v<0.02))
    datums=[]
    for xyz in [[-96,-55,0],[-96,55,0],[96,0,0],[-105,-38,8],[-105,38,8],[94,115,8]]:
        host='open_frame'
        if bolt_on and xyz[2]==8 and 'bolt_on_side_left' in meshes:
            host='bolt_on_side_left' if xyz[0]==-105 else 'bolt_on_end_fixed'
        d=float(trimesh.proximity.closest_point(meshes[host],[xyz])[1][0])
        datums.append(dict(host=host,point=xyz,distance_mm=d,passed=d<0.02))
    for x in (-98,98):
        for y in (-55,55):
            xyz=[x,y,102.3]
            d=float(trimesh.proximity.closest_point(meshes['upper_clamp_frame'],[xyz])[1][0])
            datums.append(dict(host='upper_clamp_frame',point=xyz,distance_mm=d,passed=d<0.02))
    retained={n:m for n,m in meshes.items() if rows[n].get('removal_group') not in ['camera','td04a']}
    ground=[]
    for n,m in retained.items():
        ground.append(dict(label=n,min_z=float(m.bounds[0,2]),clearance_mm=float(m.bounds[0,2]+72)))
    # Contact polygon derived from final skid vertices, at the actual bottom face.
    feet=np.concatenate([m.vertices[np.abs(m.vertices[:,2]+72)<0.001,:2] for n,m in meshes.items() if n.startswith('stand_')])
    from scipy.spatial import ConvexHull
    hull=ConvexHull(feet);polygon=feet[hull.vertices]
    margin=float(np.min(-hull.equations[:,-1]/np.linalg.norm(hull.equations[:,:2],axis=1)))
    # Unlock bolt and washer must be removed first. Rotate the complete camera unit.
    moving=[n for n in meshes if rows[n].get('removal_group')=='camera']
    fixed=[n for n in meshes if n not in moving and n not in ['camera_qr_lock_bolt','camera_qr_lock_washer','camera_qr_knob'] and rows[n]['group'] not in ['hardware','pads']]
    sweep=[];origin=np.array([-40.,0.,-30.])
    for angle in range(0,61,5):
        # Local clockwise -60 appears as global +60 after the female X flip.
        rot=trimesh.transformations.rotation_matrix(np.deg2rad(angle),[0,0,1],origin)
        rot[2,3]-=0.6*angle/60
        for a in moving:
            m=meshes[a].copy();m.apply_transform(rot)
            for b in fixed:
                v=intersection(m,meshes[b])
                if v>0.08:sweep.append(dict(angle_deg=angle,a=a,b=b,mm3=v))
    for travel in [5,10,20,40,80]:
        rot=trimesh.transformations.rotation_matrix(np.deg2rad(60),[0,0,1],origin);rot[2,3]-=0.6+travel
        for a in moving:
            m=meshes[a].copy();m.apply_transform(rot)
            for b in fixed:
                v=intersection(m,meshes[b])
                if v>0.08:sweep.append(dict(travel_mm=travel,a=a,b=b,mm3=v))
    lock_access=[]
    for travel in [0,5,10,20,30,45]:
        for a in ['camera_qr_lock_bolt','camera_qr_lock_washer','camera_qr_knob']:
            m=meshes[a].copy();m.apply_translation([0,travel,0])
            for b in meshes:
                if rows[b]['group'] in ['hardware','pads'] or b==a or b=='camera_qr_knob':continue
                v=intersection(m,meshes[b])
                if v>0.04:lock_access.append(dict(travel_mm=travel,a=a,b=b,mm3=v))
    # Preserve the exact shared functional surfaces, allowing only export noise.
    interface_checks=[]
    for variant,z0,z1 in [('female',4.01,18.1),('male',6.01,14.1)]:
        stem='parent_oneplate_camera_qr_'+variant
        new=trimesh.load(ROOT/'parts/parent/exterior/printed/parent_oneplate_camera_qr'/(stem+'.stl'),force='mesh')
        if variant=='male' and p.get('camera_twist_mount'):
            new=meshes['camera_mount'].copy()
            old_male_pose=matrix([{'translate':[-40,0,-54.5]},{'rotate':[0,0,90]}])
            new.apply_transform(np.linalg.inv(old_male_pose))
        old=trimesh.load(ROOT/'parts/common/jigs/quick_release_prototypes'/('quick_release_prototypes_twist_'+variant+'.stl'),force='mesh')
        region=trimesh.creation.box(extents=[44,44,z1-z0]);region.apply_translation([0,0,(z0+z1)/2])
        n=trimesh.boolean.intersection([new,region],engine='manifold');o=trimesh.boolean.intersection([old,region],engine='manifold')
        delta=sum(abs(trimesh.boolean.difference([a,b],engine='manifold',check_volume=False).volume) for a,b in [(n,o),(o,n)])
        interface_checks.append(dict(variant=variant,symmetric_difference_mm3=float(delta),passed=bool(delta<0.05)))
    result=dict(meshes=checks,collisions=collisions,bores=bores,datums=datums,ground=ground,support_polygon_mm=polygon.tolist(),centered_load_margin_mm=margin,camera_sweep_collisions=sweep,limits=['Actual payload COM/mass and physical tipping test are not available. Support margin is for projection (0,0).','Strength, creep, actual QR fit and actual cable routing require physical validation.','Floats and camera case remain existing provisional reference shapes.'])
    result.update(lock_access_collisions=lock_access,shared_interface_checks=interface_checks)
    tool_checks=[]
    probes=[]
    for x in (-110,110):
        for y in (-55,55):probes.append((f'M5_socket_{x}_{y}',probe([x,y,-100],[x,y,-31],11)))
    for x in (-60,-20):
        for y in (-20,20):probes.append((f'QR_female_driver_{x}_{y}',probe([x,y,-100],[x,y,-27.4 if bolt_on else -27.5],3)))
    for x in (-110,110):
        for y in (-55,55):probes.append((f'upper_M5_socket_{x}_{y}',probe([x,y,122.31],[x,y,180],11)))
    for name,tool in probes:
        hits=[]
        for n,m in retained.items():
            if rows[n]['group'] in ['hardware','pads']:continue
            v=intersection(tool,m)
            if v>0.04:hits.append(dict(part=n,mm3=v))
        tool_checks.append(dict(tool=name,collisions=hits,passed=not hits))
    result['tool_access']=tool_checks
    result['passed']=all(c['closed'] and c['winding'] and c['components']==1 for c in checks) and not collisions and all(x['passed'] for x in bores+datums+interface_checks+tool_checks) and min(x['clearance_mm'] for x in ground)>-0.01 and margin>0 and not sweep and not lock_access
    if bolt_on:
        import verify_parent_exterior_bolt_on as revision
        extra=(fixture_checker or revision.check_fixtures)(rows,meshes)
        result['bolt_on_fixtures']=extra
        result['passed']=result['passed'] and extra['passed']
    result['placement_sha256']=hashlib.sha256((ROOT/'assemblies/parent_exterior/placement.json').read_bytes()).hexdigest()
    output.mkdir(parents=True,exist_ok=True);(output/'geometry_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['meshes','ground']},ensure_ascii=False,indent=2))
    return 0 if result['passed'] else 1
if __name__=='__main__':sys.exit(main())
