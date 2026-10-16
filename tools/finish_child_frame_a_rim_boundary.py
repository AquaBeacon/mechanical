"""Remove the former rim's sub-voxel boundary foil and audit native grids."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
import numpy as np
import trimesh
from clean_stl_degenerates import precision_weld,clean

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
OSC=r'C:\Program Files\OpenSCAD\openscad.com'


def main():
    history=CASE/'input_history/crop_boundary_foil';history.mkdir(parents=True,exist_ok=True)
    for p in [PART/'child_exterior_structural_frame_full.stl',PART/'child_exterior_structural_frame.scad',PART/'spec/design_parameters.json',CASE/'study_final.json']:
        if not (history/p.name).exists():shutil.copy2(p,history/p.name)
    subprocess.run([sys.executable,str(ROOT/'tools/prepare_child_exterior_structure.py'),'--reuse-input-meshes'],check=True)
    source=PART/'child_exterior_structural_frame.scad'
    for name in ['rim_trim','rim_base']:
        with (CASE/(name+'_boundary_render.log')).open('w') as log:
            subprocess.run([OSC,'--export-format','binstl','-o',str(CASE/(name+'.stl')),'-D',f'model="{name}"',str(source)],stdout=log,stderr=subprocess.STDOUT,check=True)
    meshes={n:trimesh.load(CASE/(n+'.stl'),force='mesh') for n in ['domain_envelope','rim_trim','rim_base','seat_base','rail_stock','deep_seats']}
    preserve=trimesh.boolean.union([meshes[n] for n in ['rim_base','seat_base','rail_stock','deep_seats']],engine='manifold')
    core=trimesh.boolean.difference([meshes['domain_envelope'],meshes['rim_trim']],engine='manifold')
    domain=trimesh.boolean.intersection([trimesh.boolean.union([core,preserve],engine='manifold'),meshes['domain_envelope']],engine='manifold')
    for name,m in [('preserve',preserve),('domain',domain)]:
        p=CASE/(name+'.stl');m.export(p);precision_weld(p,CASE/(name+'_precision_weld.json'),allow_collinear=True);clean(p,CASE/(name+'_edge_flip.json'),binary=True)
    subprocess.run([sys.executable,str(ROOT/'tools/prepare_child_exterior_structure.py'),'--reuse-input-meshes'],check=True)
    from finish_child_frame_a import finish
    finish()
    for name in ['full','lower_minus','lower_plus','upper_minus','upper_plus','splice']:
        p=PART/f'child_exterior_structural_frame_{name}.stl'
        with (CASE/(name+'_boundary_export.log')).open('w') as log:
            subprocess.run([OSC,'--export-format','binstl','-o',str(p),'-D',f'model="{name}"',str(source)],stdout=log,stderr=subprocess.STDOUT,check=True)
        m=trimesh.load(p,force='mesh')
        if name=='splice' or not m.is_volume or np.any(m.area_faces<1e-12):
            precision_weld(p,CASE/(name+'_boundary_weld.json'),allow_collinear=True);clean(p,CASE/(name+'_boundary_flip.json'),binary=True)
    subprocess.run([sys.executable,str(ROOT/'tools/verify_child_frame_a.py')],check=True)
    subprocess.run([sys.executable,str(ROOT/'tools/verify_child_frame_a_contact.py')],check=True)
    from topopt.voxel import voxelize_stl,largest_connected
    previous=history/'child_exterior_structural_frame_full.stl';current=PART/'child_exterior_structural_frame_full.stl'
    rows=[]
    for h in [4,2,1]:
        a=largest_connected(voxelize_stl(str(previous),h=h));b=largest_connected(voxelize_stl(str(current),h=h))
        same=a.h==b.h and np.array_equal(a.origin,b.origin) and a.solid.shape==b.solid.shape
        changed=int(np.count_nonzero(a.solid!=b.solid)) if same else None
        row=dict(voxel_mm=h,origin_identical=same,changed_material_voxels=changed,identical=same and changed==0)
        rows.append(row);print('Native grid comparison',row,flush=True)
    report=dict(previous_sha256=hashlib.sha256(previous.read_bytes()).hexdigest(),current_sha256=hashlib.sha256(current.read_bytes()).hexdigest(),grids=rows,all_identical=all(r['identical'] for r in rows),note='Reuse only if all native material grids/origins and the load/material/boundary inputs match exactly.')
    (CASE/'boundary_native_grid_identity.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':main()
