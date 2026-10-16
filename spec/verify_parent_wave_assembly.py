"""Continuous conservative sweeps for the prescribed in-case assembly sequence.

PCB sweeps use each imported solid's own bounding box, never a whole populated
board bounding box. Carrier sweep is a union of translated boundary prisms.
No sampling of isolated poses is used to infer a clear continuous path.
"""
from parent_access_common import *
import sys,hashlib
sys.path.insert(0,str(R/'scad/lib'));import parent_gnss as G
if '--merge-sony-path' in sys.argv:
 w=O/'_work/analysis/fixed_plates_20261011'
 refined=json.loads((w/'sony_plate_path.json').read_text())
 assert refined['status']=='PASS' and refined['placement_sha256']==hashlib.sha256((O/'placement.json').read_bytes()).hexdigest()
 original=json.loads((O/'wave_assembly_checks.json').read_text(encoding='utf-8'))
 (w/'assembly_conservative_checks.json').write_text(json.dumps(original,indent=2),encoding='utf-8')
 replacement=refined['checks'][0];assert sum(q['name']==replacement['name'] for q in original['checks'])==1
 original['checks']=[replacement if q['name']==replacement['name'] else q for q in original['checks']]
 assert all(q['pass_'] for q in original['checks'])
 original.update(status='PASS',placement_sha256=refined['placement_sha256'],sony_path_refinement='Validated continuous rectangle and circular-pad prisms preserve the footprint near molded case corners. See _work/analysis/fixed_plates_20261011/sony_plate_path.json.')
 (O/'wave_assembly_checks.json').write_text(json.dumps(original,ensure_ascii=False,indent=2),encoding='utf-8')
 print('PASS continuous assembly paths with round Sony footprint');raise SystemExit(0)

d,c=load();rows=[]

def moved(s,offset):
 t=s.copy();t.translate(v(*offset));return t

def sweep(s,offset,delta,boxes=False):
 s=moved(s,offset);vec=v(*delta);out=[s]
 if boxes:
  out=[]
  for piece in s.Solids:
   # OCC's coarse box can extend below a trimmed, inclined hole entrance.
   # The precise shape box remains conservative without that false extension.
   b=piece.optimalBoundingBox(False,False)
   low=[min(q,q+t) for q,t in zip([b.XMin,b.YMin,b.ZMin],delta)]
   sizes=[q+abs(t) for q,t in zip([b.XLength,b.YLength,b.ZLength],delta)]
   if min(sizes)>1e-7:out.append(Part.makeBox(*sizes,v(*low)))
 else:
  for f in s.Faces:
   try:
    p=f.extrude(vec)
    if abs(p.Volume)>1e-7:
     if p.Volume<0:p.reverse()
     out.append(p)
   except Part.OCCError:pass  # Faces parallel to travel have zero swept volume.
 if boxes:return out
 out.append(moved(s,delta))
 # Test each prism separately. An overlapping compound is not a valid boolean
 # operand; individual positive valid prisms avoid that signed-volume artifact.
 if not all(p.isValid() and p.Volume>0 for p in out):
  result=out[0].multiFuse(out[1:]).removeSplitter()
  assert result.isValid() and result.Volume>0
  return result
 return out

def check(name,shape,targets):
 if isinstance(shape,list):
  totals={}
  for item in shape:
   for hit in collisions(item,{k:c[k] for k in targets}):totals[hit['part']]=totals.get(hit['part'],0)+hit['mm3']
  hits=[dict(part=k,mm3=round(val,4)) for k,val in totals.items()]
 else:hits=collisions(shape,{k:c[k] for k in targets})
 rows.append(dict(name=name,collisions=hits,pass_=not hits));print(name,hits,flush=True)

base=['plate','box_bcas212310g']+[n for n in c if n.startswith('case_anchor_')]
main_supports=[n for n in corner_fixtures(c) if n.startswith('main_')]
def main_support_paths():
 for n in main_supports:
  sh=c[n]
  if n=='main_mount_plate':
   low=sh.common(Part.makeBox(220,230,2.4,v(0,0,33.1)))
   high=sh.common(Part.makeBox(220,230,20,v(0,0,35.5)))
   sh=Part.makeCompound(low.Solids+high.Solids)
  check(n+' north raised insertion',sweep(sh,[0,92,100],[0,0,-85.8],True),base+['antenna_rack'])
  check(n+' south slide',sweep(sh,[0,92,14.2],[0,-92,0],True),base+['antenna_rack'])
  if n!='main_mount_plate':
   b=c[n].optimalBoundingBox(False,False)
   travel=Part.makeCylinder(3.5,b.ZLength+14.2,v((b.XMin+b.XMax)/2,(b.YMin+b.YMax)/2,b.ZMin))
  else:travel=sweep(sh,[0,0,14.2],[0,0,-14.2],True)
  check(n+' lower',travel,base+['antenna_rack'])

