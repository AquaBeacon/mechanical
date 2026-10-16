"""Regenerate placement from SCAD metrics and check meshes/motion, mm.

Geometry authority remains SCAD; placement.json is the assembled pose authority.
Run after building source variants. No load-capacity claim.
"""
import itertools
import json
import math
from pathlib import Path
import re
import subprocess

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[2]
NAME = 'dji_style_toggle_latch'
PART = ROOT / 'parts/common/jigs' / NAME
ASM = ROOT / 'assemblies' / NAME
OUT = ASM / '_work/analysis/geometry'
OUT.mkdir(parents=True, exist_ok=True)
OSC = r'C:\Program Files\OpenSCAD\openscad.exe'


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


result = subprocess.run([OSC, '-D', 'part="metrics"', '-o',
    str(ASM/'_work/intermediate/metrics.csg'), str(PART/(NAME+'.scad'))], capture_output=True, text=True, check=True)
metrics = re.search(r'METRICS = (\[.*\])', result.stderr)
assert metrics, result.stderr
(r, theta_closed, catch_x, az, ly, lt, oy, ridge_w, web_t, lever_l, pad_t,
 mount_y, keeper_mx, cz, bolt_a, bolt_b, keeper_h, chamfer, catch_gap,
 rubber_t, rubber_preload, rubber_w, rubber_h, rubber_z, rubber_recess,
 release_angle, groove_depth, groove_bottom, groove_top, underlap, toe_bottom, toe_top,
 hook_w, tip_fillet, tip_round, groove_radius, keeper_left, keeper_right, keeper_pad_w, keeper_my, keeper_mx2, groove_w, main_length) = json.loads(metrics[1])


def bpos(theta):
    t = math.radians(theta)
    return [r*math.cos(t), 0, az+r*math.sin(t)]


def pose(theta):
    b = bpos(theta)
    dz = b[2]-cz
    x = b[0]+math.sqrt(lever_l**2-dz**2)
    phi = math.degrees(math.asin(-dz/lever_l))
    return b, x, phi


def transform(xyz, angle=0):
    t = trimesh.transformations.euler_matrix(0, math.radians(-angle), 0)
    t[:3, 3] = xyz
    return t


def entries(theta, free_phi=None):
    b, x, phi = pose(theta)
    if free_phi is not None:
        phi = free_phi
    return [
        ('base', 'Base', 'SlateGray', [0,0,0], 0),
        ('keeper', 'Keeper', 'SteelBlue', [catch_x,0,0], 0),
        ('epdm', 'EPDM full fixed recess - closed envelope', 'SeaGreen', [catch_x,0,0], 0),
        ('link', 'Link left', 'Orange', [0,-ly-lt,az], theta),
        ('link', 'Link right', 'Orange', [0,ly,az], theta),
        ('lever', 'Lever', 'DimGray', b, phi),
        ('axle_a', f'M3x{bolt_a:g} A envelope', 'Silver', [0,0,az], 0),
        ('axle_b', f'M3x{bolt_b:g} B envelope', 'Silver', b, 0),
    ]


items = []
for stem, label, color, xyz, angle in entries(theta_closed):
    items.append(dict(part=PART.relative_to(ROOT).as_posix(), file=NAME+'_'+stem,
        label=label, color=color, group='hardware' if stem in ('axle_a','axle_b','epdm') else 'printed',
        ops=[{'translate':xyz}, {'rotate':[0,-angle,0]}]))
write(ASM/'placement.json', dict(name=NAME, units='mm',
    note='Fixed host spacing. Positive hook undercut and EPDM preload. Rubber model is the closed envelope, not printable or a deformation simulation.',
    groups={'printed':True,'hardware':True}, items=items))

meshes = {}
mesh_reports = {}
for stem in ['base','link','lever','keeper','epdm','axle_a','axle_b']:
    mesh = trimesh.load(PART/(NAME+'_'+stem+'.stl'), force='mesh')
    meshes[stem] = mesh
    row = dict(watertight=bool(mesh.is_watertight), winding_consistent=bool(mesh.is_winding_consistent),
        zero_area_faces=int(np.count_nonzero(mesh.area_faces<1e-12)),
        connected_components=len(mesh.split()), volume_mm3=float(mesh.volume),
        bounds_mm=mesh.bounds.tolist(), extents_mm=mesh.extents.tolist())
    assert row['watertight'] and row['winding_consistent'] and row['connected_components']==1 and mesh.volume>0, (stem,row)
    assert row['zero_area_faces']==0, (stem,'Degenerate triangles must be repaired by the configured build step')
    mesh_reports[stem] = row

