"""Prepare existing topopt/CalculiX analysis inputs; no solver implementation."""
import json, shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service/rigidity'
O.mkdir(exist_ok=True)
source=R/'parts/parent/interior/printed/parent_hand_service/lift_carrier.stl'
if (O/'baseline_carrier.stl').exists():
 raise SystemExit('Baseline already exists: refusing to overwrite analysis geometry with revised CAD.')
shutil.copy2(source,O/'baseline_carrier.stl')
regions={}
for i,(x,y) in enumerate([(19,140),(19,190),(129.5,140),(129.5,190)]):
 regions['support_'+str(i)]=dict(type='box',min=[x-2,y-2,54.95],max=[x+2,y+2,55.3])
patches={'MAIN_USB':([31.9,82.4,63.7],[45.1,86.6,64.05]),'MAIN_SD':([52.9,82.4,63.7],[72.1,86.6,64.05]),'SONY_FRONT':([153.5,69.5,62.7],[160,75.6,63.1]),'SONY_REAR':([196.5,120,62.7],[203,127,63.1])}
for name,(lo,hi) in patches.items():regions[name]=dict(type='box',min=lo,max=hi)
cases=[]
for name in patches:
 for axis in range(3):
  for sign in [-1,1]:
   f=[0,0,0];f[axis]=20*sign
   cases.append(dict(name=name+'_'+('XYZ'[axis])+('+' if sign>0 else '-'),supports=[dict(region='support_'+str(i),fix='xyz') for i in range(4)],loads=[dict(region=name,force=f)]))
study=dict(part='baseline_carrier.stl',material='PETG',build_axis='Z',units='mm_N_MPa',safety_factor=3,max_deflection_mm=.2,walls=4,infill=1,regions=regions,cases=cases,
 _what='Baseline carrier ONLY; service support patches ideally fixed. USB/SD load transferred to nearby support patches, not actual connector shell.',
 _limitations=['Not complete assembly FEA','Ideal clamps omit floor, props, joints and case flexibility','Sony front/rear patches are mounting-post loads, not connector displacement','No PCB deformation or connector solder-joint assessment','PETG provisional material card; no actual printer measurement'])
(O/'baseline_study.json').write_text(json.dumps(study,indent=2),encoding='utf-8')
print(O/'baseline_study.json')
