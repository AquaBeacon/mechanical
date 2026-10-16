"""Fill only enclosed mesh cavities; retain the complete original outer shell.

This is CAD postprocessing, not topology optimisation or a new FEM solver.
Native Manifold validates that every inward shell is inside the single outer
shell. Open holes and vessel/tool clearances remain part of that outer shell.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import trimesh
import manifold3d


def fill(source: Path, destination: Path, report: Path):
    mesh = trimesh.load(source,force='mesh')
    shells = mesh.split(only_watertight=False)
    if not all(s.is_watertight and s.is_winding_consistent for s in shells):
        raise RuntimeError('Only already closed, consistently wound shells may be filled')
    outer = [s for s in shells if s.volume>0]
    cavities = [s for s in shells if s.volume<0]
    if len(outer)!=1:
        raise RuntimeError('Expected one physical outer shell; disconnected material must not be discarded')
    solid = manifold3d.Manifold(manifold3d.Mesh(np.asarray(outer[0].vertices,dtype=np.float32),
        np.asarray(outer[0].faces,dtype=np.uint32)))
    if solid.status()!=manifold3d.Error.NoError:
        raise RuntimeError('Outer material shell is not a valid native Manifold solid')
    for cavity in cavities:
        inner = cavity.copy()
        inner.invert()
        void = manifold3d.Manifold(manifold3d.Mesh(np.asarray(inner.vertices,dtype=np.float32),
            np.asarray(inner.faces,dtype=np.uint32)))
        if void.status()!=manifold3d.Error.NoError or (void-solid).volume()>1e-4:
            raise RuntimeError('An inward shell is not an enclosed cavity of the outer material shell')
    destination.parent.mkdir(parents=True,exist_ok=True)
    outer[0].export(destination)
    result = trimesh.load(destination,force='mesh')
    expected = float(mesh.volume-sum(s.volume for s in cavities))
    if not result.is_watertight or len(result.split())!=1 or abs(result.volume-expected)>.01:
        raise RuntimeError('Closed-void fill changed more than the original enclosed void volume')
    data = dict(method='Retain unchanged positive outer shell; omit enclosed inward boundary shells',
        topology_optimisation_started=False,source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        result_sha256=hashlib.sha256(destination.read_bytes()).hexdigest(),
        enclosed_cavities_before=len(cavities),enclosed_cavities_after=0,
        added_volume_mm3=float(-sum(s.volume for s in cavities)),
        outer_surface_vertices_and_faces_unchanged=True,
        max_bounds_difference_mm=float(np.max(np.abs(mesh.bounds-result.bounds))),pass_check=True)
    report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return data
