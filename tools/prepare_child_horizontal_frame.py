"""Derive the horizontal frame interfaces and placement from existing sources.

This does not regenerate either optimised clamp/frame A. Run this, build the new
OpenSCAD part variants, then build_child_horizontal_steps.py in FreeCAD CLI.
"""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
import ast
import hashlib
import json
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_exterior_open_frame'
OUT = ROOT/'assemblies/child_exterior_horizontal'
CLAMP = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
OSC = Path('C:/Program Files/OpenSCAD/openscad.exe')
STEM = PART.name
VARIANTS = ['side_front','side_rear','splice_upper','splice_middle','clamp_link',
            'shoe','cross_half','cross_splice','tray_half','tray_splice','weight_stop',
            'camera_deck','equipment_seat','equipment_riser','equipment_bridge','bumper_half','bumper_splice',
            'foam_reference']


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def interface():
    log=OUT/'_work/logs/clamp_interface.log'
    csg=OUT/'_work/intermediate/clamp_interface.csg'
    for p in [log,csg]:p.parent.mkdir(parents=True,exist_ok=True)
    result=subprocess.run([str(OSC),'-o',str(csg),str(CLAMP/(CLAMP.name+'.scad'))],
                          capture_output=True,text=True,encoding='utf-8',errors='replace')
    log.write_text(result.stdout+result.stderr,encoding='utf-8')
    if result.returncode:raise RuntimeError('Clamp interface export failed')
    found={}
    for line in (result.stdout+result.stderr).splitlines():
        if line.startswith('ECHO: ["CLAMP_INTERFACE"') or line.startswith('ECHO: ["CAGE_INTERFACE"'):
            values=ast.literal_eval(line[6:].strip())
            found[values[0]]=dict(zip(values[1::2],values[2::2]))
    assert set(found)=={'CLAMP_INTERFACE','CAGE_INTERFACE'}
    d,c=found['CLAMP_INTERFACE'],found['CAGE_INTERFACE']
    values={'clamp_mount_y':d['mount_y'],'clamp_shoulder_y':d['shoulder_y'],
            'clamp_frame_pitch':d['frame_pitch_x'],'clamp_centres':c['centres'],
            'clamp_band_width':d['band_width'],'clamp_bolt_zs':d['bolt_zs'],
            'vessel_y0':-100,'vessel_z':140}
    target=PART/'spec/clamp_interface.scad';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('// GENERATED from the current clamp OpenSCAD echo. Do not edit.\n'+
                      '\n'.join(k+' = '+json.dumps(v)+';' for k,v in values.items())+'\n',encoding='utf-8')
    save(PART/'spec/clamp_interface.json',dict(source=CLAMP.relative_to(ROOT).as_posix(),
        source_sha256=hashlib.sha256((CLAMP/(CLAMP.name+'.scad')).read_bytes()).hexdigest(),
        reference_mesh_sha256=hashlib.sha256((CLAMP/'child_wte4_suspension_clamp_cage.stl').read_bytes()).hexdigest(),
        interface=found,layout=values))
    return d,c


