"""Build the horizontal child frame; placement.json is the assembly authority.

Shared SCAD interfaces own dimensions. Original official CAD and old optimised
parts are read only. Actual meshes, screw paths and hand access are checked.
"""
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import ast, hashlib, json, os, re, subprocess, sys
import numpy as np
import trimesh
from clean_stl_degenerates import clean
from weld_small_stl_faces import weld

ROOT=Path(__file__).resolve().parents[1]
NAME='child_horizontal_plate_frame'
PART=ROOT/f'parts/child/exterior/printed/{NAME}'
CLAMP=ROOT/'parts/child/exterior/printed/child_wte4_petg_clamp'
OUT=ROOT/f'assemblies/{NAME}'
OSC=Path('C:/Program Files/OpenSCAD/openscad.exe')
SCREW='parts/common/interior/cots/screw'
FRAME_VARIANTS=['side','bottom','top','ballast_cap','guard_front','guard_rear','guard_front_inner','guard_rear_inner','rotation_key','clamp_support']
CLAMP_VARIANTS=['upper_linked','lower_linked']
PRINTED_FRAME_VARIANTS={'side','bottom'}
PRINTED_CLAMP_VARIANTS=set(CLAMP_VARIANTS)
PRINTED_RECORD=OUT/'_work/analysis/open_nut_fastening/printed_baseline.json'

