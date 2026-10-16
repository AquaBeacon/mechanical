"""FreeCAD CLI source for the keyed, hinged WTE4 end-cap guard.

Run with FreeCAD's bundled python.exe, from repository root. JSON parameters
and the vendor STEP are the only geometry inputs. SCAD files are generated
view wrappers, never independently maintained designs.
"""
import json
import math
from pathlib import Path

import FreeCAD as App
import Part
import MeshPart

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "parts/child/exterior/printed/child_endcap_guard"
WORK = OUT / "_work"
for sub in ("logs", "images", "intermediate"):
    (WORK / sub).mkdir(parents=True, exist_ok=True)
P = json.loads((OUT / "parameters.json").read_text(encoding="utf-8"))
V = App.Vector


def box(x, y, z, dx, dy, dz):
    return Part.makeBox(dx, dy, dz, V(x, y, z))


def cyl(r, h, at, axis=V(0, 0, 1)):
    return Part.makeCylinder(r, h, V(*at), axis)


def fuse(shapes):
    return shapes[0].multiFuse(shapes[1:]).removeSplitter()


def ring(r0, r1, z, h):
    return cyl(r1, h, (0, 0, z)).cut(cyl(r0, h + 2, (0, 0, z - 1)))



cap = Part.read(str(ROOT / P["cap_source"]))
# Centre from vendor planar face, not STL bounding extrema (tessellation error).
face = max((f for f in cap.Faces if f.BoundBox.ZLength < 1e-5
            and abs(f.CenterOfMass.z - cap.BoundBox.ZMax) < 1e-4),
           key=lambda f: f.Area)
# The exposed face has a 0.5 mm chamfer: its outline is NOT the maximum
# end-cap profile. Section the unchamfered sidewall at vendor Z=8 instead.
wire = max(cap.slice(V(0, 0, 1), 8), key=lambda w: Part.Face(w).Area).copy()
wire.translate(V(-60.15, -57.15, -8))
cap.translate(V(-60.15, -57.15, -10))


def profile_prism(offset, z, height):
    w = wire.makeOffset2D(offset, join=0)
    s = Part.Face(w).extrude(V(0, 0, height))
    s.translate(V(0, 0, z))
    return s


def sharp_edges(shape):
    shape = shape.removeSplitter()
    # Cylindrical seams and tangent joins are already smooth, not fillet edges.
    edges = []
    for e in shape.Edges:
        faces = shape.ancestorsOfType(e, Part.Face)
        if len(faces) != 2:
            continue
        pt = e.valueAt((e.FirstParameter + e.LastParameter)/2)
        normals = []
        for f in faces:
            u,v = f.Surface.parameter(pt)
            normals.append(f.normalAt(u,v))
        if (normals[0]-normals[1]).Length > 1e-4:
            edges.append(e)
    return edges


def fillet_all(shape, label):
    shape = shape.removeSplitter()
    # Cage pieces are rounded before union; preserve the keyed fit at final joins.
    if label == 'integrated':
        # Round both roots where the cage rises from the receiver's top face.
        root_z = P['collar_top']
        roots = [e for e in sharp_edges(shape)
                 if abs(e.BoundBox.ZMin-root_z)<1e-5 and e.BoundBox.ZLength<1e-5
                 and all(58.5 < math.hypot(v.Point.x,v.Point.y) < P['guard_outer_radius']+.5
                         for v in e.Vertexes)]
        assert len(roots) >= 16
        shape = shape.makeFillet(P['root_fillet'], roots)
        assert shape.isValid()
        foot_edges = [e for e in sharp_edges(shape)
                      if abs(e.BoundBox.ZMin-P['collar_bottom'])<1e-5
                      and e.BoundBox.ZLength<1e-5
                      and hasattr(e.Curve,'Radius')
                      and abs(e.Curve.Radius-P['lower_flare_root_radius'])<1e-5]
        assert foot_edges
        shape = shape.makeFillet(P['edge_fillet'], foot_edges)
    edges = sharp_edges(shape)
    print(label, 'remaining sharp edges', len(edges), flush=True)
    # Small local blends keep the exact keyed profile, hole bores and hinge gap.
    # Every nonsmooth edge is included; tangent surfaces need no further blend.
    out = shape.makeFillet(P["collar_edge_fillet"], edges)
    print(label, 'fillet valid', out.isValid(), 'solids', len(out.Solids), flush=True)
    if not out.isValid() or len(out.Solids) != 1:
        raise RuntimeError("invalid full-edge fillet: " + label)
    return out


