"""Current parent_hand_service generator body, shared by its existing entry point.

Definitions and mm datums remain in scad/lib/parent_gnss.py. This is parametric
CAD, unrelated to topology-optimization output. Legacy lift parts are historical.
"""
mh=[[GNSS.MAIN_ORIGIN[0]+x,GNSS.MAIN_ORIGIN[1]-y] for x,y in holes('PARENT_MAIN')]
ph=[[GNSS.PWR_ORIGIN[0]+y,GNSS.PWR_ORIGIN[1]+x] for x,y in holes('PARENT_PWR')]
th=[[GNSS.TX_ORIGIN[0]+y,GNSS.TX_ORIGIN[1]+x] for x,y in holes('TX_improved')]
sh=[[GNSS.SONY_ORIGIN[0]-x,GNSS.SONY_ORIGIN[1]-y] for x,y in [[2.54,54.61],[50.8,53.34],[7.62,2.54],[35.56,2.54]]]
guides=[];prop_centres=[]
grid_x=[16.5,40,75,110,145,175,193.5]
grid_y=[16.5,45,85,125,165,195,213.5]
gw=GNSS.FLOOR_GRID_WIDTH;gz=GNSS.FLOOR_GRID_BOTTOM_Z;gh=GNSS.FLOOR_GRID_TOP_Z-gz
floor=None
for x in grid_x:
 rib=finished(box(x-gw/2,13.5,gz,gw,203,gh),'floor_grid_x_'+str(x),.25)
 floor=rib if floor is None else floor.fuse(rib)
for y in grid_y:floor=floor.fuse(finished(box(13.5,y-gw/2,gz,183,gw,gh),'floor_grid_y_'+str(y),.25))
# Every fixture has a positive load path to the open, full-depth grid. No skin
# spans its cells. Keep all existing mounting seats/nuts at their original Z.
floor_mounts=GNSS.CASE_ANCHOR_XY+ph+th+[GNSS.battery_xy(x,y) for x,y in [[0,0],[103,0],[0,55.5],[103,55.5]]]
floor_mounts += sum([GNSS.UNIVERSAL_FRAME_FOOT_XY,GNSS.RACK_FOOT_XY,GNSS.MAIN_CARRIER_FOOT_XY,GNSS.SONY_CARRIER_FOOT_XY],[])
for i,(x,y) in enumerate(floor_mounts):
 nx=min(grid_x,key=lambda q:abs(q-x));ny=min(grid_y,key=lambda q:abs(q-y))
 # Orthogonal legs join a retained pad to the nearest grid intersection.
 for args in [(min(x,nx)-3,y-3,gz,abs(x-nx)+6,6,gh),(nx-3,min(y,ny)-3,gz,6,abs(y-ny)+6,gh)]:
  floor=floor.fuse(finished(box(*args),'floor_mount_link_'+str((i,args[:2])),.15))
 if [x,y] in GNSS.CASE_ANCHOR_XY:floor=floor.fuse(finished(cyl(x,y,gz,7.5,gh),'case_anchor_pad_'+str(i),.15))
floor=floor.cut(box(203.75,0,8,20,240,25)).cut(box(0,223.75,8,220,20,25))
case_dir=R/'parts/parent/exterior/cots/bcas212310g'
case_dims=json.loads((case_dir/'dimensions.json').read_text(encoding='utf-8'))
case_bosses=case_dims['insert_xy_mm']+case_dims['tapping_xy_mm']
boss_top=case_dims['boss_top_z_mm']
for x,y in case_bosses:floor=floor.cut(cyl(x,y,gz-.1,5.3 if [x,y] in GNSS.CASE_ANCHOR_XY else 4.8,boss_top-gz+.1))
# Nut seats now continue to the grid underside; no raised underside pockets.
for pts,top in [(ph,28.25),(th,24.75)]:
 for x,y in pts:floor=floor.fuse(cyl(x,y,18.8,3.2 if pts==ph else 3.5,top-18.8)).cut(bore(x,y,13.7,2.6,top-13.7+.1))
for x,y in [GNSS.battery_xy(x,y) for x,y in [[0,0],[103,0],[0,55.5],[103,55.5]]]:
 floor=floor.fuse(cyl(x,y,13.84,3.5,6.16)).cut(bore(x,y,13.7,2.6,6.4))