def printed_baseline():
    """Lock printed stock once; never replace its mesh or numerical geometry."""
    paths=[PART/f'{NAME}_{v}.stl' for v in sorted(PRINTED_FRAME_VARIANTS)]
    paths += [CLAMP/f'child_wte4_petg_clamp_{v}.stl' for v in sorted(PRINTED_CLAMP_VARIANTS)]
    current={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    if not PRINTED_RECORD.exists():
        save(PRINTED_RECORD,dict(confirmed_date='2026-10-11',source='User: clamps, bottom and side frames already printed',sha256=current))
    expected=json.loads(PRINTED_RECORD.read_text(encoding='utf-8'))['sha256']
    if current!=expected: raise RuntimeError('Already printed source meshes changed; inspect printed_baseline.json')
    return current

def verify_printed_render(original,candidate):
    """Recertify unchanged legacy branches after edits to a shared SCAD source.

    Render to a separate file, compare the complete geometry and retain original
    bytes. Only after proof do we refresh its build timestamp for packaging.
    """
    from scipy.spatial import cKDTree
    weld(candidate,candidate.with_suffix('.sliver.json'))
    clean(candidate,candidate.with_suffix('.degeneracy.json'),binary=True)
    a=trimesh.load(original,force='mesh');b=trimesh.load(candidate,force='mesh')
    error=max(float(cKDTree(x.vertices).query(y.vertices)[0].max()) for x,y in [(a,b),(b,a)])
    report=dict(original=original.relative_to(ROOT).as_posix(),candidate=candidate.relative_to(ROOT).as_posix(),
        bidirectional_vertex_error_mm=error,bounds_error_mm=float(np.abs(a.bounds-b.bounds).max()),
        volume_error_mm3=abs(float(a.volume-b.volume)),candidate_watertight=bool(b.is_volume),
        original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
        candidate_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest())
    if (error>1e-4 or report['bounds_error_mm']>1e-4 or report['volume_error_mm3']>.1
            or not b.is_volume or b.euler_number!=a.euler_number or len(b.split())!=1):
        raise RuntimeError('Current SCAD changed printed stock: '+json.dumps(report))
    # Not a staleness bypass: the separate render just proved the retained STL
    # describes the current source. No mesh bytes or coordinates are modified.
    os.utime(original,None)
    save(candidate.with_suffix('.equivalence.json'),report)
    return report

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def call(command,log):
    result=subprocess.run([str(x) for x in command],capture_output=True,text=True,
                          encoding='utf-8',errors='replace')
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(result.stdout+result.stderr,encoding='utf-8')
    if result.returncode or re.search(r'\b(?:ERROR|WARNING):',result.stdout+result.stderr):
        raise RuntimeError(f'Build failed; see {log}')
    return result.stdout+result.stderr

def matrix(ops):
    total=np.eye(4)
    for operation in ops:
        for kind,values in operation.items():
            if kind=='translate': transform=trimesh.transformations.translation_matrix(values)
            elif kind=='rotate': transform=trimesh.transformations.euler_matrix(*np.radians(values))
            elif kind=='mirror':
                normal=np.asarray(values,dtype=float);transform=np.eye(4)
                transform[:3,:3]-=2*np.outer(normal,normal)/(normal@normal)
            else: raise ValueError(kind)
            total=total@transform
    return total

def build():
    locked=printed_baseline()
    logs=OUT/'_work/logs'; work=OUT/'_work/intermediate';work.mkdir(parents=True,exist_ok=True)
    if '--reuse-interfaces' in sys.argv:
        for relative in ['guards/vendor_profile.json','ballast_mount/reference.json']:
            cached=json.loads((OUT/'_work/analysis'/relative).read_text(encoding='utf-8'))
            if hashlib.sha256((ROOT/cached['source']).read_bytes()).hexdigest()!=cached['sha256']:
                raise RuntimeError('Vendor CAD changed; remove --reuse-interfaces: '+cached['source'])
    if '--reuse' not in sys.argv and '--reuse-interfaces' not in sys.argv:
        result=call(['C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/FreeCADCmd.exe',
                     ROOT/'tools/measure_child_horizontal_guard_interfaces.py'],logs/'guard_profile.log')
        if 'GUARD_PROFILE_EXTRACTED' not in result: raise RuntimeError('Vendor profile extraction incomplete')
        result=call(['C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/FreeCADCmd.exe',
                     ROOT/'tools/measure_ballast_plate_b_interface.py'],logs/'ballast_interface.log')
        if 'BALLAST_B_INTERFACE_PASS' not in result: raise RuntimeError('Ballast interface extraction incomplete')
    source=PART/f'{NAME}.scad'
    result=call([OSC,'-o',work/'layout.csg',source],logs/'layout.log')
    line=next(x for x in result.splitlines() if x.startswith('ECHO: ["LAYOUT"'))
    _,width,length,height,side_t,bottom_t,top_t,vessel_z,vessel_length,top_z,lower_z,ballast_z=ast.literal_eval(line[6:])
    line=next(x for x in result.splitlines() if x.startswith('ECHO: ["INTERFACES"'))
    p=dict(ast.literal_eval(line[6:])[1:])
    access_line=next(x for x in result.splitlines() if x.startswith('ECHO: ["TOP_CLAMP_ACCESS"'))
    _,access_d,access_chamfer,access_land,access_sides,driver_d,driver_length=ast.literal_eval(access_line[6:])
    builds=[(folder,base,variant) for folder,base,variants in
            [(PART,NAME,FRAME_VARIANTS),
             (CLAMP,'child_wte4_petg_clamp',CLAMP_VARIANTS)] for variant in variants]
    if '--reuse' not in sys.argv:
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures=[]
            for folder,base,variant in builds:
                if (folder==PART and variant in PRINTED_FRAME_VARIANTS or
                        folder==CLAMP and variant in PRINTED_CLAMP_VARIANTS):
                    stem=f'{base}_{variant}'
                    candidate=work/'printed_source_verification'/f'{stem}.stl'
                    candidate.parent.mkdir(parents=True,exist_ok=True)
                    futures.append((stem,pool.submit(call,[OSC,'--export-format','binstl','-D',
                        f'part="{variant}"','-o',candidate,folder/f'{base}.scad'],
                        logs/f'{stem}_printed_verification_render.log'),folder/f'{stem}.stl',candidate))
                    continue
                stem=f'{base}_{variant}'
                futures.append((stem,pool.submit(call,[OSC,'--export-format','binstl','-D',
                    f'part="{variant}"','-o',folder/f'{stem}.stl',folder/f'{base}.scad'],
                    logs/f'{stem}_render.log'),None,None))
            equivalence=[]
            for stem,future,original,candidate in futures:
                future.result()
                if original:
                    equivalence.append(verify_printed_render(original,candidate))
                    print('Verified and preserved printed stock',stem,flush=True)
                else: print('Rendered',stem,flush=True)
            save(OUT/'_work/analysis/open_nut_fastening/printed_source_equivalence.json',
                 dict(result='PASS',parts=equivalence,
                      note='Current SCAD separately rendered; retained STL bytes and shape unchanged after equivalence proof.'))
    reports={}
    for folder,base,variants in [(PART,NAME,FRAME_VARIANTS),
                                 (CLAMP,'child_wte4_petg_clamp',CLAMP_VARIANTS)]:
        for variant in variants:
            stem=f'{base}_{variant}'; target=folder/f'{stem}.stl'
            # --reuse is only for inspection after successful source rendering.
            # Binary STL collapses a few coplanar triangulation edges to zero
            # area. Repair triangulation only, with the existing fidelity audit.
            preserved=target.relative_to(ROOT).as_posix() in locked
            sliver_cleanup=None if preserved else weld(target,folder/'_work/analysis'/f'{stem}-local-sliver-weld.json')
            cleanup=None if preserved else clean(target,folder/'_work/analysis'/f'{stem}-degeneracy.json',binary=True)
            mesh=trimesh.load(target,force='mesh')
            if not mesh.is_watertight or not mesh.is_winding_consistent or len(mesh.split())!=1:
                raise RuntimeError(f'Invalid connected mesh: {stem}')
            # Print packaging lowers each verified part to the bed.
            if max(mesh.extents[:2]+10)>256 or mesh.extents[2]>256:
                raise RuntimeError(f'X1C envelope exceeded: {stem}, {mesh.extents}')
            reports[stem]={'dimensions_mm':mesh.extents.tolist(),'volume_mm3':float(mesh.volume),
                'watertight':True,'connected_components':1,'euler_number':int(mesh.euler_number),
                'zero_area_triangles':int(np.count_nonzero(mesh.area_faces<1e-12)),
                'numerical_cleanup':cleanup,
                'local_sliver_cleanup':sliver_cleanup,
                'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    items=[]
    def item(label,folder,file,group,ops,color,printed=False,**extra):
        row=dict(label=label,part=folder,file=file,group=group,ops=ops,color=color,print=printed)
        row.update(extra);items.append(row)
    path=PART.relative_to(ROOT).as_posix();cp=CLAMP.relative_to(ROOT).as_posix()
    left=[{'translate':[-width/2,0,height/2]},{'rotate':[90,0,90]}]
    item('left_side_frame',path,NAME+'_side','frame',left,'SteelBlue',True)
    item('right_side_frame',path,NAME+'_side','frame',[{'rotate':[0,0,180]}]+left,'SteelBlue',True,
         note='Proper rigid rotation; symmetric stations allow the same printed part x2.')
    guard_pose=[{'translate':[-width/2+side_t,0,vessel_z]},{'rotate':[90,0,90]}]
    for end in ['front','rear']:
        for side in ['left','right']:
            ops=guard_pose if side=='left' else [{'mirror':[1,0,0]}]+guard_pose
            item(f'{side}_{end}_guard',path,NAME+'_guard_'+end+'_inner','frame',ops,'SteelBlue',True,
                 role='side_frame_extension',note='Inside side plate, with clearance for top frame and rear key. Right portable STL is reflected.')
    key_pose=[{'translate':[-width/2+side_t,0,vessel_z]},{'rotate':[90,0,90]}]
    for side in ['left','right']:
        ops=key_pose if side=='left' else [{'mirror':[1,0,0]}]+key_pose
        item(f'{side}_rotation_key',path,NAME+'_rotation_key','frame',ops,'DarkOrange',True,
             role='side_bolted_rotation_key',note='Independent receiver, bolted directly to the side frame inside face.')
    item('lowest_ballast_frame',path,NAME+'_bottom','frame',[],'DarkOrange',True)
    item('removable_upper_frame',path,NAME+'_top','frame',[{'translate':[0,0,top_z]}],'CadetBlue',True)
    for s,side in [(-1,'left'),(1,'right')]:
        for station in p['stations']:
            local_station=station if s==-1 else -station
            ops=[{'translate':[-width/2+side_t,local_station-p['cross_depth']/2,lower_z]},
                 {'rotate':[-90,0,0]}]
            if s==1: ops=[{'rotate':[0,0,180]}]+ops
            item(f'{side}_clamp_support_{station}',path,NAME+'_clamp_support','frame',ops,'DarkOrange',True,
                 role='detachable_clamp_support',note='Same bracket x4, proper rotation for right side; four M3x25 bolts with exposed free nuts and two washers each.')
    for half in ['upper','lower']:
        axial_origin=(max(p['stations'])+p['band_width']/2 if half=='upper'
                      else min(p['stations'])-p['band_width']/2)
        ops=[{'translate':[0,axial_origin,vessel_z]},
             {'rotate':[90 if half=='upper' else -90,0,0]}]
        item(f'clamp_linked_{half}',cp,'child_wte4_petg_clamp_'+half+'_linked','clamp',ops,'LightSlateGray',True,
             note='Both axial stations joined by two shoulder rails; upper/lower remain removable.')
    vertical=json.loads((ROOT/'assemblies/child_vertical_assembly/placement.json').read_text(encoding='utf-8-sig'))
    for row in vertical['items']:
        if row.get('group')!='vessel': continue
        row=deepcopy(row)
        if row['label']=='end_cap_bottom':
            row['ops'][0]['translate'][2]=p['endcap_anchor_z']
            row['note']='Horizontal assembly only: STEP shoulder gives outer face Y=-114, removing old nominal 0.2 mm axial overlap.'
        row['ops']=[{'translate':[0,-vessel_length/2,vessel_z]},{'rotate':[-90,0,0]}]+row.get('ops',[])
        row['print']=False;items.append(row)
    inv=json.loads((ROOT/'parts/common/exterior/cots/ballast_inventory.json').read_text(encoding='utf-8'))
    weights={row['name']:row for row in inv['items']}
    for x in p['ballast_x']:
        weight=weights['おもりC']
        item(f'ballast_C_{x}',weight['part'],Path(weight['mesh_file']).stem,'ballast',
             [{'translate':[x,-p['ballast_length']/2,ballast_z]},{'rotate':[-90,0,0]}],'DimGray',mass_g=weight['mass_g'])
        for y in p['ballast_y']:
            item(f'ballast_cap_{x}_{y}',path,NAME+'_ballast_cap','ballast_cap',
                 [{'translate':[x,y+p['ballast_band_width']/2,ballast_z]},{'rotate':[90,0,0]}],'DarkOrange',True)
    for index,y in enumerate(p['plate_y']):
        weight=weights['おもりB']
        item(f'ballast_plate_{index+1}',weight['part'],Path(weight['mesh_file']).stem,'ballast',
             [{'translate':[0,y,bottom_t]}],'DimGray',mass_g=weight['mass_g'])
    joints=[]
    def fastener(label,seat,rotation,length,nut_start,nut_rotation,size=3,exposed=False):
        ops=[{'translate':seat},{'rotate':rotation}]
        item(label+'_screw',SCREW,f'screw_m{size}x{length}','fasteners',ops,'Silver')
        item(label+'_washer',SCREW,'screw_washer_m3_05' if size==3 else 'screw_washer_m5_10x1','fasteners',
             ops+[{'translate':[0,0,-(0.5 if size==3 else p['plate_washer_t'])]}],'Silver')
        item(label+'_nut',SCREW,'screw_nut_m3' if size==3 else 'screw_nut_m5_4','fasteners',
             [{'translate':nut_start},{'rotate':nut_rotation},{'rotate':[0,0,30]}],'Silver')
        if exposed:
            item(label+'_nut_washer',SCREW,'screw_washer_m3_05','fasteners',
                 [{'translate':nut_start},{'rotate':nut_rotation},{'translate':[0,0,-0.5]}],'Silver')
        joints.append(dict(label=label,seat_mm=seat,axis_rotation_deg=rotation,length_mm=length,
                           nut_start_mm=nut_start,nut_rotation_deg=nut_rotation,nominal_diameter_mm=size,
                           exposed_nut=exposed))
    for station in p['stations']:
        for x in p['mount_x']:
            for dy in p['mount_axial']:
                fastener(f'mount_upper_{station}_{x}_{dy}',[x,station+dy,top_z+top_t+0.5],
                         [0,0,0],p['upper_screw_l'],[x,station+dy,vessel_z+p['mount_nut_r']],[0,0,0])
                fastener(f'mount_lower_{station}_{x}_{dy}',[x,station+dy,lower_z-p['arm_t']-0.5],
                         [180,0,0],p['lower_screw_l'],[x,station+dy,vessel_z-p['mount_nut_r']],[180,0,0])
        for x,dy in p['ear_rows']:
            fastener(f'clamp_join_{station}_{x}_{dy}',[x,station+dy,vessel_z+p['ear_height']+0.5],
                     [0,0,0],p['clamp_screw_l'],[x,station+dy,vessel_z-(p['ear_height']-p['nut_t'])-2.4],[0,0,0])
    for s in [-1,1]:
        for y in p['joint_y']:
            for z in [p['lower_joint_z'],top_z+top_t/2]:
                exposed=z!=p['lower_joint_z']
                fastener(f'frame_join_{s}_{y}_{z}',[s*(width/2+0.5),y,z],[0,s*90,0],
                         p['top_frame_screw_l'] if exposed else p['frame_screw_l'],
                         [s*(width/2-side_t-p['joint_inset']-(0.5 if exposed else 0)),y,z],
                         [0,-s*90,0] if exposed else [0,s*90,0],exposed=exposed)
    for x in p['ballast_x']:
        for y in p['ballast_y']:
            for s in [-1,1]:
                fastener(f'ballast_join_{x}_{y}_{s}',[x+s*p['ballast_bolt_offset'],y,ballast_z+p['split_gap']/2+p['ballast_ear_h']+0.5],
                         [0,0,0],p['ballast_screw_l'],[x+s*p['ballast_bolt_offset'],y,p['ballast_nut_z']],[0,0,0])
    for s in [-1,1]:
        for y in p['guard_joint_y']:
            for z in p['guard_joint_z']:
                fastener(f'guard_join_{s}_{y}_{z}',[s*(width/2+0.5),y,z],[0,s*90,0],p['guard_screw_l'],
                         [s*(width/2-side_t-p['guard_t']-0.5),y,z],[0,-s*90,0],exposed=True)
    for y in p['plate_y']:
        for x in p['plate_hole_x']:
            fastener(f'plate_mount_{x}_{y}',[x,y,bottom_t+p['plate_t']+p['plate_washer_t']],
                     [0,0,0],p['plate_screw_l'],[x,y,p['plate_nut_base']],[0,0,0],size=5)
    for s in [-1,1]:
        for z in p['key_mount_z']:
            fastener(f'key_join_{s}_{z}',[s*(width/2+0.5),p['key_mount_y'],z],
                     [0,s*90,0],p['key_screw_l'],
                     [s*(width/2-side_t-p['key_mount_t']-0.5),p['key_mount_y'],z],
                     [0,-s*90,0],exposed=True)
    for s in [-1,1]:
        for station in p['stations']:
            for dy in p['support_joint_axial']:
                for z in p['support_joint_z']:
                    fastener(f'support_join_{s}_{station}_{dy}_{z}',
                        [s*(width/2+0.5),station+dy,z],[0,s*90,0],p['support_screw_l'],
                        [s*(width/2-side_t-p['support_foot_t']-0.5),station+dy,z],[0,-s*90,0],exposed=True)
    accessory_positions=([[y,z] for y in p['accessory_y'] for z in p['accessory_z']]+
                         [[y,z] for y in p['accessory_column_y'] for z in p['accessory_column_z']])
    placement=dict(name=NAME,status='fit_prototype',coordinate_system='mm. X=左右 Y=容器軸 +Y=ドーム Z=上',
        note='X1 Carbon / PETG Basic。主フレーム4枚。公式4インチの取合いに基づく新規クランプ。',
        groups={g:True for g in ['frame','clamp','vessel','ballast','ballast_cap','fasteners']},
        dimensions_mm=dict(width=width,length=length,height=height,side_thickness=side_t,
                           bottom_thickness=bottom_t,top_thickness=top_t,tube_center_z=vessel_z,
                           tube_length=vessel_length,ballast_center_z=ballast_z,
                           protected_overall_width=width,
                           protected_overall_length=p['guard_front_tip']-p['guard_rear_tip']),
        main_frame_count=4,items=items,fastener_joints=joints,
        top_clamp_access=dict(date='2026-10-12',bore_inscribed_diameter_mm=access_d,
            bore_sides=access_sides,entrance_chamfer_mm=access_chamfer,
            nominal_radial_land_mm=access_land,driver_diameter_mm=driver_d,
            driver_length_mm=driver_length,
            hole_centres_xy_mm=[j['seat_mm'][:2] for j in joints if j['label'].startswith('clamp_join_')],
            note='Six vertical service bores for the existing clamp tightening screws; preserve all mounting holes. Driver envelope is provisional.'),
        side_extension_count=4,
        rotation_key_count=2,
        print_progress=dict(confirmed_date='2026-10-11',already_printed=['side','bottom','upper_linked','lower_linked'],
                            remaining_instances=15,source_mesh_sha256=locked),
        fastening_revision=dict(date='2026-10-11',new_hole_shape='circumscribed regular octagon',
            new_hole_inscribed_diameter_mm=3.5,new_hole_sides=p['new_hole_sides'],
            nut_access_width_mm=p['open_nut_access_w'],nut_access_depth_mm=p['open_nut_access_depth'],
            note='Unprinted parts: exposed free nuts with open spanner access and through shafts; printed stock preserves legacy pockets.'),
        clamp_support=dict(count=4,fastener='M3x25',bolts_per_bracket=4,
            mounting_foot_thickness_mm=p['support_foot_t'],foot_bottom_z_mm=p['support_bottom'],
            joint_z_mm=p['support_joint_z'],joint_axial_offsets_mm=p['support_joint_axial'],
            width_mm=p['cross_depth'],lower_clamp_plane_z_mm=lower_z,
            lower_clamp_hole_x_mm=p['mount_x'],lower_clamp_hole_axial_offsets_mm=p['mount_axial'],
            note='Exposed nuts and nut-side washers at the full 8 mm foot; open axial-edge spanner relief, through shaft, M3x25/30 checked.'),
        attachment_interface=dict(fastener='M3',clearance_diameter_mm=3.5,nut_pocket_af_mm=5.8,
            nut_pocket_depth_mm=p['nut_t'],pitch_mm=20,holes_per_side=len(accessory_positions),
            hole_centres_yz_mm=accessory_positions,side_faces_x_mm=[-width/2,width/2],
            note='Outside attachment, ordinary M3 nut inserted from inside; choose screw length for actual attachment thickness.'),
        clamp_connection=dict(stations_mm=p['stations'],printed_halves=2,
            rails_per_half=2,rail_width_mm=p['link_width'],rail_thickness_mm=p['link_t'],
            root_chamfer_mm=p['link_root'],shoulder_angle_deg=p['link_angle']),
        protection=dict(front_tip_y=p['guard_front_tip'],rear_tip_y=p['guard_rear_tip'],
            side_extensions_mount='inside',side_extension_x_bounds_mm=[[-width/2+side_t,-width/2+side_t+p['guard_t']],
                [width/2-side_t-p['guard_t'],width/2-side_t]],
            cap_outer_y=p['endcap_outer_y'],cable_reserved_length_mm=p['cable_length'],
            cable_reserved_diameter_mm=p['cable_d'],key_clearance_mm=p['key_clearance'],
            rotation_key='Both existing end-cap tabs; independent open-top receivers bolted directly to the side frames',
            key_fastener_count=4,key_fastener='M3x25',key_mount_y_mm=p['key_mount_y'],
            key_mount_z_mm=p['key_mount_z'],key_mount_thickness_mm=p['key_mount_t'],
            symmetry='180 degree reversal is not rejected; align the documented cap hole pattern at assembly'),
        ballast=dict(cylindrical_C_count=2,plate_positions=4,example_A_count=0,example_B_count=4,
                     plate_hole_x_mm=p['plate_hole_x'],plate_fastener_count=16,
                     mass_g=sum(row.get('mass_g',0) for row in items),mass_source='ballast_inventory.json'),
        purchased_consumables=[dict(name='クランプ内面EPDM',thickness_mm_provisional=1,quantity=4),
                               dict(name='C受け保護材',thickness_mm_provisional=0.8,quantity=8)],
        access_reservations=[dict(label='left_hand',bounds_mm=[[-110,-40,174],[-75,40,204]]),
                             dict(label='right_hand',bounds_mm=[[75,-40,174],[110,40,204]]),
                             dict(label='rear_cable',shape='cylinder',diameter_mm=p['cable_d'],length_mm=p['cable_length'],
                                  centre_mm=[0,p['endcap_outer_y']-p['cable_length']/2,vessel_z],rotation_deg=[90,0,0])],
        unresolved=['実PETGの締付/クリープ・手持ち荷重試験','保護材とM5固定穴・ナット実物の嵌合',
                    '実ドームとペネトレータ配線・曲げ半径','横置き内装保持・浮力と重心'])
    save(OUT/'placement.json',placement)
    save(OUT/'print_config.json',dict(status='fit_prototype',supports='none',note='X1 Carbon / Bambu PETG Basic、0.2 mm、8周、100%インフィル、5 mmブリム、サポートなし（無効）。2026-10-11：側板2・底板1・クランプ上下各1は印刷済み、再印刷不要（形状とSHA保持）。残りは上部1・前後延長左右各1（計4）・回転止め左右各1（計2）・支持治具4・C押さえ4＝15個。下表は組立総数20個。回転止めは広い底面をベッドへ向けるようSTLを回転済み、スライサ上で寝かせ直さない。支持治具は広いガセット面をベッドへ、開放部のブリッジ幅8 mm。未印刷部品のM3穴は内接円径3.5 mmの八角形。支持治具と回転止めはM3×25、上部の板接合はM3×30、ナット側にも0.5 mmワッシャ。埋込み六角ナット溝を廃止し開放部でナットを工具保持する。印刷済み部品の既存ナット受けは残る。嵌合・荷重試験用。',
         notes=[str((PART/'README.md').relative_to(ROOT)).replace('\\','/'),str((CLAMP/'README.md').relative_to(ROOT)).replace('\\','/')]))
    call(['python',ROOT/'scad/lib/asm_gen.py',OUT/'placement.json',OUT/f'{NAME}_view.scad'],logs/'view_generation.log')
    validate(placement,reports,p)
    printed_baseline()
    draw(placement)
    print(json.dumps(dict(source_variants=len(reports),main_frames=4,side_extensions=4,printed_count=sum(r['print'] for r in items),items=len(items),ballast_g=placement['ballast']['mass_g']),ensure_ascii=False))

def load_world(placement):
    rows=[]
    for item in placement['items']:
        mesh=trimesh.load(ROOT/item['part']/(item['file']+'.stl'),force='mesh')
        mesh.apply_transform(matrix(item.get('ops',[])));rows.append((item,mesh))
    return rows

def overlap(a,b):
    if np.any(a.bounds[0]>=b.bounds[1]) or np.any(b.bounds[0]>=a.bounds[1]): return 0.0
    common=trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
    return 0.0 if common is None or common.is_empty else abs(float(common.volume))

def validate(placement,reports,p):
    world=load_world(placement); structural=[(r,m) for r,m in world if r['group']!='fasteners']
    intersections=[];failures=[]
    for i,(a,am) in enumerate(structural):
        for b,bm in structural[i+1:]:
            # Existing vessel components legitimately overlap at bonded joints.
            if a['group']=='vessel' and b['group']=='vessel': continue
            v=overlap(am,bm)
            intersections.append(dict(a=a['label'],b=b['label'],volume_mm3=v))
            if v>0.1: failures.append(intersections[-1])
    fastener_checks=[]
    exposed_labels={j['label'] for j in placement['fastener_joints'] if j.get('exposed_nut')}
    for row,mesh in world:
        if row['group']!='fasteners': continue
        for target,tm in structural:
            v=overlap(mesh,tm)
            if v>0.1: failures.append(dict(a=row['label'],b=target['label'],volume_mm3=v))
        fastener_checks.append(row['label'])
    hand=[]
    for reservation in placement['access_reservations']:
        if reservation.get('shape')=='cylinder':
            box=trimesh.creation.cylinder(radius=reservation['diameter_mm']/2,height=reservation['length_mm'],sections=96)
            box.apply_transform(matrix([{'translate':reservation['centre_mm']},{'rotate':reservation['rotation_deg']}]))
        else:
            lo,hi=np.array(reservation['bounds_mm']);box=trimesh.creation.box(hi-lo)
            box.apply_translation((lo+hi)/2)
        total=sum(overlap(box,mesh) for row,mesh in world)
        hand.append(dict(label=reservation['label'],intersection_volume_mm3=total))
        if total>0.1: failures.append(hand[-1])
    tool_checks=[]
    nuts=[]
    for row,mesh in world:
        if row['group']!='fasteners': continue
        if row['label'].endswith('_screw'):
            seat=np.array(row['ops'][0]['translate'])
            axis=matrix(row['ops'][1:])[:3,2] # outward from screw seating face
            head_height=np.max((mesh.vertices-seat)@axis)
            lower=row['label'].startswith('mount_lower_')
            c_retainer=row['label'].startswith('ballast_join_')
            upper_service=row['label'].startswith('clamp_join_')
            service=placement.get('top_clamp_access',{})
            tool_length=service['driver_length_mm'] if upper_service else 70 if lower or c_retainer else 35
            tool_diameter=service['driver_diameter_mm'] if upper_service else 8
            tool=trimesh.creation.cylinder(radius=tool_diameter/2,height=tool_length,sections=32)
            pose=matrix(row['ops']);pose[:3,3]=seat+axis*(head_height+0.2+tool_length/2)
            tool.apply_transform(pose)
            # Lower service explicitly removes A/B; fixed C remains installed.
            blocked=[dict(part=r['label'],volume_mm3=overlap(tool,m)) for r,m in world
                     if r['label']!=row['label'] and not (lower and r['label'].startswith('ballast_plate_'))
                     and not (c_retainer and r['group']=='vessel')]
            blocked=[r for r in blocked if r['volume_mm3']>0.1]
            record=dict(screw=row['label'],driver_d_mm=tool_diameter,driver_length_mm=tool_length,
                        plates_removed=lower,vessel_removed=c_retainer,blocked=blocked)
            tool_checks.append(record)
            if blocked: failures.append(record)
        if row['label'].endswith('_nut'):
            label=row['label']
            if label.removesuffix('_nut') in exposed_labels and label.startswith('frame_join_'):
                direction=np.array([0,0,1]);distance=20
            elif label.startswith('mount_'):
                dy=float(label.rsplit('_',2)[-2]);direction=np.array([0,np.sign(dy),0]);distance=16
            elif label.startswith('guard_join_'):
                direction=np.array([-np.sign(mesh.centroid[0]),0,0]);distance=20
            elif label.startswith('key_join_'):
                direction=np.array([0,1,0]);distance=20
            elif label.startswith('support_join_'):
                dy=float(label.rsplit('_',3)[-3]);direction=np.array([0,np.sign(dy),0]);distance=16
            elif label.startswith('frame_join_'):
                direction=np.array([0,0,1]);distance=20
            elif label.startswith('ballast_join_'):
                direction=np.array([0,1,0]);distance=16
            else:
                direction=np.array([0,0,-1]);distance=12
            swept=trimesh.convex.convex_hull(np.vstack([mesh.vertices,mesh.vertices+direction*distance]))
            blocked=[dict(part=r['label'],volume_mm3=overlap(swept,m)) for r,m in structural
                     if r['print']]
            blocked=[r for r in blocked if r['volume_mm3']>0.1]
            record=dict(nut=label,insertion_direction=direction.tolist(),travel_mm=distance,blocked=blocked)
            nuts.append(record)
            if blocked: failures.append(record)
    plate_holes=[]
    bottom=next(m for r,m in structural if r['label']=='lowest_ballast_frame')
    for y in p['plate_y']:
        plate=next(m for r,m in structural if r['label'].startswith('ballast_plate_') and abs(m.centroid[1]-y)<.01)
        for x in p['plate_hole_x']:
            probe=trimesh.creation.cylinder(radius=2.5,height=p['plate_t']+8,sections=48)
            probe.apply_translation([x,y,(p['plate_t']+8)/2])
            total=overlap(probe,bottom)+overlap(probe,plate)
            record=dict(position_mm=[x,y],nominal_fastener_mm=5,intersection_mm3=total)
            plate_holes.append(record)
            if total>.1:failures.append(record)
    result=dict(status='fit_prototype',meshes=reports,pair_intersections=intersections,
                fastener_paths_checked=len(fastener_checks),access_boxes=hand,failures=failures,
                driver_paths=tool_checks,nut_insertion_paths=nuts,plate_mount_holes=plate_holes,
                not_certified=['material strength and creep','retention pull/load tests','actual cable routes'])
    save(OUT/'_work/analysis/layout/validation.json',result)
    if failures:
        print(json.dumps(failures,indent=2));raise RuntimeError('Assembly intersections; inspect validation.json')

def draw(placement):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    plt.rcParams['font.family']='Yu Gothic'
    fig=plt.figure(figsize=(15,9),facecolor='#f4f3ef')
    ax=fig.add_axes([.02,.12,.63,.74],projection='3d',facecolor='#f4f3ef')
    world=load_world(placement)
    colors=dict(frame='#46839a',clamp='#8797a1',vessel='#b5d6dd',ballast='#4b525c',ballast_cap='#d19043')
    for row,mesh in world:
        if row['group']=='fasteners': continue
        color='#d19043' if row['label']=='lowest_ballast_frame' else colors[row['group']]
        # Decimation is for the display only; verification uses the complete mesh.
        if len(mesh.faces)>20000:
            try: mesh=mesh.simplify_quadric_decimation(face_count=20000)
            except (ImportError,ModuleNotFoundError): pass
        alpha=.2 if row['label']=='acrylic_tube_200' else .7 if row['group']=='vessel' else 1
        ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolor=color,edgecolor='none',alpha=alpha,rasterized=True))
    ax.set_xlim(-140,140);ax.set_ylim(-190,190);ax.set_zlim(0,245)
    ax.set_box_aspect([280,380,245]);ax.view_init(elev=24,azim=38);ax.set_axis_off()
    fig.text(.05,.93,'子機筐体  /  横向きWTE4・4枚フレーム',fontsize=24,weight='bold',color='#29464f')
    fig.text(.05,.875,'X1 Carbon  /  Bambu PETG Basic  /  内側保護枠を含む外形244 × 350 × 230 mm',fontsize=12,color='#5b6b73')
    fig.text(.67,.77,'容器の固定',fontsize=17,weight='bold',color='#29464f')
    fig.text(.67,.63,'前後クランプを左右の肩の材で連結\n上側：上部フレームへねじ止め\n下側：独立支持治具4個へねじ止め\n治具はM3×25・開放ナット各4組',fontsize=12,linespacing=1.7,color='#5b6b73')
    fig.text(.67,.51,'バラストと持ち手',fontsize=17,weight='bold',color='#29464f')
    fig.text(.67,.36,'C ×2：胴部をねじ式押さえで固定\nB：4か所・各4本のM5ねじ\n例：C ×2 + B ×4 = 2.24 kg\n左右に90 ×34 mmの持ち手開口',fontsize=12,linespacing=1.7,color='#5b6b73')
    fig.text(.67,.24,'主4枚 + 延長4 + 回転止め2\n+ 支持治具4 + クランプ2 + 押さえ4\n合計20個 / 治具は同じSTLを4個\n追加取付用：M3穴22か所/側',fontsize=12,color='#5b6b73',linespacing=1.7)
    fig.text(.05,.075,'嵌合・荷重試験用モデル  /  fit_prototype',fontsize=12,color='#af702e',weight='bold')
    fig.text(.05,.037,'保護材・Bの穴径は仮寸法。実機の持ち運び荷重、締付け、PETGのクリープ、実配線は追加確認が必要。',fontsize=10,color='#657078')
    image_dir=OUT/'_work/images';image_dir.mkdir(parents=True,exist_ok=True)
    fig.savefig(image_dir/'four_plate_layout.png',dpi=140);plt.close(fig)

if __name__=='__main__': build()
