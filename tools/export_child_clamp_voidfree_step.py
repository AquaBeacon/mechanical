"""FreeCAD CLI: export the void-free STEP and reuse its shape in the assembly.

Environment ASM_ROOT. Uses the original source STEP/STL converter and assembly
writer unchanged, with its native shape passed through the optional cache.
"""
import os
import runpy
from pathlib import Path

root = Path(os.environ['ASM_ROOT'])
part = root/'parts/child/exterior/printed/child_wte4_suspension_clamp'
case = part/'_work/analysis/connected_cage_rubber1_solid'
step = part/'child_wte4_suspension_clamp_cage.step'
os.environ.update(STL_IN=str(case/'step_interface_proxy.stl'),STEP_OUT=str(step))
exported = runpy.run_path(str(root/'scad/lib/stl_to_step.py'))
shape = exported['result']
if not shape.isValid() or len(shape.Solids)!=1 or len(shape.Shells)!=1:
    raise RuntimeError('Void-free source STEP must be a valid single-shell solid')
os.environ.update(ASM_JSON=str(root/'assemblies/child_clamp_suspension/placement.json'),
    STEP_OUT=str(root/'assemblies/child_clamp_suspension/child_clamp_suspension.step'))
key = (os.path.normcase(os.path.abspath(step)),step.stat().st_mtime_ns)
runpy.run_path(str(root/'scad/lib/asm_to_step.py'),init_globals={'_shape_cache':{key:shape}})