checks = []
failures = []
swept_bounds = []
states = [(float(t),None) for t in np.linspace(theta_closed,release_angle,round(2*(theta_closed-release_angle))+1)]
open_phi = pose(release_angle)[2]
states += [(release_angle,float(p)) for p in np.linspace(open_phi,30,91)[1:]]
cb,_,cp=pose(theta_closed)
closed_transform=transform(cb,cp)
keeper_world=meshes['keeper'].copy()
keeper_world.apply_translation([catch_x,0,0])
# Probe all lined surfaces, including the curved back/ceiling transition.
probes=[]
for y in [-9,0,9]:
    for z in np.linspace(.2,groove_top-groove_radius-.1,24):
        probes.append(('back',[catch_x+keeper_right,y,z],[1,0,0]))
    for x in np.linspace(keeper_right+groove_radius+.01,web_t/2-.01,8):
        probes.append(('ceiling',[catch_x+x,y,groove_top],[0,0,-1]))
    for t in np.linspace(0,math.pi/2,31):
        probes.append(('corner',[catch_x+keeper_right+groove_radius-groove_radius*math.cos(t),y,groove_top-groove_radius+groove_radius*math.sin(t)],[math.cos(t),0,-math.sin(t)]))
for side in [-1,1]:
    for x in np.linspace(keeper_right+.1,web_t/2-.1,9):
        for z in np.linspace(.2,groove_top-groove_radius-.1,16):
            probes.append(('side',[catch_x+x,side*groove_w/2,z],[0,-side,0]))
rubber_origins=np.array([p[1] for p in probes])
rubber_directions=np.array([p[2] for p in probes])
rubber_checks=[]
for theta, free_phi in states:
    placed = []
    for stem,label,color,xyz,angle in entries(theta,free_phi):
        if stem=='epdm':
            continue # Contact gaps below quantify the rubber space at every pose.
        m = meshes[stem].copy()
        m.apply_transform(transform(xyz,angle))
        placed.append((label,m))
        swept_bounds.append(m.bounds)
        if stem=='lever':
            moving_lever=m
    overlaps = []
    for (an,a),(bn,b) in itertools.combinations(placed,2):
        if np.any(np.minimum(a.bounds[1],b.bounds[1])-np.maximum(a.bounds[0],b.bounds[0])<=1e-5):
            continue
        intersection = trimesh.boolean.intersection([a,b], engine='manifold')
        volume = 0 if intersection.is_empty else abs(float(intersection.volume))
        if volume>0.015:
            overlaps.append(dict(pair=[an,bn], volume_mm3=round(volume,5)))
    checks.append(dict(link_angle_deg=theta, free_lever_angle_deg=free_phi, overlaps=overlaps))
    if overlaps:
        failures.append(checks[-1])
    locations,rays,_=moving_lever.ray.intersects_location(rubber_origins,rubber_directions)
    locations=np.asarray(locations).reshape((-1,3))
    gaps=[]
    for k,origin in enumerate(rubber_origins):
        distances=(locations[rays==k]-origin)@rubber_directions[k]
        positive=distances[distances>1e-5]
        gaps.append(float(positive.min()) if len(positive) else None)
    squeezes=[max(0,rubber_t-g) if g is not None else 0 for g in gaps]
    rubber_checks.append(dict(link_angle_deg=theta,free_lever_angle_deg=free_phi,
        minimum_available_thickness_mm=min((g for g in gaps if g is not None),default=None),
        maximum_squeeze_mm=max(squeezes),mean_squeeze_mm=float(np.mean(squeezes))))

