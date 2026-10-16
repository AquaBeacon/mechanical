"""Independent OpenSCAD/STEP comparison of the drawing-derived purchased case."""
import FreeCAD as A,Part,Mesh
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'parts/parent/exterior/cots/bcas212310g'
W=P/'_work/analysis/cad_correction_20261010';rows=[];shapes=[]
for stem in ['bcas212310g','bcas212310g_cover']:
 f=P/(stem+'.scad');out=W/(stem+'_scad_check.stl')
 p=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(out),str(f)],capture_output=True,text=True,creationflags=0x08000000)
 (W/(stem+'_scad_check.log')).write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0,p.stderr
 s=Part.read(str(f.with_suffix('.step')));m=Mesh.Mesh(str(out));b=s.optimalBoundingBox(False,False)
 delta=max(abs(getattr(b,k)-getattr(m.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
 dv=abs(s.Volume-m.Volume)/s.Volume
 assert s.isValid() and len(s.Solids)==1 and m.isSolid() and delta<.05 and dv<.02
 rows.append(dict(part=stem,valid_step=True,closed_scad_stl=True,solids=1,bbox_difference_mm=delta,relative_volume_difference=dv,volume_mm3=s.Volume,bbox_mm=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],step_sha256=hashlib.sha256(f.with_suffix('.step').read_bytes()).hexdigest()))
 shapes.append(s)
overlap=shapes[0].common(shapes[1]).Volume;assert overlap<.01
data=dict(status='PASS',checks=rows,body_cover_overlap_mm3=overlap,limits='Drawing reconstruction only; physical molding tolerance and unsectioned corner draft unverified.')
(W/'cad_checks.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print('PASS body and cover',overlap)
