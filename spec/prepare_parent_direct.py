from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'parts/parent/exterior/printed'
src=(P/'parent_light_frame/parent_light_frame.scad').read_text()
helpers=src[src.index('// Rounded profile extrusions'):]
src=src.replace('carrier_x=[-85,-65,65,85];','carrier_x=[65,85];')
src=src.replace(' union(){',''' union(){
  // Horizontal camera attachment integrated with frame; M3 40x40 rear mount.
  translate([-70,-67,-12])difference(){
   rb([60,134,12],3);
   translate([18,17,-.02])rb([24,100,12.04],3);
  }
  for(x=[-60,-20],y=[-20,20])translate([x,y,-24])cylinder(d=12,h=14,$fn=48);
''',1)
src=src.replace(' for(x=carrier_x){',''' // M3 heat-set insert pilots open toward existing mount; 7 mm deep.
 for(x=[-60,-20],y=[-20,20])translate([x,y,-24.02])hole(4.2,7.02);
 for(x=carrier_x){''')
def save(n,s):
 d=P/n;d.mkdir(exist_ok=True);(d/(n+'.scad')).write_text(s)
save('parent_direct_frame',src)
save('parent_td_support','''// TD04A support only. Camera has no angle bracket.
wall=8; x0=20; width=85; rear_y=-67; top_z=-12; bottom_z=-54;
td_x=55; td_z=-35; pitch=36;
$fn=48;
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
difference(){
 union(){
  translate([x0,rear_y,top_z-wall])rb([width,-rear_y,wall],2);
  translate([x0,-wall,bottom_z])rb([width,wall,top_z-bottom_z],2,"y");
 }
 for(x=[65,85])translate([x,-55,top_z-wall-.02])roof(5.5,wall+.04,-90);
 for(x=[td_x-pitch/2,td_x+pitch/2])translate([x,-wall-.02,td_z])rotate([-90,0,0])hole(4.5,wall+.04);
 translate([32,0,top_z-wall-.02])linear_extrude(wall+.04)polygon([[0,-16],[20,-16],[20,-33],[10,-43],[0,-33]]);
}
'''+helpers)
print('Direct horizontal camera fixing and TD-only support prepared')
