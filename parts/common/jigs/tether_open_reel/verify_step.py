"""Run in FreeCAD; compare delivered STEP to STL and check mating geometry."""
from pathlib import Path
import json,re
import FreeCAD as A
import Part,Mesh
P=Path(__file__).resolve().parent
s=(P/'tether_open_reel.scad').read_text()
v={k:float(x) for k,x in re.findall(r'^([a-z_]+)\s*=\s*([\d.]+)\s*;',s,re.M)}
w=v['winding_width']+2*v['flange_t'];r=v['flange_d']/2;sr=r+v['shell_clear']+v['shell_wall']
shapes={};report={'parts':{},'contacts':{}}
for part in ['base','lid','stand','cover_half','clip','coupon_socket','coupon_spring']:
 t=Part.Shape();t.read(str(P/f'tether_open_reel_{part}.step'))
 mesh=Mesh.Mesh(str(P/f'tether_open_reel_{part}.stl')); bb=t.BoundBox;mb=mesh.BoundBox
 err=max(abs(a-b) for a,b in zip([bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax],
                               [mb.XMin,mb.XMax,mb.YMin,mb.YMax,mb.ZMin,mb.ZMax]))
 volerr=abs(t.Volume-abs(mesh.Volume))/abs(mesh.Volume)
 report['parts'][part]=dict(valid=t.isValid(),solids=len(t.Solids),bbox_error_mm=err,volume_error_fraction=volerr)
 assert t.isValid() and len(t.Solids)==1 and err<.5 and volerr<.02,part
 shapes[part]=t
def check(label,a,b,expected_contact=False):
 common=a.common(b);overlap=common.Volume; dist=a.distToShape(b)[0]
 if overlap>=.05: print(label,'intersection bounds',common.BoundBox)
 bb=common.BoundBox
 report['contacts'][label]=dict(intersection_mm3=overlap,distance_mm=dist,
   intersection_bounds=[bb.XMin,bb.XMax,bb.YMin,bb.YMax,bb.ZMin,bb.ZMax] if overlap>.05 else [])
 (P/'step_check_progress.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 assert overlap<.05,(label,overlap)
 if expected_contact:assert dist<.05,(label,dist)
lid=shapes['lid'].copy();lid.rotate(A.Vector(0,0,0),A.Vector(1,0,0),180);lid.translate(A.Vector(0,0,w))
check('base_lid',shapes['base'],lid,True)
shell=shapes['cover_half'].copy();shell.translate(A.Vector(0,0,-v['cover_lip']-v['fit_clear']))
shell2=shell.copy();shell2.rotate(A.Vector(),A.Vector(0,0,1),180)
check('half_shells',shell,shell2,True)
check('base_shell',shapes['base'],shell)
check('lid_shell',lid,shell)
cl=shapes['clip'].copy();cl.translate(A.Vector(sr-v['clip_l']+v['clip_t'],0,30-v['tab_axial_w']/2))
check('clip_upper_tab',cl,shell,True);check('clip_lower_tab',cl,shell2,True)
check('clip_reel',cl,shapes['base'])
for closed in [False,True]:
 z=v['stand_floor']+(sr if closed else r)
 for label,shape in [('base',shapes['base']),('lid',lid)]+([('shell',shell),('shell2',shell2)] if closed else []):
  placed=shape.copy();placed.rotate(A.Vector(),A.Vector(1,0,0),90);placed.translate(A.Vector(0,w/2,z))
  check(f'stand_{label}_{closed}',shapes['stand'],placed, label=='shell2' if closed else label in ('base','lid'))
coupon=shapes['coupon_spring'].copy();coupon.rotate(A.Vector(),A.Vector(1,0,0),180);coupon.translate(A.Vector(0,0,36+v['flange_t']))
check('snap_coupon',shapes['coupon_socket'],coupon,True)
(P/'step_check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('STEP solid/bbox/volume and mating interference checks PASS')
import Import,MeshPart
root=P.parents[3]
for aname in ['tether_open_reel','tether_open_reel_closed']:
 ap=root/'assemblies'/aname
 cs=json.loads((ap/'placement.json').read_text())['parts']
 doc=A.newDocument(aname);objs=[];placed_shapes=[]
 for c in cs:
  key=c['file'].replace('tether_open_reel_','',1)
  shape=shapes[key].copy()
  for op in reversed(c['ops']):
   if 'translate' in op:shape.translate(A.Vector(*op['translate']))
   if 'rotate' in op:
    for axis,ang in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],op['rotate']):
     if ang:shape.rotate(A.Vector(),axis,ang)
  ob=doc.addObject('Part::Feature','Component');ob.Label=c['label'];ob.Shape=shape
  objs.append(ob);placed_shapes.append(shape)
 doc.recompute();Import.export(objs,str(ap/f'{aname}.step'))
 compound=Part.makeCompound(placed_shapes)
 mm=MeshPart.meshFromShape(Shape=compound,LinearDeflection=.15,AngularDeflection=.15,Relative=False)
 mm.write(str(ap/f'{aname}.stl'))
 reread=Part.Shape();reread.read(str(ap/f'{aname}.step'))
 assert reread.isValid() and len(reread.Solids)==len(cs)
 assert abs(reread.Volume-compound.Volume)<1
 (ap/'assembly_check.json').write_text(json.dumps(dict(valid=True,solids=len(cs),volume_mm3=reread.Volume),indent=2),encoding='utf-8')
 A.closeDocument(doc.Name)
print('Both named assembly STEP/STL exports reread and checked')
