"""Create compact, geometry-checked STEP companions of frame A print STLs."""
from pathlib import Path
import os,subprocess
from compact_coplanar_mesh import compact

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
FC=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'


if __name__=='__main__':
    for name in ['lower_minus','lower_plus','upper_minus','upper_plus','splice']:
        source=PART/f'child_exterior_structural_frame_{name}.stl'
        mesh=CASE/f'step_mesh_{name}.stl'
        result=compact(source,mesh,CASE/f'step_coplanar_{name}.json')
        env=os.environ.copy();env['STL_IN']=str(mesh);env['STEP_OUT']=str(source.with_suffix('.step'))
        with (CASE/f'step_compact_{name}.log').open('w') as log:
            subprocess.run([FC,str(ROOT/'scad/lib/stl_to_step.py')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        print(name,result['triangles_before'],result['triangles_after'],flush=True)