hy, hz = P["hinge_y"], P["hinge_z"]
ly = P["latch_y"]
outer = profile_prism(P["profile_clearance"] + P["collar_wall"],
                      P["collar_bottom"], P["collar_top"] - P["collar_bottom"])
# Open-backed keyed skirt. Below key_projection_top keep the complete offset
# profile: inward projecting circular lands, with recesses ONLY at the two
# end-cap tabs. A circular through-cut would erase these locating lands.
collar = outer.cut(profile_prism(P["profile_clearance"], P['collar_bottom']-1,
                                0.45-P['collar_bottom']+1))
# Relieve the region near/above the cap face separately for the six screw heads.
collar = collar.cut(cyl(P['collar_central_radius'], 100,
                       (0, 0, P['key_projection_top'])))

# Unanchored fixed hinge reference, to be replaced by the future clamp mount.
hinge_reference = fuse([box(-18, hy-6, hz-16, 36, 12, 14),
    cyl(P['hinge_radius'], 12, (-18,hy,hz), V(1,0,0)),
    cyl(P['hinge_radius'], 12, (6,hy,hz), V(1,0,0))])
hinge_reference = hinge_reference.cut(box(-6, hy-7, hz-7, 12, 14, 20))
hinge_reference = hinge_reference.cut(cyl(P['hinge_bore']/2, 60, (-30,hy,hz), V(1,0,0)))

bottom, top = P["guard_bottom"], P["guard_height"]
ri, ro, t = P["guard_inner_radius"], P["guard_outer_radius"], P["ring_thickness"]
# Sloped lower skirt replaces the unsupported horizontal bottom-ring step.
# The foot is wider than the keyed recess, for continuous perimeter support.
lower_flare = Part.makeCone(P['lower_flare_root_radius'], P['lower_flare_top_radius'],
                           bottom+t-P['collar_bottom'], V(0,0,P['collar_bottom']))
lower_flare = lower_flare.cut(cyl(P['collar_central_radius'], bottom+t-P['collar_bottom']+2,
                                  (0,0,P['collar_bottom']-1)))
lower_flare = lower_flare.cut(profile_prism(P['profile_clearance'], P['collar_bottom']-1,
                                          0.45-P['collar_bottom']+1))
# The sloping inner shelf gives the larger root blends enough material, above
# the screw-head keepouts, and still leaves the central sensor space open.
shelf_h = P['collar_top']-P['root_shelf_bottom']
shelf = cyl(P['lower_flare_root_radius'], shelf_h, (0,0,P['root_shelf_bottom']))
shelf = shelf.cut(Part.makeCone(P['collar_central_radius'],P['root_shelf_inner_radius'],
                              shelf_h,V(0,0,P['root_shelf_bottom'])))
lower_flare = lower_flare.fuse(shelf).removeSplitter()
# An octagonal cage keeps its inner apothem clear of the reserved volume.
# Pointed window roofs close at 45 degrees instead of bridging the whole window.
def polygon_prism(radius, z, h):
    points = [V(radius*math.cos(math.radians(a)), radius*math.sin(math.radians(a)), z)
              for a in range(0,360,45)]
    return Part.Face(Part.makePolygon(points+[points[0]])).extrude(V(0,0,h))

cage_start = bottom+t-1.0  # overlap rounded cage foot into the sloped skirt
cage = polygon_prism(ro, cage_start, top-cage_start)
cage = cage.cut(polygon_prism(ri/math.cos(math.radians(22.5)), cage_start-1, top-cage_start+2))
w = P['window_half_width']
z0, zs, za = bottom+2*t, P['window_shoulder_z'], top-t
outline = [V(-w,0,z0),V(w,0,z0),V(w,0,zs),V(0,0,za),V(-w,0,zs)]
window_wire = Part.Wire(Part.makePolygon(outline+[outline[0]]).Edges)
window_wire = window_wire.makeOffset2D(-P['window_corner_fillet'], join=0)
window_wire = window_wire.makeOffset2D(P['window_corner_fillet'], join=0)
window_face = Part.Face(window_wire)
window = window_face.extrude(V(0,40,0))
window.translate(V(0,45,0))
for angle in range(0,360,45):
    cut = window.copy()
    cut.rotate(V(0,0,0), V(0,0,1), angle-67.5)
    cage = cage.cut(cut)
cage = cage.removeSplitter()
cage = cage.makeFillet(P['edge_fillet'], [e for e in sharp_edges(cage)
                       if e.BoundBox.ZMax > cage_start+1e-5])
