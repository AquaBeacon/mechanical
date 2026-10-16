"""Register the clamp's provisional Bambu PETG Basic card for native topopt.

Only input data registration: all solvers, stresses and optimisation stay native.
The generic PETG registry entry and installed package files are untouched.
"""
from dataclasses import replace
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'parts/child/exterior/printed/child_wte4_suspension_clamp'
CARD = PART / 'spec/bambu_petg_basic_material.json'


def register():
    from topopt.materials import MATERIALS, ORTHOTROPIC, Orthotropic
    data = json.loads(CARD.read_text(encoding='utf-8'))
    name = data['name']
    card = Orthotropic(**data['orthotropic'])
    errors, warnings = card.check()
    if errors:
        raise ValueError(errors)
    MATERIALS[name] = replace(MATERIALS['PETG'], name=name,
        E_xy=card.Ex, E_z=card.Ez, sigma_xy=card.Xt, sigma_z=card.Zt,
        density=card.density_kg_m3/1000,
        notes='Bambu PETG Basic TDS V3.0 anchored provisional card; see '+str(CARD))
    ORTHOTROPIC[name] = card
    return data


if __name__ == '__main__':
    register()
    argv=sys.argv[1:]
    high_order=0
    minimum_mm=None
    if '--gmsh-min-mm' in argv:
        pos=argv.index('--gmsh-min-mm')
        minimum_mm=float(argv[pos+1])
        if minimum_mm<=0: raise ValueError('Gmsh minimum must be positive')
        del argv[pos:pos+2]
        if '--gmsh-algorithm' not in argv:
            raise ValueError('Specify --gmsh-algorithm with the minimum size override')
    straight_second_order='--gmsh-straight-second-order' in argv
    if straight_second_order:
        argv.remove('--gmsh-straight-second-order')
        if '--gmsh-algorithm' not in argv:
            raise ValueError('Specify --gmsh-algorithm with the midpoint-placement override')
    if '--gmsh-high-order-optimize' in argv:
        pos=argv.index('--gmsh-high-order-optimize')
        high_order=int(argv[pos+1])
        if high_order not in [1,2]: raise ValueError('High-order optimizer must be 1 or 2')
        del argv[pos:pos+2]
        if '--gmsh-algorithm' not in argv:
            raise ValueError('Specify --gmsh-algorithm with the high-order override')
    if '--gmsh-algorithm' in argv:
        # Expose the existing native write_geo algorithm parameter only.
        # HXT crashed on this CAD shell; Delaunay is also supported by topopt.
        # All meshing, FE assembly, solve, stresses and verdicts remain native.
        pos=argv.index('--gmsh-algorithm')
        algorithm=int(argv[pos+1])
        if algorithm not in [1,10]: raise ValueError('Gmsh algorithm must be 1 or 10')
        del argv[pos:pos+2]
        from topopt import ccx as native_ccx
        original_write_geo=native_ccx.write_geo
        def configured_write_geo(path,stl_path,target_mm,algorithm=algorithm):
            result=original_write_geo(path,stl_path,target_mm,algorithm=algorithm)
            if minimum_mm is not None:
                with open(path,'a',encoding='utf-8') as stream:
                    stream.write(f'\nMesh.MeshSizeMin = {minimum_mm};\n')
            if straight_second_order:
                # Retains C3D10 quadratic displacement interpolation. Only
                # locates midside nodes on the straight faceted STL edges.
                with open(path,'a',encoding='utf-8') as stream:
                    stream.write('\nMesh.SecondOrderLinear = 1;\n')
            if high_order:
                # Gmsh 4.15.2 tutorial t5 / Mesh options. Native mesher setting,
                # not a change to elements, loads, FE solver or acceptance.
                with open(path,'a',encoding='utf-8') as stream:
                    stream.write(f'\nMesh.HighOrderOptimize = {high_order};\n')
            return result
        native_ccx.write_geo=configured_write_geo
        out=Path(argv[argv.index('--out')+1]) if '--out' in argv else Path('ccx_out')
        out.mkdir(parents=True,exist_ok=True)
        (out/'clamp_mesher_override.json').write_text(json.dumps(dict(
            gmsh_algorithm_3d=algorithm,native_function='topopt.ccx.write_geo',
            gmsh_high_order_optimize=high_order,
            gmsh_minimum_mm=minimum_mm,
            gmsh_second_order_linear=straight_second_order,
            finite_element_order=2,
            option_reference='https://gmsh.info/doc/texinfo/',
            installed_package_modified=False,command=sys.argv),indent=2)+'\n',encoding='utf-8')
        print(f'Native Gmsh write_geo algorithm={algorithm}',flush=True)
    from topopt.cli import main
    sys.exit(main(argv))
