// Parent lower assembly. mm. Purchased TD04A dimensions are PROVISIONAL.
/* [Fin cartridge] */
disk_d=225;
disk_t=5;
fin_h=125;
fin_w=65;
fin_t=4;
socket_outer=46;
beam_size=32;
beam_clear=0.5;
/* [Sensor carrier] */
carrier_w=210;
carrier_h=141;
carrier_t=8;
carrier_back=-75;
camera_x=-45;
camera_z=-110;
td_x=65;
td_z=-100;
/* [TD04A clamp: measure before printing] */
td_d=26;
td_len=55;
clamp_gap=0.5;
grip_h=32;
$fn=64;
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
module yhole(d,h){rotate([-90,0,0])hole(d,h);}

module cartridge(){
 assert(disk_d+10<=236 && fin_h+disk_t<=250);
 difference(){
  union(){
   cylinder(d=disk_d,h=disk_t,$fn=128);
   translate([-socket_outer/2,-socket_outer/2,disk_t])cube([socket_outer,socket_outer,fin_h]);
   for(a=[0:90:270])rotate([0,0,a])translate([socket_outer/2-0.2,-fin_t/2,disk_t])cube([fin_w+0.2,fin_t,fin_h]);
   for(x=[-23,23])for(y=[-23,23])translate([x,y,disk_t])cylinder(d=12,h=12);
  }
  translate([-(beam_size+beam_clear)/2,-(beam_size+beam_clear)/2,disk_t])cube([beam_size+beam_clear,beam_size+beam_clear,fin_h+1]);
  // Access to ballast bolt heads: open corner channels, not captive inaccessible pockets.
  for(x=[-23,23])for(y=[-23,23]){
   translate([x,y,-1])hole(5.5,19);
   translate([x,y,17])hole(12,fin_h);
  }
  for(z=[29,122])translate([-socket_outer/2-1,10,z])rotate([0,90,0])hole(6.5,socket_outer+2);
  for(x=[-75,75])for(y=[-50,-25])translate([x,y,-1])hole(5.5,disk_t+2);
  // Central M8 ballast screw access, its head remains inside the beam's existing recess.
  translate([0,0,-1])hole(18,disk_t+2);
 }
}

// Native Z=0 meets underside of disk. Rear plate is also the camera/TD mounting face.
module carrier(){
 difference(){
  union(){
   translate([-carrier_w/2,carrier_back,-carrier_h])cube([carrier_w,carrier_t,carrier_h]);
   difference(){
    translate([-carrier_w/2,carrier_back,-carrier_t])cube([carrier_w,55,carrier_t]);
    translate([0,0,-carrier_t-1])cylinder(r=64,h=carrier_t+2);
   }
  }
  for(x=[-75,75])for(y=[-50,-25])translate([x,y,-carrier_t-1])hole(5.5,carrier_t+2);
  for(x=[-11,11])for(z=[-16,16])translate([camera_x+x,carrier_back-1,camera_z+z])yhole(5.5,carrier_t+2);
  for(x=[-25,25])for(z=[-23,23])translate([td_x+x,carrier_back-1,td_z+z])yhole(5.5,carrier_t+2);
  // Clamp through-bolts also pass through carrier, retaining the split clamp with real nuts.
  for(x=[-22,22])translate([td_x+x,carrier_back-1,td_z])yhole(4.5,carrier_t+2);
  // Cable lacing eyes; no cut connector required to route cable alongside the plate.
  for(z=[-25,-50])for(x=[-45,65])translate([x,carrier_back-1,z])yhole(8,carrier_t+2);
 }
}

// Local mounting face Y=0, cylinder axis Z, center Y=27. Grip height 32.
module td_clamp(cap=false){
 assert(td_d>0 && td_d<32 && td_len>=grip_h);
 difference(){
  if(!cap)union(){
   translate([-32,0,-30])cube([64,8,60]);
   translate([-29,8,-grip_h/2])cube([58,19,grip_h]);
  }else translate([-29,27+clamp_gap,-grip_h/2])cube([58,19,grip_h]);
  translate([0,27,-grip_h/2-1])hole(td_d,grip_h+2);
  for(x=[-22,22])translate([x,-1,0])yhole(4.5,50);
  if(!cap)for(x=[-25,25])for(z=[-23,23])translate([x,-1,z])yhole(5.5,10);
 }
}
