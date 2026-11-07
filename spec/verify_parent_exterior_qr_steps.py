"""Run with the documented FreeCAD CLI; compare current solids and mesh evidence."""
from pathlib import Path
import json,os
import Part
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
revision=os.environ.get('PARENT_REVISION','qr_standing')
assert revision in ('qr_standing','bolt_on_plate','universal_plate','support_reduction','removable_locators_20261022')
W=A/'_work/analysis'/revision
r=json.loads((W/'geometry_checks.json').read_text(encoding='utf-8'))
assert r['passed'],'geometry must pass before STEP release'
checks=[];seen=set()
for entry in r['meshes']:
    f=ROOT/entry['source']
    if f in seen:continue
    seen.add(f)
    sh=Part.read(str(f.with_suffix('.step')))
    bb=sh.BoundBox;b=[[bb.XMin,bb.YMin,bb.ZMin],[bb.XMax,bb.YMax,bb.ZMax]]
    delta=max(abs(b[j][i]-entry['bounds_mm'][j][i]) for j in range(2) for i in range(3))
    err=abs(sh.Volume-entry['volume_mm3'])/entry['volume_mm3']
    c=dict(file=str(f.with_suffix('.step').relative_to(ROOT)),valid=sh.isValid(),solids=len(sh.Solids),bounds_delta_mm=delta,relative_volume_error=err)
    c['passed']=c['valid'] and c['solids']==1 and delta<0.05 and err<0.0025
    checks.append(c);print(c,flush=True)
passed=all(x['passed'] for x in checks)
(W/'step_checks.json').write_text(json.dumps(dict(passed=passed,parts=checks),indent=2)+'\n',encoding='utf-8')
assert passed,'STEP checks failed'
# Preserve the existing structural alias, derived from the canonical placement.
p=json.loads((A/'placement.json').read_text(encoding='utf-8'))
p['items']=[x for x in p['items'] if x['group']!='hardware']
filtered=A/'_work/intermediate/qr_structure_placement.json';filtered.parent.mkdir(parents=True,exist_ok=True)
filtered.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
os.environ.update(ASM_JSON=str(filtered),ASM_ROOT=str(ROOT),STEP_OUT=str(A/'parent_oneplate_structure.step'))
os.environ.pop('ASM_GROUP',None)
exec(compile((ROOT/'scad/lib/asm_to_step.py').read_text(encoding='utf-8-sig'),'asm_to_step.py','exec'))
