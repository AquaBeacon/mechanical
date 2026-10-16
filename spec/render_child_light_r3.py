from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[1]
src=R/'parts/child/exterior/printed/child_simple_rear/child_simple_rear.scad'
out=src.parent/'child_simple_rear_light_r3.png'
subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(out),'--imgsize=1000,1000','--camera=0,0,100,90,0,0,600','--viewall','--autocenter','--projection=o',str(src)],check=True)
