"""Read-only component packing probe; exact existing purchased/PCB solids."""
import FreeCAD as A, Part
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
O=R/'assemblies/parent_hand_service/_work/analysis/switch_tx_revision_20261008'
O.mkdir(parents=True,exist_ok=True)
def v(*p):return A.Vector(*p)
def place(s,xyz,angle=0):
    s.rotate(v(0,0,0),v(0,0,1),angle);s.translate(v(*xyz));return s
a=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
over={'p_main':([18,112,42],0),'p_pwr':([19.8,115,28.3],90),'spresense':([202.34,208,65.6],180),
     'gnss_receiver':([119.5,205,64.6],180),'gnss_sma_plug':([119.5,205,64.6],180),'gnss_pin_headers':([119.5,205,64.6],180),
     'gnss_universal_pcb':([75,139,56],0),'gnss_xh_keepout':([66.7,168,57.6],0),'pen_tether':([28,0,65],0)}
ss={}
for it in a['items']:
    n=it['label']
    if n not in over and n not in ['tx_improved','gnss_antenna','antenna_ground_plate','coax_coil_keepout','lipo','lipo_tray','lipo_ret_lid','box_bcas212310g','pen_tether','pen_td04a'] and not n.startswith(('ground_plate_','antenna_mount_','antenna_nut_')):continue
    s=Part.read(str(R/it['part']/(it.get('file',Path(it['part']).name)+'.step')))
    if n in over:s=place(s,*over[n])
    else:
        for op in reversed(it['ops']):
            if 'rotate' in op:
                for axis,ang in zip([v(1,0,0),v(0,1,0),v(0,0,1)],op['rotate']):s.rotate(v(0,0,0),axis,ang)
            if 'translate' in op:s.translate(v(*op['translate']))
    ss[n]=s
    print('Loaded',n,flush=True)
def common(s,t):
    if not s.BoundBox.intersect(t.BoundBox):return 0
    aa=[p for p in s.Solids if p.BoundBox.intersect(t.BoundBox)]
    bb=[p for p in t.Solids if p.BoundBox.intersect(s.BoundBox)]
    if not aa or not bb:return 0
    return Part.makeCompound(aa).common(Part.makeCompound(bb)).Volume
def cols(sh,exclude=()):
    out=[]
    for n,t in ss.items():
        if n in exclude:continue
        if sh.BoundBox.intersect(t.BoundBox):
            vol=common(sh,t)
            if vol>.1:out.append([n,round(vol,3)])
    return out
rows=[]
for n in ['p_main','p_pwr','spresense','gnss_receiver','gnss_sma_plug','gnss_pin_headers','gnss_universal_pcb','gnss_xh_keepout']:
    rows.append([n,cols(ss[n],[n])]);print('Checked',n,flush=True)
levers=[]
for s in ss['p_pwr'].Solids:
    b=s.BoundBox
    if b.ZMax>52:
        levers.append([(b.XMin+b.XMax)/2,(b.YMin+b.YMax)/2,b.ZMin,b.ZMax])
access=[]
for i,(x,y,z0,z1) in enumerate(levers):
    sh=Part.makeCylinder(10,110-47,v(x,y,47))
    access.append(['switch'+str(i),[x,y,z0,z1],cols(sh,['p_pwr'])])
for n,x,y,z,d,host in [('MAIN_SD',62,26.29,44.5,-1,'p_main'),('SONY_SD',165.16,134.72,68,-1,'spresense')]:
    card=Part.makeBox(11,16,1,v(x-5.5,y if d==1 else y-16,z-.5))
    rise=Part.makeBox(11,15,60,v(x-5.5,y+1 if d==1 else y-16,z-.5))
    finger=Part.makeBox(14,12,60,v(x-7,y+4 if d==1 else y-16,z-5))
    for name,sh in [('card',card),('rise',rise),('finger',finger)]:access.append([n+name,cols(sh,[host])])
b=ss['tx_improved'].BoundBox
sh=Part.makeBox(b.XLength,b.YLength,20,v(b.XMin,b.YMin,b.ZMax))
access.append(['TX20',cols(sh,['tx_improved'])])
report={'pairs':rows,'access':access,'bbox':{n:[s.BoundBox.XMin,s.BoundBox.YMin,s.BoundBox.ZMin,s.BoundBox.XMax,s.BoundBox.YMax,s.BoundBox.ZMax] for n,s in ss.items()}}
(O/'packing_probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'pairs':rows,'access':access},indent=2))
nut=ss['ground_plate_nut_3'];bolt=ss['ground_plate_mount_3']
for p in ss['p_main'].Solids:
    if common(p,nut)>.01:print('Nut obstructing MAIN solid',p.BoundBox,flush=True)
for x,y in [(100,75),(100,70),(92,85),(85,85),(100,40),(95,35)]:
    print('GP candidate',x,y,common(ss['p_main'],nut.translated(v(x-100,y-85,0))),common(ss['p_main'],bolt.translated(v(x-100,y-85,0))),flush=True)
