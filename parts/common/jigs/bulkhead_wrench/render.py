from pathlib import Path
import subprocess
p=Path('parts/common/jigs/bulkhead_wrench').resolve()
r=subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(p/'bulkhead_wrench.stl'),str(p/'bulkhead_wrench.scad')],capture_output=True,text=True)
print(r.stdout,r.stderr);raise SystemExit(r.returncode)
