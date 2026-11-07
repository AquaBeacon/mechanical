"""Check the nut envelope against exported STL sections and save review views."""
from pathlib import Path
import json
import numpy as np
import trimesh
from shapely.geometry import Polygon, Point
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'parts/common/jigs/nut_driver_af10'
OUT = PART / '_work/analysis/geometry'
OUT.mkdir(parents=True, exist_ok=True)
mesh = trimesh.load_mesh(PART / 'nut_driver_af10.stl')
assert mesh.is_watertight and mesh.is_winding_consistent
assert len(mesh.split()) == 1
assert np.allclose(mesh.extents, [72, 32, 10], atol=0.015)
angles = np.radians(np.arange(6)*60+30)
nut = Polygon(np.column_stack([np.cos(angles), np.sin(angles)]) * 10/np.sqrt(3))
sections = []
for z in [0.01, 0.3, 1, 2.7, 2.99, 3.001, 3.05, 3.11, 5, 9.6, 9.99]:
    section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    loops = sorted([Polygon(p[:, :2]) for p in section.discrete], key=lambda p:p.area)
    assert len(loops) == 4
    outer = loops[-1]
    socket = min(loops[:-1], key=lambda p:abs(p.centroid.x))
    fingers = [p for p in loops[:-1] if abs(p.centroid.x)>10]
    for hole in fingers:
        assert hole.contains(Point(hole.centroid.x,0).buffer(10.999, resolution=128))
    if z>=3:
        assert socket.contains(nut), f'nut envelope collision at Z={z}'
        if 3.11<=z<=9.6:
            assert abs(socket.bounds[2]-socket.bounds[0]-10.05)<0.0001
        clearance=nut.boundary.distance(socket.boundary)
    else:
        # The nut must intersect the lid at every section along its escape path.
        assert nut.difference(socket).area>35, f'lid does not stop nut at Z={z}'
        assert socket.contains(Point(0,0).buffer(3.25, resolution=128))
        clearance=None
    sections.append(dict(z_mm=z, nut_clearance_min_mm=clearance,
                         lid_blocked_nut_area_mm2=float(nut.difference(socket).area),
                         minimum_outer_wall_mm=min(p.boundary.distance(outer.boundary) for p in loops[:-1]),
                         socket_to_finger_web_mm=min(socket.boundary.distance(p.boundary) for p in fingers)))
report = dict(watertight=True, consistent_winding=True, components=1,
              extents_mm=mesh.extents.tolist(), volume_mm3=float(mesh.volume), sections=sections,
              lid_direction='blocks nut towards Z negative; open towards Z positive',
              socket_af_mm=10.05, total_af_clearance_mm=0.05,
              provisional_socket_depth_mm=7, provisional_bolt_hole_mm=7,
              physical_fit='unverified', torque_strength='unverified', slicer='unverified')
(OUT/'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
images = PART/'_work/images'
images.mkdir(parents=True, exist_ok=True)
fig = plt.figure(figsize=(13, 5), facecolor='#f4f6f8')
ax = fig.add_subplot(131, projection='3d')
light = np.array([-0.3,-0.5,0.8]); light /= np.linalg.norm(light)
shade = 0.48 + 0.52*np.maximum(0,mesh.face_normals @ light)
colors = np.column_stack([shade*0.94,shade*0.68,shade*0.30,np.ones(len(shade))])
ax.add_collection3d(Poly3DCollection(mesh.triangles, facecolor=colors, edgecolor='none'))
ax.set(xlim=(-38,38), ylim=(-18,18), zlim=(0,13))
ax.set_box_aspect([76,36,18]); ax.view_init(elev=55, azim=-65); ax.set_axis_off()
ax.set_title('Capped spinner | 72 x 32 x 10 mm')
ax2=fig.add_subplot(132)
sec=mesh.section(plane_origin=[0,0,5], plane_normal=[0,0,1])
for p in sec.discrete:
    ax2.plot(p[:,0],p[:,1],color='#b37c27')
x,y=nut.exterior.xy
ax2.plot(x,y,'--',color='#34495e',label='10 mm AF nut envelope')
ax2.set_aspect('equal'); ax2.legend(loc='upper center',fontsize=8)
ax2.set_xlabel('mm'); ax2.set_ylabel('mm'); ax2.set_title('Socket AF 10.05 | finger holes 22 mm')
ax3=fig.add_subplot(133)
sec=mesh.section(plane_origin=[0,0,0], plane_normal=[0,1,0])
for p in sec.discrete:
    ax3.plot(p[:,0],p[:,2],color='#b37c27')
ax3.plot([-5,5],[3,3],'--',color='#34495e')
ax3.set_aspect('equal'); ax3.set_xlabel('X mm'); ax3.set_ylabel('Z mm')
ax3.set_title('Section | 3 mm lid, 7 mm pocket')
fig.tight_layout(); fig.savefig(images/'nut_driver_af10_preview.png',dpi=160)
plt.close(fig)
print(json.dumps(report))
