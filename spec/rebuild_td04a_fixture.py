"""Run the existing CAD/STEP/print-pack pipeline only for the TD04A fixture."""
from pathlib import Path
import json
import hashlib
import io
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/common/exterior/printed/td04a_bracket_mount'
A=ROOT/'assemblies/td04a_fixture'
OPENSCAD=Path(os.environ.get('OPENSCAD',r'C:\Program Files\OpenSCAD\openscad.exe'))
FREECAD=Path(os.environ.get('FREECADCMD',r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'))

def run(args,env=None):
    import datetime
    proc=subprocess.Popen([str(a) for a in args],cwd=ROOT,env=env)
    print(json.dumps(dict(pid=proc.pid,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),purpose=str(args[0]),ownership='td04a-r6')),flush=True)
    try:
        code=proc.wait(timeout=600)
        if code: raise subprocess.CalledProcessError(code,args)
    except BaseException:
        if proc.poll() is None:
            proc.terminate(); proc.wait(timeout=15)
        raise
def main():
    for d in [A/'_work/logs',A/'_work/images',A/'_work/analysis',A/'_work/intermediate',PART/'_work/intermediate',PART/'_work/analysis']:
        d.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    data=json.loads((A/'placement.json').read_text(encoding='utf-8'))
    for v in data['fixture_variants']:
        stem=v['stem'];stl=PART/(stem+'.stl')
        old=stl.read_bytes() if data.get('preserve_parent_accepted_bytes', False) and v['unit']=='parent' and stl.exists() else None
        run([OPENSCAD,'--export-format','asciistl','-D','variant="'+v['variant']+'"','-o',stl,PART/'td04a_bracket_mount.scad'])
        run([sys.executable,'tools/clean_stl_degenerates.py',stl,'--configured','--report',PART/'_work/analysis'/(stem+'_cleanup.json')])
        if old is not None:
            import numpy as np
            import trimesh as tm
            from scipy.spatial import cKDTree
            before=tm.load_mesh(io.BytesIO(old),file_type='stl');after=tm.load_mesh(stl)
            distances=[float(cKDTree(a.vertices).query(b.vertices)[0].max()) for a,b in [(before,after),(after,before)]]
            delta=abs(float(before.volume)-float(after.volume))
            same=np.allclose(before.bounds,after.bounds,atol=1e-5) and delta<1e-4 and max(distances)<1e-4
            record=dict(passed=bool(same),method='Fresh source render and cleaned candidate compared to accepted mesh; accepted bytes retained only after equivalence.',accepted_sha256=hashlib.sha256(old).hexdigest(),candidate_sha256=hashlib.sha256(stl.read_bytes()).hexdigest(),max_bidirectional_vertex_delta_mm=max(distances),volume_delta_mm3=delta)
            (A/'_work/analysis/parent_preservation.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
            if not same:
                stl.write_bytes(old)
                raise RuntimeError('Parent geometry changed; accepted bytes restored; investigate.')
            (PART/'_work/intermediate/parent_verified_candidate.stl').write_bytes(stl.read_bytes())
            stl.write_bytes(old)
            continue
        compact=PART/'_work/intermediate'/(stem+'-step-mesh.stl')
        run([sys.executable,'tools/compact_coplanar_mesh.py',stl,'--out',compact,'--report',PART/'_work/analysis'/(stem+'-step-coplanar.json')])
        env.update(STL_IN=str(compact),STEP_OUT=str(stl.with_suffix('.step')))
        run([FREECAD,'scad/lib/stl_to_step.py'],env)
    run([sys.executable,'tools/assembly_parts.py','sync','td04a_fixture'])
    run([sys.executable,'spec/render_td04a_fixture.py'])
    env.update(ASM_JSON=str(A/'placement.json'),ASM_ROOT=str(ROOT),STEP_OUT=str(A/'td04a_fixture.step'),STEP_IN=str(A/'td04a_fixture.step'))
    run([FREECAD,'scad/lib/asm_to_step.py'],env)
    run([FREECAD,'scad/lib/verify_asm_step.py'],env)
if __name__=='__main__':main()
