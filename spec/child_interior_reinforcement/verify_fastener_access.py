"""Audit straight screwdriver access with the tube removed; mm.

Tool envelopes are explicit assumptions, not a specification of a purchased tool.
Intersections describe assembly-order constraints, not automatic design failures.
"""
import json
import sys
from pathlib import Path
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scad/lib'))
from check_asm_contacts import load
from verify_child_interior import matrix

items=json.loads((ROOT/'assemblies/child_interior/placement.json').read_text(encoding='utf-8'))['items']
meshes={i['label']:load(ROOT,i) for i in items}
results=[]
for it in items:
    if '/cots/screw' not in it['part'] or not it.get('file','').startswith('screw_m3'):
        continue
    for diameter in (2.5,4.,6.):
        start=0.2 if it['file'].endswith('_flat') else 2.2
        tool=trimesh.creation.cylinder(radius=diameter/2,height=50,sections=48)
        tool.apply_translation([0,0,start+25])
        if diameter==2.5:
            shaft=trimesh.creation.cylinder(radius=2,height=42,sections=48)
            shaft.apply_translation([0,0,start+8+21])
            tool=trimesh.boolean.union([tool,shaft],engine='manifold')
        tool.apply_transform(matrix(it['ops']))
        blockers=[]
        for other in items:
            name=other['label']
            if name==it['label'] or name=='acrylic_tube_200':continue
            m=meshes[name]
            if np.any(tool.bounds[0]>=m.bounds[1]-.001) or np.any(m.bounds[0]>=tool.bounds[1]-.001):continue
            overlap=trimesh.boolean.intersection([tool,m],engine='manifold',check_volume=False)
            volume=abs(float(overlap.volume)) if len(overlap.faces) else 0.
            if volume>.01:blockers.append(dict(part=name,volume_mm3=round(volume,5)))
        results.append(dict(screw=it['label'],file=it['file'],tool_diameter_mm=diameter,blockers=blockers))
errors=[]
for r in results:
    allowed={'flange_top'}
    if r['screw'].startswith(('rail_screw_','batt_box_screw_')):
        allowed.add('child_main')
        allowed.update(i['label'] for i in items if i['label'].startswith('harness_'))
    if r['screw'].startswith('rx_clamp_cap_screw_'):
        allowed.update(i['label'] for i in items if i['label'].startswith('harness_'))
    r['assembly_order_removals']=[b['part'] for b in r['blockers'] if b['part'] in allowed]
    r['unresolved']=[b for b in r['blockers'] if b['part'] not in allowed]
    if r['tool_diameter_mm']==4 and r['unresolved']:errors.append(r)
report=dict(tool_length_mm=50,removed=['acrylic_tube_200'],
            assumption='4 mm straight shaft is the acceptance envelope; 6 mm and stepped 2.5/4 mm are diagnostics. Real bit and handle must be checked',
            errors=errors,results=results)
target=ROOT/'assemblies/child_interior/_work/analysis/fastener_access_20261006'
target.mkdir(parents=True,exist_ok=True)
(target/'access.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
for r in results:
    if r['blockers']:print(r['screw'],r['tool_diameter_mm'],[x['part'] for x in r['blockers']])
print('checked',len(results),'tool paths')
print('unresolved with 4 mm shaft and documented assembly order',len(errors))
sys.exit(bool(errors))