def sony_support_paths():
 n='sony_mount_plate';b=c[n].optimalBoundingBox(False,False)
 pts=G.SONY_CARRIER_FOOT_XY
 x0=min(q[0] for q in pts);y0=min(q[1] for q in pts)
 travel=Part.makeBox(max(q[0] for q in pts)-x0,max(q[1] for q in pts)-y0,b.ZLength+100,v(x0,y0,b.ZMin))
 # Circumscribed circular pads preserve the rounded footprint at case corners.
 for x,y in pts:travel=travel.fuse(Part.makeCylinder(3.5,b.ZLength+100,v(x,y,b.ZMin)))
 for x,y in json.loads((O/'hole_sources.json').read_text())['SONY']:travel=travel.fuse(Part.makeCylinder(3,b.ZLength+100,v(x,y,b.ZMin)))
 for x,y in G.SONY_CARRIER_FOOT_XY:
  key=G.SONY_COLUMN_VARIANTS['sony_column_right' if x>200 else 'sony_column_left'][1]
  clearance=Part.makeCylinder((key+G.SONY_COLUMN_KEY_CLEARANCE)/2,G.SONY_COLUMN_KEY_HEIGHT+.2,v(x,y,G.SONY_COLUMN_JOINT_Z-.1))
  assert common(clearance,c[n])<.001,('Actual key clearance',n)
  travel=travel.cut(clearance)
 assert c[n].cut(travel).Volume<.001,('Plate containment',n)
 check(n+' over installed TX',travel,base+['tx_improved','p_pwr']+['sony_column_'+str(j) for j in range(4)])

