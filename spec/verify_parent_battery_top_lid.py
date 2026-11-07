"""Exact assembly and continuous vertical removal checks for the battery lid."""
from pathlib import Path
import sys,json
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'spec'),str(R/'scad/lib')]
from parent_access_common import load,common,v
import parent_battery_slide as B
def place(s,item):
    s=s.copy()
    for op in reversed(item['ops']):
        if 'rotate' in op:
            for axis,angle in zip([v(1,0,0),v(0,1,0),v(0,0,1)],op['rotate']):s.rotate(v(),axis,angle)
        if 'translate' in op:s.translate(v(*op['translate']))
    return s
def build(doc,parameters):
    d,c=load();items={i['label']:i for i in d['items']};rows=[]
    local={n:Part.read(str(R/p)) for n,p in parameters.items()}
    c['lipo_tray']=place(local['battery_base'],items['lipo_tray'])
    c['lipo_ret_lid']=place(local['parent_lipo_retainer_lid_slide'],items['lipo_ret_lid'])
    # The source screw has its bearing face at local Z=0, shaft toward -Z.
    bolt_item=items['lipo_ret_bolt_0']
    c['lipo_ret_bolt_0']=Part.read(str(R/bolt_item['part']/(bolt_item['file']+'.step')))
    c['lipo_ret_bolt_0'].translate(v(197.5-B.SCREW_XY[1],22.1+B.SCREW_XY[0],52))
    lid=c['lipo_ret_lid'];base=c['lipo_tray'];bolt=c['lipo_ret_bolt_0']
    def check(name,ok,**details):
        rows.append(dict(name=name,passed=bool(ok),**details))
        print(name,ok,details,flush=True)
    def hits(s,excluded):
        return [dict(part=n,volume_mm3=round(common(s,t),6)) for n,t in c.items() if n not in excluded and common(s,t)>.01]
    for name in ['lipo_tray','lipo_ret_lid']:
        h=hits(c[name],{name,'lipo_ret_bolt_0'})
        check(name+' installed interference',not h,hits=h)
    check('Lid seated on base',common(lid,base)<.001 and lid.distToShape(base)[0]<.001,common_mm3=common(lid,base),gap_mm=lid.distToShape(base)[0])
    # Extrude every face, union with start solid: exact swept solid for a straight translation.
    extrusions=[]
    for face in lid.Faces:
        ex=face.extrude(v(0,0,120))
        if ex.Volume>1e-6:extrusions.append(ex)
    sweep=lid.multiFuse(extrusions).removeSplitter()
    h=hits(sweep,{'lipo_ret_lid','lipo_ret_bolt_0','lid_keepout'})
    check('Continuous lid removal vertically 120mm, tray installed',not h,hits=h)
    x=197.5-B.SCREW_XY[1];y=22.1+B.SCREW_XY[0]
    driver=Part.makeCylinder(3,125,v(x,y,55))
    h=hits(driver,{'lipo_ret_bolt_0','lid_keepout'})
    check('Vertical driver diameter6 access',not h,hits=h)
    screw_out=Part.makeCylinder(3,130,v(x,y,49))
    h=hits(screw_out,{'lipo_tray','lipo_ret_lid','lipo_ret_bolt_0','lid_keepout'})
    check('Screw withdrawal corridor',not h,hits=h)
    check('One lid screw',len([n for n in c if n.startswith('lipo_ret_bolt_')])==1)
    check('No lid nut needed',not any(n.startswith('lipo_ret_nut_') for n in c))
    check('Head seated on lid',common(bolt,lid)<.001 and bolt.distToShape(lid)[0]<.001)
    raised=lid.copy();raised.translate(v(0,0,.5))
    check('Installed screw head resists lid uplift',common(raised,bolt)>.1,overlap_mm3=common(raised,bolt))
    thread=Part.makeCylinder(1.5,9,v(x,y,40))
    check('Screw engages base pilot 9mm',common(thread,base)>1,nominal_engagement_mm=9,bottom_clearance_mm=2,thread_material_overlap_mm3=common(thread,base))
    pilot=Part.makeCylinder(1.39,10.5,v(x,y,38.5))
    check('Pilot core open and bottom clear',common(pilot,base)<.001)
    check('Lid strength reinforcement height',abs(local['parent_lipo_retainer_lid_slide'].BoundBox.ZMax-6)<.001)
    # Battery and wires are the existing source geometry; no opening is filled.
    wire=Part.makeBox(2.6,39.6,25.5,v(-3.3,7.7,3.3))
    check('Existing full west wire mouth retained',common(wire,local['battery_base'])<.001)
    report=dict(status='PASS' if all(r['passed'] for r in rows) else 'FAIL',checks=rows,
        operation='Open waterproof vessel cover, remove one M3x12, lift battery lid vertically120mm; tray and its four screws stay installed',
        fastening_path='Screw head -> 3mm lid ear -> boss top at local Z29 -> integrated base boss -> 9mm plastic thread engagement. No nut or adhesive.',
        limitations=['Nominal CAD geometry only; printed pilot thread strip/pullout, repeated opening, lid flex, PETG creep and actual wire routing require physical checks.'])
    print('BATTERY_TOP_REPORT='+json.dumps(report),flush=True)
    obj=doc.addObject('Part::Feature','lid_verified');obj.Shape=local['parent_lipo_retainer_lid_slide'].cleaned()
    return [obj]
