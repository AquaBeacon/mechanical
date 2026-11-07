"""Read-only electronics placement study; no manufacturing geometry is generated."""
from pathlib import Path
import json,sys
import FreeCAD as A
import Part

LABELS = ['plate','p_main','p_pwr','main_mount_plate','gnss_universal_carrier',
          'tx_improved','spresense','lipo','lipo_tray','lipo_ret_lid',
          'box_bcas212310g','lid_keepout','gnss_receiver','gnss_sma_plug',
          'gnss_pin_headers','gnss_universal_pcb','gnss_xh_keepout',
          'antenna_ground_plate','gnss_antenna','coax_coil_keepout','coax_ring','magnetometer','sony_mount_plate']

def build(doc, parameters):
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
    if 'retrofit' in config:
        # This study applies deltas to the pre-retrofit assembly. Snapshot this
        # baseline as a native-job dependency when replaying after publication.
        baseline=root/'assemblies/parent_hand_service/_work/analysis/retrofit_20261024/placement_before_retrofit.json'
        assert baseline.exists(), 'Include placement_before_retrofit.json in replay dependencies'
        config=json.loads(baseline.read_text(encoding='utf-8'))
    scene = {}
    main_lift = parameters.get('main_lift', 3)
    pwr_lift = parameters.get('pwr_lift', 5.5)
    pwr_south = parameters.get('pwr_south', 11)
    sensor_lift = parameters.get('sensor_lift', 16)
    ant_lift = parameters.get('ant_lift', 8.8)
    ant_south = parameters.get('ant_south', 12)
    def bb(s):
        b=s.BoundBox
        return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
    for row in config['items']:
        name=row['label']
        if name not in LABELS: continue
        folder=root/row['part']
        s=Part.read(str(folder/(row.get('file',folder.name)+'.step')))
        for op in reversed(row.get('ops',[])):
            if 'rotate' in op:
                for axis,angle in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],op['rotate']):
                    s.rotate(A.Vector(),axis,angle)
            if 'translate' in op: s.translate(A.Vector(*op['translate']))
        if name=='p_pwr':
            s.translate(A.Vector(0,-pwr_south,pwr_lift))
        elif name in ['p_main','main_mount_plate']: s.translate(A.Vector(0,0,main_lift))
        elif name in ['gnss_universal_carrier','gnss_receiver','gnss_sma_plug','gnss_pin_headers','gnss_universal_pcb','gnss_xh_keepout','magnetometer']:
            s.translate(A.Vector(0,0,sensor_lift))
        elif name in ['antenna_ground_plate','gnss_antenna']: s.translate(A.Vector(0,-ant_south,ant_lift))
        scene[name]=s
        print('Loaded '+name,flush=True)
    if parameters.get('candidate_parts',0):
        sys.path.insert(0,str(root/'scad/lib'))
        import parent_gnss as G
        from parent_service_retrofit import main_antenna_cradle,power_adapter,fixed_sensor_columns,retrofit_fasteners,hex_tool,ring_service,cable_routes,MAIN_LIFT,ANT_LIFT,spacer_threads
        assert main_lift==MAIN_LIFT and ant_lift==ANT_LIFT and sensor_lift==16 and pwr_lift==5.5 and pwr_south==11
        data=json.loads((root/'assemblies/parent_hand_service/_work/analysis/retrofit_20261024/interfaces.json').read_text(encoding='utf-8'))
        scene['main_mount_plate']=main_antenna_cradle([[18+x,112-y] for x,y in data['PARENT_MAIN']['holes'].values()],G)
        scene.update({n:s for n,s in main_antenna_cradle([[18+x,112-y] for x,y in data['PARENT_MAIN']['holes'].values()],G,True).items() if n.startswith('cradle_floor_foot_')})
        scene['power_adapter']=power_adapter([[25.8+y,115+x] for x,y in data['PARENT_PWR']['holes'].values()],pwr_lift,pwr_south)
        columns=fixed_sensor_columns(G,parameters['pcb_holes']['TX_improved'])
        scene.update(columns)
        from parent_corner_mounts import sony_shapes,sony_holes
        scene['sony_mount_plate']=sony_shapes(sony_holes(G),G)['sony_mount_plate']
        scene['spresense'].translate(A.Vector(0,0,G.SONY_BOARD_LIFT))
        scene['coax_ring']=ring_service(scene['coax_ring'],world=True)
        scene.update(cable_routes(G))
        if parameters.get('service_check',0):
            scene['p_main']=Part.makeCompound([scene['p_main'],Part.makeBox(22,54.6,18,A.Vector(28.11,24.23,46.6))])
            from parent_retrofit_service_check import verify
            return verify(doc,scene)
        hardware=retrofit_fasteners(G,[[18+x,112-y] for x,y in data['PARENT_MAIN']['holes'].values()],[[25.8+y,115+x] for x,y in data['PARENT_PWR']['holes'].values()])
        for row in hardware:
            x,y=row['xy'];z=row['head_z'];d=row['diameter'];direction=row['direction'];length=row['length']
            shaft=Part.makeCylinder(d/2,length,A.Vector(x,y,z),A.Vector(0,0,direction))
            head=Part.makeCylinder(2.75 if d==3 else 3.5,3 if d==3 else 4,A.Vector(x,y,z),A.Vector(0,0,-direction))
            pieces=[shaft,head]
            if row['nut_z'] is not None:
                nz=row['nut_z'];h=2.4 if d==3 else 3.2
                pieces.append(hex_tool(x,y,nz,5.5 if d==3 else 7,h).cut(Part.makeCylinder(d/2,h+.2,A.Vector(x,y,nz-.1))))
            if row['washer']:pieces.append(Part.makeCylinder(3.5,.5,A.Vector(x,y,8.34)).cut(Part.makeCylinder(1.6,.7,A.Vector(x,y,8.24))))
            scene['hardware_'+row['label']]=Part.makeCompound(pieces)
    # Actual RTC model bounding box plus user-requested +10 mm above its top.
    scene['rtc_service_reserve']=Part.makeBox(42,22,20,A.Vector(58,82.3,52.095+main_lift))
    # XT30 body front plane from imported STEP. 20 mm depth; 2 mm lateral/vertical allowance.
    for name,x in [('xt_bat_20mm',42.3),('xt_tx_20mm',76.3)]:
        plug=Part.makeBox(17.4,20,9.2,A.Vector(x-8.7,95.849125,27.895))
        plug.translate(A.Vector(0,-pwr_south,pwr_lift))
        scene[name]=plug
    # Approach from west at lever height; assumptions explicit in report.
    for name,x,y in [('switch_pwr_side',33.26,199.54-pwr_south),('switch_tx_side',63.34,130.46-pwr_south)]:
        scene[name]=Part.makeCylinder(6,x-10,A.Vector(10,y,parameters.get('finger_z',56.5)),A.Vector(1,0,0))
    scene['pico_measured_17mm']=Part.makeBox(22,54.6,17,A.Vector(28.11,24.23,46.6))
    scene['pico_extra_1mm']=Part.makeBox(22,54.6,18,A.Vector(28.11,24.23,46.6))
    checks=[]
    solid_cache={}
    def solids(name):
        if name not in solid_cache:
            solid_cache[name]=[(q,q.BoundBox) for q in scene[name].Solids]
        return solid_cache[name]
    def pair(a,b):
        s,t=scene[a],scene[b]
        if not s.BoundBox.intersect(t.BoundBox):
            checks.append({'a':a,'b':b,'volume_mm3':0.0,'bounds_mm':None,'method':'disjoint_bounding_boxes'})
            return
        aa=[q for q,bounds in solids(a) if bounds.intersect(t.BoundBox)]
        tt=[q for q,bounds in solids(b) if bounds.intersect(s.BoundBox)]
        overlap=Part.makeCompound(aa).common(Part.makeCompound(tt)) if aa and tt else Part.Shape()
        # Only intended thread-forming engagement in each PCB's own boss is
        # exempted; independent fastening checks verify the plastic and PCB path.
        for hw in hardware if parameters.get('candidate_parts',0) else []:
            target='main_mount_plate' if hw['label'].startswith('main_pcb_') else 'power_adapter' if hw['label'].startswith('pwr_pcb_') else None
            if a=='hardware_'+hw['label'] and b==target and not overlap.isNull():
                x,y=hw['xy'];tip=hw['head_z']-hw['length'];seat=44.95 if target=='main_mount_plate' else 33.75
                overlap=overlap.cut(Part.makeCylinder(1.501,seat-tip,A.Vector(x,y,tip)))
        # Exempt only intentional thread forming in each PCB's own plastic boss.
        for hw in hardware if parameters.get('candidate_parts',0) else []:
            target='main_mount_plate' if hw['label'].startswith('main_pcb_') else 'power_adapter' if hw['label'].startswith('pwr_pcb_') else None
            if a=='hardware_'+hw['label'] and b==target and not overlap.isNull():
                x,y=hw['xy'];tip=hw['head_z']-hw['length'];seat=44.95 if target=='main_mount_plate' else 33.75
                overlap=overlap.cut(Part.makeCylinder(1.501,seat-tip,A.Vector(x,y,tip)))
        for spec in spacer_threads(G) if parameters.get('candidate_parts',0) else []:
            target='main_mount_plate' if spec['host']=='main_service_frame' else spec['host']
            if a=='hardware_'+spec['label'] and b==target and not overlap.isNull():
                hw=next(r for r in hardware if r['label']==spec['label']);x,y=hw['xy']
                overlap=overlap.cut(Part.makeCylinder(1.501,spec['zhi']-spec['zlo'],A.Vector(x,y,spec['zlo'])))
        volume=0.0 if overlap.isNull() else overlap.Volume
        row={'a':a,'b':b,'volume_mm3':volume,'bounds_mm':bb(overlap) if volume>.001 else None}
        checks.append(row)
        print('CHECK '+json.dumps(row),flush=True)
    for a,b in [('p_main','p_pwr'),('main_mount_plate','p_pwr'),('p_pwr','plate'),
                ('rtc_service_reserve','antenna_ground_plate'),('rtc_service_reserve','gnss_antenna'),
                ('p_main','antenna_ground_plate'),('p_main','gnss_antenna'),
                ('p_pwr','gnss_universal_carrier')]: pair(a,b)
    for a in ['xt_bat_20mm','xt_tx_20mm','switch_pwr_side','switch_tx_side']:
        for b in ['main_mount_plate','p_main','plate','gnss_universal_carrier','gnss_universal_pcb','magnetometer',
                  'coax_ring','coax_coil_keepout','box_bcas212310g']:
            pair(a,b)
    for a in ['p_main','p_pwr','antenna_ground_plate','gnss_antenna','gnss_receiver','gnss_sma_plug','gnss_universal_carrier']:
        for b in ['box_bcas212310g','lid_keepout','lipo','spresense']: pair(a,b)
    if parameters.get('candidate_parts',0):
        for a in ['pico_measured_17mm','pico_extra_1mm']:
            for b in ['main_mount_plate','antenna_ground_plate','gnss_antenna','p_pwr','coax_service_loop','coax_receiver_service','lid_keepout']:pair(a,b)
        for a in ['main_mount_plate','power_adapter']:
            for b in ['p_main','p_pwr','plate','antenna_ground_plate','gnss_antenna','gnss_universal_carrier','lipo','lipo_tray','lipo_ret_lid','spresense','tx_improved','coax_ring','coax_coil_keepout','box_bcas212310g','rtc_service_reserve','xt_bat_20mm','xt_tx_20mm']:
                pair(a,b)
        pair('main_mount_plate','power_adapter')
        for a in ['coax_service_loop','coax_receiver_service']:
            for b in ['p_main','p_pwr','main_mount_plate','power_adapter','coax_ring','antenna_ground_plate','gnss_antenna','gnss_universal_carrier','gnss_universal_pcb','magnetometer','box_bcas212310g','lid_keepout','rtc_service_reserve','switch_pwr_side','switch_tx_side']+list(columns):pair(a,b)
        pair('coax_service_loop','coax_receiver_service')
        for a in columns:
            for b in ['plate','p_pwr','tx_improved','spresense','gnss_universal_carrier','sony_mount_plate','box_bcas212310g','xt_bat_20mm','xt_tx_20mm','switch_pwr_side','switch_tx_side']:
                pair(a,b)
        for row in hardware:
            a='hardware_'+row['label']
            for b in ['main_mount_plate','power_adapter','p_main','p_pwr','sony_mount_plate','spresense','tx_improved','gnss_universal_carrier','gnss_universal_pcb','antenna_ground_plate','coax_ring','box_bcas212310g','lipo_tray','rtc_service_reserve']+list(columns)+[n for n in scene if n.startswith('cradle_floor_foot_')]:
                pair(a,b)
    for target in ['sony_mount_plate','spresense']:
        for other in scene:
            if other!=target and not other.startswith('hardware_'):
                pair(target,other)
    report=dict(status='EXPLORATION_ONLY',parameters=dict(main_lift=main_lift,pwr_lift=pwr_lift,pwr_south=pwr_south,
                    sensor_lift=sensor_lift,ant_lift=ant_lift,ant_south=ant_south),
                bounds={k:bb(s) for k,s in scene.items()},checks=checks,
                limitations=['Support columns, retention and mounting adapters must be designed and verified separately.',
                             'XT mating plug cross-section is provisional: STEP body bounds plus 2 mm.',
                             'Finger approach diameter 12 mm is a design assumption; physical operation unverified.',
                             'Cable routes and assembly removal sweep are not yet verified.'])
    print('LAYOUT_SURVEY='+json.dumps(report),flush=True)
    # Deliberately export only simple, labelled envelopes to keep the review run light.
    out=[]
    for name,s in scene.items():
        b=s.BoundBox
        o=doc.addObject('Part::Feature',name)
        o.Label=name+' [ENVELOPE / NOT PRINTABLE]'
        o.Shape=Part.makeBox(b.XLength,b.YLength,b.ZLength,A.Vector(b.XMin,b.YMin,b.ZMin))
        out.append(o)
    out[0].addProperty('App::PropertyString','LayoutSurvey')
    out[0].LayoutSurvey=json.dumps(report)
    return out