for name,pts in [('gnss',GNSS.UNIVERSAL_FRAME_FOOT_XY),('rack',GNSS.RACK_FOOT_XY),('main',GNSS.MAIN_CARRIER_FOOT_XY),('sony',GNSS.SONY_CARRIER_FOOT_XY)]:
 for i,(x,y) in enumerate(pts):
  # Local floor tabs remain inside the exact case wall; support each recess.
  x0=min(194,x-5.5) if x>196.5 else max(15 if name=='gnss' and i==2 else 7.8,x-5.5)
  x1=min(203.75,x+5.5);y0=max(7.8,y-5.5);y1=min(223.75,y+5.5)
  floor=floor.fuse(finished(box(x0,y0,gz,x1-x0,y1-y0,gh),f'{name}_floor_tab_{i}',.15))
  floor=floor.cut(bore(x,y,gz-.1,3.45,gh+.2))
  radius=5.8/math.sqrt(3)
  ps=[v(x+radius*math.cos(math.pi/6+i*math.pi/3),y+radius*math.sin(math.pi/6+i*math.pi/3),16.2) for i in range(6)]
  pocket=CSG(Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(v(0,0,2.8)),f'translate([{x},{y},16.2]) rotate([0,0,30]) cylinder(r={radius},h=2.8,$fn=6);')
  floor=floor.cut(pocket)
# Keep the new full-depth mount links clear of the case's four corner posts.
# In particular the rear-west GNSS foot links past the post at(9,221).
# Filled nut tabs may cross the edge of a real case boss; trim only that boss
# envelope after adding the tabs, preserving support under the nut axis.
for x,y in case_bosses:floor=floor.cut(cyl(x,y,gz-.1,5.3 if [x,y] in GNSS.CASE_ANCHOR_XY else 4.8,boss_top-gz+.1))
for x,y in [(9,9),(201,9),(9,221),(201,221)]:floor=floor.cut(cyl(x,y,8.7,5.45,10.3))
inside=Part.read(str(case_dir/'interior_corner_clearance.step'))
bottom_face=next(f for f in inside.Faces if abs(f.BoundBox.ZMin)<1e-6 and abs(f.BoundBox.ZMax)<1e-6)
mask=bottom_face.extrude(v(0,0,gh));mask.translate(v(0,0,gz))
rim=[e for e in mask.Edges if abs(e.BoundBox.ZLength)<1e-6]
mask=mask.makeChamfer(.15,rim)  # bevel the allowed-volume rim before clipping
upper_mask=bottom_face.extrude(v(0,0,100-18.8));upper_mask.translate(v(0,0,18.8))
floor=CSG(floor.s.common(mask.fuse(upper_mask)),'')  # 0.5 mm corner clearance
for x,y in GNSS.CASE_ANCHOR_XY:
 # Continuous local bearing from the real Z10 boss to the existing grid/seat.
 floor=floor.fuse(cyl(x,y,boss_top,4.5,18.8-boss_top))
 floor=floor.cut(bore(x,y,boss_top-.1,4.5,18.9-boss_top)).cut(cyl(x,y,GNSS.CASE_ANCHOR_SEAT_Z,4.1,2.2))
save('floor_plate',finished(floor,'floor_plate',.15))

# Battery source is inserted by the entry point; it is unchanged from the
# confirmed LiPo-retainer variant and shares its original six foam pads/lid.
build_battery_base()

def underside_mounts(c,pts,top):
 for x,y in pts:
  radius=2.8 if pts==GNSS.SONY_CARRIER_FOOT_XY and x>200 else 3.5
  c=c.fuse(finished(cyl(x,y,18.8,radius,top-18.8),'support_post_'+str((x,y,top)),.15))
  c=c.cut(cyl(x,y,18.7,1.725,top-18.7+.1))
  if pts==GNSS.MAIN_CARRIER_FOOT_XY:
   c=c.fuse(cyl(x,y,18.8,4.5,3))
   taper=Part.makeCone(4.5,3.5,1,v(x,y,21.8))
   c=c.fuse(CSG(taper,f'translate([{x},{y},21.8]) cylinder(r1=4.5,r2=3.5,h=1,$fn=64);'))
  else:
   x0,w=(140.5,7) if x<180 else (198.3,5.4)
   c=c.fuse(box(x0,y-5,18.8,w,10,3))
 return c
