"""Validate only the revised parent LiPo box; preserve every other source mesh."""
from parent_access_common import *
import MeshPart,Mesh,hashlib,runpy,os,contextlib,io
W=O/'_work/analysis/battery_box_20261011';P=R/'parts/parent/interior/printed/parent_hand_service'
rows=[]
def checked(name,ok,**data):
 rows.append(dict(name=name,passed=bool(ok),**data));assert ok,rows[-1]
# The packager tracks siblings in one folder. Re-mesh the unchanged siblings
# independently, prove identical bytes, then replace them with that real export.
# This is not a timestamp-only workaround, nor a CAD redesign.
for stem in ['battery_base','floor_plate','main_mount_plate','sony_mount_plate','main_corner_column']:
 s=Part.read(str(P/(stem+'.step')));m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.025,AngularDeflection=.1,Relative=False)
 checked(stem+' mesh',s.isValid() and len(s.Solids)==1 and m.isSolid(),volume_difference=abs(s.Volume-mesh_volume(m))/s.Volume)
 temp=W/(stem+'_remesh.stl');m.write(str(temp))
 if stem!='battery_base':checked(stem+' bytes unchanged',temp.read_bytes()==(P/(stem+'.stl')).read_bytes())
 (P/(stem+'.stl')).write_bytes(temp.read_bytes())
old=Part.read(str(W/'history/parts/parent/interior/printed/parent_hand_service/battery_base.step'))
box=Part.read(str(P/'battery_base.step'));pads=Part.read(str(P/'battery_pads_open_end.step'))
checked('box only removes material',box.cut(old).Volume<.01,removed_mm3=old.Volume-box.Volume)
wire=Part.makeBox(3.5,40,26,v(-5,7.5,3))
checked('entire lead face 40x26 open',common(box,wire)<.01,interference_mm3=common(box,wire))
checked('no foam across lead face',common(pads,wire)<.01)
checked('four retained foam pieces',len(pads.Solids)==4)
maxpack=Part.makeBox(104,36,25,v(-.5,9.5,3))
checked('104x36x25 rigid pack fits box',common(box,maxpack)<.01,interference_mm3=common(box,maxpack))
# Original frame datums and mounting/lid interfaces are untouched.
for x,y in [[0,0],[103,0],[0,55.5],[103,55.5]]:
 sh=Part.makeCylinder(1.725,3,v(x,y,0));checked('mount bore '+str((x,y)),common(box,sh)<.01)
d,c=load();checked('nominal battery fits retained foam',common(c['lipo'],c['lipo_ret_pads'])<.01)
col=collisions(c['lipo_tray'],c,['lipo_tray','lipo_ret_pads']+[n for n in c if n.startswith(('lipo_ret_bolt_','lipo_ret_nut_','battery_floor_bolt_'))])
checked('revised box vs entire installed scene',not col,collisions=col)
# Immutable geometry and every placement row outside the battery foam variant.
oldhash=json.loads((W/'before_hashes.json').read_text());allowed={
 'parts/parent/interior/printed/parent_hand_service/battery_base.'+ext for ext in ['step','stl','scad']}
allowed.add('assemblies/parent_hand_service/parts/battery_base.stl')
allowed.update('assemblies/parent_hand_service/'+n for n in ['placement.json','service_placement.json','print_config.json'])
delta=[f for f,sha in oldhash.items() if f not in allowed and hashlib.sha256((R/f).read_bytes()).hexdigest()!=sha]
checked('all non-box source/copied geometry unchanged',not delta,checked_files=len(oldhash)-len(allowed),changes=delta)
before_config=json.loads((W/'print_config.json').read_text())
after_config=json.loads((O/'print_config.json').read_text())
for key in ['note','notes']:before_config.pop(key);after_config.pop(key)
checked('print quantities and orientations unchanged',before_config==after_config)
for name in ['placement.json','service_placement.json']:
 before=json.loads((W/name).read_text());after=json.loads((O/name).read_text());
 for a,b in zip(before['items'],after['items']):
  if a['label']=='lipo_ret_pads':
   for key in ['part','file']:a[key]=b[key]
 checked(name+' no other changes',before==after)
# Derive both STEP assemblies from the unchanged canonical placement, without
# reconstructing placement from any historical assembly.
for pose,name in [('closed','placement.json'),('service','service_placement.json')]:
 os.environ.update(ASM_JSON=str(O/name),ASM_ROOT=str(R),STEP_OUT=str(O/(pose+'.step')))
 log=io.StringIO()
 with contextlib.redirect_stdout(log):runpy.run_path(str(R/'scad/lib/asm_to_step.py'),run_name='__main__')
 (W/(pose+'_export.log')).write_text(log.getvalue())
report=dict(status='PASS',checks=rows,lead_face_local='-X',lead_opening_mm=[40,26],unchanged_geometry_files=len(oldhash)-len(allowed),maximum_rigid_pack_mm=[104,36,25],limitations='Foam thickness selected from actual pack. Actual leads/connectors not measured. No new structural qualification. Open lead end relies on adjusted compliant holding rather than a rigid end stop.')
(W/'checks.json').write_text(json.dumps(report,indent=2));print('PASS',len(rows),'battery-box checks',flush=True)