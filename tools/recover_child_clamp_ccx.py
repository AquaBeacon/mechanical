"""Read completed CCX steps using native topopt postprocessing (no re-solve)."""
from pathlib import Path
import json
import sys
from topopt import ccx as native
from topopt.cli.ccx import mesh_context,build_cases,_case_results
from topopt.loadcase import load_case_from_json
from topopt.materials import material_model

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=PART/'_work/analysis/stress_smooth_r85_v065'
h=float(sys.argv[1]) if len(sys.argv)>1 else 10.0
base=CASE/f'ccx/child_wte4_suspension_clamp_smooth_h{h:.2f}'
study=load_case_from_json(str(CASE/'study_final.json'))
mat,ortho,mat_info=material_model(study.material)
mesh=mesh_context(str(base)+'_mesh.inp')
quality=native.mesh_quality(mesh['xyz'],mesh['elements'],ids=mesh['ids'])
mass=native.mass_properties(mesh['xyz'],mesh['elements'],density_kg_m3=ortho.density_kg_m3,ids=mesh['ids'])
cases=build_cases(study,mesh,map_mode='surface',density_kg_m3=ortho.density_kg_m3,volume_mm3=mass['volume_mm3'])
res=native.parse_frd(str(base)+'.frd')
dat=native.parse_dat(str(base)+'.dat')
rows=[]
for i,case in enumerate(cases):
    c=dict(case=case['name'],step=i+1,load_class=case['load_class'],
           required_safety_factor=case['required_safety_factor'],worst_element_minimum=1.5,mapping=case['report'])
    _case_results(c,case,res['steps'][i],res,mesh,ortho,study,0.0,dat,i,ortho.density_kg_m3,mass['volume_mm3'])
    rows.append(c)
result=dict(mesh_target_mm=h,nodes=len(mesh['ids']),elements=len(mesh['elements']),mesh_quality=quality,
            mass_properties=mass,cases=rows,
            note='Native postprocessing of completed result files only. The full CLI convergence job is still running; this is not a mesh-converged acceptance.')
result['pass']=False
(CASE/f'ccx/native_partial_h{h:g}.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(mesh_target_mm=h,quality=quality,
                     cases=[dict(case=c['case'],sf=c['worst_element_safety_factor'],hotspot=c['hotspot']) for c in rows])))
