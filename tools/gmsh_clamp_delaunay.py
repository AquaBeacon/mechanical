"""Run native Gmsh with explicit cavity loops and visible batch logs."""
from pathlib import Path
import sys
import gmsh
import re
import trimesh
import hashlib
import json
import os

if sys.argv[1:]==['--version']:
    print(gmsh.__version__)
    raise SystemExit(0)
source=Path(sys.argv[1]).resolve()
wrapper=source.with_suffix('.delaunay.geo')
original=source.read_text(encoding='utf-8')
match=re.search(r'Merge\s+"([^"]+)";',original)
if not match:
    raise RuntimeError('Expected the native topopt STL import')
mesh=trimesh.load(match[1],force='mesh')
shells=mesh.split(only_watertight=False)
outer=[s for s in shells if s.volume>0]
cavities=[s for s in shells if s.volume<0]
if cavities:
    if len(outer)!=1 or not all(s.is_watertight for s in shells):
        raise RuntimeError('Expected one closed outer shell with closed cavities')
    geometry=[]
    audit=[]
    for i,shell in enumerate(outer+cavities,1):
        boundary=source.with_name(source.stem+f'_boundary{i}.stl')
        shell.export(boundary)
        audit.append(dict(surface=i,source_signed_volume_mm3=float(shell.volume),path=str(boundary),
                          sha256=hashlib.sha256(boundary.read_bytes()).hexdigest()))
        geometry.append(f'Merge "{boundary.as_posix()}";\nSurface Loop({i}) = {{{i}}};')
    geometry += ['Volume(1) = {'+','.join(str(i) for i in range(1,len(shells)+1))+'};',
                 'Physical Volume("part") = {1};']
    settings=original[original.index('Mesh.'):]
    # Distinct native boundary surfaces give each void its own surface loop.
    # A single STL surface with five disconnected shells fills the voids in
    # Delaunay and fails HXT's Brep color reconstruction.
    wrapper.write_text('\n'.join(geometry)+'\n'+settings,encoding='utf-8')
    source.with_suffix('.boundary_import.json').write_text(json.dumps(dict(
        method='Native Gmsh Surface Loop per original closed boundary; one material Volume with inner void loops',
        source=str(Path(match[1])),source_sha256=hashlib.sha256(Path(match[1]).read_bytes()).hexdigest(),
        source_material_volume_mm3=float(mesh.volume),boundaries=audit),indent=2)+'\n',encoding='utf-8')
else:
    wrapper.write_text('Include "'+source.as_posix()+'";\nMesh.Algorithm3D = 1;\n',encoding='utf-8')
# run=True invokes Gmsh's own command-line parser/batch pipeline. No custom
# meshing, refinement, finite elements or solver are implemented here.
algorithm=os.environ.get('TOPOPT_GMSH_ALGORITHM')
if algorithm:
    with wrapper.open('a',encoding='utf-8') as stream:
        stream.write(f'\nMesh.Algorithm3D = {int(algorithm)};\n')
gmsh.initialize(['gmsh',str(wrapper),*sys.argv[2:],'-nt',os.environ.get('TOPOPT_GMSH_THREADS','4'),'-nopopup','-log',str(source.with_suffix('.gmsh.log'))],run=True)
gmsh.finalize()