# MAIN rotated: flat fixing plate with raised screw seats.
from parent_corner_mounts import main_shapes,sony_shapes
def corner_csg(shape):
 mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.025,AngularDeflection=.1,Relative=False)
 points,faces=mesh.Topology
 return CSG(shape,'polyhedron(points='+json.dumps([[p.x,p.y,p.z] for p in points])+',faces='+json.dumps([list(f) for f in faces])+',convexity=10);')
for stem,shape in main_shapes(mh,GNSS).items():
 save(stem,corner_csg(shape))
 edge_finishing[stem]=dict(chamfer_mm=.15,permitted_sharp_edges='Specified flat bearing surfaces and pilot/key fits; no component-shaped pockets')
# Sony shelf: lightened flat fixing plate with raised screw seats.
for stem,shape in sony_shapes(sh,GNSS).items():
 save(stem,corner_csg(shape))
 edge_finishing[stem]=dict(chamfer_mm=.15,permitted_sharp_edges='Specified flat bearing surfaces and pilot/key fits; no component-shaped pockets')

old=json.loads((R/'assemblies/parent_service_review/placement.json').read_text(encoding='utf-8'))
a=copy.deepcopy(old);a['name']='parent_hand_service';a['items']=[it for it in a['items'] if not it['label'].startswith('main_spacer')]
def setops(label,xyz,rot=None):
 it=next(it for it in a['items'] if it['label']==label);it['ops']=[{'translate':xyz}]+([{'rotate':rot}] if rot else []);it.pop('note',None)
setops('p_main',GNSS.MAIN_ORIGIN,GNSS.MAIN_ROTATION);setops('p_pwr',GNSS.PWR_ORIGIN,[0,0,90]);setops('tx_improved',GNSS.TX_ORIGIN,[0,0,90]);setops('spresense',GNSS.SONY_ORIGIN,GNSS.SONY_ROTATION)
setops('lipo',GNSS.battery_xy(102.5,44.5)+[23],[0,0,270]);setops('lipo_tray',GNSS.BATTERY_ORIGIN,GNSS.BATTERY_ROTATION);setops('lipo_ret_lid',GNSS.BATTERY_ORIGIN[:2]+[49],GNSS.BATTERY_ROTATION);setops('lipo_ret_pads',GNSS.BATTERY_ORIGIN,GNSS.BATTERY_ROTATION)
next(it for it in a['items'] if it['label']=='lipo_ret_lid')['file']='parent_lipo_retainer_lid_slide'
setops('pen_tether',[28,0,65],[-90,0,0]);setops('pen_td04a',[120,0,65],[-90,0,0])
for i,(x,y) in enumerate(bc['bolt_xy']):
 setops('lipo_ret_bolt_'+str(i),GNSS.battery_xy(x,y)+[52]);setops('lipo_ret_nut_'+str(i),GNSS.battery_xy(x,y)+[41.6],GNSS.BATTERY_ROTATION)
a['items']=[it for it in a['items'] if it['label'] not in [f'lipo_ret_{kind}_{i}' for kind in ['bolt','nut'] for i in [1,2,3]]]
for i,(x,y) in enumerate([[0,0],[103,0],[0,55.5],[103,55.5]]):setops('lipo_ret_mount_'+str(i),GNSS.battery_xy(x,y)+[23])
for label,name in [('plate','floor_plate'),('lipo_tray','battery_base')]:
 it=next(it for it in a['items'] if it['label']==label);it['part']=P.relative_to(R).as_posix();it['file']=name
 if label=='plate':it['ops']=[]
def add(label,part,name,xyz=None,rot=None,color='Orange',alpha=None):
 it=dict(label=label,part=part,file=name,group='interior',color=color,ops=[] if xyz is None else [{'translate':xyz}]+([{'rotate':rot}] if rot else []))
 if alpha is not None:it['alpha']=alpha
 a['items'].append(it)
