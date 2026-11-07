"""Rear hinge keepout regression, using actual old/new meshes (mm)."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'spec'))
from verify_parent_exterior_qr import intersection, probe
PART = ROOT / 'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
OUT = PART / '_work/analysis/rear_clearance_20261024'

def box(lo, hi):
    lo, hi = np.array(lo), np.array(hi)
    m = trimesh.creation.box(hi-lo)
    m.apply_translation((lo+hi)/2)
    return m

def main():
    current = trimesh.load(PART/'camera_mount_twist.stl', force='mesh')
    old = trimesh.load(OUT/'history'/PART.relative_to(ROOT)/'camera_mount_twist.stl', force='mesh')
    checks = []
    checks.append(dict(name='single_closed_solid', passed=bool(current.is_volume and len(current.split()) == 1)))
    for side in [-1, 1]:
        # Full vertical void above the original base in each support band.
        region = box([side*32-6, -22.95, 8.001], [side*32+6, -2.95, 36.501])
        volume = intersection(current, region)
        checks.append(dict(name=f'rear_20mm_side_{side}', intersection_mm3=volume, passed=volume < .01))
        points = [[side*32+x, y, 36.5] for x in [-4,0,4] for y in [-1,3,6]]
        distance = trimesh.proximity.closest_point(current, points)[1]
        checks.append(dict(name=f'front_bottom_contact_{side}', max_distance_mm=float(max(distance)), passed=bool(max(distance)<.01)))
        volume = intersection(current, probe([side*25,0,24],[side*50,0,24],12))
        checks.append(dict(name=f'D12_tool_{side}', intersection_mm3=volume, passed=volume<.01))
    for name, lo, hi in [
        ('M5_fingers_and_nut_seat', [-16,-8,8.001],[16,8,32]),
        ('rear_plate_and_C_interface', [-50,-80,8.001],[50,-25.5,90]),
        ('base', [-50,-80,0],[50,10,7.99])]:
        region = box(lo,hi)
        a = trimesh.boolean.intersection([current,region],engine='manifold')
        b = trimesh.boolean.intersection([old,region],engine='manifold')
        delta = max(0, abs(a.volume)+abs(b.volume)-2*intersection(a,b))
        checks.append(dict(name='unchanged_'+name,symmetric_difference_mm3=float(delta),passed=bool(delta<.05)))
    volume=intersection(current,probe([-60,0,24],[60,0,24],5))
    checks.append(dict(name='M5_axis',intersection_mm3=volume,passed=volume<.01))
    # Compare actual surfaces in a section through the right support.
    fig, axes = plt.subplots(1,2,figsize=(11,5),sharex=True,sharey=True)
    for ax, mesh, title in zip(axes,[old,current],['Before','Rear 20 mm clearance']):
        section=mesh.section(plane_origin=[32,0,0],plane_normal=[1,0,0])
        for path in section.discrete:
            ax.plot(path[:,1],path[:,2],color='steelblue',linewidth=1.5)
        ax.add_patch(plt.Rectangle((-22.95,8),20,28.5,color='tomato',alpha=.22,label='Required empty space'))
        ax.add_patch(plt.Rectangle((-22.95,36.5),45.9,35,color='gray',alpha=.18,label='Nominal case'))
        ax.axvline(-22.95,color='black',ls=':',lw=1)
        ax.set(title=title,xlabel='Y / forward (mm)',xlim=(-58,25),ylim=(0,76),aspect='equal')
        ax.grid(alpha=.25)
    axes[0].set_ylabel('Z (mm)'); axes[1].legend(fontsize=8)
    fig.tight_layout()
    image=PART/'_work/images/rear_clearance_20261024_section.png'
    fig.savefig(image,dpi=160);plt.close(fig)
    result=dict(passed=all(c['passed'] for c in checks),checks=checks,
        source_sha256=hashlib.sha256((PART/'camera_mount_twist.stl').read_bytes()).hexdigest(),
        bounds_mm=current.bounds.tolist(),volume_cm3=float(current.volume/1000),
        limits=['Keepout applies to lateral bottom supports above Z=8 mm base; central M5 mating fingers remain.',
                'Photo identifies hinge interference but does not establish exact hinge height/width or actual contact height.',
                'Physical fit, bolt clamping, rotation holding, material strength and creep are not certified.'])
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'clearance_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1

if __name__=='__main__':
    raise SystemExit(main())

