"""Compare exact rim revisions around the existing native optimisation surface.

CAD operations and study authoring only; the installed native topopt solver
performs every analysis. Candidate meshes stay under _work and are not prints.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
import numpy as np
import trimesh
from clean_stl_degenerates import precision_weld,clean

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
BASE=PART/'_work/analysis/frame_a_compact_grip'
OSC=r'C:\Program Files\OpenSCAD\openscad.com'
CLI=[sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py')]


def save(p,v):
    p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def rank(fea,maximum,minimum):
    failures=[check for c in fea['cases'] for check in c['checks'] if not check['pass']]
    # Resolution failures are expected for coarse ranking and stay visible.
    # They require the final 4/2/1mm study, never a strength qualification.
    return minimum>=3 and maximum<=1.8 and all(x['name']=='mesh resolution' for x in failures),failures


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bases',nargs='+',type=float,default=[4,6,8]);ap.add_argument('--reuse-fea',action='store_true');args=ap.parse_args()
    source=PART/'child_exterior_structural_frame.scad'
    surface=trimesh.load(PART/'spec/frame_a_density_surface.stl',force='mesh')
    cuts=trimesh.load(CASE/'cuts.stl',force='mesh')
    fixed=trimesh.boolean.union([trimesh.load(CASE/(n+'.stl'),force='mesh') for n in ['rail_stock','seat_base','deep_seats']],engine='manifold')
    core=trimesh.boolean.difference([trimesh.load(CASE/'domain_envelope.stl',force='mesh'),trimesh.load(CASE/'rim_trim.stl',force='mesh')],engine='manifold')
    baseline=json.loads((BASE/'final_fea/child_exterior_structural_frame_full_fea_convergence.json').read_text())
    oldpath=BASE/'input_history/before_rim_revision'/PART.relative_to(ROOT)/'child_exterior_structural_frame_full.stl'
    old=trimesh.load(oldpath,force='mesh')
    study_template=json.loads((BASE/'study_final.json').read_text())
    rows=[]
    for base in args.bases:
        depth=45
        folder=CASE/'candidates'/f'base_{base:g}_solid_grip';folder.mkdir(parents=True,exist_ok=True)
        if args.reuse_fea:
            row=json.loads((folder/'candidate.json').read_text())
            assert row['source_sha256']==sha(folder/'frame.stl')
            fea=json.loads((folder/'fea/frame_fea.json').read_text())
            row['ranking_eligible'],row['coarse_check_failures']=rank(fea,row['max_displacement_mm'],row['min_worst_element_safety_factor'])
            rows.append(row);save(folder/'candidate.json',row)
            print('Rim base',base,'shortlist',row['ranking_eligible'],flush=True)
            continue
        for kind in ['rim_base']:
            cmd=[OSC,'--export-format','binstl','-o',str(folder/(kind+'.stl')),
                 '-D',f'model="{kind}"','-D',f'rim_base_thickness={base}',str(source)]
            with (folder/(kind+'_render.log')).open('w') as log:
                subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
        rim=trimesh.load(folder/'rim_base.stl',force='mesh')
        preserve=trimesh.boolean.union([fixed,rim],engine='manifold')
        domain=trimesh.boolean.intersection([trimesh.boolean.union([core,preserve],engine='manifold'),trimesh.load(CASE/'domain_envelope.stl',force='mesh')],engine='manifold')
        for n,m in [('preserve',preserve),('domain',domain)]:
            p=folder/(n+'.stl');m.export(p)
            precision_weld(p,folder/(n+'_precision_weld.json'),allow_collinear=True)
            clean(p,folder/(n+'_edge_flip.json'),binary=True)
        domain=trimesh.load(folder/'domain.stl',force='mesh')
        preserve=trimesh.load(folder/'preserve.stl',force='mesh')
        frame=trimesh.boolean.union([surface,preserve],engine='manifold')
        frame=trimesh.boolean.difference([frame,cuts],engine='manifold')
        frame=trimesh.boolean.intersection([frame,domain],engine='manifold')
        path=folder/'frame.stl';frame.export(path)
        precision_weld(path,folder/'precision_weld.json',allow_collinear=True)
        clean(path,folder/'edge_flip.json',binary=True)
        frame=trimesh.load(path,force='mesh')
        assert frame.is_volume and not np.any(frame.area_faces<1e-12)
        assert len(frame.split(only_watertight=False))==1
        assert np.max(np.abs(old.bounds-frame.bounds))<1e-5,'Comparison bounds/grid origin changed'
        study=dict(study_template,part=str(path),_part_sha256=sha(path),
                   _rim_revision=dict(base_mm=base,wall_mm=3,depth_mm=depth,solid_grip_retained=True),
                   _status='exploration_only; 2mm ranking is not mesh convergence')
        save(folder/'study.json',study)
        with (folder/'fea.log').open('w') as log:
            result=subprocess.run(CLI+['fea',str(folder/'study.json'),'--out',str(folder/'fea'),'--voxel','2'],
                                  stdout=log,stderr=subprocess.STDOUT)
        fea=json.loads((folder/'fea/frame_fea.json').read_text())
        minimum=min(c['min_safety_factor'] for c in fea['cases'])
        maximum=max(c['max_displacement_mm'] for c in fea['cases'])
        eligible,failures=rank(fea,maximum,minimum)
        row=dict(depth_mm=depth,base_mm=base,wall_mm=3,source_sha256=sha(path),volume_mm3=float(frame.volume),
                 part_mass_g=float(frame.volume*1.25/1000),fea_exit_code=result.returncode,
                 max_displacement_mm=maximum,min_worst_element_safety_factor=minimum,
                 ranking_eligible=eligible,coarse_check_failures=failures,
                 # A 10% displacement margin is for shortlist selection only.
                 cases=fea['cases'],bounds_identical=True,voxel_mm=2)
        rows.append(row);save(folder/'candidate.json',row)
        print('Rim base',base,'mass',round(row['part_mass_g'],1),'max displacement',round(maximum,4),
              'worst SF',round(minimum,2),'shortlist',row['ranking_eligible'],flush=True)
    eligible=[r for r in rows if r['ranking_eligible']]
    report=dict(status='exploration_only',method='Existing native density surface plus thinner exact rim; same seven native FEA cases, bounds and 2mm voxel',
                baseline_mass_g=float(old.volume*1.25/1000),
                baseline_2mm={n:next(x for x in v['runs'] if x['target_mm']==2) for n,v in baseline['cases'].items()},
                candidates=rows,selected_base_mm=min(eligible,key=lambda r:r['volume_mm3'])['base_mm'] if eligible else None)
    save(CASE/'rim_comparison.json',report)
    if not eligible:raise RuntimeError('No rim candidate met the coarse shortlist criteria')


if __name__=='__main__':main()
