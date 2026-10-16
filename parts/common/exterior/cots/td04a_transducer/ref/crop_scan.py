import trimesh,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as p
from pathlib import Path
out=Path('parts/common/exterior/cots/td04a_transducer/ref');m=trimesh.load(out/'scan_aligned.ply');v=m.vertices
ok=(v[:,0]>-65)&(v[:,0]<30)&(v[:,1]>-40)&(v[:,1]<45)&(v[:,2]>2)
sub=m.submesh([np.flatnonzero(ok[m.faces].all(axis=1))],append=True); sub.export(out/'td04a_scan_crop.ply');q=sub.vertices
f=p.figure(figsize=(12,10))
for i,(e,z) in enumerate([(25,-60),(90,-90),(0,-90),(0,0)]):
 a=f.add_subplot(2,2,i+1,projection='3d');a.scatter(*q.T,c=q[:,2],s=.5);a.view_init(e,z);a.set_box_aspect(np.ptp(q,axis=0));a.set_xlabel('X');a.set_ylabel('Y');a.set_zlabel('Z')
f.savefig(out/'scan_crop.png',dpi=130)