def screw(label,stem,x,y,z,rot=None):add(label,'parts/common/interior/cots/screw',stem,[x,y,z],rot,'Silver')
for i,(x,y) in enumerate(GNSS.CASE_ANCHOR_XY[:3]):screw('case_anchor_'+str(i),'screw_m4x12_button',x,y,GNSS.CASE_ANCHOR_SEAT_Z)
# Independent lower spacers support flat printable fixing plates.
for i,(x,y) in enumerate(GNSS.MAIN_CARRIER_FOOT_XY):
 add('main_column_'+str(i),P.relative_to(R).as_posix(),'main_corner_column',[x,y,18.8]);a['items'][-1].update(print=False,print_set='parent_stack_spacer_set')
for name in ['main_mount_plate','sony_mount_plate']:add(name,P.relative_to(R).as_posix(),name)
for i,(x,y) in enumerate(GNSS.SONY_CARRIER_FOOT_XY):
 add('sony_column_'+str(i),'parts/common/interior/printed/stack_spacers','sony_column_right' if x>200 else 'sony_column_left',[x,y,GNSS.FLOOR_GRID_TOP_Z])
 a['items'][-1].update(print=False,print_set='parent_stack_spacer_set')
add('lid_keepout','parts/parent/exterior/cots/bcas212310g','bcas212310g_cover',color='LightGray',alpha=.18)
next(it for it in a['items'] if it['label']=='box_bcas212310g')['note']='2026-10-10 drawing-derived body: floor3, boss top10, 4 inserts/12 tapping bosses, drafted walls and corner bays; vendor STEP and physical fit pending.'
next(it for it in a['items'] if it['label']=='plate')['note']='Grid top18.8 retained. Drawing corner contour minus0.5 clearance; actual Z10 boss bearing. M4x12 button anchors.'
for stem,pts,seat in [('main',mh,43.6),('sony',sh,67.2),('pwr',ph,29.9),('tx',th,26.4)]:
 for i,(x,y) in enumerate(pts):screw(f'{stem}_mount_{i}','screw_m2_5x6' if stem=='sony' else ('screw_m3x30' if stem=='main' and [x,y] in GNSS.MAIN_CARRIER_FOOT_XY else 'screw_m3x8'),x,y,seat)
for stem,pts in [('main_carrier',GNSS.MAIN_CARRIER_FOOT_XY),('sony_carrier',GNSS.SONY_CARRIER_FOOT_XY),('gnss_frame',GNSS.UNIVERSAL_FRAME_FOOT_XY),('antenna_rack',GNSS.RACK_FOOT_XY)]:
 for i,(x,y) in enumerate(pts):
  screw(f'{stem}_nut_{i}','screw_nut_m3',x,y,16.2,[0,0,30])
  if stem=='main_carrier' and i>0:continue
  size,seat={'main_carrier':('25',36.8),'sony_carrier':('50',GNSS.SONY_COLUMN_JOINT_Z+1.6),'gnss_frame':('40',52.5),'antenna_rack':('50',63.6)}[stem]
  screw(f'{stem}_mount_{i}','screw_m3x'+size,x,y,seat)
bp=GNSS.BOARD_DIR.relative_to(R).as_posix();ap=GNSS.ANTENNA_DIR.relative_to(R).as_posix();fp='parts/parent/interior/printed/gnss_universal_carrier';rp='parts/parent/interior/printed/ann_mb1_internal_rack'
for label,file in [('gnss_receiver','sparkfun_neo_f9p'),('gnss_sma_plug','sma_plug_envelope'),('gnss_pin_headers','gnss_pin_headers')]:add(label,bp,file,GNSS.BOARD_ORIGIN,GNSS.BOARD_ROTATION,'Green')
add('gnss_universal_pcb',bp,'universal_pcb_60x80',GNSS.UNIVERSAL_ORIGIN,color='Olive')
add('gnss_xh_keepout',bp,'xh_plug_keepout',GNSS.XH_KEEPOUT_PROVISIONAL[:3],color='Yellow',alpha=.3)
add('gnss_universal_carrier',fp,'gnss_universal_carrier')
for i,(x,y) in enumerate(GNSS.UNIVERSAL_FRAME_FOOT_XY):
 add('gnss_column_'+str(i),fp,'gnss_column_rear' if y>200 else 'gnss_column_front',[x,y,18.8])
 a['items'][-1].update(print=False,print_set='parent_stack_spacer_set')
