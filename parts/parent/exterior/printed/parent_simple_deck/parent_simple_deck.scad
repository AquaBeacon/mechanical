// Simple parent exterior. mm; box bottom is Z=0, underside is -plate_t.
// Mount holes are BLIND heat-set insert pilots, not printed threads.
/* [Deck] */
plate_x=236;
plate_y=236;
plate_t=12;
/* [Existing BCAS212310G mounting] */
box_pitch_x=192;
box_pitch_y=212;
box_hole=4.5;
nut_access_d=10;
nut_access_depth=4;
/* [Accessory mounts on underside] */
camera_center=[-48,0];
camera_pitch=[22,32];
td_center=[55,0];
td_pitch=[50,46];
insert_d=6.4;
insert_depth=8;
/* [Rope eyes outside box footprint] */
rope_x=112;
rope_y=75;
rope_d=8;
/* [Open cable exit at south edge] */
notch_x0=-30;
notch_x1=25;
notch_depth=8;
/* [Hidden] */
$fn=48;
eps=0.02;
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
mounts=concat([for(x=[-1,1],y=[-1,1])
 [camera_center[0]+x*camera_pitch[0]/2,camera_center[1]+y*camera_pitch[1]/2]],
 [for(x=[-1,1],y=[-1,1])
 [td_center[0]+x*td_pitch[0]/2,td_center[1]+y*td_pitch[1]/2]]);
assert(plate_t-insert_depth>=3,"Insert needs a closed roof >=3 mm");
assert(plate_t-nut_access_depth>=6);
assert(rope_x-rope_d/2>105,"Rope eyes must remain outside box cover");
assert(rope_x+rope_d/2+1.5<plate_x/2);
assert(plate_x+10<=256 && plate_y+10<=256);
for(p=mounts)assert(abs(p[0])+insert_d/2+4<plate_x/2 && abs(p[1])+insert_d/2+4<plate_y/2);
for(i=[0:len(mounts)-2],j=[i+1:len(mounts)-1])assert(norm(mounts[i]-mounts[j])>insert_d+4);
module deck(){
 difference(){
  translate([-plate_x/2,-plate_y/2,-plate_t])cube([plate_x,plate_y,plate_t]);
  for(x=[-box_pitch_x/2,box_pitch_x/2],y=[-box_pitch_y/2,box_pitch_y/2]){
   translate([x,y,-plate_t-eps])hole(box_hole,plate_t+2*eps);
   // Open underside recess for standard M4 nut and small socket driver.
   translate([x,y,-plate_t-eps])hole(nut_access_d,nut_access_depth+eps);
  }
  for(p=mounts)translate([p[0],p[1],-plate_t-eps])hole(insert_d,insert_depth+eps);
  for(x=[-rope_x,rope_x],y=[-rope_y,rope_y])translate([x,y,-plate_t-eps])hole(rope_d,plate_t+2*eps);
  translate([notch_x0,-plate_y/2-eps,-plate_t-eps])cube([notch_x1-notch_x0,notch_depth+eps,plate_t+2*eps]);
 }
}
deck();
