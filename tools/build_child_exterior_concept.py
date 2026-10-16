"""Create the sketch-based Blender visual study; never export manufacturing CAD.

Run with Blender 5.2: blender --background --factory-startup --python this_file
Geometry proportions come from the concept part; placement.json owns all instances.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Matrix, Vector, Euler

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assemblies/child_exterior_concept"
IMAGES = OUT / "_work/images"
SCALE = 0.001
scene = bpy.context.scene
collections = {}
source_hashes = {}


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def collection(name):
    if name not in collections:
        c = bpy.data.collections.new(name)
        scene.collection.children.link(c)
        collections[name] = c
    return collections[name]


def place_in(obj, group):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collection(group).objects.link(obj)


def material(name, rgb, metallic=0.0, roughness=0.35, glass=False):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*rgb, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if glass:
        bsdf.inputs["Transmission Weight"].default_value = 1.0
        bsdf.inputs["IOR"].default_value = 1.49
    return mat


def shade(obj, mat, bevel=0):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Soft concept edges", "BEVEL")
        mod.width = bevel * SCALE
        mod.segments = 4
    if obj.type == "MESH":
        for face in obj.data.polygons:
            face.use_smooth = True
        # STL triangles must split normals at actual corners, not ripple across
        # the clamp's flat caps, cylindrical wall and bolt seats.
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        for edge in bm.edges:
            edge.smooth = bool(edge.is_manifold and edge.calc_face_angle() < math.radians(32))
        bm.to_mesh(obj.data)
        bm.free()
        mod = obj.modifiers.new("Surface normals", "WEIGHTED_NORMAL")
        mod.keep_sharp = True


def box(name, size, loc, mat, group, bevel=2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=Vector(loc) * SCALE)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = Vector(size) * SCALE
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    shade(obj, mat, bevel)
    place_in(obj, group)
    return obj


def cylinder(name, radius, depth, loc, mat, group, axis="Z", bevel=0.5):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=radius*SCALE,
                                      depth=depth*SCALE, location=Vector(loc)*SCALE)
    obj = bpy.context.object
    obj.name = name
    if axis == "Y":
        obj.rotation_euler.x = math.pi/2
    elif axis == "X":
        obj.rotation_euler.y = math.pi/2
    shade(obj, mat, bevel)
    place_in(obj, group)
    return obj


def cut_hole(obj, loc, radius, depth, axis="Y"):
    cutter = cylinder("Concept hole cutter", radius, depth, loc, MAT["steel"], "Construction", axis, 0)
    mod = obj.modifiers.new("Concept through hole", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = cutter
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def cut_box(obj, spec):
    cutter = box("Concept window cutter", spec["size_mm"], spec["center_mm"],
                 MAT["steel"], "Construction", 0)
    mod = obj.modifiers.new("Lightening / lap", "BOOLEAN")
    mod.operation = "DIFFERENCE"
    mod.object = cutter
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def joined(parts, name, group):
    for obj in parts:
        bpy.context.view_layer.objects.active = obj
        for mod in list(obj.modifiers):
            bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.ops.object.select_all(action="DESELECT")
    for obj in parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    place_in(obj, group)
    return obj


def curve(name, points, radius, mat, group):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 18
    data.bevel_depth = radius*SCALE
    data.bevel_resolution = 5
    data.use_fill_caps = True
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points)-1)
    for bp, p in zip(spline.bezier_points, points):
        bp.co = Vector(p)*SCALE
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    # Keep the A-side cable straight: automatic tangents otherwise overshoot
    # the inner face near the transition from the transducer.
    for bp in spline.bezier_points:
        if abs(abs(bp.co.x)-.0728)<1e-7:
            left,right=bp.handle_left.copy(),bp.handle_right.copy()
            bp.handle_left_type=bp.handle_right_type='FREE'
            left.x=right.x=bp.co.x
            left.y=right.y=bp.co.y
            bp.handle_left=left
            bp.handle_right=right
    obj = bpy.data.objects.new(name, data)
    collection(group).objects.link(obj)
    data.materials.append(mat)
    return obj


def op_matrix(ops):
    transform = Matrix.Identity(4)
    for op in ops:
        for kind, value in op.items():
            if kind == "translate":
                m = Matrix.Translation(Vector(value)*SCALE)
            elif kind == "rotate":
                m = Euler(tuple(math.radians(v) for v in value), "XYZ").to_matrix().to_4x4()
            else:
                raise ValueError(f"Unsupported concept operation: {kind}")
            # Match assembly OpenSCAD wrappers: first operation is outermost.
            transform = transform @ m
    return transform


def import_item(item):
    source = ROOT/item["part"]/(item["file"]+".stl")
    source_hashes[source.relative_to(ROOT).as_posix()] = hashlib.sha256(source.read_bytes()).hexdigest()
    bpy.ops.wm.stl_import(filepath=str(source), global_scale=SCALE)
    obj = bpy.context.object
    obj.name = item["label"]
    obj.matrix_world = op_matrix(item.get("ops", [])) @ obj.matrix_world
    shade(obj, MAT[item["material"]])
    place_in(obj, item["group"])
    obj["reference_source"] = source.relative_to(ROOT).as_posix()
    obj["status"] = "reference_visualization_only"
    return obj


def concept_item(item):
    path = ROOT/item["part"]/"concept.json"
    source_hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = read(path)["variants"][item["file"]]
    name, group = item["label"], item["group"]
    if spec['kind'] == 'composite':
        pieces=[]
        for j,part in enumerate(spec.get('boxes',[])):
            piece=box(f'{name} bracket {j}',part['size_mm'],part['center_mm'],MAT[item['material']],group,0)
            for mod in list(piece.modifiers): piece.modifiers.remove(mod)
            # Cut each solid before joining the visual assembly. A boolean on
            # overlapping joined shells can leave mounting holes obstructed.
            for hole in spec.get('post_holes',[]):
                cut_hole(piece,hole['center_mm'],hole['radius_mm'],hole['depth_mm'],hole['axis'])
            shade(piece,MAT[item['material']],1)
            pieces.append(piece)
        for j,part in enumerate(spec.get('rings',[])):
            ring=cylinder(f'{name} retaining band {j}',part['outer_radius_mm'],part['height_mm'],part['center_mm'],MAT['steel'],group,'Z',0)
            for mod in list(ring.modifiers): ring.modifiers.remove(mod)
            cut_hole(ring,part['center_mm'],part['inner_radius_mm'],part['height_mm']+2,'Z')
            if part.get('split_gap_mm'):
                cut_box(ring,dict(center_mm=part['center_mm'],size_mm=[part['outer_radius_mm']*2+2,part['split_gap_mm'],part['height_mm']+2]))
            shade(ring,MAT['steel'],.6)
            pieces.append(ring)
        obj=joined(pieces,name,group)
        scene.cursor.location=(0,0,0)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    elif spec["kind"] == "integrated_clamps":
        source = ROOT/spec["reference_assembly"]
        source_hashes[spec["reference_assembly"]] = hashlib.sha256(source.read_bytes()).hexdigest()
        pieces = []
        for original in read(source)["items"]:
            if original["group"] not in ["clamps", "rubber"]:
                continue
            row = dict(original, group=group, material="clamp" if original["group"] == "clamps" else "rubber")
            pieces.append(import_item(row))
        for j, spine in enumerate(spec["spines"]):
            pieces.append(box(f"Unified spine {j}", spine["size_mm"], spine["center_mm"],
                              MAT["clamp"], group, 2))
        obj = joined(pieces, name, group)
        obj["clamp_levels"] = 3
        obj["construction"] = "Existing clamp levels linked by concept spines and fixed hinge neck"
        # The join is a visual representation of a connected cradle, not a
        # fabrication boolean union or a newly certified clamp design.
        bpy.context.scene.cursor.location = (0,0,0)
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    else:
        obj = box(name, spec["size_mm"], [0,0,0], MAT[item["material"]], group,
                  0 if spec["kind"] == "panel" else spec["bevel_mm"])
        if spec["kind"] == "panel":
            for mod in list(obj.modifiers):
                obj.modifiers.remove(mod)
            for window in spec.get("windows", []):
                cut_box(obj, window)
            for extra in spec.get('add_boxes',[]):
                extension=box('Integrated panel extension',extra['size_mm'],extra['center_mm'],MAT[item['material']],group,0)
                mod=obj.modifiers.new('Extend lower A rail','BOOLEAN')
                mod.operation='UNION';mod.object=extension
                bpy.context.view_layer.objects.active=obj
                bpy.ops.object.modifier_apply(modifier=mod.name)
                bpy.data.objects.remove(extension,do_unlink=True)
            if "lap_cut" in spec:
                cut_box(obj, spec["lap_cut"])
                z = 109 if item["file"] == "frame_a_lower" else -67
                for y in [-86,86]:
                    cut_hole(obj, [0,y,z], 2, 30, "X")
            for hole in spec.get("holes", []):
                cut_hole(obj, hole["center_mm"], hole["radius_mm"], hole["depth_mm"], hole["axis"])
            shade(obj, MAT[item["material"]], spec["bevel_mm"])
        if "mounting_webs" in spec:
            web_spec = spec["mounting_webs"]
            pieces = [obj]
            for level in web_spec["local_z_mm"]:
                web = box(f"{name} flat mounting web {level}",web_spec["size_mm"],
                          [0,0,level],MAT[item["material"]],group,0)
                pieces.append(web)
            # Union the webs into A before drilling; overlapping joined shells
            # can remove sections of the mating face during later booleans.
            bpy.context.view_layer.objects.active = obj
            for mod in list(obj.modifiers):
                bpy.ops.object.modifier_apply(modifier=mod.name)
            for web in pieces[1:]:
                mod=obj.modifiers.new('Fuse direct mounting web','BOOLEAN')
                mod.operation='UNION'
                mod.object=web
                bpy.ops.object.modifier_apply(modifier=mod.name)
                bpy.data.objects.remove(web,do_unlink=True)
            bpy.context.scene.cursor.location = (0,0,0)
            bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
            for level in web_spec["local_z_mm"]:
                for y in web_spec["hole_y_mm"]:
                    for dz in web_spec["hole_z_mm"]:
                        cut_hole(obj,[0,y,level+dz],web_spec["hole_radius_mm"],30,"X")
            shade(obj,MAT[item["material"]],1)
            obj["flat_mounting_levels"] = len(web_spec["local_z_mm"])
            obj["attachment_interface"] = "existing_clamp_frame_holes"
    for hole in ([] if spec['kind']=='composite' else spec.get('post_holes',[])):
        cut_hole(obj,hole['center_mm'],hole['radius_mm'],hole['depth_mm'],hole['axis'])
    obj.matrix_world = op_matrix(item.get("ops", [])) @ obj.matrix_world
    obj["status"] = "exploration_only"
    obj["variant"] = item["file"]
    obj["geometry_source"] = path.relative_to(ROOT).as_posix()
    return obj


def proxy_item(item):
    path = ROOT/item["part"]/"visual_proxy.json"
    spec = read(path)
    source_hashes[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    group, name = item["group"], item["label"]
    parts = []
    if spec["kind"] == "camera":
        w,d,h = spec["case_mm"]
        parts.append(box("Waterproof housing silhouette", [w,d,h], [0,0,0], MAT["equipment"], group, 5))
        parts.append(box("Camera front", [w-13,3,h-14], [0,d/2,0], MAT["rubber"], group, 4))
        parts.append(box("Front display", [30,3,30], [-23,d/2+2,0], MAT["lens"], group, 2))
        parts.append(cylinder("Lens bezel", spec["lens_radius_mm"]+4, 8,
                              [23,d/2+4,1], MAT["steel"], group, "Y"))
        parts.append(cylinder("Outward lens", spec["lens_radius_mm"], 2,
                              [23,d/2+9,1], MAT["lens"], group, "Y"))
        parts.append(box("Case latch", [25,15,7], [0,0,h/2+2], MAT["steel"], group, 2))
    else:
        r,l = spec["body_diameter_mm"]/2, spec["body_length_provisional_mm"]
        parts.append(cylinder("Dive light body", r, l, [0,0,0], MAT["equipment"], group))
        parts.append(cylinder("Upward light head", r+3, 13, [0,0,l/2+4], MAT["steel"], group))
        parts.append(cylinder("Upward lamp window", r-2, 2, [0,0,l/2+12], MAT["lamp"], group))
        for z in [-25,10]:
            parts.append(cylinder("Light retaining band", r+1, 7, [0,0,z], MAT["steel"], group))
        parts.append(box("Light mount to C", [24,32,50], [0,-22,-7], MAT["frame_c"], group, 2))
    obj = joined(parts, name, group)
    bpy.context.scene.cursor.location = (0,0,0)
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
    obj.matrix_world = op_matrix(item["ops"])
    obj["status"] = "exploration_only_generic_equipment_proxy"
    obj["geometry_source"] = path.relative_to(ROOT).as_posix()
    obj["view_direction"] = item["view_direction"]
    return obj


def camera(name, loc, target, ortho):
    data = bpy.data.cameras.new(name)
    obj = bpy.data.objects.new(name, data)
    collection("Studio").objects.link(obj)
    obj.location = Vector(loc)*SCALE
    obj.rotation_euler = (Vector(target)*SCALE-obj.location).to_track_quat("-Z", "Y").to_euler()
    data.type = "ORTHO"
    data.ortho_scale = ortho*SCALE
    data.clip_start = .001
    data.clip_end = 10
    return obj


def area(name, loc, target, power, size, rgb):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.shape = "DISK"
    data.size = size*SCALE
    data.color = rgb
    obj = bpy.data.objects.new(name, data)
    collection("Studio").objects.link(obj)
    obj.location = Vector(loc)*SCALE
    obj.rotation_euler = (Vector(target)*SCALE-obj.location).to_track_quat("-Z", "Y").to_euler()


def render(name, cam, size=(1500,1500)):
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = size
    scene.render.filepath = str(IMAGES/(name+".png"))
    bpy.ops.render.render(write_still=True)


def render_guard_motion():
    floor.hide_render = True
    scene.frame_set(50)
    render('child_exterior_guard_open', service)
    scene.cycles.samples = 16
    animation_frames = IMAGES/'guard_animation_frames'
    animation_frames.mkdir(exist_ok=True)
    for frame in hinge['preview_frames']:
        scene.frame_set(frame)
        scene.camera = service
        scene.render.resolution_x, scene.render.resolution_y = 900,760
        scene.render.filepath = str(animation_frames/f'guard_{frame:03d}.png')
        bpy.ops.render.render(write_still=True)
    scene.cycles.samples = 48


# Horizontal visual study. Previous generator is archived with the old layout.
if bpy.context.object and bpy.context.object.mode != "OBJECT":
    bpy.ops.object.mode_set(mode="OBJECT")
for obj in list(scene.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
IMAGES.mkdir(parents=True, exist_ok=True)
(OUT/"_work/logs").mkdir(parents=True,exist_ok=True)
scene.name = "Child exterior | horizontal open frame"
scene.unit_settings.system = "METRIC"
scene.unit_settings.length_unit = "MILLIMETERS"
scene["status"] = "exploration_only"
scene["coordinate_system"] = "X right; +Y forward (vessel); +Z up. Blender metres, UI mm."
MAT = {
    "frame_a": material("Side frame | ocean blue", (.025,.25,.52), .25, .28),
    "frame_c": material("Mount | blue", (.025,.25,.52), .25, .28),
    "clamp": material("Reference cradle | teal", (.035,.20,.22), .18, .31),
    "guard": material("Skids and guards | graphite", (.035,.055,.067), .18, .34),
    "steel": material("Brushed metal", (.36,.42,.45), .75, .3),
    "ballast": material("Ballast C | dark metal", (.15,.18,.20), .72, .28),
    "plate": material("Ballast B | silver", (.55,.59,.61), .75, .3),
    "rubber": material("Reference liner", (.02,.025,.027), 0, .7),
    "glass": material("Acrylic vessel", (.76,.90,.96), 0, .09, True),
    "flange": material("Anodized flange", (.09,.12,.135), .65, .28),
    "ground": material("Warm studio", (.80,.82,.83), 0, .65),
    "equipment": material("Equipment", (.018,.025,.03), .12, .32),
    "lens": material("Optics", (.015,.045,.06), .4, .13),
    "lamp": material("Upward light face", (.92,.96,1), .15, .16),
    "foam": material("Buoyancy space | provisional amber", (.95,.55,.07), .06, .5),
    "cable_sensor": material("TD04A cable", (.87,.025,.27), 0, .4),
    "cable_upper": material("Tether", (.60,.82,.05), 0, .4),
}
placement = read(OUT/"placement.json")
assert placement['layout'] == 'horizontal_open_frame_20261007', "Use archived generator for vertical history"
assert len({i['label'] for i in placement['items']}) == len(placement['items'])
source_hashes["assemblies/child_exterior_concept/placement.json"] = hashlib.sha256((OUT/"placement.json").read_bytes()).hexdigest()
objects = {}
for item in placement['items']:
    if item.get('geometry') == 'concept':
        obj = concept_item(item)
    elif item.get('geometry') == 'proxy':
        obj = proxy_item(item)
    else:
        obj = import_item(item)
    obj['placement_label'] = item['label']
    obj['explode_offset_mm'] = item.get('explode_mm',[0,0,0])
    objects[item['label']] = obj
# These are indicative cable paths; end fittings and ties are not fabrication CAD.
for route in placement['cable_routes']:
    obj = curve(route['label'],route['points_mm'],route['radius_mm'],MAT[route['material']],'Cable routes')
    obj['status'] = 'indicative_route_only'
    obj['route_note'] = route['note']

scene.render.engine = 'CYCLES'
scene.cycles.samples = 28
scene.cycles.use_denoising = True
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_percentage = 100
scene.world.color = (.35,.35,.35)
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.65,.72,.78,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = .35
scene.view_settings.view_transform = 'AgX'
scene.view_settings.exposure = -1.25
scene.render.film_transparent = False
floor = box('Studio floor',[2000,2000,8],[0,0,0],MAT['ground'],'Studio',0)
area('Key softbox',[-700,700,1000],[0,0,140],75,850,(1,.91,.80))
area('Fill softbox',[750,400,600],[0,0,140],55,650,(.72,.86,1))
area('Rear softbox',[0,-600,900],[0,0,140],65,550,(.89,.95,1))
hero = camera('01 | Front three quarter',[650,880,580],[0,12,145],690)
rear = camera('02 | Rear and cable access',[-650,-880,520],[0,0,145],690)
plan = camera('03 | Plan',[0,0,1200],[0,0,140],690)
side = camera('04 | Side elevation',[1200,0,150],[0,0,150],640)
front = camera('05 | Front elevation',[0,1200,150],[0,0,150],640)
explode = camera('06 | Exploded layout',[700,950,620],[0,30,150],930)
service = camera('07 | Cradle and lower ballast',[650,-820,460],[0,-30,110],640)
views = [('child_exterior_hero',hero,(1700,1300)),
         ('child_exterior_rear',rear,(1700,1300)),
         ('child_exterior_plan',plan,(1500,1500)),
         ('child_exterior_side',side,(1700,1150)),
         ('child_exterior_front',front,(1500,1150))]
for obj in objects.values():
    obj.keyframe_insert(data_path='location',frame=1)
    obj.location += Vector(obj['explode_offset_mm'])*SCALE
    obj.keyframe_insert(data_path='location',frame=100)
scene.frame_end = 100
scene.timeline_markers.new('ASSEMBLED',frame=1)
scene.timeline_markers.new('EXPLODED / VISUAL ONLY',frame=100)
scene.frame_set(1)
scene.camera = hero
scene.render.resolution_x,scene.render.resolution_y = 1700,1300
scene.render.filepath = str(IMAGES/'child_exterior_hero.png')
notes = bpy.data.texts.new('READ ME | Horizontal layout')
notes.use_fake_user = True
notes.write((OUT/'README.md').read_text(encoding='utf-8'))
for workspace in bpy.data.workspaces:
    for screen in workspace.screens:
        for ar in screen.areas:
            if ar.type == 'VIEW_3D':
                ar.spaces.active.region_3d.view_perspective='CAMERA'
                ar.spaces.active.shading.type='MATERIAL'
                ar.spaces.active.overlay.show_overlays=False
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'child_exterior_concept.blend'))
report = dict(status='exploration_only',layout=placement['layout'],blender_version=bpy.app.version_string,
              objects=len(objects),source_sha256=source_hashes,cameras=[c.name for _,c,_ in views],
              poses={'assembled':1,'exploded':100},
              validation_scope='Reference provenance and visual layout only. No approved printable parts or strength claims.')
(OUT/'_work/logs/build_manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
if '--build-only' in sys.argv:
    raise SystemExit(0)
for name,cam,size in views:
    if '--hero-only' in sys.argv and name!='child_exterior_hero':
        continue
    render(name,cam,size)
if '--hero-only' not in sys.argv:
    for group in ['Open side frames','Buoyancy reservation']:
        collection(group).hide_render=True
    render('child_exterior_cradle',service,(1700,1300))
    for group in ['Open side frames','Buoyancy reservation']:
        collection(group).hide_render=False
    collection('Cable routes').hide_render=True
    scene.frame_set(100)
    render('child_exterior_exploded',explode,(1700,1300))
    scene.frame_set(1)
    collection('Cable routes').hide_render=False
print('CHILD_EXTERIOR_HORIZONTAL_COMPLETE',str(OUT))
