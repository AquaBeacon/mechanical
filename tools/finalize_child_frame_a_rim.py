"""Promote the measured rim shortlist, rebuild CAD, and rerun native checks."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
import trimesh
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
BASE=PART/'_work/analysis/frame_a_compact_grip'
OSC=r'C:\Program Files\OpenSCAD\openscad.com'
CLI=[sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py')]


def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def run(name,cmd,allowed=(0,),timeout=None):
    with (CASE/(name+'.log')).open('w',encoding='utf-8') as stream:
        result=subprocess.run(cmd,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,timeout=timeout)
    save(CASE/(name+'_status.json'),dict(exit_code=result.returncode))
    print(name,'exit',result.returncode,flush=True)
    if result.returncode not in allowed:raise RuntimeError(f'{name} exit {result.returncode}')


def main():
    comparison=json.loads((CASE/'rim_comparison.json').read_text())
    base=comparison['selected_base_mm'];assert base is not None
    folder=CASE/'candidates'/f'base_{base:g}_solid_grip'
    run('prepare_selected',[sys.executable,str(ROOT/'tools/prepare_child_exterior_structure.py'),
                            '--rim-base',str(base)])
    from finish_child_frame_a import finish
    finish()
    from clean_stl_degenerates import precision_weld,clean
    source=PART/'child_exterior_structural_frame.scad'
    for name in ['full','lower_minus','lower_plus','upper_minus','upper_plus','splice']:
        p=PART/f'child_exterior_structural_frame_{name}.stl'
        run('render_'+name,[OSC,'--export-format','binstl','-o',str(p),'-D',f'model="{name}"',str(source)])
        m=trimesh.load(p,force='mesh')
        if name=='splice' or not m.is_volume or np.any(m.area_faces<1e-12):
            precision_weld(p,CASE/(name+'_export_precision_weld.json'),allow_collinear=True)
            clean(p,CASE/(name+'_export_edge_flip.json'),binary=True)
    run('geometry',[sys.executable,str(ROOT/'tools/verify_child_frame_a.py')])
    run('clamp_contact',[sys.executable,str(ROOT/'tools/verify_child_frame_a_contact.py')])
    study=json.loads((CASE/'study_frame_a.json').read_text())
    for k in ['geometry','design','finish','voxel_mm']:study.pop(k,None)
    full=PART/'child_exterior_structural_frame_full.stl'
    study.update(part=str(full),_part_sha256=sha(full))
    old=json.loads((BASE/'study_final.json').read_text())
    same=['material','build_axis','raster_axis','infill','walls','safety_factor','max_deflection_mm','cases']
    assert all(study[k]==old[k] for k in same)
    save(CASE/'study_final.json',study)
    save(CASE/'rim_revision_provenance.json',dict(source_scad_sha256=sha(source),
          reused_native_surface_sha256=sha(PART/'spec/frame_a_density_surface.stl'),
          native_optimisation_case=str(BASE),same_load_material_keys=same,listed_inputs_equal=True,
          load_patch_revision='Upper C regions now span33..45, matching the preserved45mm seat; other interfaces remain0..12.',
          selected_base_mm=base,retained_rail_depth_mm=45,full_sha256=sha(full),
          unchanged_splice_sha256=sha(PART/'child_exterior_structural_frame_splice.stl'),
          method='Native optimised interior retained; rim cropped to thinner rounded CAD stock. No new topology optimisation run.'))
    run('final_fea',CLI+['fea',str(CASE/'study_final.json'),'--out',str(CASE/'final_fea'),
                        '--voxel','2','--converge'],allowed=(0,1))
    fea=json.loads((CASE/'final_fea/child_exterior_structural_frame_full_fea.json').read_text())
    strict=all(c['min_safety_factor']>=3 and c['max_displacement_mm']<=2 for c in fea['cases'])
    save(CASE/'fine_mesh_thresholds.json',dict(pass_fine_thresholds=strict,
         note='Fine-mesh thresholds alone do not imply mesh convergence or bolt-joint qualification.'))
    if not strict:raise RuntimeError('Rim shortlist failed final fine-mesh thresholds; reconsider before packaging')


if __name__=='__main__':main()
