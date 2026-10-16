import trimesh,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
out=Path('parts/common/exterior/cots/td04a_transducer/ref')
m=trimesh.load(r'C:/Users/ryupc/Downloads/model.ply'); v=m.vertices
rng=np.random.default_rng(2); sample=v[rng.choice(len(v),10000,False)]; best=0
for _ in range(250):
 p=sample[rng.choice(len(sample),3,False)]; n=np.cross(p[1]-p[0],p[2]-p[0]); n/=np.linalg.norm(n); d=-p[0]@n; ok=np.abs(sample@n+d)<1
 if ok.sum()>best: best=ok.sum(); normal=n; offset=d
inlier=v[np.abs(v@normal+offset)<1]; origin=inlier.mean(0); _,_,vh=np.linalg.svd(inlier-origin,full_matrices=False); normal=vh[-1]; heights=(v-origin)@normal
if abs(np.percentile(heights,1))>abs(np.percentile(heights,99)): normal=-normal
x=vh[0]; y=np.cross(normal,x); R=np.array([x,y,normal]); w=(v-origin)@R.T
np.savez(out/'scan_alignment.npz',rotation=R,origin=origin)
m.vertices=w;m.export(out/'scan_aligned.ply')
sel=rng.choice(len(w),65000,False); q=w[sel]
f,axes=plt.subplots(1,3,figsize=(15,5))
for a,(i,j) in zip(axes,[(0,1),(0,2),(1,2)]):
 a.scatter(q[:,i],q[:,j],c=q[:,2],s=.5,cmap='viridis',vmin=0,vmax=60);a.set_aspect('equal');a.set_xlabel('XYZ'[i]);a.set_ylabel('XYZ'[j]);a.grid()
f.savefig(out/'scan_aligned.png',dpi=130)
print('height percentiles',np.percentile(w[:,2],[0,1,50,90,99,100]))
