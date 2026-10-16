"""Apply fillets in printable profile planes; retain flat bearing and bed faces."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'parts/parent/exterior/printed'
helper='''
// Rounded profile extrusions preserve planar mating faces and bed contact.
module rz(s,r){
 assert(r>0 && 2*r<min(s[0],s[1]));
 union(){
  translate([r,0,0])cube([s[0]-2*r,s[1],s[2]]);
  translate([0,r,0])cube([s[0],s[1]-2*r,s[2]]);
  for(x=[r,s[0]-r],y=[r,s[1]-r])translate([x,y,0])cylinder(r=r,h=s[2],$fn=32);
 }
}
module rb(s,r=2,axis="z"){
 if(axis=="z")rz(s,r);
 if(axis=="y")translate([0,s[1],0])rotate([90,0,0])rz([s[0],s[2],s[1]],r);
 if(axis=="x")translate([0,0,s[2]])rotate([0,90,0])rz([s[2],s[1],s[0]],r);
}
// +X peak; rotate in bore plane so peak points upward in the supplied print STL.
module roof(d,h,angle=0){
 r=d/2/cos(180/32);
 rotate([0,0,angle])linear_extrude(height=h)union(){
  circle(r=r,$fn=32);
  polygon([[r/sqrt(2),-r/sqrt(2)],[sqrt(2)*r,0],[r/sqrt(2),r/sqrt(2)]]);
 }
}
'''
def load(n):return (P/n/(n+'.scad')).read_text()
def save(n,s):(P/n/(n+'.scad')).write_text(s+helper)
s=load('parent_light_frame')
s=s.replace('cube([8,32,32])','rb([8,32,32],3,"x")').replace('cube([rail,depth,thick])','rb([rail,depth,thick],3)').replace('cube([width,rail,thick])','rb([width,rail,thick],3)')
s=s.replace('hole(lug_hole,8.04)','roof(lug_hole,8.04)')
s=s.replace('translate([x,-clamp_y,-6])hole(10,6.02);','translate([x,-clamp_y,-2.45])cylinder(d1=5.5/cos(180/32),d2=10.4/cos(180/32),h=2.45+.02,$fn=32);')
s=s.replace('cube([10,60,thick+.04])','rb([10,60,thick+.04],3)').replace('cube([108,10,thick+.04])','rb([108,10,thick+.04],3)')
save('parent_light_frame',s)
s=load('parent_light_bar').replace('cube([width,depth,thickness])','rb([width,depth,thickness],3)').replace('cube([160,8,thickness+.04])','rb([160,8,thickness+.04],3)')
save('parent_light_bar',s)
s=load('parent_light_carrier').replace('cube([width,-rear_y,wall])','rb([width,-rear_y,wall],2)').replace('cube([width,wall,top_z-bottom_z])','rb([width,wall,top_z-bottom_z],2,"y")')
s=s.replace('for(x=[-50,-8,34])translate([x,-43,top_z-wall-.02])cube([20,27,wall+.04]);','''for(x=[-50,-8,34])translate([x,0,top_z-wall-.02])linear_extrude(height=wall+.04)
 polygon([[0,-16],[20,-16],[20,-33],[10,-43],[0,-33]]); // 45-degree roof, print up=-Y''')
s=s.replace('cube([c[2],wall+.04,c[3]])','rb([c[2],wall+.04,c[3]],2,"y")').replace('cube([6,wall+.04,14])','rb([6,wall+.04,14],2,"y")')
s=s.replace('hole(5.5,wall+.04);','roof(5.5,wall+.04,-90);',1)
save('parent_light_carrier',s)
# Separate rounded jaw; never mutate the earlier design's shared jaw.
n='parent_light_jaw';(P/n).mkdir(exist_ok=True)
s=load('parent_td_bracket_jaw').replace('cube([width,thick,height])','rb([width,thick,height],2,"y")')
save(n,s)
print('Rounded 4 parts; horizontal bores and flange windows have 45-degree roofs.')
