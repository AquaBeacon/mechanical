"""Installed fit, continuous slide/lift sweeps and retention of the one-screw lid."""
from pathlib import Path
import sys,json,math,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'spec'));sys.path.insert(0,str(R/'scad/lib'))
from parent_access_common import load,common,v
import parent_gnss as G
import parent_battery_slide as B
O=R/'assemblies/parent_hand_service';D=O/'_work/analysis/battery_side_grooves_20261013'
_,c=load();rows=[]
def check(name,ok,**data):
    rows.append(dict(name=name,pass_=bool(ok),**data))
    if not ok:print('FAIL',name,data,flush=True)
bolts=json.loads((R/'parts/parent/interior/printed/parent_lipo_retainer/dimensions.json').read_text(encoding='utf-8'))['bolt_xy']
base=c['lipo_tray'];lid=c['lipo_ret_lid']
nut=c['lipo_ret_nut_0']
check('Lid nut aligned with captured hex pocket',common(nut,base)<.001,overlap_mm3=common(nut,base))
raised=nut.copy();raised.translate(v(0,0,.8))
check('Tapered roof captures lid nut',common(raised,base)>.1,overlap_mm3=common(raised,base))
nr=5.5/math.sqrt(3)
points=sorted({(round(12+nr*math.cos(i*math.pi/3),9),round(5+nr*math.sin(i*math.pi/3)+shift,9)) for i in range(6) for shift in [0,-10]})
def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
lower=[];upper=[]
for p in points:
    while len(lower)>1 and turn(lower[-2],lower[-1],p)<=0:lower.pop()
    lower.append(p)
for p in reversed(points):
    while len(upper)>1 and turn(upper[-2],upper[-1],p)<=0:upper.pop()
    upper.append(p)
ps=[v(x,y,21.6) for x,y in lower[:-1]+upper[:-1]]
local_nut=Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(v(0,0,2.4))
local_nut.rotate(v(),v(0,0,1),90);local_nut.translate(v(*G.BATTERY_ORIGIN))
check('Continuous M3 nut side insertion',common(local_nut,base)<.001,overlap_mm3=common(local_nut,base))
from parent_case_access import BATTERY_TOOL_D
tray_tool=Part.makeCylinder((BATTERY_TOOL_D-.2)/2,10,v(185,25,18))
check('Enlarged tray tool opening clears 7.8 mm envelope',common(tray_tool,base)<.001,diameter_mm=BATTERY_TOOL_D-.2)
check('Coax ring unchanged after cancelled request',hashlib.sha256((R/'parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring.stl').read_bytes()).hexdigest()==json.loads((D/'baseline.json').read_text())['parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring.stl'])
check('One installed lid screw and one nut',len([n for n in c if n.startswith('lipo_ret_bolt_')])==1 and len([n for n in c if n.startswith('lipo_ret_nut_')])==1)
check('Lid and base seated without penetration',common(lid,base)<.001 and lid.distToShape(base)[0]<1e-5,overlap_mm3=common(lid,base))
for label in ['lipo_ret_lid','lipo_tray']:
    hits=[]
    for other,shape in c.items():
        if other==label or other in ['lid_keepout','lipo_ret_nut_0','lipo_ret_bolt_0']:continue
        vol=common(c[label],shape)
        if vol>.01:hits.append(dict(part=other,mm3=vol))
    check(label+' installed clearance',not hits,hits=hits)
def placed(s):
    s=s.copy();s.rotate(v(0,0,0),v(0,0,1),90);s.translate(v(*G.BATTERY_ORIGIN[:2],49));return s
module=['lipo_tray','lipo_ret_lid','lipo','lipo_ret_pads','lipo_ret_bolt_0','lipo_ret_nut_0']
removed=module+[n for n in c if n.startswith('lipo_ret_mount_')]
hits=[]
for name in module:
    for solid in c[name].Solids:
        b=solid.optimalBoundingBox(False,False)
        env=Part.makeBox(b.XLength,b.YLength,b.ZLength+B.MODULE_LIFT,v(b.XMin,b.YMin,b.ZMin))
        for other,shape in c.items():
            if other in removed or other=='lid_keepout':continue
            vol=common(env,shape)
            if vol>.001:hits.append(dict(moving=name,part=other,mm3=vol))
