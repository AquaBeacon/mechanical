"""Preview copied finished STEP/STL with actual study regions; no FEM logic."""
from pathlib import Path
import sys,json,subprocess
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';tag=sys.argv[1]
for name in sys.argv[2:]:
 p=O/'_work/analysis/wave_rigidity_20261009'/tag/name;s=json.loads((p/'study.json').read_text())
 t='color("Gainsboro",0.65) import("'+(p/(name+'.stl')).as_posix()+'",convexity=30);\n'
 for k,r in s['regions'].items():
  if k=='self_mass':continue
  lo=r['min'];hi=r['max'];size=[max(.7,b-a) for a,b in zip(lo,hi)]
  t+='color('+('"LimeGreen"' if k.startswith('foot') else '"Tomato"')+',0.8) translate('+json.dumps(lo)+') cube('+json.dumps(size)+');\n'
 sc=O/'_work/intermediate'/f'wave_bc_{tag}_{name}.scad';sc.write_text(t)
 image=O/'_work/images'/f'wave_bc_{tag}_{name}.png'
 cmd=['C:/Program Files/OpenSCAD/openscad.exe','--preview','--imgsize=1200,900','--viewall','--autocenter','--camera=0,0,0,60,0,30,500','-o',str(image),str(sc)]
 subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL)
 print(image)
