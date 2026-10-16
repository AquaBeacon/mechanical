"""Verify full extraction sweeps with the carrier CLOSED and the floor in its case.

Card/fingertip and tool sizes are explicit design envelopes, not human certification.
LiPo lid and its own screw(s) are removed only for the battery extraction checks.
"""
from parent_access_common import *
import sys
sys.path.insert(0,str(R/'scad/lib'))
import parent_gnss as G
def v(*p):return A.Vector(*p)
d,c=load()
def check(sh,exclude=()):
    out=[]
    for n,t in c.items():
        if n=='lid_keepout' or n in exclude:continue
        if sh.BoundBox.intersect(t.BoundBox):
            vol=common(sh,t)
            if vol>.1:out.append({'part':n,'mm3':round(vol,4)})
    return out
rows=[];proxies={}
for n in ['plate','lipo_tray','lipo_ret_lid','antenna_rack','coax_ring','gnss_universal_carrier']+corner_fixtures(c)+[n for n in c if n.startswith(('gnss_column_','sony_column_'))]:
    sh=c[n];t=c['box_bcas212310g'];vol=common(sh,t)
    rows.append(dict(name=n+' vs case',collisions=[dict(part='box_bcas212310g',mm3=round(vol,4))] if vol>.1 else []))
removed=['lipo_ret_lid']+[n for n in c if n.startswith('lipo_ret_bolt_')]
b=c['lipo'].optimalBoundingBox(False,False)
sh=Part.makeBox(b.XLength,b.YLength,100,v(b.XMin,b.YMin,b.ZMin))
rows.append(dict(name='LiPo continuous vertical extraction',collisions=check(sh,removed+['lipo','lipo_ret_pads'])))
proxies['battery_extraction']=sh
# Slide lid: verify the complete release/lift path in its dedicated checker.
if 'battery_lid_design' in d:
    import runpy
    runpy.run_path(str(R/'spec/verify_parent_battery_slide_lid.py'),run_name='__main__')
    rows.append(dict(name='Slide lid continuous release/lift',collisions=[],evidence='battery_slide_lid_checks.json'))
else:
    b=c['lipo_ret_lid'].optimalBoundingBox(False,False)
    sh=Part.makeBox(b.XLength,b.YLength,100,v(b.XMin,b.YMin,b.ZMin))
    rows.append(dict(name='LiPo lid vertical removal',collisions=check(sh,removed)))
    proxies['battery_lid_extraction']=sh
for name in [n for n in c if n.startswith('lipo_ret_bolt_')]:
    b=c[name].BoundBox;x=(b.XMin+b.XMax)/2;y=(b.YMin+b.YMax)/2
    tool=Part.makeCylinder(2.5,100-b.ZMax,v(x,y,b.ZMax))
    rows.append(dict(name=name+' driver',collisions=check(tool,[name])))
# Continuous horizontal 16 mm card sweep, then lift a fully cleared 15 mm card.
for n,x,y,z,d,host in [('MAIN_SD',*G.MAIN_SD_MOUTH,-1,'p_main'),('SONY_SD',*G.SONY_SD_MOUTH,-1,'spresense')]:
    card=Part.makeBox(11,16,1,v(x-5.5,y if d==1 else y-16,z-.5))
    rise=Part.makeBox(11,15,50,v(x-5.5,y+1 if d==1 else y-16,z-.5))
    finger=Part.makeBox(14,12,45,v(x-7,y+4 if d==1 else y-16,z-5))
    for label,sh in [('card_slide',card),('card_lift',rise),('fingertip',finger)]:
        rows.append(dict(name=n+' '+label,collisions=check(sh,[host])))
        proxies[n+'_'+label]=sh
# Winding remains inside OD100/ID75/H10, with the new SW tool guard excluded.
ring=c['coax_coil_keepout'];bb=ring.BoundBox
ideal=Part.makeCylinder(50,10,v(60,60,22.3)).cut(Part.makeCylinder(37.5,10.2,v(60,60,22.2)))
from parent_case_access import GUIDE_OD
expected=ideal.cut(Part.makeCylinder((GUIDE_OD+.4)/2,10.2,v(25,25,22.2)))
assert ring.common(expected).Volume>expected.Volume-.01 and ring.cut(expected).Volume<.01
ring_collision=check(ring,['coax_coil_keepout'])
rows.append(dict(name='Winding OD100 ID75 H10 minus SW tool guard clearance',collisions=ring_collision,guard_excluded_mm3=ideal.Volume-expected.Volume))
centre=Part.makeCylinder(37.5,10,v(60,60,22.3))
rows.append(dict(name='Winding centre ID75 empty through H10',collisions=check(centre,['coax_coil_keepout'])))
report=dict(status='PASS' if all(not r['collisions'] for r in rows) else 'FAIL',carrier_lift_mm=0,
    conditions='Case lid open; disconnect power lead, remove four tray mount screws, lift closed battery module90, remove one lid screw and slide south108; no board, floor or GNSS removal',
    envelope_assumptions=dict(card_mm=[11,15,1],card_slide_mm=16,fingertip_mm=[14,12,45],driver_diameter_mm=5),checks=rows,
    user_coil_mm=dict(outer_diameter=100,inner_diameter=75,height=10,centre_xy=[60,60],bottom_z=22.3),
    limitations='Actual card latch/finger grip, LiPo lead/plug and winding transitions require fit check. Reserved winding size does not certify 5 m capacity.')
(O/'battery_sd_access_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
Part.makeCompound(list(proxies.values())).exportStep(str(O/'_work/intermediate/battery_sd_access_sweeps.step'))
print(json.dumps(report,ensure_ascii=False,indent=2))
assert report['status']=='PASS'