def main():
    d,c=interface()
    original=read(ROOT/'assemblies/child_exterior_concept/placement.json')
    source=(PART/(STEM+'.scad')).read_text(encoding='utf-8')
    scalars={n:float(v) for n,v in re.findall(r'^([a-z_]+)\s*=\s*(-?[\d.]+)\s*;',source,re.M)}
    sx=scalars['side_x'];pt=scalars['panel_t'];inside=sx-pt/2;outside=sx+pt/2
    upper_z=scalars['frame_top']-scalars['rail_height']/2
    beam_y=scalars['lower_beam_y'];shoe_y=scalars['shoe_y']
    rear_beam_y=scalars['rear_beam_y'];rear_beam_z=scalars['rear_beam_z']
    ref=read(ROOT/'assemblies/child_clamp_suspension/placement.json')
    data=dict(name=OUT.name,status='fit_prototype',units='mm',
              coordinate_system=original['coordinate_system'],
              reference_concept='assemblies/child_exterior_concept/placement.json',
              groups={k:True for k in ['frame','connections','feet','crossbars','ballast_support',
                                     'equipment_mounts','bumper','vessel','clamps','rubber','equipment',
                                     'ballast','foam','hardware']},
              notes=['Fabrication fit prototype; no lifting or underwater strength qualification.',
                     'All 24 existing cage mounting bores are used. Cage topology is unchanged.',
                     'Unselected light/TD04A brackets and buoyancy foam remain provisional.'],
              cable_routes=deepcopy(original['cable_routes']),items=[])
    items=data['items']; interface_rows=[]; joints=[]
    def add(label,variant,group,ops,color='SteelBlue',printed=True):
        row=dict(label=label,part=PART.relative_to(ROOT).as_posix(),file=STEM+'_'+variant,
                 group=group,color=color,ops=ops,print=printed)
        items.append(row);return row
    def t(p):return dict(translate=p)
    def r(p):return dict(rotate=p)
    def mirrored():return dict(mirror=[1,0,0])
    def axis_rotation(n):
        if n==[1,0,0]:return [0,90,0]
        if n==[-1,0,0]:return [0,-90,0]
        if n==[0,1,0]:return [-90,0,0]
        if n==[0,-1,0]:return [90,0,0]
        if n==[0,0,1]:return [0,0,0]
        if n==[0,0,-1]:return [180,0,0]
        raise ValueError(n)
    def hardware(label,file,p,n):
        items.append(dict(label=label,part='parts/common/interior/cots/screw',file='screw_'+file,
                          group='hardware',color='Silver',print=False,ops=[t(p),r(axis_rotation(n))]))
    def bolt(label,face,n,length,nut_face,head_washer='washer_m3_05',nut_washer=False):
        wt=1 if head_washer=='washer_m3_9x1' else .5
        head=[face[i]+wt*n[i] for i in range(3)]
        hardware(label+'_washer',head_washer,face,n)
        hardware(label+'_screw',f'm3x{length}',head,n)
        back=[-x for x in n]
        nut=list(nut_face)
        if nut_washer:
            hardware(label+'_nut_washer',head_washer,nut,back)
            nut=[nut[i]+wt*back[i] for i in range(3)]
        hardware(label+'_nut','nut_m3',nut,back)
        joints.append(dict(label=label,head_seat_mm=head,axis_outward=n,length_mm=length,
                           nut_seat_mm=nut,nut_thickness_mm=2.4,head_washer=head_washer))
    # Existing references, including original mesh coordinates and rigid poses.
    for row in original['items']:
        if row.get('group') in ['vessel','Horizontal cradle','Ballast B','Ballast C','Cameras','Upward lights','Transducer']:
            row=deepcopy(row)
            row['group']='vessel' if row['group']=='vessel' else ('rubber' if row['file'].endswith('liner') else
                'clamps' if row['file'].endswith('cage') else 'ballast' if row['group'].startswith('Ballast') else 'equipment')
            row.pop('geometry',None);row['print']=False
            if row['label'].startswith('ballast_B_'):
                number=int(row['label'][-1]);x=-150 if number<3 else 150;y=-85 if number%2 else 85
                row['ops']=[t([x,y,36]),r([0,0,90])]
                row['note']='60 g each, resting on lower rail; two purchased straps per plate.'
            items.append(row)
    H=[t([0,-100,140]),r([-90,0,0]),r([0,0,90])]
    for row in ref['items']:
        if row.get('group')=='hardware':
            row=deepcopy(row);row['label']='existing_'+row['label'];row['ops']=H+row['ops'];row['print']=False
            items.append(row)
    # Side plates are native UVW=world YZX. No assembly rotation enters print pose.
    for s,name in [(-1,'left'),(1,'right')]:
        for half in ['rear','front']:
            add(f'{name}_{half}','side_'+half,'frame',[t([s*sx-pt/2,0,0]),r([90,0,90])])
        for mid,z in [(False,upper_z),(True,140)]:
            x=outside if s>0 else -outside-6
            add(f'{name}_splice_'+('middle' if mid else 'upper'),'splice_middle' if mid else 'splice_upper',
                'connections',[t([x,0,z]),r([90,0,90])],'RoyalBlue')
            for y in ([-26,26] if mid else [-18,18]):
                for dz in ([-18,18] if mid else [-6,6]):
                    bolt(f'{name}_splice_{z}_{y}_{dz}',[s*(outside+6),y,z+dz],[s,0,0],25,[s*inside,y,z+dz],nut_washer=True)
        for y in [-shoe_y,0,shoe_y]:
            add(f'{name}_shoe_{y}','shoe','feet',[t([s*sx,y,5])]+([mirrored()] if s<0 else []),'DarkSlateGray')
            for dy in [-16,16]:
                bolt(f'{name}_shoe_{y}_{dy}',[s*(sx+15),y+dy,20],[s,0,0],30,[s*(sx-10.5),y+dy,20])
        for ci,centre in enumerate(c['centres']):
            y=-100+centre;ops=[t([0,y,140])]+([mirrored()] if s<0 else [])
            add(f'{name}_clamp_link_{ci}','clamp_link','connections',ops,'CadetBlue')
            for dy in [-8,8]:
                for dz in [-d['frame_pitch_x']/2,d['frame_pitch_x']/2]:
                    x=abs(d['mount_y']);z=140+dz
                    hardware(f'{name}_clamp_{ci}_{dy}_{dz}_spacer','washer_m3_9x1',[s*x,y+dy,z],[s,0,0])
                    bolt(f'{name}_clamp_{ci}_{dy}_{dz}',[s*(x+9),y+dy,z],[s,0,0],30,
                         [s*abs(d['shoulder_y']),y+dy,z],'washer_m3_9x1',True)
                    interface_rows.append(dict(label=f'{name}_clamp_link_{ci}',cage_label='cage_rear' if s>0 else 'cage_front',
                          axis_point_mm=[s*x,y+dy,z],normal=[s,0,0],shaft_d_mm=3,clearance_d_mm=3.5,
                          spacer_mm=1,frame_hole_mm=[s*(x+1),y+dy,z]))
            for dy in [-10,10]:
                face=outside+6 if ci==1 else outside;length=25 if ci==1 else 20
                bolt(f'{name}_link_frame_{ci}_{dy}',[s*face,y+dy,140],[s,0,0],length,[s*(inside-4),y+dy,140])
    for y,z,name in [(rear_beam_y,rear_beam_z,'rear_lower'),(beam_y,12,'front_lower'),(200,66,'camera')]:
        for s,side in [(-1,'left'),(1,'right')]:
            add(name+'_'+side,'cross_half','crossbars',[t([0,y,z])]+([mirrored()] if s<0 else []),'DarkSlateGray')
            for dy in [-9,9]:
                bolt(f'{name}_{side}_end_{dy}',[s*outside,y+dy,z+12],[s,0,0],20,[s*(inside-4),y+dy,z+12])
        add(name+'_splice','cross_splice','connections',[t([0,y+25,z+12]),r([90,0,0])],'SlateGray')
        for x in [-18,18]:
            for dz in [6,18]:bolt(f'{name}_splice_{x}_{dz}',[x,y+25,z+dz],[0,1,0],50,[x,y-19,z+dz],nut_washer=True)
    for s,name in [(-1,'left'),(1,'right')]:
        add('ballast_tray_'+name,'tray_half','ballast_support',[t([0,-90,24])]+([mirrored()] if s<0 else []),'DarkSlateGray')
        for y in [-126,-54]:bolt(name+'_tray_end_'+str(y),[s*outside,y,29],[s,0,0],20,[s*(inside-4),y,29])
        for x in [32,120]:
            add(f'{name}_weight_stop_{x}','weight_stop','ballast_support',[t([s*x,-90,34])],'SlateGray')
            for dy in [-18,18]:bolt(f'{name}_weight_stop_{x}_{dy}',[s*x,-90+dy,46],[0,0,1],30,[s*x,-90+dy,24],nut_washer=True)
    add('tray_splice','tray_splice','connections',[t([0,-90,18])],'SlateGray')
    for x in [-18,18]:
        for dy in [-30,30]:bolt(f'tray_splice_{x}_{dy}',[x,-90+dy,34],[0,0,1],20,[x,-90+dy,18],nut_washer=True)
    add('camera_deck','camera_deck','equipment_mounts',[t([0,229,90])])
    for x in [-24,24]:
        for y in [198,208]:bolt(f'camera_deck_{x}_{y}',[x,y,102],[0,0,1],45,[x,y,66],nut_washer=True)
    for s,y,variant,name in [(-1,-110,'equipment_seat','light'),(1,-110,'equipment_riser','transducer')]:
        add(name+'_exchangeable_seat',variant,'equipment_mounts',[t([s*inside,y,144])]+([mirrored()] if s>0 else []))
        for dy in [-10,10]:bolt(f'{name}_seat_{dy}',[s*outside,y+dy,152],[s,0,0],30,[s*(inside-12),y+dy,152])
    bridge_z=144+scalars['transducer_seat_height']
    add('transducer_bridge','equipment_bridge','equipment_mounts',[t([inside-36,-86,bridge_z])])
    for y in [-120,-100]:bolt(f'transducer_bridge_{y}',[inside-45,y,bridge_z+6],[0,0,1],25,[inside-45,y,bridge_z-12],nut_washer=True)
    for s,name in [(-1,'left'),(1,'right')]:
        add('bumper_'+name,'bumper_half','bumper',[t([0,-208,140]),r([90,0,0])]+([mirrored()] if s<0 else []),'DarkSlateGray')
        for z in [122,158]:bolt(name+'_bumper_'+str(z),[s*outside,-214,z],[s,0,0],20,[s*(inside-4),-214,z])
        add('foam_space_'+name,'foam_reference','foam',[t([s*111,100,225])],'Goldenrod',False)
    for z in [108,172]:
        add('bumper_splice_'+str(z),'bumper_splice','connections',[t([0,-226,z]),r([-90,0,0])],'SlateGray')
        for x in [-18,18]:bolt(f'bumper_splice_{x}_{z}',[x,-226,z],[0,-1,0],25,[x,-208,z],nut_washer=True)
    data['clamp_attachment']=dict(interface='existing_clamp_four_hole_mounting_faces',holes=interface_rows,
        source='parts/child/exterior/printed/child_exterior_open_frame/spec/clamp_interface.json')
    data['ballast_mass_g']=2240
    assert len(interface_rows)==24 and len({row['label'] for row in items})==len(items)
    save(OUT/'placement.json',data)
    save(PART/'spec/fastener_schedule.json',dict(joints=joints,purchased_counts=Counter(i['file'] for i in items if i['group']=='hardware')))
    save(PART/'manufacturing.json',dict(material='Bambu PETG Basic',
        non_print_files=[STEM+'_foam_reference'],
        print_rotations_deg={STEM+'_'+v:([90,0,0] if v in ['clamp_link','equipment_seat','equipment_riser'] else [0,0,0])
                             for v in VARIANTS if v!='foam_reference'},
        source_dependencies=['spec/clamp_interface.scad','spec/clamp_interface.json','spec/fastener_schedule.json',
                             '../../../../../tools/prepare_child_horizontal_frame.py',
                             '../../../../../assemblies/child_exterior_concept/placement.json',
                             '../child_wte4_suspension_clamp/child_wte4_suspension_clamp.scad'],
        degenerate_precision_weld_files=[STEM+'_'+v for v in VARIANTS],
        degenerate_edge_flip_files=[STEM+'_'+v for v in VARIANTS],stl_export_format='binstl',
        note='Fit prototype. 0.20 mm layers, 8 walls, 100% infill; frame panels flat. Connector Y build. '
             'Support horizontal nut-access channels on connectors; remove and gauge all holes. '
             'Closed manufacturing meshes only; foam is a non-print reserved volume.'))
    (PART/'variants.txt').write_text('\n'.join(v+' part="'+v+'"' for v in VARIANTS)+'\n',encoding='utf-8-sig')
    save(OUT/'print_config.json',dict(status='fit_prototype',
        note='クランプ24穴へ固定する横置き外装の取付確認用試作。PETG Basic、層高0.20 mm、外周8、100%インフィル、5 mmブリム。'
             '平面部品は平置き、接続部と機器台はY方向へ積層（STLに反映済み）。ねじ・ワッシャ・ナット・ゴム・ストラップ・浮力予約体積は印刷しません。'
             '完成接続部のFEAはメッシュ収束FAIL、局所安全率も要求3未達です。耐荷重未承認。'
             'クランプは既存の未承認参照品です。吊り上げ・水中使用の強度承認なし。機器の実取付台は型番・ブラケット寸法を確認して交換。',
        notes=[]))
    print('Prepared',len(items),'items, 24 cage bores;',sum(i.get('print',False) for i in items),'printed instances')


if __name__=='__main__':main()
