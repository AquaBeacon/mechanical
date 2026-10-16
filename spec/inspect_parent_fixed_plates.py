"""Read-only envelope probes for flat PCB fixing plates, mm."""
from parent_access_common import *
rows=[]
d=json.loads((O/'placement.json').read_text(encoding='utf-8'))
for name,z in [('p_main',42),('spresense',65.6)]:
 it=next(q for q in d['items'] if q['label']==name)
 s=Part.read(str(R/it['part']/(it.get('file',Path(it['part']).name)+'.step')))
 for op in reversed(it['ops']):
  for axis,ang in zip([v(1,0,0),v(0,1,0),v(0,0,1)],op.get('rotate',[0,0,0])):s.rotate(v(0,0,0),axis,ang)
  if 'translate' in op:s.translate(v(*op['translate']))
 b=s.optimalBoundingBox(False,False)
 under=[p.optimalBoundingBox(False,False) for p in s.Solids if p.optimalBoundingBox(False,False).ZMin<z-.05]
 print(name,'bbox',b,'underside',sorted([(round(q.ZMin,4),round(q.ZMax,4),round(q.XMin,3),round(q.XMax,3),round(q.YMin,3),round(q.YMax,3)) for q in under])[:80],flush=True)
 for zz,thick in ([(33.1,2.4)] if name=='p_main' else [(60.5,2),(60.5,1.2)]):
  plate=Part.makeBox(b.XLength,b.YLength,thick,v(b.XMin,b.YMin,zz))
  print('candidate',zz,thick,'collision_mm3',common(s,plate),flush=True)
