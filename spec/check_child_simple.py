"""Reproducible mesh, strength screening and print checks for new parts only."""
import json
import subprocess
import sys
from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assemblies/child_simple_assembly'
result = {'parts': {}, 'scope': 'CAD/mesh and idealized FEA. Physical joints, EVA, preload, water exposure and impact remain untested.'}
for suffix in ['front','rear','guard']:
    name='child_simple_'+suffix
    part=ROOT/'parts/child/exterior/printed'/name/(name+'.stl')
    mesh=trimesh.load(part,force='mesh')
    record=dict(watertight=bool(mesh.is_watertight),winding_consistent=bool(mesh.is_winding_consistent),components=len(mesh.split()),bbox_mm=mesh.extents.tolist(),bounds_mm=mesh.bounds.tolist(),volume_cm3=mesh.volume/1000)
    assert record['watertight'] and record['components']==1 and record['winding_consistent'],record
    result['parts'][name]=record
    with (OUT/(suffix+'_print.log')).open('w',encoding='utf-8') as log:
        r=subprocess.run([sys.executable,'-m','topopt','print',str(part),'--printer','X1C','--load-axis','0,0,1','--keep-flat','Z' if suffix=='guard' else 'Y','--json',str(OUT/(suffix+'_print.json'))],stdout=log,stderr=subprocess.STDOUT)
        record['print_exit']=r.returncode
    print(name,record,flush=True)
    with (OUT/(suffix+'_fea_final.log')).open('w',encoding='utf-8') as log:
        r=subprocess.run([sys.executable,'-m','topopt','fea',str(OUT/(name+'_study.json')),'--out',str(OUT/('fea_'+suffix+'_final')),'--voxel','2','--converge','--no-png'],stdout=log,stderr=subprocess.STDOUT)
        record['fea_exit']=r.returncode
    print(name,'FEA exit',r.returncode,flush=True)
    (OUT/'mesh_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
