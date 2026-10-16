from pathlib import Path
import subprocess,json,trimesh
root=Path.cwd(); out=root/'assemblies/parent_spar_concept'
scad=out/'parent_spar_concept.scad'; exe=r'C:\Program Files\OpenSCAD\openscad.exe'
report={}
for p in ['disk','fin','hub','coupler','adapter']:
 target=out/(p+'.stl')
 r=subprocess.run([exe,'-D',f'part="{p}"','-o',str(target),str(scad)],capture_output=True,text=True)
 (out/(p+'_render.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
 if r.returncode: raise RuntimeError(r.stderr)
 mesh=trimesh.load(target)
 report[p]={'watertight':bool(mesh.is_watertight),'bodies':len(mesh.split()),'dimensions_mm':mesh.extents.tolist(),'volume_mm3':float(mesh.volume)}
 assert mesh.is_watertight and len(mesh.split())==1,report[p]
print(json.dumps(report,indent=2)); (out/'mesh_checks.json').write_text(json.dumps(report,indent=2))
r=subprocess.run([exe,'--imgsize=1000,1100','--viewall','--autocenter','--camera=0,0,0,70,0,30,1200','-o',str(out/'parent_spar_concept_preview.png'),str(scad)],capture_output=True,text=True)
print(r.returncode,r.stderr)

