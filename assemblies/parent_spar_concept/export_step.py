from pathlib import Path
import subprocess,os
root=Path.cwd(); out=root/'assemblies/parent_spar_concept'
oscad=r'C:\Program Files\OpenSCAD\openscad.exe'
fc=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'
for p in ['disk','fin','hub','coupler','adapter']:
 csg=out/(p+'.csg'); target=out/(p+'.step')
 subprocess.run([oscad,'-D',f'part="{p}"','-o',str(csg),str(out/'parent_spar_concept.scad')],check=True,capture_output=True)
 env=os.environ.copy(); env.update(OPENSCAD=oscad,CSG_IN=str(csg),STEP_OUT=str(target),STL_REF=str(out/(p+'.stl')))
 r=subprocess.run([fc,str(root/'scad/lib/csg_to_step.py')],env=env,capture_output=True,text=True)
 (out/(p+'_step.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
 assert target.exists(),r.stdout+r.stderr
 print(p,'STEP OK',flush=True)