# Hole rays in the actual exported meshes: mounting, axles, and catch entry.
hole_checks=[]
for stem,origin,direction,length in [
    ('base',[-10,-mount_y,-1],[0,0,1],pad_t+2), ('base',[3,mount_y,-1],[0,0,1],pad_t+2),
    ('base',[0,-5,az],[0,1,0],10), ('link',[0,-1,0],[0,1,0],lt+2),
    ('link',[r,-1,0],[0,1,0],lt+2), ('lever',[0,-oy-1,0],[0,1,0],2*oy+2),
    ('keeper',[keeper_mx2,-keeper_my,-1],[0,0,1],pad_t+2),
    ('keeper',[keeper_mx,keeper_my,-1],[0,0,1],pad_t+2), ('lever',[lever_l,0,-8],[0,0,1],8),
]:
    locations, _, _ = meshes[stem].ray.intersects_location([origin],[direction])
    distances = (locations-np.asarray(origin))@np.asarray(direction) if len(locations) else []
    clear=not any(1e-5<d<length-1e-5 for d in distances)
    hole_checks.append(dict(part=stem, origin=origin, direction=direction, length_mm=length, clear=clear))
    assert clear, hole_checks[-1]

# Actual screwdriver envelope above the pads. Base must be fitted before A axle.
tool_checks=[]
tool_radius=3.2
for stem,xs,my in [('base',[-10,3],mount_y),('keeper',[keeper_mx,keeper_mx2],keeper_my)]:
    for x,y in itertools.product(xs,[-my,my]):
        tool=trimesh.creation.cylinder(radius=tool_radius,height=50,sections=48)
        tool.apply_translation([x,y,pad_t+0.02+25])
        v=trimesh.boolean.intersection([meshes[stem],tool],engine='manifold').volume
        tool_checks.append(dict(part=stem,xy=[x,y],diameter_mm=2*tool_radius,
            installation_state='before A axle installation' if stem=='base' else 'lever open',
            overlap_mm3=float(abs(v))))
        assert abs(v)<0.015, tool_checks[-1]

# Verify the rectangular crest and continuous material beneath it.
beam_points=[[dx,y,z] for y in np.linspace(-ridge_w/2+0.2,ridge_w/2-0.2,31)
             for dx,z in [(0,keeper_h-chamfer-0.2),(web_t*0.4,keeper_h-chamfer-0.2),
                          (-web_t*0.4,keeper_h-chamfer-0.2),(0,keeper_h-0.1),(0,pad_t+0.1)]]
beam_solid=bool(np.all(meshes['keeper'].contains(beam_points)))
assert beam_solid, 'Integral catch beam missing material'
web_points=[[x,y,z] for x in [-web_t/2+0.2,0,web_t/2-groove_depth-0.2]
            for y in np.linspace(-ridge_w/2+0.2,ridge_w/2-0.2,9)
            for z in np.linspace(pad_t+0.1,keeper_h-chamfer-0.1,15)]
web_solid=bool(np.all(meshes['keeper'].contains(web_points)))
assert web_solid, 'Keeper is not grounded continuously to its base'
# Quantify the closed flat load face, including nominal clearance. Rays through
# the upper face must find a matching parallel plane, not only a rounded point.
closed_lever=meshes['lever'].copy()
cb,_,cp=pose(theta_closed)
closed_lever.apply_transform(transform(cb,cp))
flat_checks=[]
for y,z in itertools.product([-6,0,6],np.linspace(7.3,9.0,9)):
    origin=np.array([catch_x+keeper_right,y,z])
    hits,_,_=closed_lever.ray.intersects_location([origin],[[1,0,0]])
    ds=(hits-origin)[:,0]
    distance=float(min(d for d in ds if d>0))
    flat_checks.append(dict(y_mm=y,z_mm=float(z),clearance_mm=distance))
    assert abs(distance-(rubber_t-rubber_preload))<0.035, flat_checks[-1]
# Measure toe and neck continuously across the actual exported solid.
sections=[]
for x,y in itertools.product(np.linspace(web_t/2-underlap+tip_round+.05,web_t/2+1.5,35),[-9,0,9]):
    origin=np.array([catch_x+x,y,0])
    hits,_,_=closed_lever.ray.intersects_location([origin],[[0,0,1]])
    zs=sorted(hits[:,2])
    thickness=zs[1]-zs[0]
    sections.append(float(thickness))
assert min(sections)>toe_top-toe_bottom-.03, ('Thin toe neck',min(sections))
epdm_world=meshes['epdm'].copy()
epdm_world.apply_translation([catch_x,0,0])
for other in [closed_lever,keeper_world]:
    overlap=trimesh.boolean.intersection([epdm_world,other],engine='manifold')
    assert overlap.is_empty or abs(overlap.volume)<0.015, 'Closed rubber envelope intersects a rigid part'
