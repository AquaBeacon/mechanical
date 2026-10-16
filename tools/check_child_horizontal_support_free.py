"""Check remaining print jobs and explicit integral-part support exceptions."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np
import trimesh
from shapely import maximum_inscribed_circle
from shapely.geometry import Polygon
from shapely.ops import unary_union
from prepare_child_horizontal_plate_frame import ROOT,OUT,save,printed_baseline


def bridge_regions(mesh):
    # Project faces steeper than45 degrees into the bed plane. The short side
    # of its maximum inscribed circle reports the widest local empty region.
    # A connected U-shaped footprint can contain several narrow hole roofs;
    # its bounding rectangle would incorrectly join those into one wide span.
    # This is not a physical guarantee or an unsupported toolpath length.
    selected=(mesh.face_normals[:,2]<-0.709)&(mesh.triangles[:,:,2].mean(axis=1)>.3)
    polys=[Polygon(triangle[:,:2]) for triangle in mesh.triangles[selected]]
    polys=[p for p in polys if p.area>1e-6]
    if not polys:return []
    merged=unary_union(polys)
    regions=[merged] if merged.geom_type=='Polygon' else list(merged.geoms)
    rows=[]
    for region in regions:
        if region.geom_type!='Polygon' or region.area<.005:continue
        points=np.asarray(region.minimum_rotated_rectangle.exterior.coords)
        widths=np.linalg.norm(np.diff(points,axis=0),axis=1)
        rows.append(dict(area_mm2=float(region.area),short_width_mm=float(min(widths)),
                         long_width_mm=float(max(widths)),bounds_xy_mm=list(region.bounds),
                         local_width_mm=float(2*maximum_inscribed_circle(region,tolerance=.02).length)))
    return rows


def main():
    manifest=json.loads((OUT/'parts/manifest.json').read_text(encoding='utf-8'))
    locked=printed_baseline();failures=[];rows=[]
    for entry in manifest['parts']:
        if entry['source'] in locked:continue
        file=OUT/'parts'/entry['file'];mesh=trimesh.load(file,force='mesh')
        metadata_path=ROOT/entry['part']/'manufacturing.json'
        metadata=json.loads(metadata_path.read_text(encoding='utf-8')) if metadata_path.exists() else {}
        mode=metadata.get('support_modes',{}).get(entry['stem'],'none')
        job=OUT/'print_jobs/x1c_petg_basic'/file.stem
        report=json.loads((job/'slice.json').read_text(encoding='utf-8'))
        record=json.loads((job/'source_manifest.json').read_text(encoding='utf-8'))
        with zipfile.ZipFile(job/(file.stem+'.3mf')) as archive:
            settings=json.loads(archive.read('Metadata/project_settings.config'))
        features=report.get('filament_by_feature_mm',{})
        support_mm=sum(v for k,v in features.items() if k.lower().startswith('support'))
        regions=bridge_regions(mesh)
        max_width=max([r['local_width_mm'] for r in regions],default=0)
        row=dict(file=entry['file'],quantity=entry['quantity'],print_rotation_deg=entry['rotation_deg'],
            dimensions_mm=mesh.extents.tolist(),watertight=bool(mesh.is_volume),
            connected_components=len(mesh.split()),source_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
            supports=report.get('supports'),support_used=report.get('support_used'),
            project_enable_support=str(settings.get('enable_support')),support_filament_mm=support_mm,
            bed_fits=report.get('bed_fits'),warnings=report.get('warnings'),
            bridge_region_width_limit_mm=10,max_local_bridge_width_mm=max_width,
            projected_bridge_regions=regions,
            gcode_sha256=hashlib.sha256((job/'plate_1.gcode').read_bytes()).hexdigest(),
            project_3mf_sha256=hashlib.sha256((job/(file.stem+'.3mf')).read_bytes()).hexdigest())
        rows.append(row)
        row['required_support_mode']=mode
        basic_bad=(not row['watertight'] or row['connected_components']!=1 or row['source_sha256']!=record['source_sha256']
                   or not row['bed_fits'] or row['warnings'] or row['supports']!=mode)
        if mode=='none':
            mode_bad=(max_width>10.01 or not record.get('support_free_verified') or row['support_used'] is not False
                      or row['project_enable_support']!='0' or support_mm!=0)
        else:
            mode_bad=(row['project_enable_support']!='1' or str(settings.get('support_on_build_plate_only'))!='1'
                      or abs(float(settings.get('support_top_z_distance',0))-.2)>1e-8)
            # This exception requires the dedicated bore/cam support exclusion
            # check; an enabled-support flag alone never qualifies the part.
            details=json.loads((OUT/'_work/analysis/side_twist_mount/slicing.json').read_text(encoding='utf-8'))
            match=next((r for r in details['parts'] if r['file']==entry['file']),None)
            mode_bad=mode_bad or (match is None or match['source_sha256']!=row['source_sha256']
                                  or match.get('protected_region_support_strokes')!=0)
        if basic_bad or mode_bad:failures.append(row)
    expected=[r for r in manifest['parts'] if r['source'] not in locked]
    if len(rows)!=len(expected) or sum(r['quantity'] for r in rows)!=sum(r['quantity'] for r in expected):
        failures.append(dict(error='Incomplete remaining print set'))
    result=dict(result='FAIL' if failures else 'PASS',parts=rows,failures=failures,
        printed_mesh_sha256=locked,
        method='Compare STL hashes, retained orientations, actual sliced3MF settings and per-feature G-code extrusion; project steep downward faces and inspect maximum local footprint widths.',
        limitations=['Projected bridge widths do not prove physical bridge quality',
                     'PETG bridges, small horizontal holes and bed adhesion require first-print inspection',
                     'Already printed stock stays unchanged; its old auto-support jobs are historical'])
    save(OUT/'_work/analysis/print_verification/validation.json',result)
    subset=dict(result='FAIL' if any(r in failures for r in rows if r['required_support_mode']=='none') else 'PASS',
                scope='Only the parts whose manufacturing metadata specifies no supports',
                parts=[r for r in rows if r['required_support_mode']=='none'],
                integral_support_exceptions=[r['file'] for r in rows if r['required_support_mode']!='none'])
    save(OUT/'_work/analysis/support_free/validation.json',subset)
    print(json.dumps(dict(result=result['result'],types=len(rows),instances=sum(r['quantity'] for r in rows),
        support_filament_mm=sum(r['support_filament_mm'] for r in rows),
        max_local_bridge_width_mm=max(r['max_local_bridge_width_mm'] for r in rows),
        failures=failures),ensure_ascii=False))
    if failures:raise RuntimeError('Print setting checks failed')


if __name__=='__main__':main()
