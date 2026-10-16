"""Read-only STEP clearance probes for the wave-retention revision."""
from pathlib import Path
import sys,json,subprocess
if '--mesh' in sys.argv:
 R=Path(__file__).resolve().parents[1];D=R/'assemblies/parent_hand_service/_work/analysis/wave_rigidity_20261009/wave_floor_budget/floor_plate'
 t='SetFactory("OpenCASCADE");\nv()=ShapeFromFile("'+(D/'floor_plate.step').as_posix()+'");\n'
 for i in [373,465]:
  t+=f'b{i}()=BoundingBox Surface {{{i}}};\n'
  t+=f'Printf("SURFACE {i} %g %g %g %g %g %g",'+','.join(f'b{i}({j})' for j in range(6))+');\n'
 (D/'mesh_probe.geo').write_text(t)
 r=subprocess.run(['C:/Users/ryupc/Tools/gmsh-4.15.2-Windows64/gmsh.exe',str(D/'mesh_probe.geo'),'-0','-o',str(D/'mesh_probe.geo_unrolled')],capture_output=True,text=True)
 (D/'mesh_probe.log').write_text(r.stdout+r.stderr)
 print(r.stdout+r.stderr);raise SystemExit(r.returncode)
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'spec'))
from parent_access_common import load,v,common
d,s=load()
probes={'gnss_front_beam':(9.5,142,50,129,6,6),'gnss_rear_beam':(16,216,50,123,6,6),'gnss_rear_columns':(16,216,18.8,8,6,37.2),'floor_under_ribs':(14,14,8.84,182,202,5)}
for n,xyz in probes.items():
 b=Part.makeBox(*xyz[3:],v(*xyz[:3]));out=[]
 for label in ['p_pwr','tx_improved','p_main','spresense','case']:
  if label not in s:continue
  for i,p in enumerate(s[label].Solids):
   if not p.BoundBox.intersect(b.BoundBox):continue
   vol=common(b,p)
   if vol>.001:
    bb=p.BoundBox;out.append(dict(label=label,solid=i,volume=vol,bounds=[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax]))
 print(n,json.dumps(out),flush=True)
