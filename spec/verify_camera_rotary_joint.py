from pathlib import Path
import json, math, numpy as np, trimesh
root=Path(__file__).resolve().parents[1]
f=trimesh.load(root/'parts/parent/exterior/printed/parent_oneplate_camera_qr/parent_oneplate_camera_qr_female.stl',force='mesh')
m=trimesh.load(root/'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount_twist.stl',force='mesh')
m.apply_transform(np.array([[0,0,1,-40],[-1,0,0,0],[0,-1,0,-37.45],[0,0,0,1]],float))
records=[]
for angle in range(0,-61,-5):
 a=math.radians(angle);c=math.cos(a);s=math.sin(a)
 rot=np.array([[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]])
 flip=np.array([[1,0,0,0],[0,-1,0,0],[0,0,-1,24.5+.6*(-angle)/60],[0,0,0,1]])
 x=m.copy();x.apply_transform(rot@flip)
 overlap=trimesh.boolean.intersection([f,x],engine='manifold')
 vol=abs(float(overlap.volume)) if len(overlap.faces) else 0.0
 records.append(dict(angle_deg=angle,travel_mm=.6*(-angle)/60,intersection_mm3=round(vol,6),intersection_bounds=overlap.bounds.tolist() if vol>1e-6 else None))
 if angle==-45: cross=overlap
out=root/'parts/child/exterior/printed/dji_osmo_action6_mount_m3/_work/analysis/camera_rotary_20261029'
out.mkdir(parents=True,exist_ok=True)
result=dict(test='Parent receiver and complete camera mount; nominal prior lift path sampled every 5 degrees',receiver_local_transform='male x=cam_z-40; male y=-cam_x; male z=-37.45-cam_y; then receiver=RotZ(angle)*FlipX180 plus Z=24.5+lift',status=('FAIL' if any(r['intersection_mm3']>1e-5 for r in records) else 'SAMPLED_CLEAR'),note='Positive overlap means release is blocked. Discrete sampling alone does not prove a path clear.',samples=records)
(out/'rotary_release_current.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(7,4))
for mesh,color,label in [(f,'#72869e','receiver'),(cross,'#e44c35','intersection')]:
 sec=mesh.section(plane_origin=[0,0,0],plane_normal=[1,0,0])
 if sec is not None:
  for i,line in enumerate(sec.discrete): ax.plot(line[:,1],line[:,2],color=color,lw=1.2,label=label if i==0 else None)
ax.set(xlabel='Receiver Y (mm)',ylabel='Receiver Z (mm)',title='Release check at -45°, X = 0 section')
ax.set_aspect('equal');ax.grid(True,alpha=.3);ax.legend()
images=root/'parts/child/exterior/printed/dji_osmo_action6_mount_m3/_work/images';images.mkdir(parents=True,exist_ok=True)
fig.tight_layout();fig.savefig(images/'camera_rotary_release_current_section.png',dpi=150);plt.close(fig)
print(out/'rotary_release_current.json')
print('max intersection',max(r['intersection_mm3'] for r in records))
# Axis pull and side insertion samples of an ideal oriented M3 nut, with the
# real cavity mesh; positive intersection under pull records the reaction roof.
rows=[]
for side in [-1,1]:
 for motion, distances, base in [('axial_pull',[0,.05,.1,.25,.5,1,2,3.2],3.6),
                                  ('radial_insertion',list(range(11)),3.2)]:
  for d in distances:
   n=trimesh.creation.cylinder(radius=5.5/math.sqrt(3),height=2.4,sections=6)
   n.apply_transform(trimesh.transformations.rotation_matrix(math.radians(30),[0,0,1]))
   n.apply_translation([0,side*(52+(d if motion=='radial_insertion' else 0)),
                        base+(d if motion=='axial_pull' else 0)])
   v=trimesh.boolean.intersection([f,n],engine='manifold')
   volume=abs(float(v.volume)) if len(v.faces) else 0
   rows.append(dict(side=side,motion=motion,distance_mm=d,overlap_mm3=round(volume,6)))
(out/'nut_motion_samples.json').write_text(json.dumps(dict(
 method='Manifold intersections with oriented ideal AF5.5 x 2.4 mm hex nut; discrete samples, not continuous sweep proof',
 nut_seated_z=[2.4,4.8],screw_clearance_bottom_z=.5,results=rows),indent=2),encoding='utf-8')
