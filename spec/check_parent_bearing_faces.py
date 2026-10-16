"""Check washer bearing faces against structural parts, never against other hardware.

A screw/washer/nut group can float together and fool an all-pairs nearest check.
This separate test checks distributed points on both washer faces against the
actual printed/purchased support surfaces. Geometry only, not a strength test.
"""
from pathlib import Path
import sys,json
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scad/lib'))
from check_asm_contacts import load,matrix
OUT=ROOT/'assemblies/parent_bottom_sensors'
asm=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
solid={it['label']:load(ROOT,it) for it in asm['items'] if it['group'] in ['exterior','vessel','reference']}
results=[]
for it in asm['items']:
 name=it.get('file','')
 if it['group']!='hardware' or not name.startswith('washer_'):continue
 d=int(name.split('_m')[1].split('x')[0]);outer={4:9,5:10,6:12,8:16}[d]
 # Mid-annulus ring avoids the clearance bore and washer outside edge.
 r=((d+.5)/2+outer/2)/2
 a=np.arange(24)*np.pi/12
 p=np.array([[r*np.cos(t),r*np.sin(t),z] for z in [0,1] for t in a])
 p=trimesh.transform_points(p,matrix(it['ops']))
 all_dist=np.full(48,np.inf);supports=[]
 for label,m in solid.items():
  if np.any(p.min(axis=0)>m.bounds[1]+1) or np.any(p.max(axis=0)<m.bounds[0]-1):continue
  _,dist,_=trimesh.proximity.closest_point(m,p)
  all_dist=np.minimum(all_dist,dist)
  if np.any(dist<.08):supports.append(label)
 faces=all_dist.reshape(2,24)
 best=(float(np.median(faces,axis=1).min()),supports,int((faces<.08).sum(axis=1).max()))
 results.append(dict(label=it['label'],support=best[1],median_gap_mm=best[0],contact_points_of_24=best[2],pass_bearing=best[2]>=12))
bad=[r for r in results if not r['pass_bearing']]
(OUT/'bearing_checks.json').write_text(json.dumps(dict(washers=len(results),failures=bad,results=results),indent=2),encoding='utf-8')
print('Washer bearing faces:',len(results),'FAIL:',len(bad),flush=True)
for r in bad:print(r,flush=True)
sys.exit(bool(bad))
