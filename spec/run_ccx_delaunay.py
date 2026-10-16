"""Use the existing Gmsh Delaunay option with unmodified topopt/CalculiX kernels.

The topopt CLI has no algorithm flag. Its public write_geo function already has
an algorithm argument: bind that configuration argument before calling the same
CLI main. All surface refinement, mapping, solving, checking and convergence
remain the existing implementation. This is not a new FEA implementation.
"""
import sys
from topopt import ccx
from topopt.cli.ccx import main
original_write_geo=ccx.write_geo
def configured_geo(path,stl,target_mm):
 original_write_geo(path,stl,target_mm,algorithm=1)
 with open(path,'a',encoding='utf-8') as f:
  f.write('\n// Disable optional Netgen optimisation after Windows access violation.\nMesh.OptimizeNetgen = 0;\n// STL facets are straight; keep quadratic mid-edge nodes on those straight edges.\nMesh.SecondOrderLinear = 1;\n')
ccx.write_geo=configured_geo
print('Mesher configuration: Gmsh Algorithm3D=1 (Delaunay), OptimizeNetgen=0, SecondOrderLinear=1; surface refinement remains enabled. Mesh quality still checked.',flush=True)
raise SystemExit(main(sys.argv[1:]))
