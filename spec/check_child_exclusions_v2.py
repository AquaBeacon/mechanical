"""Geometric review checks only; no strength calculation."""
from pathlib import Path
import json, sys
import numpy as np
import trimesh
from topopt.voxel import voxelize_stl
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'assemblies/child_frame2_assembly/topopt_review_20260910_v2'
origin=np.array([-60.,-152.,80.]);shape=(120,100,140);h=1.
def vox(name):return voxelize_stl(str(OUT/'scene'/f'{name}.stl'),h=h,origin=origin,shape=shape).solid
hand=vox('hand_clearance');cables=vox('cables')
overlap=np.argwhere(hand&cables)
before=trimesh.load(OUT/'child_core_frame/inputs/preserve_before_cable_passages.stl',force='mesh')
after=trimesh.load(OUT/'child_core_frame/inputs/preserve.stl',force='mesh')
arrows=json.loads((OUT/'load_arrow_manifest.json').read_text(encoding='utf-8'))
studies=[json.loads(p.read_text(encoding='utf-8')) for p in OUT.glob('child_*/study.json')]
expected=sum(len(c['loads']) for s in studies for c in s['cases'])
actual=sum(len(c['loads']) for c in arrows)
assert expected==actual
result={'hand_cable_check':{'voxel_mm':h,'overlap_voxels':len(overlap),'overlap_centres_mm':(origin+(overlap+.5)*h).tolist()},
 'preserve_before_mm3':float(before.volume),'preserve_after_mm3':float(after.volume),'explicit_cable_cut_mm3':float(before.volume-after.volume),
 'force_arrows':actual,'cases':len(arrows),'gravity_arrows':sum(c['gravity'] is not None for c in arrows),
 'setup':{p.parent.parent.name:json.loads(p.read_text(encoding='utf-8'))['ok'] for p in OUT.glob('child_*/setup/study_setup.json')}}
(OUT/'review_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
