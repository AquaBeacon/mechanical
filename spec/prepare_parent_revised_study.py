"""Prepare an explicitly limited carrier-only analysis of the current revision."""
import json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service/rigidity'
shutil.copy2(R/'parts/parent/interior/printed/parent_hand_service/lift_carrier.stl',O/'revised_carrier.stl')
d=json.loads((O/'baseline_study.json').read_text())
d['part']='revised_carrier.stl'
centres=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))['service_prop_centres_mm']
for i,(x,y) in enumerate(centres):
 d['regions']['support_'+str(i)]=dict(type='box',min=[x-4,y-13,54.45],max=[x+4,y+13,54.75])
# For a linear, contact-free subcomponent model the opposite force has the same
# displacement magnitude. Physical assembly contact cases still need both signs.
d['cases']=[c for c in d['cases'] if c['name'].endswith('+')]
for c in d['cases']:c['supports']=[dict(region='support_'+str(i),fix='xyz') for i in range(len(centres))]
d['_what']='Revised carrier ONLY; ideal clamps at bolted service-cap faces. Not complete assembly certification.'
(O/'revised_study.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print(O/'revised_study.json')