if '--sony-path-only' in sys.argv:
 sony_support_paths()
 result=dict(status='PASS' if all(q['pass_'] for q in rows) else 'FAIL',checks=rows,placement_sha256=hashlib.sha256((O/'placement.json').read_bytes()).hexdigest(),method='Continuous rectangle/circular-pad prism union with validated key void; actual shape containment verified.')
 (O/'_work/analysis/fixed_plates_20261011/sony_plate_path.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 assert result['status']=='PASS';raise SystemExit(0)
# Floor anchored first; top-loaded nuts are inserted before the separate modules.
for stem,pts in [('main_carrier',G.MAIN_CARRIER_FOOT_XY),('sony_carrier',G.SONY_CARRIER_FOOT_XY),('gnss_frame',G.UNIVERSAL_FRAME_FOOT_XY),('antenna_rack',G.RACK_FOOT_XY)]:
 for i,(x,y) in enumerate(pts):
  n=f'{stem}_nut_{i}'
  check(n+' insertion',sweep(c[n],[0,0,90],[0,0,-90]),base)
check('coax ring vertical insertion',sweep(c['coax_ring'],[0,0,100],[0,0,-100]),base)
check('antenna rack vertical insertion',sweep(c['antenna_rack'],[0,0,100],[0,0,-100]),base+['coax_ring'])
base += ['coax_ring']
main_support_paths()
main_obstacles=base+['antenna_rack']+main_supports
check('MAIN PCB north raised insertion',sweep(c['p_main'],[0,92,100],[0,0,-95.2],True),main_obstacles)
check('MAIN PCB south slide raised',sweep(c['p_main'],[0,92,4.8],[0,-92,0],True),main_obstacles)
check('MAIN PCB lower at final XY',sweep(c['p_main'],[0,0,4.8],[0,0,-4.8],True),main_obstacles)
for n in ['main_mount_'+str(i) for i in range(4)]:
 bolt=c[n];bb=bolt.BoundBox
 targets=main_obstacles
 if n=='main_mount_1':
  # The one retained short screw intentionally forms a thread in the2.6 pilot.
  # Exempt only its3mm shaft's pilot region, never its head or the access path.
  pilot=Part.makeCylinder(1.3,6.3,v(22.5,32,35.6))
  rows.append(dict(name=n+' actual2.6mm pilot',overlap_mm3=common(pilot,c['main_mount_plate']),pass_=common(pilot,c['main_mount_plate'])<.01))
  host=c['main_mount_plate'];c['main_mount_plate']=host.cut(Part.makeCylinder(1.51,6.6,v(22.5,32,35.5)))
 check(n+' insertion',sweep(bolt,[0,0,90],[0,0,-90]),targets)
 if n=='main_mount_1':c['main_mount_plate']=host
 check(n+' driver',Part.makeCylinder(2.6,110-bb.ZMax,v((bb.XMin+bb.XMax)/2,(bb.YMin+bb.YMax)/2,bb.ZMax)),['antenna_rack']+main_supports)
for n in [q for q in c if q.startswith(('ground_plate_nut_','antenna_nut_'))]:
 check(n+' top insertion before steel plate',sweep(c[n],[0,0,90],[0,0,-90]),main_obstacles)
 bb=c[n].BoundBox;x=(bb.XMin+bb.XMax)/2;y=(bb.YMin+bb.YMax)/2
 turn=c[n].copy();turn.rotate(v(x,y,0),v(0,0,1),30)
 stop=common(turn,c['antenna_rack'])
 rows.append(dict(name=n+' captured hex rotation stop',interference_at30deg_mm3=stop,pass_=stop>.1))
for i in range(4):check('Sony column '+str(i)+' vertical insertion',sweep(c['sony_column_'+str(i)],[0,0,100],[0,0,-100]),base+['tx_improved','p_pwr'])
sony_support_paths()
gnss_obstacles=base+['p_main','p_pwr','tx_improved','spresense']+['sony_column_'+str(i) for i in range(4)]+corner_fixtures(c)
for i in range(4):check('GNSS column '+str(i)+' vertical insertion',sweep(c['gnss_column_'+str(i)],[0,0,100],[0,0,-100]),gnss_obstacles)
check('GNSS frame vertical insertion',sweep(c['gnss_universal_carrier'],[0,0,100],[0,0,-100]),gnss_obstacles+['gnss_column_'+str(i) for i in range(4)])
# Every carrier bolt is installed from the top, with its own fixture included.
for it in d['items']:
 n=it['label']
 if not n.startswith(('main_carrier_mount_','sony_carrier_mount_','gnss_frame_mount_','antenna_rack_mount_')):continue
 fixture={'main_carrier':'main_mount_plate','sony_carrier':sony_corner_for_foot(int(n.rsplit('_',1)[1])),'gnss_frame':'gnss_universal_carrier','antenna_rack':'antenna_rack'}[n.rsplit('_mount_',1)[0]]
 bolt=c[n];bb=bolt.BoundBox
 joints=['coax_ring'] if fixture=='antenna_rack' else ['gnss_column_'+str(i) for i in range(4)] if fixture=='gnss_universal_carrier' else ['sony_column_'+str(i) for i in range(4)] if fixture=='sony_mount_plate' else []
 check(n+' insertion',sweep(bolt,[0,0,90],[0,0,-90]),['plate',fixture]+joints)
 tool=Part.makeCylinder(2.6,110-bb.ZMax,v((bb.XMin+bb.XMax)/2,(bb.YMin+bb.YMax)/2,bb.ZMax))
 check(n+' driver',tool,[fixture])
out=dict(status='PASS' if all(r['pass_'] for r in rows) else 'FAIL',checks=rows,
 sequence=['Anchor unchanged floor to SW/SE/NW case M4 inserts; NE unused.','Insert16 M3 nuts from above, flats parallel X.','Install antenna rack with four M3x50; keep antenna, steel plate and cable off for MAIN installation.','Insert four MAIN lower columns and flat fixing plate north92/up14.2, slide south92 then lower.','Insert MAIN PCB north92/up4.8, slide south92, lower4.8; install three M3x30 and one short PCB screw plus front carrier M3x25.','Insert four M3 and two M4 captive nuts from above, then steel plate/antenna.','Install PWR, TX, Sony columns/fixing plate/PCB, GNSS frame/PCB. Case anchors accessible with installed modules, SE after pack/lid/top foam removal. Full interior lift-out still requires disconnected case harness and a separate extraction-path check.'],
 limitations=['Case inner envelope is a conservative DXF-based proxy; real boss height and screw dimensions require fit check.','Continuous PCB paths use each actual solid bounding box; conservative PASS is sufficient, FAIL needs geometry review.','Assembly paths assume loose cables disconnected/parked; user handling and harness slack need physical trial.'])
(O/'wave_assembly_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
assert out['status']=='PASS',out['status']
