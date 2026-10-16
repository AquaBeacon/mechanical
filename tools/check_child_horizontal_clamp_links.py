"""Verify connected clamp geometry against the original two-station interfaces."""
import hashlib,json,sys
import numpy as np
import trimesh
from prepare_child_horizontal_plate_frame import ROOT,OUT,CLAMP,load_world,overlap,save

def portable():
    from scipy.spatial import cKDTree
    manifest=json.loads((OUT/'parts/manifest.json').read_text(encoding='utf-8'))
    placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    expected={r['label']:r for r in placement['items'] if r['print']}
    rows=[];failures=[];labels=[]
    for entry in manifest['parts']:
        source=ROOT/entry['source'];target=OUT/'parts'/entry['file']
        original=trimesh.load(source,force='mesh');packed=trimesh.load(target,force='mesh')
        restored=packed.copy();restored.apply_transform(np.linalg.inv(entry['model_to_print']))
        error=max(float(cKDTree(a.vertices).query(b.vertices)[0].max())
                  for a,b in [(original,restored),(restored,original)])
        bounds_error=float(np.abs(original.bounds-restored.bounds).max())
        volume_error=abs(float(original.volume-restored.volume))
        row=dict(file=entry['file'],labels=entry['labels'],quantity=entry['quantity'],
            bidirectional_vertex_set_error_mm=error,bounds_error_mm=bounds_error,
            volume_error_mm3=volume_error,watertight=bool(packed.is_watertight),
            connected_components=len(packed.split()),zero_area_triangles=int(np.sum(packed.area_faces<1e-12)),
            sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        rows.append(row);labels.extend(entry['labels'])
        if (error>1e-6 or bounds_error>1e-6 or volume_error>.001 or not packed.is_volume
                or row['connected_components']!=1 or row['zero_area_triangles']
                or entry['quantity']!=len(entry['labels']) or row['sha256']!=entry['sha256']):
            failures.append(row)
        for label in entry['labels']:
            item=expected.get(label,{})
            if item.get('part')!=entry['part'] or item.get('file')!=entry['stem']:
                failures.append(dict(label=label,error='Placement/source mismatch'))
    if sorted(labels)!=sorted(expected): failures.append(dict(error='Placement quantities differ'))
    save(OUT/'_work/analysis/guards/portable_validation.json',dict(
        result='FAIL' if failures else 'PASS',
        method='Undo saved print transform; compare all vertices in both directions, volume, bounds and placement labels',
        parts=rows,printed_instances=len(labels),failures=failures))
    print(json.dumps(dict(result='PORTABLE_FAIL' if failures else 'PORTABLE_PASS',
        types=len(rows),printed_instances=len(labels),maximum_vertex_error_mm=max(r['bidirectional_vertex_set_error_mm'] for r in rows))))
    if failures: raise RuntimeError('Portable STL checks failed')

def main():
    placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    world=load_world(placement)
    connection=placement['clamp_connection']
    stations=connection['stations_mm']
    failures=[];halves=[]
    inputs={OUT/'placement.json'}
    for half in ['upper','lower']:
        source=CLAMP/f'child_wte4_petg_clamp_{half}.stl'
        linked_source=CLAMP/f'child_wte4_petg_clamp_{half}_linked.stl'
        inputs.update([source,linked_source])
        original=trimesh.load(source,force='mesh')
        linked=trimesh.load(linked_source,force='mesh')
        band_width=float(original.extents[2])
        pitch=max(stations)-min(stations)
        reference=[]
        for axial in [0,pitch]:
            old=original.copy();old.apply_translation([0,0,axial])
            reference.append(old)
        missing=[max(0.,float(old.volume)-overlap(old,linked)) for old in reference]
        section=linked.section(plane_origin=[0,0,(pitch+band_width)/2],plane_normal=[0,0,1])
        loops=[] if section is None else section.discrete
        rails=[]
        for loop in loops:
            points=loop[:,:2]
            centre=points.mean(axis=0)
            sign=np.sign(centre[0]);angle=np.radians(connection['shoulder_angle_deg'])
            radial=np.array([sign*np.sin(angle),np.cos(angle)])
            tangent=np.array([np.cos(angle),-sign*np.sin(angle)])
            rails.append(dict(width_mm=float(np.ptp(points@tangent)),
                thickness_mm=float(np.ptp(points@radial)),
                minimum_radius_mm=float(np.linalg.norm(points,axis=1).min())))
        row=dict(half=half,watertight=bool(linked.is_watertight),
            components=len(linked.split()),dimensions_mm=linked.extents.tolist(),
            original_band_material_missing_mm3=missing,midspan_rails=rails,
            added_volume_mm3=float(linked.volume-sum(m.volume for m in reference)))
        halves.append(row)
        if (not row['watertight'] or row['components']!=1 or max(missing)>.1
                or len(rails)!=2 or abs(linked.extents[2]-(pitch+band_width))>.001):
            failures.append(row)
        for rail in rails:
            if (abs(rail['width_mm']-connection['rail_width_mm'])>.001
                    or abs(rail['thickness_mm']-connection['rail_thickness_mm'])>.001):
                failures.append(rail)
    # Upper linked half and removable top frame are removed before lowering the vessel.
    fixed=[(r,m) for r,m in world if r['print'] and r['label'] not in
           ('clamp_linked_upper','removable_upper_frame')]
    vessel=[(r,m) for r,m in world if r['group']=='vessel']
    insertion=[]
    for height in [0,.5,1,2,5,10,20,40,80,100]:
        blocked=[]
        for row,mesh in vessel:
            test=mesh.copy();test.apply_translation([0,0,height])
            for target,tm in fixed:
                volume=overlap(test,tm)
                if volume>.1: blocked.append(dict(vessel=row['label'],part=target['label'],volume_mm3=volume))
        insertion.append(dict(vertical_lift_mm=height,blocked=blocked))
        failures.extend(blocked)
    save(OUT/'_work/analysis/clamp_connection/validation.json',dict(
        status='fit_prototype',halves=halves,vertical_vessel_entry=insertion,failures=failures,
        inputs_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(inputs)},
        note='Geometric connection and interface check; no strength or creep qualification.'))
    print(json.dumps(dict(result='CLAMP_LINKS_FAIL' if failures else 'CLAMP_LINKS_PASS',halves=halves,
        insertion_poses=len(insertion)),ensure_ascii=False))
    if failures: raise RuntimeError('Connected clamp checks failed')

if __name__=='__main__':
    if '--portable-only' in sys.argv: portable()
    else: main()