assert cage.isValid() and len(cage.Solids)==1
# Fused with the same keyed receiver; still one moving/printed body.
guard_bits = [collar, lower_flare, cage]
# User request: fully open end; no grille or lid across the central space.
guard_bits += [box(-5.5, 58.5, bottom, 11, hy-58.5, t),
               box(-5.5, hy-10, hz, 11, 10, bottom+t-hz),
               cyl(P["hinge_radius"], 12-2*P["hinge_axial_gap"],
                   (-6+P["hinge_axial_gap"], hy, hz), V(1, 0, 0)),
               box(-9, ly-6, bottom, 18, -58.5-(ly-6), t)]
guard = fuse(guard_bits)
guard = guard.cut(cyl(P["hinge_bore"]/2, 60, (-30, hy, hz), V(1, 0, 0)))
guard = guard.cut(cyl(P["bolt_bore"]/2, 20, (0, ly, -5)))

shapes = {}
checks = {"parameters": P, "parts": {}}
checks['print_geometry'] = {
    'upright_local_axis': '+Z',
    'window_roof_angle_from_vertical_deg': math.degrees(math.atan(
        P['window_half_width']/(top-t-P['window_shoulder_z']))),
    'lower_flare_angle_from_vertical_deg': math.degrees(math.atan(
        (P['lower_flare_top_radius']-P['lower_flare_root_radius'])/(bottom+t-P['collar_bottom']))),
    'window_corner_radius_mm': P['window_corner_fillet'],
    'cage_edge_radius_mm': P['edge_fillet'],
    'receiver_cage_root_radius_mm': P['root_fillet'],
    'temporary_hinge_below_main_foot_mm': P['collar_bottom']-(hz-P['hinge_radius']),
    'note': 'Main cage print geometry only; provisional hinge remains and requires support below the main foot.'
}
assert checks['print_geometry']['window_roof_angle_from_vertical_deg'] <= 45.001
assert checks['print_geometry']['lower_flare_angle_from_vertical_deg'] <= 45.001
for label, raw in (("integrated", guard), ("hinge_reference", hinge_reference)):
    s = fillet_all(raw, label)
    stem = "child_endcap_guard_" + label
    s.exportStep(str(OUT / (stem + ".step")))
    mesh = MeshPart.meshFromShape(Shape=s, LinearDeflection=0.06,
                                 AngularDeflection=0.15, Relative=False)
    mesh.write(str(OUT / (stem + ".stl")))
    (OUT / (stem + ".scad")).write_text(
        "// GENERATED by spec/build_child_endcap_guard.py; edit parameters.json.\n"
        'import("' + stem + '.stl");\n', encoding="utf-8")
    shapes[label] = s
    b = s.BoundBox
    checks["parts"][label] = {"volume_mm3": s.Volume,
                             "bbox_mm": [b.XLength, b.YLength, b.ZLength],
                             "valid": s.isValid(), "solids": len(s.Solids),
                             "fillet_radius_all_edges_mm": P["collar_edge_fillet"],
                             "upper_cage_fillet_mm": P["edge_fillet"] if label == "integrated" else None}

# Exact BRep intersections, including hinge sweep and orientation rejection.
checks["cap_intersections_mm3"] = {k: s.common(cap).Volume for k,s in shapes.items()}
checks["part_intersections_mm3"] = {'integrated_hinge_reference': shapes['integrated'].common(shapes['hinge_reference']).Volume}
checks["sweep"] = []
central = cyl(P["central_keepout_diameter"]/2, top, (0,0,0))
checks['central_keepout_intersections_mm3'] = {k: s.common(central).Volume for k,s in shapes.items()}
checks['screw_keepouts'] = []
screw_keepouts = []
for w in face.Wires:
    b = w.BoundBox
    if 3.0 < b.XLength < 3.8 and 3.0 < b.YLength < 3.8:
        x, y = w.CenterOfMass.x-60.15, w.CenterOfMass.y-57.15
        screw = cyl(P['cap_screw_keepout_radius'], P['cap_screw_keepout_height'], (x,y,0))
        screw_keepouts.append(screw)
        checks['screw_keepouts'].append({'xy': [x,y], 'intersection_mm3': sum(s.common(screw).Volume for s in shapes.values()),
            'clearance_mm': min(s.distToShape(screw)[0] for s in shapes.values())})
sweep_angles = sorted(set(range(0,11)) | set(range(15,36)) | set(range(0,111,5)))
for angle in sweep_angles:
    s = shapes["integrated"].copy()
    s.rotate(V(0, hy, hz), V(1, 0, 0), -angle)
    checks["sweep"].append({"angle": angle,
        "cap_mm3": s.common(cap).Volume,
        "central_keepout_mm3": s.common(central).Volume,
        "screw_keepouts_mm3": sum(s.common(c).Volume for c in screw_keepouts),
        "hinge_reference_mm3": s.common(shapes["hinge_reference"]).Volume})
