"""Native STEP mesher input adapter; the existing CalculiX pipeline is unchanged."""
import sys,json,hashlib,os
from pathlib import Path
from topopt import ccx
from topopt.cli.ccx import main
step=Path(sys.argv[1]).with_suffix('.step').resolve()
assert step.exists()
surface_algorithm=int(os.environ.get('PARENT_GMSH_SURFACE_ALGORITHM','6'))
circle_points=int(os.environ.get('PARENT_GMSH_CIRCLE_POINTS','7'))
floor_mode=os.environ.get('PARENT_GMSH_FLOOR_LOCAL','')
floor_local=bool(floor_mode)
def native_geo(path,unused_stl,target_mm):
 # Gmsh imports and remeshes exact CAD surfaces independently at every size.
 # No numerical meshing or FEM algorithm is implemented in this adapter.
 local=f'MeshSize {{ PointsOf{{ Surface{{373,465}}; }} }} = {target_mm/6};\n' if floor_local else ''
 if floor_mode=='smallfaces':
  local='''all_s()=Surface{:};
For i In {0:#all_s()-1}
  bb()=BoundingBox Surface{all_s(i)};
  If ((bb(3)-bb(0))<10 && (bb(4)-bb(1))<10)
    MeshSize{PointsOf{Surface{all_s(i)};}} = LOCAL_H;
  EndIf
EndFor
'''.replace('LOCAL_H',str(target_mm/6))
 Path(path).write_text(f'''SetFactory("OpenCASCADE");
v() = ShapeFromFile("{step.as_posix()}");
Physical Volume("part") = {{v()}};
Mesh.CharacteristicLengthMin = {target_mm/(8 if floor_local else 2)};
Mesh.CharacteristicLengthMax = {target_mm};
Mesh.Algorithm = {surface_algorithm};
Mesh.MinimumCirclePoints = {circle_points};
Mesh.Algorithm3D = 1;
Mesh.ElementOrder = 2;
Mesh.SecondOrderIncomplete = 0;
Mesh.SecondOrderLinear = 1;
Mesh.Optimize = 1;
Mesh.OptimizeNetgen = 0;
'''+local,encoding='utf-8')
ccx.write_geo=native_geo
# Observability only: preserve exactly the native runner's return and verdict.
native_run_ccx=ccx.run_ccx
def logged_run_ccx(inp_path,*args,**kwargs):
    stdout,base=native_run_ccx(inp_path,*args,**kwargs)
    Path(base+'_solver_stdout.log').write_text(stdout,encoding='utf-8')
    return stdout,base
ccx.run_ccx=logged_run_ccx
out=Path(sys.argv[sys.argv.index('--out')+1]);out.mkdir(exist_ok=True)
(out/'mesher_override.json').write_text(json.dumps(dict(method='Native STEP surfaces remeshed at each requested size; legacy STL surface_refinement metadata is not the mesh actually solved.',step=str(step),step_sha256=hashlib.sha256(step.read_bytes()).hexdigest(),algorithm2D=surface_algorithm,minimum_circle_points=circle_points,algorithm3D=1,second_order_linear=True,optimize_netgen=False),indent=2))
if floor_local:
 (out/'local_refinement.json').write_text(json.dumps(dict(mode=floor_mode,surface_selection='All surfaces whose X and Y bounding lengths are both <10mm' if floor_mode=='smallfaces' else [373,465],coarse_failure='Thin counterbores and deep PWR pilots; overlapping coarse surface facets. Refining only one pilot moved the failure to another pilot.',local_size='target/6',minimum='target/8',geometry_probe=str(step.parent/'mesh_probe.log')),indent=2))
print('Native STEP meshing: '+str(step)+'; independent surface/volume mesh at each target.',flush=True)
raise SystemExit(main(sys.argv[1:]))
