"""Inspect exact topology CAD export without changing the design envelope."""
from pathlib import Path
import subprocess
import sys
import trimesh
import numpy as np

PART=Path(__file__).resolve().parents[1]/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=PART/'_work/analysis/stress_smooth_r85_v065'
if sys.argv[1]=='off':
    with (CASE/'off.log').open('w') as log:
        p=subprocess.Popen(['C:/Program Files/OpenSCAD/openscad.com','-o',str(CASE/'exact.off'),
                            '-D','model="smooth"',str(PART/'child_wte4_suspension_clamp.scad')],
                            stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
    print(p.pid)
elif sys.argv[1]=='inspect':
    m=trimesh.load(CASE/'exact.off',force='mesh')
    print(len(m.faces),m.is_watertight,m.volume,np.count_nonzero(m.area_faces<1e-12))
    (CASE/'exact_off.stl').write_text(m.export(file_type='stl_ascii'),encoding='ascii')
    r=trimesh.load(CASE/'exact_off.stl',force='mesh')
    print('reload',len(r.faces),r.is_watertight,r.volume,np.count_nonzero(r.area_faces<1e-12))
elif sys.argv[1]=='gmsh':
    import gmsh
    gmsh.initialize()
    gmsh.logger.start()
    gmsh.open(str(Path(sys.argv[2]).resolve()))
    gmsh.option.setNumber('Mesh.Algorithm3D',1)
    gmsh.model.mesh.generate(3)
    print('NODES',len(gmsh.model.mesh.getNodes()[0]))
    gmsh.write(str(CASE/'gmsh_diagnostic.inp'))
    gmsh.finalize()
elif sys.argv[1]=='hxt':
    import gmsh
    gmsh.initialize()
    gmsh.option.setNumber('General.NumThreads',4)
    gmsh.open(str(CASE/'ccx/child_wte4_suspension_clamp_smooth_h5.00.geo'))
    gmsh.model.mesh.generate(3)
    gmsh.write(str(CASE/'hxt_probe.inp'))
    gmsh.finalize()
elif sys.argv[1] in ['remesh','remesh_relaxed','remesh_tight_smooth']:
    import pymeshlab
    m=trimesh.load(PART/'child_wte4_suspension_clamp_smooth.stl',force='mesh')
    ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(m.vertices,m.faces))
    relaxed=sys.argv[1]=='remesh_relaxed'
    smoothed=sys.argv[1]=='remesh_tight_smooth'
    ms.meshing_isotropic_explicit_remeshing(iterations=8 if relaxed or smoothed else 5,targetlen=pymeshlab.PureValue(1.0),
                                          featuredeg=30,checksurfdist=True,maxsurfdist=pymeshlab.PureValue(0.01 if relaxed else 0.001),
                                          smoothflag=relaxed or smoothed,reprojectflag=True)
    r=trimesh.Trimesh(ms.current_mesh().vertex_matrix(),ms.current_mesh().face_matrix())
    filename='exact_remeshed_tight_smooth.stl' if smoothed else ('exact_remeshed_relaxed.stl' if relaxed else 'exact_remeshed.stl')
    (CASE/filename).write_text(r.export(file_type='stl_ascii'),encoding='ascii')
    print('remesh',len(r.faces),r.is_watertight,r.is_winding_consistent,r.volume,np.count_nonzero(r.area_faces<1e-12))
elif sys.argv[1]=='degenerate':
    import pymeshfix
    m=trimesh.load(PART/'child_wte4_suspension_clamp_smooth.stl',force='mesh')
    f=pymeshfix.MeshFix(m.vertices,m.faces)
    print('removed',f.degeneracy_removal(max_iter=10))
    r=trimesh.Trimesh(f.points,f.faces)
    (CASE/'exact_cleaned_ascii.stl').write_text(r.export(file_type='stl_ascii'),encoding='ascii')
    s=trimesh.load(CASE/'exact_cleaned_ascii.stl',force='mesh')
    print('reload',len(s.faces),s.is_watertight,s.volume,np.count_nonzero(s.area_faces<1e-12))
elif sys.argv[1]=='tvertices':
    import pymeshlab
    m=trimesh.load(PART/'child_wte4_suspension_clamp_smooth.stl',force='mesh')
    ms=pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(m.vertices,m.faces))
    ms.meshing_remove_t_vertices(method='Edge Collapse',threshold=1e9,repeat=True)
    r=trimesh.Trimesh(ms.current_mesh().vertex_matrix(),ms.current_mesh().face_matrix())
    (CASE/'exact_tvertices.stl').write_text(r.export(file_type='stl_ascii'),encoding='ascii')
    s=trimesh.load(CASE/'exact_tvertices.stl',force='mesh')
    print('reload',len(s.faces),s.is_watertight,s.volume,np.count_nonzero(s.area_faces<1e-12))
elif sys.argv[1]=='reproduce':
    import hashlib,json
    from clean_stl_degenerates import clean
    target=CASE/'reproduced.stl'
    subprocess.run(['C:/Program Files/OpenSCAD/openscad.com','-o',str(target),
                    '-D','model="smooth"',str(PART/'child_wte4_suspension_clamp.scad')],check=True)
    clean(target,CASE/'reproduced_degeneracy.json')
    source=PART/'child_wte4_suspension_clamp_smooth.stl'
    a=trimesh.load(source,force='mesh'); b=trimesh.load(target,force='mesh')
    info=dict(canonical_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              reproduced_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
              bytes_identical=source.read_bytes()==target.read_bytes(),
              volume_delta_mm3=abs(a.volume-b.volume),bounds_delta_mm=float(np.max(abs(a.bounds-b.bounds))))
    def canonical(m):
        vertices,inverse=np.unique(m.vertices,axis=0,return_inverse=True)
        faces=np.sort(inverse[m.faces],axis=1)
        return vertices,faces[np.lexsort(faces.T)]
    va,fa=canonical(a); vb,fb=canonical(b)
    info.update(vertices_identical=np.array_equal(va,vb),faces_identical_ignoring_order=np.array_equal(fa,fb))
    info['pass_check']=info['vertices_identical'] and info['faces_identical_ignoring_order']
    (CASE/'reproduction.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(info))
