"""Read-only packing probe for the 2026-10-08 battery/SD/coax revision."""
import FreeCAD as A, Part
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
O=R/'assemblies/parent_hand_service/_work/analysis/access_revision_20261008'
O.mkdir(parents=True,exist_ok=True)
def v(*p):return A.Vector(*p)
def place(s,xyz,angle=0):
    s.rotate(v(0,0,0),v(0,0,1),angle);s.translate(v(*xyz));return s
a=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
override={'p_main':([130,113,64],180),'p_pwr':([16.8,113,28.3],90),'spresense':([202.34,208,63],180),
          'lipo_tray':([197.5,18.5,20],90),'lipo_ret_lid':([197.5,18.5,49],90),'lipo_ret_pads':([197.5,18.5,20],90),
          'lipo':([153,121,23],270),'gnss_antenna':([60,60,64.6],90),
          'antenna_ground_plate':([60,60,63.6],0)}
names=['p_main','p_pwr','tx_improved','spresense','lipo','lipo_tray','lipo_ret_lid','box_bcas212310g','gnss_receiver','gnss_sma_plug','gnss_universal_pcb','gnss_pin_headers','gnss_universal_carrier','gnss_edge_cap_0','gnss_edge_cap_1','gnss_antenna','antenna_ground_plate','pen_tether','pen_td04a']
ss={}
for it in a['items']:
    n=it['label']
    if n not in names:continue
    s=Part.read(str(R/it['part']/(it.get('file',Path(it['part']).name)+'.step')))
    if n in override:s=place(s,*override[n])
    else:
        for op in reversed(it['ops']):
            if 'rotate' in op:
                for axis,ang in zip([v(1,0,0),v(0,1,0),v(0,0,1)],op['rotate']):s.rotate(v(0,0,0),axis,ang)
            if 'translate' in op:s.translate(v(*op['translate']))
    ss[n]=s
ss['pen_td04a'].translate(v(-65,0,0))
ss['coil']=Part.makeCylinder(50,10,v(60,60,22.3)).cut(Part.makeCylinder(37.5,10.2,v(60,60,22.2)))
ss['xh_provisional']=Part.makeBox(11,24,6,v(138,159,45))
def cols(sh,exclude=()):
    out=[]
    for n,t in ss.items():
        if n in exclude:continue
        if sh.BoundBox.intersect(t.BoundBox):
            vol=sh.common(t).Volume
            if vol>.1:out.append([n,round(vol,3)])
    return out
pairs=[]
for i,n in enumerate(names+['coil','xh_provisional']):
    for m in (names+['coil','xh_provisional'])[i+1:]:
        if n=='lipo' and m in ['lipo_tray','lipo_ret_lid']:continue
        sh,t=ss[n],ss[m]
        if sh.BoundBox.intersect(t.BoundBox):
            vol=sh.common(t).Volume
            if vol>.1:pairs.append([n,m,round(vol,3)])
b=ss['lipo'].BoundBox
sweep=Part.makeBox(b.XLength,b.YLength,100,v(b.XMin,b.YMin,b.ZMin))
access={'battery_vertical':cols(sweep,['lipo','lipo_tray','lipo_ret_lid'])}
for n,x,y,z,d in [('MAIN_SD',86,198.71,66.5,1),('SONY_SD',165.16,134.72,65.4,-1)]:
    card=Part.makeBox(11,16,1,v(x-5.5,y if d==1 else y-16,z-.5))
    # Card fully clear of the mouth, then raised through the open lid.
    rise=Part.makeBox(11,15,40,v(x-5.5,y+1 if d==1 else y-16,z-.5))
    fingertip=Part.makeBox(14,12,35,v(x-7,y+4 if d==1 else y-16,z-5))
    access[n]={'card':cols(card,['p_main' if d==1 else 'spresense']), 'rise':cols(rise,['p_main' if d==1 else 'spresense']), 'finger':cols(fingertip,['p_main' if d==1 else 'spresense'])}
report={'pairs':pairs,'access':access,'bbox':{n:[s.BoundBox.XMin,s.BoundBox.YMin,s.BoundBox.ZMin,s.BoundBox.XMax,s.BoundBox.YMax,s.BoundBox.ZMax] for n,s in ss.items()}}
(O/'packing_probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'pairs':pairs,'access':access},indent=2))
