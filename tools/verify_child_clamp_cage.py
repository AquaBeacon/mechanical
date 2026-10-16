"""Verify the actual connected-cage STL, holes, vessel fit and X1C placement.

No FEA is implemented here. Strength verdicts remain in native topopt outputs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import trimesh
import manifold3d

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
from child_clamp_case import analysis_case
CASE = analysis_case(PART)


def native_solid(mesh):
    # ASCII CAD tessellations carry double precision. Keep it for verification:
    # float32 conversion alone changed a valid candidate volume by 0.055 mm3.
    solid = manifold3d.Manifold(manifold3d.Mesh64(np.asarray(mesh.vertices,dtype=np.float64),
        np.asarray(mesh.faces,dtype=np.uint64)))
    if solid.status()!=manifold3d.Error.NoError or abs(solid.volume()-mesh.volume)>.01:
        raise RuntimeError('Native ray-cast solid does not match verified STL')
    return solid


def contains(solid, points):
    # Native Manifold's acceleration structure bounds memory for organic meshes.
    # A non-axial ray avoids the axis-aligned feature edges in these samples.
    direction = np.array([997.,431.,271.])
    result = []
    for point in np.asarray(points):
        hits = solid.ray_cast(point.tolist(),(point+direction).tolist())
        distances = sorted(hit.distance for hit in hits)
        unique = [v for i,v in enumerate(distances) if i==0 or v-distances[i-1]>1e-9]
        result.append(len(unique)%2==1)
    return np.array(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stl', type=Path, default=CASE/'finished_cage.stl')
    parser.add_argument('--out', type=Path, default=CASE/'geometry_checks.json')
    parser.add_argument('--require-no-closed-voids',action='store_true',
        help='reject any enclosed inward boundary shell')
    parser.add_argument('--print-stl', type=Path, default=CASE/'cage_print_orientation.stl',
        help='derived orientation output; use a separate path for STEP proxies')
    args = parser.parse_args()
    data = json.loads((CASE/'interface.json').read_text(encoding='utf-8'))
    d, c = data['clamp'], data['cage']
    mesh = trimesh.load(args.stl, force='mesh')
    shells = mesh.split(only_watertight=False)
    outer = [s for s in shells if s.volume>0]
    cavities = [s for s in shells if s.volume<0]
    solid = native_solid(mesh)
    outer_solid = native_solid(outer[0]) if len(outer)==1 else None
    checks = dict(source=str(args.stl.resolve()), sha256=hashlib.sha256(args.stl.read_bytes()).hexdigest(),
        extents_mm=mesh.extents.tolist(), volume_mm3=float(mesh.volume),
        PETG_mass_g_per_half=float(mesh.volume*1.25/1000),
        PETG_mass_g_two_halves=float(mesh.volume*1.25/1000*2),
        boundary_shells=len(shells), internal_cavity_volume_mm3=float(-sum(s.volume for s in cavities)),
        watertight_one_physical_body=bool(mesh.is_watertight and mesh.is_winding_consistent and len(outer)==1 and
            all(contains(outer_solid,s.vertices[::max(1,len(s.vertices)//24)]).all() for s in cavities)),
        no_zero_area_triangles=bool(np.min(mesh.area_faces)>1e-12))
    if args.require_no_closed_voids:
        checks['no_enclosed_material_cavities'] = len(cavities)==0 and len(shells)==1
    # Query the whole bore volume including its centre; functional working size.
    def passage(axis, centre, low, high, radius):
        axes = [i for i in range(3) if i!=axis]
        points = []
        for t in np.linspace(low, high, 15):
            for r in [0,radius]:
                for angle in np.linspace(0,2*np.pi,16,endpoint=False):
                    p = np.array(centre, dtype=float)
                    p[axis] = t
                    p[axes[0]] += r*np.cos(angle)
                    p[axes[1]] += r*np.sin(angle)
                    points.append(p)
        return not contains(solid,points).any()
    frames, tools, washers, clamps, contacts = [], [], [], [], []
    clamp_washer_access, clamp_washer_seats = [], []
    washer_seat_planes=[]
    for band in c['centres']:
        z0 = band-d['band_width']/2
        for z in d['bolt_zs']:
            zz = z0+z
            for x in [-d['frame_pitch_x']/2,d['frame_pitch_x']/2]:
                frames.append(passage(1,[x,0,zz],d['mount_y']-.2,d['shoulder_y']+.2,1.5))
                tools.append(passage(1,[x,0,zz],d['shoulder_y']+.2,0,4))
                washers.append(passage(1,[x,0,zz],d['shoulder_y']+.1,d['shoulder_y']+1.1,4.5))
            for x in [-d['bolt_x'],d['bolt_x']]:
                clamps.append(passage(1,[x,0,zz],-30,-.9,1.5))
                seat=-d.get('ear_t',24)-0.8
                clamp_washer_access.append(passage(1,[x,0,zz],-100,seat-.05,6.0))
                # The intentional 3.5 mm teardrop bore reaches radius 2.48
                # at its apex; require the complete bearing annulus outside it.
                seat_points=[[x+r*np.cos(a),seat+.2,zz+r*np.sin(a)]
                    for r in [3.0,5.7] for a in np.linspace(0,2*np.pi,32,endpoint=False)]
                clamp_washer_seats.append(bool(contains(solid,seat_points).all()))
                hits=solid.ray_cast([x+3,-100,zz],[x+3,0,zz])
                if not hits: raise RuntimeError('Missing actual washer seat')
                washer_seat_planes.append(min(h.position[1] for h in hits))
        vertices = mesh.vertices[(mesh.vertices[:,2]>z0+.7)&(mesh.vertices[:,2]<z0+d['band_width']-.7)]
        contacts.append(float(np.linalg.norm(vertices[:,:2],axis=1).min()-d['tube_od']/2))
    checks.update(all_12_mount_M3_paths_clear=all(frames), all_12_OD8_tool_paths_clear=all(tools),
        all_12_OD9_washers_fit=all(washers), all_12_clamp_M3_paths_clear=all(clamps),
        all_12_clamp_OD12_washer_approaches_clear=all(clamp_washer_access),
        all_12_clamp_OD12_washer_seats_supported=all(clamp_washer_seats),
        clamp_washer_verified_bearing_radii_mm=[3.0,5.7],
        clamp_washer_seat_y=float(min(washer_seat_planes)),
        clamp_washer_seat_planes_mm=washer_seat_planes,
        clamp_washer_seat_surface_deviation_mm=float(max(washer_seat_planes)-min(washer_seat_planes)),
        # The fn16 entrance fillet differs from the original flat ear by
        # 0.0096mm. Place metal at the outermost face; bound this facet effect
        # to 0.02mm (one tenth of the specified print layer), not zero gap.
        clamp_washer_seat_planarity_within_0p02mm=bool(max(washer_seat_planes)-min(washer_seat_planes)<.02),
        band_tube_radial_clearances_mm=contacts,
        compressed_rubber_0p8mm_clearance=all(v>=.799 for v in contacts),
        rope_hole_10p5mm_clear=passage(0,c['eye'],-c['eye_width']/2-.2,c['eye_width']/2+.2,5.24),
        other_half_gap_at_least_1p59mm=bool(mesh.bounds[1,1]<=-.795))
    roofs = []
    for band in c['centres']:
        zz = band-d['band_width']/2+d['bolt_zs'][-1]
        for x in [-d['frame_pitch_x']/2,d['frame_pitch_x']/2]:
            for offset in [.2,.8]:
                origin = [x,d['shoulder_y']+offset,zz]
                hits = solid.ray_cast(origin,[x,origin[1],zz+500])
                heights = np.unique(np.round([h.position[2] for h in hits],6))
                roofs.append(float(heights[1]-heights[0]) if len(heights)>=2 else 0.)
    checks['tool_pocket_roof_min_mm'] = min(roofs)
    checks['tool_pocket_roofs_at_least_3mm'] = min(roofs)>=3
    checks['internal_cavity_dimensions_in_print_axes_mm'] = [[float(s.extents[i]) for i in [0,2,1]] for s in cavities]
    # Exact same source orientation as material build Y: X rotation +90 degrees.
    printed = mesh.copy()
    printed.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
    printed.apply_translation(-printed.bounds[0])
    target = args.print_stl
    printed.export(target)
    profile_path = Path(r'C:\Program Files\Bambu Studio\resources\profiles\BBL\machine\Bambu Lab X1 Carbon 0.4 nozzle.json')
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    exclusion = np.array([[float(x) for x in row.split('x')] for row in profile['bed_exclude_area']])
    # Place at bed centre, 5mm brim. Check against actual installed exclusion polygon.
    dims = printed.extents
    minimum_xy = (256-dims[:2])/2-5
    maximum_xy = (256+dims[:2])/2+5
    outside_exclusion = (minimum_xy[0]>exclusion[:,0].max() or minimum_xy[1]>exclusion[:,1].max())
    checks.update(print_rotation_deg=[90,0,0], print_extents_mm=dims.tolist(),
        fits_x1c_250mm_with_5mm_brim=bool(np.all(dims[:2]+10<=250) and dims[2]<=250),
        avoids_installed_x1c_exclusion=bool(outside_exclusion and np.all(minimum_xy>=0) and np.all(maximum_xy<=256)),
        printer_profile=str(profile_path), printer_profile_sha256=hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        print_orientation_stl_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
    # Confirm all vessel COTS using exact assembly transforms and mesh intersections.
    placement = json.loads((ROOT/'assemblies/child_clamp_suspension/placement.json').read_text(encoding='utf-8'))
    intersections = []
    for item in placement['items']:
        if item.get('group')!='vessel':
            continue
        file = ROOT/item['part']/(item['file']+'.stl')
        vessel = trimesh.load(file, force='mesh')
        matrix = np.eye(4)
        for op in item.get('ops',[]):
            if 'translate' in op:
                transform = np.eye(4)
                transform[:3,3] = op['translate']
            elif 'rotate' in op:
                angles = np.radians(op['rotate'])
                transform = trimesh.transformations.euler_matrix(*angles, axes='sxyz')
            else:
                raise ValueError('Unhandled vessel transform')
            matrix = matrix@transform
        vessel.apply_transform(matrix)
        intersection = trimesh.boolean.intersection([mesh,vessel], engine='manifold')
        intersections.append(dict(label=item['label'], volume_mm3=float(abs(intersection.volume))))
    checks['vessel_intersections'] = intersections
    checks['all_vessel_parts_clear'] = all(x['volume_mm3']<.01 for x in intersections)
    checks['pass'] = all(value for value in checks.values() if isinstance(value,bool))
    args.out.write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(checks,indent=2))
    raise SystemExit(0 if checks['pass'] else 1)


if __name__ == '__main__':
    main()
