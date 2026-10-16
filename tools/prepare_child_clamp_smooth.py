"""All-eight-case stress-constrained topology, direct smoothing, same final BCs.

This supersedes the simplified-CAD route at the user's explicit request.
No FEM, optimiser, or mesh-smoothing algorithm is implemented here.
"""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=PART/'_work/analysis/stress_smooth_r85_v065'


def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    CASE.mkdir(parents=True,exist_ok=True)
    for name,model in [('preserve','topopt_preserve'),('cuts','topopt_cuts')]:
        run=subprocess.run([r'C:\Program Files\OpenSCAD\openscad.com','-o',str(CASE/(name+'.stl')),
                            '-D',f'model="{model}"',str(PART/'child_wte4_suspension_clamp.scad')],
                           capture_output=True,text=True)
        (CASE/(name+'_render.log')).write_text(run.stdout+run.stderr,encoding='utf-8')
        run.check_returncode()
    # The previous exact study already contains the 2g forces and eccentricity.
    study=json.loads((PART/'_work/analysis/topology_petg/study_candidate.json').read_text(encoding='utf-8'))
    study.pop('part',None)
    study.pop('_part_sha256',None)
    study.pop('resolution_mm',None)
    for name,region in study['regions'].items():
        if name.startswith(('frame_hole_','cap_bolt_')):
            # Covers the complete 3.5mm teardrop bore (apex radius ~2.5mm).
            # Same finite selection is used by the independent surface map.
            region['r']=2.6
        if name.startswith('rubber_contact_'):
            region['r']=12.0
        if name.startswith('clamp_washer_'):
            # Identical 1mm-thick pad in both optimisation and final CCX.
            # The CCX surface map reaches the washer face and bore entrance.
            region['range'][1]=region['range'][0]+1.1
    study['geometry']={'design_space':str(PART/'child_wte4_suspension_clamp_half.stl'),
                       'preserve':{'functional_interfaces':{'stl':str(CASE/'preserve.stl'),
                                                             'attach':[{'type':'all'}]}},
                       'clearance_mm':0}
    study['resolution_mm']=1.0
    study['required_cases']=[case['name'] for case in study['cases']]
    study['design']={'volfrac':0.65,'filter_mm':4.0,'overhang':False,'symmetry':[],
                     'optimizer':'mma','stress':{'safety_factor':3.0,'p_norm':8,
                                                'relax_q':0.5,'samples':'all'}}
    study['finish']={'voxel_mm':1.0,'smooth_mm':0.75,
                     'add':{'functional_interfaces':str(CASE/'preserve.stl')},
                     'cut':{'functional_holes':str(CASE/'cuts.stl')}}
    study['_boundary']='Identical regions, forces, support DOFs, material axes and safety factors in topology and final CCX. Four M3 teardrop-bore regions, r2.6mm to include their apex, fixed xyz; no r4.5mm substitute.'
    study['_limits']='Generic dry orthotropic PETG; no rubber contact, bolt elasticity, creep or wet strength model. Numerical stress is not an extra external load. Finite patch load, CCX surface mapping versus voxel nodal mapping, remains a discretisation difference.'
    study['_not_a_part']='User authorised directly smoothed organic topology, with CAD interfaces restored; no replacement by simple ribs. Smoothed shape still requires verification.'
    study['_what']='PETG WTE4 clamp: stress-constrained topology, direct density-field smoothing, unchanged M3 and rubber interfaces.'
    save(CASE/'study_stress_smooth.json',study)
    identity={key:study[key] for key in ['material','build_axis','raster_axis','infill','walls','safety_factor','max_deflection_mm','regions','cases']}
    save(CASE/'condition_identity.json',dict(shared_conditions=identity,
         sha256=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest(),
         note='The final verification study is derived from this same condition block. No CCX-only load cases or arbitrary hotspot forces.'))
    print(CASE/'study_stress_smooth.json')


if __name__=='__main__':
    main()