dead_x=math.sqrt((lever_l-r)**2-(az-cz)**2)
dead_angle=180-math.degrees(math.atan2(az-cz,dead_x))
assert release_angle<dead_angle<theta_closed
# Regression for the user's upward escape: both a vertical lift and a lift
# about B must hit the rigid ledge before the toe clears it.
keeper_world=meshes['keeper'].copy()
keeper_world.apply_translation([catch_x,0,0])
retention=[]
for name,matrix in [('vertical_lift_2.3mm',trimesh.transformations.translation_matrix([0,0,2.3])@transform(cb,cp)),
                    ('lift_about_B_4deg',transform(cb,cp+4)),
                    ('lift_with_0.4mm_outward_play',trimesh.transformations.translation_matrix([0.4,0,2.3])@transform(cb,cp))]:
    raised=meshes['lever'].copy()
    raised.apply_transform(matrix)
    overlap=trimesh.boolean.intersection([keeper_world,raised],engine='manifold')
    volume=0 if overlap.is_empty else abs(float(overlap.volume))
    retention.append(dict(test=name,blocked_volume_mm3=volume))
    assert volume>0.5, ('Missing positive upward retention',retention[-1])
max_squeeze=max(p['maximum_squeeze_mm'] for p in rubber_checks)
assert max_squeeze<0.45, ('Provisional squeeze limit exceeded; revise geometry',max_squeeze)
assert rubber_checks[-1]['maximum_squeeze_mm']==0, 'Rubber not released when fully open'
envelope=np.asarray(swept_bounds)
report=dict(status='PASS' if not failures else 'FAIL',
    method='Trimesh manifold solid intersection, discrete rigid poses; STL hole rays. No elastic/contact/load analysis.',
    mesh=mesh_reports, closed_catch_distance_mm=catch_x,
    dead_center_catch_distance_mm=dead_x,
    dead_center_angle_deg=dead_angle,
    reference_dead_center_draw_mm=catch_x-dead_x,
    host_fixed=True,
    pose_count=len(checks), motion=checks, hole_checks=hole_checks, tool_access=tool_checks,
    flat_contact=flat_checks,
    positive_retention=retention,
    epdm=dict(sheet_thickness_mm=rubber_t,closed_squeeze_mm=rubber_preload,
        attached_to='fixed keeper recess: back, ceiling and both side walls; bottom open',
        surface_probe_count=len(probes),main_strip_cut_mm=[rubber_w,main_length,rubber_t],
        side_sheet_count=2,side_sheet_bounds_mm=[groove_depth,groove_top,rubber_t],
        maximum_squeeze_mm=max_squeeze,
        poses=rubber_checks, note='Geometric space only; no material force law, bulging, bondline or creep simulation.'),
    integral_keeper=dict(total_height_mm=keeper_h,height_above_pad_mm=keeper_h-pad_t,
        top_round_mm=chamfer,ridge_width_mm=ridge_w,web_thickness_mm=web_t,
        groove_root_fillet_mm=groove_radius,
        solid_neck_thickness_mm=web_t-groove_depth,nominal_hook_underlap_mm=underlap,
        crest_probe_count=len(beam_points),crest_solid=beam_solid,
        web_probe_count=len(web_points),web_solid=web_solid),
    reinforced_hook=dict(width_mm=hook_w,nominal_tip_height_mm=toe_top-toe_bottom,
        root_fillet_mm=tip_fillet,outer_round_mm=tip_round,minimum_measured_toe_neck_mm=min(sections)),
    keeper_pad=dict(size_mm=[keeper_right-keeper_left,keeper_pad_w,pad_t],previous_size_mm=[35,46,5]),
    swept_bounds_mm=[envelope[:,0,:].min(axis=0).tolist(),envelope[:,1,:].max(axis=0).tolist()],
    limitations=['Solid EPDM hardness and bondline thickness are unknown. Nominal squeeze is a trial value.', 'No physical fit, preload, fatigue or force validation.',
                 'Metal models are nominal occupancy envelopes, not purchased hardware measurements.'])
write(OUT/'report.json', report)
print(json.dumps(dict(status=report['status'],poses=len(checks),failed_poses=len(failures),
    maximum_rubber_squeeze_mm=max_squeeze,first_failures=failures[:3]),indent=2))
if failures:
    raise SystemExit(1)
