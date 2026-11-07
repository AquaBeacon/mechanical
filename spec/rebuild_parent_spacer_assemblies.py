"""Refresh both existing STEP poses through the repository's assembly exporter."""
import hashlib
import json
import os
from pathlib import Path
import runpy

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_hand_service'
cache={};results=[]
for pose,filename in [('closed','placement.json'),('service','service_placement.json')]:
    os.environ.update(ASM_ROOT=str(ROOT),ASM_JSON=str(OUT/filename),STEP_OUT=str(OUT/(pose+'.step')))
    namespace=runpy.run_path(str(ROOT/'scad/lib/asm_to_step.py'),init_globals={'_shape_cache':cache})
    cache=namespace['_shape_cache']
    assert namespace['made']==len(json.loads((OUT/filename).read_text(encoding='utf-8'))['items'])
    assert not namespace['missing']
    os.environ['STEP_IN']=str(OUT/(pose+'.step'))
    try:
        runpy.run_path(str(ROOT/'scad/lib/verify_asm_step.py'),run_name='__main__')
    except SystemExit as exc:
        assert exc.code in (None,0),(pose,exc.code)
    results.append(dict(pose=pose,items=namespace['made'],status='PASS',bbox_tolerance_mm=.5,
                        step_sha256=hashlib.sha256((OUT/(pose+'.step')).read_bytes()).hexdigest()))
(OUT/'assembly_checks.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print('PASS both assembly poses; Sony right bearing foot updated',flush=True)
