"""Native STEP mesher input adapter; the existing CalculiX pipeline is unchanged."""
import sys,json,hashlib
from pathlib import Path
from topopt import ccx
from topopt.cli.ccx import main
step=Path(sys.argv[1]).with_suffix('.step').resolve()
assert step.exists()
def native_geo(path,unused_stl,target_mm):
 # Gmsh imports and remeshes exact CAD surfaces independently at every size.
 # No numerical meshing or FEM algorithm is implemented in this adapter.
 Path(path).write_text(f'''SetFactory("OpenCASCADE");
v() = ShapeFromFile("{step.as_posix()}");
Physical Volume("part") = {{v()}};
Mesh.CharacteristicLengthMin = {target_mm/2};
Mesh.CharacteristicLengthMax = {target_mm};
Mesh.Algorithm3D = 1;
Mesh.ElementOrder = 2;
Mesh.SecondOrderIncomplete = 0;
Mesh.SecondOrderLinear = 1;
Mesh.Optimize = 1;
Mesh.OptimizeNetgen = 0;
''',encoding='utf-8')
ccx.write_geo=native_geo
out=Path(sys.argv[sys.argv.index('--out')+1]);out.mkdir(exist_ok=True)
(out/'mesher_override.json').write_text(json.dumps(dict(method='Native STEP surfaces remeshed at each requested size; legacy STL surface_refinement metadata is not the mesh actually solved.',step=str(step),step_sha256=hashlib.sha256(step.read_bytes()).hexdigest(),algorithm3D=1,second_order_linear=True,optimize_netgen=False),indent=2))
print('Native STEP meshing: '+str(step)+'; independent surface/volume mesh at each target.',flush=True)
raise SystemExit(main(sys.argv[1:]))
