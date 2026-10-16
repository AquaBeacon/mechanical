"""Installed switch paths, populated TX overhead and MAIN USB out of case."""
from parent_access_common import *
import sys,math,re
sys.path.insert(0,str(R/'scad/lib'))
import parent_gnss as G
d,c=load();rows=[];proxies={};switches=[]
text=(R.parent/'hardware/pcb/PARENT_PWR/PARENT_PWR.kicad_pcb').read_text(encoding='utf-8')
starts=[m.start() for m in re.finditer(r'\(footprint ',text)]
levers=[s for s in c['p_pwr'].Solids if s.BoundBox.ZMax>52]
assert len(levers)==2
for a,b in zip(starts,starts[1:]+[len(text)]):
    t=text[a:b];ref=re.search(r'\(property "Reference" "(SW_PWR|SW_TX)"',t)
    if not ref:continue
    at=re.search(r'\(at ([\d.-]+) ([\d.-]+) ([\d.-]+)',t)
    off=re.search(r'SW_2MD1_lever.step"\s*\(offset\s*\(xyz ([\d.-]+) ([\d.-]+) ([\d.-]+)',t)
    assert at and off
    x,y,angle=map(float,at.groups());ox,oy,oz=map(float,off.groups());a=math.radians(angle)
    # KiCad models use +Y up, PCB footprint coordinates use +Y down.
    nx=x+ox*math.cos(a)-oy*math.sin(a);ny=-y+ox*math.sin(a)+oy*math.cos(a)
    wx,wy=G.PWR_ORIGIN[0]-ny,G.PWR_ORIGIN[1]+nx
    actual=min(levers,key=lambda s:math.hypot(s.CenterOfMass.x-wx,s.CenterOfMass.y-wy))
    assert math.hypot(actual.CenterOfMass.x-wx,actual.CenterOfMass.y-wy)<.01
    b=actual.BoundBox
    # 20 mm finger column starts around the upper lever, with a separate
    # 12 mm diameter actuator envelope from its pivot to the lever top.
    finger=Part.makeCylinder(10,120-47,v(wx,wy,47))
    travel=Part.makeCylinder(6,b.ZLength,v(wx,wy,b.ZMin))
    other_pwr=Part.makeCompound([s for s in c['p_pwr'].Solids if s.BoundBox.ZMax<=52])
    for name,sh in [('finger_column',finger),('actuator_envelope',travel)]:
        col=collisions(sh,c,['p_pwr'])
        overlap=common(sh,other_pwr)
        if overlap>.1:col.append(dict(part='adjacent_PWR_components',mm3=round(overlap,4)))
        rows.append(dict(name=ref[1]+' '+name,collisions=col));proxies[ref[1]+'_'+name]=sh
    switches.append(dict(reference=ref[1],centre_xy_mm=[wx,wy],lever_z_mm=[b.ZMin,b.ZMax],source='Current KiCad footprint/model offset cross-checked against imported STEP lever solid'))
tx=c['tx_improved'].optimalBoundingBox(False,False);keep=c['tx_top_keepout']
assert abs(keep.BoundBox.ZMin-tx.ZMax)<.01 and abs(keep.BoundBox.ZLength-G.TX_TOP_EXTRA_MM)<.01
rows.append(dict(name='20 mm above highest TX component, complete populated XY envelope',collisions=collisions(keep,c,['tx_improved','tx_top_keepout'])))
# Plug body: 14 wide, 30 insertion travel, 10 high. Grip approach is explicitly
# checked only after the interior is removed and case-mounted harness unplugged.
x,y,z=G.MAIN_USB_MOUTH
plug=Part.makeBox(14,30,10,v(x-7,y-30,z-5))
grip=Part.makeBox(24,35,20,v(x-12,y-65,z-10))
sh=plug.fuse(grip)
rows.append(dict(name='MAIN USB plug/grip approach outside case',collisions=collisions(sh,c,['p_main','box_bcas212310g','pen_tether','pen_td04a'])))
proxies['main_usb_out_of_case']=sh
# Every fixture and electronic pair; intentional mating/fastener contact is
# verified separately. Include all actual case interfaces and new floor tabs.
fixture=['plate','antenna_rack','gnss_universal_carrier']
fixture += corner_fixtures(c)+['coax_ring']+[n for n in c if n.startswith(('gnss_column_','sony_column_'))]
elec=['p_main','p_pwr','tx_improved','spresense','lipo','gnss_receiver','gnss_universal_pcb','gnss_pin_headers','gnss_sma_plug','gnss_antenna','antenna_ground_plate','magnetometer']
for i,n in enumerate(elec):
    targets=elec[i+1:]+fixture+['box_bcas212310g','pen_tether','pen_td04a']
    for m in targets:
        vol=common(c[n],c[m])
        rows.append(dict(name=n+' vs '+m,collisions=[dict(part=m,mm3=round(vol,4))] if vol>.1 else []))
for i,n in enumerate(fixture):
    for m in fixture[i+1:]+['box_bcas212310g']:
        vol=common(c[n],c[m]);rows.append(dict(name=n+' vs '+m,collisions=[dict(part=m,mm3=round(vol,4))] if vol>.1 else []))
for n in ['gnss_coax_route','gnss_xh_keepout']:
    rows.append(dict(name=n+' occupied envelope',collisions=collisions(c[n],c,[n,'gnss_antenna'] if n=='gnss_coax_route' else [n])))
lid=[]
case_dims=json.loads((R/'parts/parent/exterior/cots/bcas212310g/dimensions.json').read_text(encoding='utf-8'))
roof_z=case_dims['cover_roof_bottom_z_mm']
for it in d['items']:
    n=it['label']
    if it['group']!='interior' or n in ['lid_keepout','tx_top_keepout']:continue
    margin=roof_z-c[n].BoundBox.ZMax
    lid.append(dict(part=n,lid_clearance_mm=margin))
    overlap=common(c[n],c['lid_keepout'])
    if overlap>.1:rows.append(dict(name=n+' actual cover intersection',collisions=[dict(part='lid_keepout',mm3=overlap)]))
    if margin<3:rows.append(dict(name=n+' lid clearance',collisions=[dict(part='lid_keepout',clearance_mm=margin)]))
status='PASS' if all(not r['collisions'] for r in rows) else 'FAIL'
report=dict(status=status,switches=switches,tx=dict(populated_top_z_mm=tx.ZMax,reserved_top_z_mm=keep.BoundBox.ZMax,height_mm=G.TX_TOP_EXTRA_MM),checks=rows,lid_closure=dict(minimum_clearance_mm=min(i['lid_clearance_mm'] for i in lid),parts=lid),conditions='Case lid open. Both power switches and SD cards at installed height. MAIN USB checked with case and case-mounted penetrators disconnected/removed. Cable harness and human grip require fit check.',manufacturing_release=False)
(O/'switch_tx_access_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
Part.makeCompound(list(proxies.values())+[keep]).exportStep(str(O/'_work/intermediate/switch_tx_access_sweeps.step'))
print(status,[r for r in rows if r['collisions']],flush=True)
assert status=='PASS'