for i,(x,y) in enumerate(GNSS.universal_mounting_xy()):
 screw('gnss_pcb_bolt_'+str(i),'screw_m3x10',x,y,GNSS.UNIVERSAL_ORIGIN[2]+GNSS.UNIVERSAL_SIZE[2])
 screw('gnss_pcb_nut_'+str(i),'screw_nut_m3',x,y,GNSS.UNIVERSAL_BEAM_BOTTOM_Z-2.4)
add('antenna_rack',rp,'ann_mb1_internal_rack',GNSS.ANTENNA_CENTRE+[GNSS.RACK_BASE_Z])
add('coax_ring',rp,'ann_mb1_coax_ring',GNSS.ANTENNA_CENTRE+[GNSS.RACK_BASE_Z])
add('antenna_ground_plate',ap,'ground_plate_internal',GNSS.ANTENNA_CENTRE+[GNSS.GROUND_PLATE_Z],color='Silver')
add('gnss_antenna',ap,'ann_mb1',GNSS.ANTENNA_CENTRE+[GNSS.ANTENNA_Z],GNSS.ANTENNA_ROTATION,'DimGray')
add('coax_coil_keepout',ap,'coax_coil_keepout',GNSS.ANTENNA_CENTRE+[GNSS.RACK_BASE_Z],color='Purple',alpha=.2)
add('gnss_coax_route',ap,'coax_route',color='Black')
mp=GNSS.MAG_DIR.relative_to(R).as_posix()
add('magnetometer',mp,'adafruit_lis3mdl',GNSS.MAG_ORIGIN,GNSS.MAG_ROTATION,color='MediumSeaGreen')
for i,(x,y) in enumerate(GNSS.magnetometer_mounting_xy()):
 add('mag_bolt_'+str(i),mp,'nylon_m2x8_envelope',[x,y,GNSS.MAG_ORIGIN[2]+GNSS.MAG_PCB_THICKNESS],color='Ivory')
 add('mag_nut_'+str(i),mp,'nylon_nut_m2_envelope',[x,y,GNSS.MAG_SHELF_BOTTOM_Z-GNSS.MAG_NUT_AF_HEIGHT[1]],color='Ivory')
for i,(x,y) in enumerate(GNSS.GROUND_PLATE_HOLES_XY):
 screw('ground_plate_mount_'+str(i),'screw_m3x6',x,y,64.6);screw('ground_plate_nut_'+str(i),'screw_nut_m3',x,y,61.2)
for i,x in enumerate([26,94]):
 screw('antenna_mount_'+str(i),'screw_m4x12',x,60,70.6);screw('antenna_nut_'+str(i),'screw_nut_m4',x,60,60.4)
def transform(s,ops):
 for op in reversed(ops):
  if 'rotate' in op:
   for axis,ang in zip([v(1,0,0),v(0,1,0),v(0,0,1)],op['rotate']):s.rotate(v(0,0,0),axis,ang)
  if 'translate' in op:s.translate(v(*op['translate']))
 return s
for it in a['items']:
 if it['label']=='lipo_ret_pads':
  it['part']='parts/parent/interior/printed/parent_hand_service';it['file']='battery_pads_open_end'
