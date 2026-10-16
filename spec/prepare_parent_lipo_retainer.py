"""Generate 6-face LiPo retention from the parent tray datums and child removable enclosure reference."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];P=R/'parts/parent/interior/printed/parent_lipo_retainer';P.mkdir(exist_ok=True)
# Nominal installed geometry. Foam thickness is adjusted to actual pack, not by bolt torque.
c={'l':102,'w':34,'h':23,'floor':3,'end_gap':2,'side_gap':3,'top_gap':3,'wall':2.5,'hole_pitch':[103,75.5],'origin_box':[20,48.5,51.4],'lid_t':3,'bolt_xy':[[12,5],[91,5],[12,50],[91,50]],'nut_floor':21.5,'nut_ceiling':24.0,'reference':'parts/child/interior/printed/child_vtray_batt_box + child_vtray_batt_floor'}
(P/'dimensions.json').write_text(json.dumps(c,indent=2))
s='''// Parent 6-face LiPo retainer, inspired by child_vtray_batt_box/floor.
/* [Output] */
part="base"; // [base,lid,pads,assembly]
/* [Pack and compliant clearance] */
lipo_l=102; lipo_w=34; lipo_h=23;
end_gap=2; side_gap=3; top_gap=3;
/* [Structure] */
floor_t=3; wall=2.5; lid_t=3; rail_w=8; rail_h=12;
hole_px=103; hole_py=75.5;
west_trim=0; // hand-service variant: 0.6 mm clears the west guide
lead_open=16; bolt_x=[12,91]; bolt_y=[5,50];
boss_d=8; bore_d=3.45; nut_af=5.8; nut_floor=21.5; nut_ceiling=24;
$fn=48;
in_l=lipo_l+2*end_gap; in_w=lipo_w+2*side_gap;
bay_x=-4; bay_y=5; bay_l=in_l+2*wall; bay_w=in_w+2*wall;
cap_z=floor_t+lipo_h+top_gap;
mounts=[[0,0],[hole_px,0],[0,hole_py],[hole_px,hole_py]];
bolts=[for(x=bolt_x,y=bolt_y)[x,y]];
assert(cap_z+lid_t+51.4+2 < 90.9,"Retainer touches enclosure lid");
assert(nut_ceiling-nut_floor>=2.4 && cap_z-nut_ceiling>=4,"Nut roof too thin");
assert(top_gap>0 && end_gap>0 && side_gap>0,"No compliant pack clearance");
module bore(d,h){cylinder(r=d/2/cos(180/12),h=h,$fn=12);}
module base(){difference(){
 union(){
  translate([bay_x,bay_y,0]) cube([bay_l,bay_w,cap_z]);
  for(x=[0,hole_px]) translate([x-rail_w/2,-4.5,0]) cube([rail_w,hole_py+9,rail_h]);
  for(p=bolts) translate([p[0],p[1],0]) cylinder(d=boss_d,h=cap_z);
 }
 translate([bay_x+wall,bay_y+wall,floor_t]) cube([in_l,in_w,cap_z]);
 // West wire outlet is clear of top/bottom corner pads.
 translate([bay_x-.1,bay_y+bay_w/2-lead_open/2,floor_t+2]) cube([wall+.2,lead_open,cap_z-floor_t-4]);
 for(p=mounts){
  translate([p[0],p[1],-.1]) bore(bore_d,3.2);
  translate([p[0],p[1],floor_t]) cylinder(d=6.2,h=cap_z+1);
 }
 for(p=bolts){
  translate([p[0],p[1],-.1]) bore(bore_d,cap_z+.2);
  translate([p[0],p[1],nut_floor]) cylinder(d=nut_af/cos(30),h=nut_ceiling-nut_floor,$fn=6);
  translate([p[0]-nut_af/cos(30)/2,p[1]==bolt_y[0]?p[1]-4.5:p[1],nut_floor]) cube([nut_af/cos(30),4.5,nut_ceiling-nut_floor]);
 }
}}
module lid(){difference(){
 translate([bay_x,bolt_y[0]-boss_d/2,0]) cube([bay_l,bolt_y[1]-bolt_y[0]+boss_d,lid_t]);
 for(p=bolts) translate([p[0],p[1],-.1]) bore(bore_d,lid_t+.2);
 if(west_trim>0) translate([bay_x-.1,-1,-.1]) cube([west_trim+.1,60,lid_t+.2]);
}}
module pads(){
 // Installed compressed thickness; choose uncompressed sheets after measuring pack.
 translate([1,11,floor_t+lipo_h]) cube([101,33,top_gap]);
 for(y=[bay_y+wall,bay_y+wall+side_gap+lipo_w]) translate([20,y,floor_t+.5]) cube([63,side_gap,22]);
 translate([bay_x+wall+end_gap+lipo_l,11,floor_t+.5]) cube([end_gap,33,22]);
 for(y=[11,36]) translate([bay_x+wall,y,floor_t+.5]) cube([end_gap,8,22]);
}
if(part=="base")base();
if(part=="lid")lid();
if(part=="pads")pads();
if(part=="assembly"){
 color("DarkOrange")base();
 color("Tomato")translate([bay_x+wall+end_gap,bay_y+wall+side_gap,floor_t])cube([lipo_l,lipo_w,lipo_h]);
 color("LightPink",.7)pads();
 color("Orange",.6)translate([0,0,cap_z])lid();
}
'''
(P/'parent_lipo_retainer.scad').write_text(s,encoding='utf-8')
# Reproducible assembly integration, also called by prepare_parent_service.py.
def integrate(path):
 a=json.loads(path.read_text(encoding='utf-8'));a['items']=[i for i in a['items'] if not i['label'].startswith('lipo_ret_')]
 t=next(i for i in a['items'] if i['label']=='lipo_tray');t['part']='parts/parent/interior/printed/parent_lipo_retainer';t['file']='parent_lipo_retainer_base';t['note']='6-face retained battery; rigid lid stops, compliant pads; same 4 MAIN spacers'
 for name,stem,color,z in [('lid','parent_lipo_retainer_lid','Orange',29),('pads','parent_lipo_retainer_pads','LightPink',0)]:
  a['items'].append(dict(label='lipo_ret_'+name,part=t['part'],file=stem,group='interior',color=color,ops=[{'translate':[20,48.5,51.4+z]}]))
 for n,(x,y) in enumerate(c['bolt_xy']):
  for typ,stem,z in [('bolt','screw_m3x12',32),('nut','screw_nut_m3',21.6)]:
   a['items'].append(dict(label=f'lipo_ret_{typ}_{n}',part='parts/common/interior/cots/screw',file=stem,group='interior',color='Silver',ops=[{'translate':[20+x,48.5+y,51.4+z]}]))
 for n,(x,y) in enumerate([[0,0],[103,0],[0,75.5],[103,75.5]]):
  a['items'].append(dict(label=f'lipo_ret_mount_{n}',part='parts/common/interior/cots/screw',file='screw_m3x8',group='interior',color='Silver',ops=[{'translate':[20+x,48.5+y,54.4]}]))
 path.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':
 integrate(R/'assemblies/parent_service_review/placement.json');print('Generated 6-face retainer and assembly placement')
