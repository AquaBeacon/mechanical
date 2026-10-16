"""Show the manufactured CAD in a new Blender document; preserve concept blend.

Run Blender --background --python this_file. Equipment proxy STLs are derived
from the exact visual study meshes, and remain non-print reference geometry.
"""
import hashlib
import json
import math
from pathlib import Path
import bpy
from mathutils import Matrix,Vector,Euler

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_horizontal'
SCALE=.001
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assemblies/child_exterior_concept/child_exterior_concept.blend'))
scene=bpy.context.scene
scene.frame_set(1)
placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
images=OUT/'_work/images';images.mkdir(parents=True,exist_ok=True)


def matrix(ops):
    m=Matrix.Identity(4)
    for op in ops:
        for kind,value in op.items():
            if kind=='translate':a=Matrix.Translation(Vector(value)*SCALE)
            elif kind=='rotate':a=Euler(tuple(math.radians(x) for x in value),'XYZ').to_matrix().to_4x4()
            elif kind=='mirror':
                n=Vector(value).normalized();a=Matrix.Identity(4)
                for i in range(3):
                    for j in range(3):a[i][j]-=2*n[i]*n[j]
            elif kind=='scale':a=Matrix.Diagonal((*value,1))
            else:raise ValueError(kind)
            m=m@a
    return m


def export_proxy(obj,path):
    deps=bpy.context.evaluated_depsgraph_get();evaluated=obj.evaluated_get(deps)
    mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
    # Mesh coordinates are already metres. Store the original local mm axes.
    with path.open('w',encoding='ascii') as f:
        f.write('solid non_print_visual_proxy\n')
        for tri in mesh.loop_triangles:
            vertices=[mesh.vertices[i].co/SCALE for i in tri.vertices]
            normal=(vertices[1]-vertices[0]).cross(vertices[2]-vertices[0]).normalized()
            f.write('facet normal '+' '.join(str(x) for x in normal)+'\nouter loop\n')
            for v in vertices:f.write('vertex '+' '.join(str(x) for x in v)+'\n')
            f.write('endloop\nendfacet\n')
        f.write('endsolid non_print_visual_proxy\n')
    evaluated.to_mesh_clear()


for label,folder in [('action_camera_front','action_camera'),('dive_light_rear','dive_light')]:
    obj=next(o for o in scene.objects if o.get('placement_label')==label)
    export_proxy(obj,ROOT/'parts/child/exterior/cots'/folder/'visual_proxy.stl')

# Retain the studio, original cameras and indicative cable curves.
for obj in list(scene.objects):
    if obj.get('placement_label'):
        bpy.data.objects.remove(obj,do_unlink=True)

cache={};hashes={}
palette={'frame':(.025,.25,.52),'connections':(.025,.35,.42),'feet':(.035,.055,.067),
         'crossbars':(.035,.055,.067),'ballast_support':(.10,.13,.15),'equipment_mounts':(.025,.25,.52),
         'bumper':(.035,.055,.067),'hardware':(.55,.60,.62),'foam':(.95,.55,.07)}
materials={}
for group,rgb in palette.items():
    mat=bpy.data.materials.new('Horizontal CAD | '+group);mat.diffuse_color=(*rgb,1);mat.use_nodes=True
    bsdf=mat.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(*rgb,1)
    bsdf.inputs['Metallic'].default_value=.6 if group=='hardware' else .15
    bsdf.inputs['Roughness'].default_value=.3;materials[group]=mat
reference_material={'vessel':'Acrylic vessel','clamps':'Reference cradle | teal','rubber':'Reference liner',
                    'equipment':'Equipment','ballast':'Ballast C | dark metal'}
collection=bpy.data.collections.new('Horizontal fabrication fit prototype');scene.collection.children.link(collection)
objects={}
for item in placement['items']:
    src=ROOT/item['part']/(item['file']+'.stl');key=str(src)
    if key not in cache:
        if not src.exists():raise RuntimeError('Missing CAD mesh: '+str(src))
        bpy.ops.wm.stl_import(filepath=str(src),global_scale=SCALE)
        imported=bpy.context.object;cache[key]=imported.data
        cache[key].transform(imported.matrix_world)
        bpy.data.objects.remove(imported,do_unlink=True)
        hashes[src.relative_to(ROOT).as_posix()]=hashlib.sha256(src.read_bytes()).hexdigest()
    obj=bpy.data.objects.new(item['label'],cache[key]);collection.objects.link(obj)
    obj.matrix_world=matrix(item.get('ops',[]));obj['placement_label']=item['label']
    obj['source']=src.relative_to(ROOT).as_posix();obj['is_printed']=item.get('print',False)
    group=item['group'];mat=materials.get(group) or bpy.data.materials.get(reference_material.get(group,'Equipment'))
    if group=='vessel' and item['label']!='acrylic_tube_200' and item['label']!='dome_top':mat=bpy.data.materials.get('Anodized flange')
    if group=='vessel' and item['label']=='dome_top':mat=bpy.data.materials.get('Acrylic vessel')
    obj.data.materials.clear()
    if mat:obj.data.materials.append(mat)
    objects[item['label']]=obj
scene.frame_end=1
scene.cycles.samples=24
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.threads_mode='FIXED';scene.render.threads=8
scene.render.engine='CYCLES'
scene.camera=bpy.data.objects.get('01 | Front three quarter')
readme=bpy.data.texts.new('READ ME | Fabrication fit prototype');readme.use_fake_user=True
if (OUT/'README.md').exists():readme.write((OUT/'README.md').read_text(encoding='utf-8'))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'child_exterior_horizontal.blend'))
for name,cam,size in [('overview','01 | Front three quarter',(1500,1150)),
                      ('rear','02 | Rear and cable access',(1500,1150)),
                      ('side','04 | Side elevation',(1500,1100)),
                      ('plan','03 | Plan',(1400,1400))]:
    scene.camera=bpy.data.objects[cam];scene.render.resolution_x,scene.render.resolution_y=size
    scene.render.filepath=str(images/(name+'.png'));bpy.ops.render.render(write_still=True)
# A focused view makes the actual screws/stand-offs and all three clamp links reviewable.
scene.camera=bpy.data.objects['07 | Cradle and lower ballast']
scene.camera.location=Vector((520,-350,340))*SCALE
direction=Vector((80,-5,140))*SCALE-scene.camera.location
scene.camera.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();scene.camera.data.ortho_scale=.40
scene.render.resolution_x,scene.render.resolution_y=1400,1100
scene.render.filepath=str(images/'clamp_attachment.png');bpy.ops.render.render(write_still=True)
report=dict(status='fit_prototype',items=len(objects),source_sha256=hashes,
            original_concept_preserved=True,proxies='Exact evaluated local visual-study meshes; not production interfaces')
(OUT/'_work/logs/blender_manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