key_z = (P['collar_bottom'] + P['key_projection_top']) / 2
checks['key_profile'] = {
    'section_z_mm': key_z,
    'fit_clearance_mm': P['profile_clearance'],
    'land_present': shapes['integrated'].isInside(V(0, 57.85, key_z), 1e-6, False),
    'right_tab_recess_empty': not shapes['integrated'].isInside(V(60.5, 0, key_z), 1e-6, False),
    'left_tab_recess_empty': not shapes['integrated'].isInside(V(-60.5, 0, key_z), 1e-6, False),
    'screw_relief_empty': not shapes['integrated'].isInside(V(0, 57.85, 1), 1e-6, False),
}
assert all(checks['key_profile'][k] for k in ('land_present', 'right_tab_recess_empty',
                                           'left_tab_recess_empty', 'screw_relief_empty'))
section = {}
for name, shape in (('guard', shapes['integrated']), ('cap', cap)):
    section[name] = [[[pt.x, pt.y] for pt in w.discretize(Deflection=0.03)]
                     for w in shape.slice(V(0,0,1), key_z)]
(WORK/'intermediate/key_section.json').write_text(json.dumps(section), encoding='utf-8')
checks["wrong_direction"] = {}
for angle in (5, 15, 30, 90, 180):
    c = cap.copy()
    c.rotate(V(0,0,0), V(0,0,1), angle)
    checks["wrong_direction"][str(angle)] = shapes['integrated'].common(c).Volume

# Use existing COTS hole wires to locate provisional outward keepouts.
checks["penetrator_keepouts"] = []
for w in face.Wires:
    b = w.BoundBox
    if 9 < b.XLength < 11 and 9 < b.YLength < 11:
        x, y = w.CenterOfMass.x-60.15, w.CenterOfMass.y-57.15
        keepout = cyl(P["provisional_penetrator_radius"],
                      P["provisional_penetrator_height"], (x,y,0))
        checks["penetrator_keepouts"].append({"xy": [x,y],
            "closed_intersection_mm3": sum(s.common(keepout).Volume for s in shapes.values()),
            "closed_clearance_mm": min(s.distToShape(keepout)[0] for s in shapes.values())})

# Check flange and purchased hardware in the authoritative assembly placement.
def placement_matrix(ops):
    m = App.Matrix()
    for op in ops:
        if 'translate' in op:
            t = App.Matrix()
            t.move(V(*op['translate']))
        elif 'rotate' in op:
            x,y,z = op['rotate']
            t = App.Rotation(z,y,x).toMatrix()
        else:
            raise ValueError('unsupported guard placement operation')
        m = m.multiply(t)
    return m

assembly = json.loads((ROOT/'assemblies/child_endcap_guard/placement.json').read_text(encoding='utf-8'))
guard_item = next(i for i in assembly['items'] if i['label']=='guard_integrated')
to_local = placement_matrix(guard_item['ops']).inverse()
checks['assembly_context'] = {}
for item in assembly['items']:
    if item['group'] in ('guard', 'reference'):
        continue
    s = Part.read(str(ROOT/item['part']/(item['file']+'.step')))
    s.transformShape(to_local.multiply(placement_matrix(item['ops'])))
    intersections = {k: s.common(shape).Volume for k,shape in shapes.items()}
    checks['assembly_context'][item['label']] = intersections
    assert max(intersections.values()) < 1e-5, (item['label'], intersections)
    if item['label']=='flange_bot':
        assert s.common(cap).Volume < 1e-5
        for angle in sweep_angles:
            moving = shapes['integrated'].copy()
            moving.rotate(V(0,hy,hz), V(1,0,0), -angle)
            assert moving.common(s).Volume < 1e-5
report = WORK / "logs/geometry_checks.json"
report.write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
assert max(checks['cap_intersections_mm3'].values()) < 1e-5
assert max(checks['part_intersections_mm3'].values()) < 1e-5
assert max(checks['central_keepout_intersections_mm3'].values()) < 1e-5
assert len(checks['screw_keepouts']) == 6
assert all(c['intersection_mm3'] < 1e-5 and c['clearance_mm'] > 0.4 for c in checks['screw_keepouts'])
assert all(max(v for k,v in c.items() if k != 'angle') < 1e-5 for c in checks['sweep'])
assert checks['wrong_direction']['90'] > 1
assert checks['wrong_direction']['180'] < 1e-5
print('PASS: valid solids, keyed fit, central keepout, 6 screw keepouts, 0..110 degree sweep.')