shapes={it['label']:transform(Part.read(str(R/it['part']/(it.get('file',Path(it['part']).name)+'.step'))),it['ops']) for it in a['items']}
# Reservation is based on the imported populated TX model, not bare PCB height.
txbb=shapes['tx_improved'].optimalBoundingBox(False,False)
save('tx_top_keepout',box(txbb.XMin,txbb.YMin,txbb.ZMax,txbb.XLength,txbb.YLength,GNSS.TX_TOP_EXTRA_MM))
add('tx_top_keepout',P.relative_to(R).as_posix(),'tx_top_keepout',color='Cyan',alpha=.15)
shapes['tx_top_keepout']=Part.read(str(P/'tx_top_keepout.step'))
a.update(service_only=[],lift_mm=0,moving_labels=[it['label'] for it in a['items'] if it['group']=='interior' and it['label'] not in ['lid_keepout','tx_top_keepout']],
 service_translation_mm=[230,0,0],coordinate_system='Box exterior southwest bottom origin; mm. Floor top18.8; MAIN PCB42; Sony PCB65.6; antenna top87.1.',
 note='Power switches, LiPo and both SD cards accessible with lid open. MAIN USB accessed after removing interior from case. No lift carrier/props in this variant.',
 access_revision=dict(date='2026-10-13',switches='Direct top access, both SW_PWR and SW_TX, at installed height',tx_extra_mm=20,tx_reservation='Full populated TX XY bounding envelope, 20 mm above its highest component',main_usb='Out of case, straight south approach',battery='Remove four tray mount screws, lift closed module90, then remove one lid screw and slide south108',sd='Both face south; direct card slide then lift'),
 gnss_design=dict(receiver='SparkFun GPS-23288 / NEO-F9P v1.1',antenna='u-blox ANN-MB1-00',universal_carrier_mm=GNSS.UNIVERSAL_SIZE[:2],mounting_hole_pitch_mm=GNSS.UNIVERSAL_HOLE_PITCH,mounting_holes_xy_mm=GNSS.universal_mounting_xy(),mount='Four M3x10 bolts and M3 nuts; edge caps removed',battery_status='Parent LiPo retained, no dedicated SPRESENSE battery',provisional_envelopes='XH pin count/edge/height and header height unselected; connector and SMA plug envelopes require measurement'))
a['magnetometer_design']=dict(product='Adafruit 4479 LIS3MDL / Switch Science 6266',date='2026-10-11',mount='Coplanar rectangular frame connected to GNSS west rail and rear beam, four vendor 2.5 mm holes, nylon M2x8/nuts',origin_mm=GNSS.MAG_ORIGIN,rotation_deg=GNSS.MAG_ROTATION,connection='South STEMMA QT socket reserved; north socket unused inside case. Cable and host unselected',calibration='ANN-MB1 has magnetic base. Increased separation does not certify accuracy; measure/calibrate complete powered enclosure, check range/saturation before calibration')
a['case_anchor_access']=dict(date='2026-10-12',used_anchor_indices=[0,1,2],unused_anchor_index=3,floor_geometry='unchanged',tool='Long 2.5 mm ball-end hex key: SW tilted10 degrees SW; NW tilted10 degrees W; SE vertical after removing pack/lid/top foam',guide_id_mm=4.2,three_anchor_strength='unverified')
a['battery_lid_design']=dict(type='full_length_side_grooves_and_one_screw',screw='M3x12 + M3 nut, retained location0',release_translation_box_mm=[0,-108,0],module_lift_mm=90,lid_installed_z_mm=[49,52],base_and_pack_origins='unchanged',floor='unchanged',tool_opening_mm=8,rail_length_mm=107.4,side_groove_depth_mm=1.2,clearance_mm=.3)
b=copy.deepcopy(a);b['name']='service';b['items']=[it for it in b['items'] if it['label'] not in ['lid_keepout','tx_top_keepout']]
for it in b['items']:
 if it['label'] in a['moving_labels']:it['ops'].insert(0,{'translate':a['service_translation_mm']})
(O/'placement.json').write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'service_placement.json').write_text(json.dumps(b,ensure_ascii=False,indent=2),encoding='utf-8')
def asmexport(name,ss):
 doc=A.newDocument(name)
 for k,s in ss.items():ob=doc.addObject('PartDesign::Feature',k);ob.Label=k;ob.Shape=s
 Import.export(doc.Objects,str(O/(name+'.step')));A.closeDocument(doc.Name)
asmexport('closed',shapes)
service={it['label']:transform(Part.read(str(R/it['part']/(it.get('file',Path(it['part']).name)+'.step'))),it['ops']) for it in b['items']}
asmexport('service',service)
(O/'hole_sources.json').write_text(json.dumps(dict(MAIN=mh,PWR=ph,TX=th,SONY=sh,derived_from_kicad=True),indent=2),encoding='utf-8')
(O/'edge_finishing.json').write_text(json.dumps(edge_finishing,indent=2),encoding='utf-8')
print('Built current switch/TX clearance assembly; run access and interference verifiers.',flush=True)