check('Closed battery module continuous vertical removal',not hits,hits=hits,lift_mm=B.MODULE_LIFT)
for name in [n for n in c if n.startswith('lipo_ret_mount_')]:
    b=c[name].BoundBox;x=(b.XMin+b.XMax)/2;y=(b.YMin+b.YMax)/2
    driver=Part.makeCylinder(2.5,100-b.ZMax,v(x,y,b.ZMax))
    hits=[other for other,s in c.items() if other not in [name,'lid_keepout'] and common(driver,s)>.001]
    check(name+' driver with lid closed',not hits,hits=hits)
for name in module:c[name].translate(v(0,0,B.MODULE_LIFT))
parts=[placed(s) for s in B.lid_boxes(bolts)]
for s in parts:s.translate(v(0,0,B.MODULE_LIFT))
remaining=lid
for sh in parts:remaining=remaining.cut(sh)
check('Removal envelopes contain actual chamfered lid',remaining.Volume<.001,uncovered_mm3=remaining.Volume)
def sweep_box(s,delta):
    b=s.optimalBoundingBox(False,False)
    points={(round(p.Point.x+dx,9),round(p.Point.y+dy,9)) for p in s.Vertexes for dx,dy in [(0,0),(delta[0],delta[1])]}
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    seq=sorted(points);lo=[];hi=[]
    for p in seq:
        while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    for p in reversed(seq):
        while len(hi)>1 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
        hi.append(p)
    z=min(b.ZMin,b.ZMin+delta[2]);ps=[v(x,y,z) for x,y in lo[:-1]+hi[:-1]]
    return Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(v(0,0,b.ZLength+abs(delta[2])))
def path(name,parts,delta):
    hits=[]
    for index,sh in enumerate(parts):
        if delta==[0,-B.TRAVEL,0] and index in [1,2]:
            # The rail is extruded parallel to travel: preserve the exact
            # sloped YZ profile rather than filling its dovetail with a box.
            env=placed(B.rail(index-1,B.TRAVEL));env.translate(v(0,0,B.MODULE_LIFT))
        else:env=sweep_box(sh,delta)
        for label,other in c.items():
            if label in ['lipo_ret_lid','lipo_ret_bolt_0','lid_keepout']:continue
            vol=common(env,other)
            if vol>.001:hits.append(dict(part=label,mm3=vol))
    check(name,not hits,hits=hits)
path('Continuous full-length slide after raising module',parts,[0,-B.TRAVEL,0])
for s in parts:s.translate(v(0,-B.TRAVEL,0))
path('Continuous released lid lift',parts,[0,0,100])
for side in [0,1]:
    h=placed(B.rail(side));h.translate(v(0,0,B.MODULE_LIFT+1))
    vol=common(h,base);check('Side rail '+str(side)+' prevents direct lift',vol>.1,overlap_mm3=vol)
# Screw shaft blocks the long slide before the rails can be withdrawn.
bolt=c['lipo_ret_bolt_0'];shift=lid.copy();shift.translate(v(0,-1,0))
check('Retained screw blocks release slide',common(shift,bolt)>.1,overlap_mm3=common(shift,bolt))
maxpack=Part.makeBox(104,36,25,v(-.5,9.5,3));maxpack.rotate(v(),v(0,0,1),90);maxpack.translate(v(*G.BATTERY_ORIGIN))
maxpack.translate(v(0,0,B.MODULE_LIFT))
check('Maximum rigid pack envelope clears lid and base',common(maxpack,lid)<.001 and common(maxpack,base)<.001)
baseline=json.loads((D/'baseline.json').read_text(encoding='utf-8'))
for suffix in ['scad','step','stl']:
    rel=f'parts/parent/interior/printed/parent_hand_service/floor_plate.{suffix}'
    check('Floor '+suffix+' unchanged',hashlib.sha256((R/rel).read_bytes()).hexdigest()==baseline[rel])
wire=Part.makeBox(3.5,40,26,v(-5,7.5,3));wire.rotate(v(),v(0,0,1),90);wire.translate(v(*G.BATTERY_ORIGIN))
wire.translate(v(0,0,B.MODULE_LIFT))
check('Full lead-face opening retained',common(wire,base)<.001)
report=dict(status='PASS' if all(r['pass_'] for r in rows) else 'FAIL',checks=rows,slide_mm=B.TRAVEL,module_lift_mm=B.MODULE_LIFT,groove_depth_mm=1.2,outer_wall_remaining_mm=1.3,groove_roof_deg=45,clearance_mm=.3,screw='M3x12 + M3 nut, location0 unchanged',limitations='Full-length slide requires removing four tray mount screws and lifting the closed module first. Geometry validation only; physical PETG fit and strength require trial.')
(O/'battery_slide_lid_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['status'],len(rows),'slide-lid checks',flush=True);assert report['status']=='PASS'
