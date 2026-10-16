"""Hardware/tools and continuous GNSS cartridge extraction at installed height."""
from parent_access_common import *
d,c=load();hardware=[];tools=[]
targets=['p_main','p_pwr','tx_improved','spresense','lipo','lipo_tray','lipo_ret_lid','box_bcas212310g','gnss_receiver','gnss_universal_pcb','gnss_sma_plug','antenna_ground_plate','gnss_antenna','antenna_rack','gnss_universal_carrier','gnss_coax_route','tx_top_keepout','magnetometer']
hosts={'gnss_frame':'gnss_universal_carrier','antenna_rack':'antenna_rack','main_carrier':'main_mount_plate','sony_carrier':'sony_mount_plate'}
targets += corner_fixtures(c)+['coax_ring']+[n for n in c if n.startswith(('gnss_column_','sony_column_'))]
for name,shape in c.items():
    if not name.startswith(tuple(prefix+'_mount_' for prefix in hosts)+('gnss_pcb_bolt_','gnss_pcb_nut_','ground_plate_mount_','ground_plate_nut_','antenna_mount_','antenna_nut_')):continue
    b=shape.BoundBox;x=(b.XMin+b.XMax)/2;y=(b.YMin+b.YMax)/2
    host=next((host for prefix,host in hosts.items() if name.startswith(prefix+'_mount_')),None)
    scene={n:c[n] for n in targets}
    if host and name.startswith('sony_carrier_mount_'):host=sony_corner_for_foot(int(name.rsplit('_',1)[1]))
    if host:
        col=collisions(shape,{**scene,'plate':c['plate']})
        tool=Part.makeCylinder(2.5,120-b.ZMax,v(x,y,b.ZMax))
        tools.append(dict(name=name,stage='Module installation from above; PCB/antenna accessories not yet fitted, per wave_assembly_checks',collisions=collisions(tool,{host:c[host],'plate':c['plate']})))
    else:
        col=collisions(shape,scene)
        if '_nut_' not in name:
            tool=Part.makeCylinder(2.5,120-b.ZMax,v(x,y,b.ZMax))
            tools.append(dict(name=name,stage='Lid open',collisions=collisions(tool,scene)))
        elif name.startswith('gnss_pcb_nut_'):
            tool=Part.makeCylinder(3.5,5,v(x,y,b.ZMin-5)).cut(Part.makeCylinder(1.7,5.2,v(x,y,b.ZMin-5.1)))
            tools.append(dict(name=name,stage='Hold M3 nut from below before tightening PCB',collisions=collisions(tool,{**scene,**{n:c[n] for n in c if n.startswith('gnss_column_')}})))
        else:
            # Top-loaded hex pockets prevent free nut rotation. No underside
            # wrench is needed after MAIN has been installed below the rack.
            tool=Part.makeCylinder(4.3 if name.startswith('antenna_nut') else 3.4,100-b.ZMax,v(x,y,b.ZMax))
            tools.append(dict(name=name,stage='Insert captive nut from above before steel plate/antenna; turn-stop checked in wave_assembly_checks',collisions=collisions(tool,{n:c[n] for n in ['p_main']})))
    hardware.append(dict(name=name,collisions=col))
moving=['gnss_universal_pcb','gnss_receiver','gnss_pin_headers','gnss_xh_keepout']
remove=moving+['gnss_sma_plug','gnss_coax_route']+[n for n in c if n.startswith(('gnss_pcb_bolt_','gnss_pcb_nut_'))]
parked=Part.makeCompound([Part.read(str(R/'parts/parent/interior/cots/ann_mb1'/(stem+'.step'))) for stem in ['coax_parked','sma_plug_parked']])
park_check=collisions(parked,c,['gnss_antenna','gnss_coax_route','gnss_sma_plug']);removal=[]
for name in moving:
    for i,s in enumerate(c[name].Solids):
        b=s.optimalBoundingBox(False,False)
        sweep=Part.makeBox(b.XLength,b.YLength,b.ZLength+110,v(b.XMin,b.YMin,b.ZMin))
        col=collisions(sweep,c,remove);vol=common(sweep,parked)
        if vol>.1:col.append(dict(part='parked SMA/coax',mm3=round(vol,4)))
        removal.append(dict(part=name,solid=i,collisions=col))
report=dict(status='PASS' if all(not r['collisions'] for r in hardware+tools+removal) and not park_check else 'FAIL',hardware=hardware,tools=tools,removal=removal,parked_coax_collisions=park_check,
 removal_conditions='Lid open. Four M3 PCB bolts/nuts removed, SMA and XH disconnected, coax parked at antenna rear. Cartridge lifts straight up with MAIN/Sony installed. Continuous swept boxes through 110 mm extraction.',
 floor_mount='16 top-loaded M3 metal nuts atZ16.2; main3PCB-shared M3x30+1carrier M3x25, Sony4M3x50, GNSS4M3x40, antenna4M3x50. Install from above per wave_assembly_checks. Torque/creep/loosening unverified.',
 tool_assumption='Driver diameter5; nut access diameter8.6/7.4. Human grip, wrench swing and real harness unverified.')
(O/'gnss_access_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(report['status'],[r for r in hardware+tools+removal if r['collisions']],park_check,flush=True)
assert report['status']=='PASS'
