from pathlib import Path
import numpy as np,trimesh,json
from topopt.voxel import voxelize_stl
O=Path(__file__).resolve().parents[1]/'assemblies/child_petg100_design'
kwargs=dict(h=2,origin=[-250,-170,-50],shape=[220,250,175])
fixed=[voxelize_stl(O/'cad/child_core_frame_print.stl',**kwargs).solid,voxelize_stl(O/'scene/pressure_vessel.stl',**kwargs).solid]
m=trimesh.load(O/'cad/child_jaw_gate_print.stl');out=[]
for angle in [0,15,30,45,60,75,90]:
 t=trimesh.transformations.rotation_matrix(np.deg2rad(angle),[0,0,1],point=[-72,10,0]);a=m.copy();a.apply_transform(t)
 g=voxelize_stl(a.triangles,**kwargs).solid
 out.append(dict(angle_deg=angle,core_overlap_mm3=int((g&fixed[0]).sum())*8,vessel_overlap_mm3=int((g&fixed[1]).sum())*8))
(O/'gate_opening_2mm.json').write_text(json.dumps(out,indent=2));print(out)
