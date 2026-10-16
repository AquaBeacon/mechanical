// Parent spar buoy exterior study, mm. Concept envelopes are NOT manufacturing parts.
/* [View] */
part = "assembly"; // [assembly,packed,disk,fin,hub,coupler,adapter]
/* [Fins] */
disk_d = 225; // [200:250]
disk_t = 5;
fin_h = 125; // [100:150]
fin_w = 65; // [50:80]
fin_t = 4;
/* [Demountable keel] */
spine_w = 25; // provisional square metal tube, confirm procurement
fit = 0.5;
hub_w = 60;
hub_h = 24;
bolt_d = 5.5;
root_depth = 12;
/* [Provisional envelopes - not sealed printable hulls] */
float_d = 180;
float_h = 300;
box_h = 100.3;
ballast_d = 90;
ballast_h = 35;
keel_h = 300;
$fn = 96;
eps = 0.05;
disk_z = -keel_h;
fin_z = disk_z + disk_t;
root_x = hub_w/2-root_depth;
assert(disk_d >= 200 && disk_d <= 250);
assert(fin_h >= 100 && fin_h <= 150 && fin_w >= 50 && fin_w <= 80);
assert(root_x > (spine_w+fit)/2+2);
assert(2*(root_x+fin_w) < disk_d);
assert(fin_h > 2*hub_h+20);
module hole(d,h) { cylinder(d=d/cos(180/32),h=h,$fn=32); }
module square_bore(h) { translate([-(spine_w+fit)/2,-(spine_w+fit)/2,-eps]) cube([spine_w+fit,spine_w+fit,h+2*eps]); }
module disk() {
 difference() {
  cylinder(d=disk_d,h=disk_t);
  square_bore(disk_t);
  for(a=[45:90:315]) rotate([0,0,a]) translate([hub_w/2,0,-eps]) hole(bolt_d,disk_t+2*eps);
 }
}
// Local fin: X radial, Y thickness, Z height. Two M5 bolts through each root.
module fin() {
 difference() {
  cube([fin_w,fin_t,fin_h]);
  for(z=[hub_h/2,fin_h-hub_h/2]) translate([root_depth/2,-eps,z]) rotate([-90,0,0]) hole(bolt_d,fin_t+2*eps);
 }
}
module hub() {
 difference() {
  cube([hub_w,hub_w,hub_h],center=true);
  translate([0,0,-hub_h/2]) square_bore(hub_h);
  for(a=[0:90:270]) rotate([0,0,a]) {
   translate([root_x-fit/2,-(fin_t+fit)/2,-hub_h/2-eps]) cube([root_depth+fit+eps,fin_t+fit,hub_h+2*eps]);
   translate([root_x+root_depth/2,-hub_w/2-eps,0]) rotate([-90,0,0]) hole(bolt_d,hub_w+2*eps);
  }
  // Disk fastening, accessible from either face (M5 through bolts and nuts).
  for(a=[45:90:315]) rotate([0,0,a]) translate([hub_w/2,0,-hub_h/2-eps]) hole(bolt_d,hub_h+2*eps);
 }
}
// Two 25 mm square tube segments join at Z=0; M6 removable through pins at +/-20.
module coupler() {
 difference() {
  translate([-20,-20,-40]) cube([40,40,80]);
  translate([0,0,-40]) square_bore(80);
  for(z=[-20,20]) translate([0,-21,z]) rotate([-90,0,0]) hole(6.5,42);
 }
}
// HP40 deck interface. Top face Z=60, blind square socket below the top plate.
module adapter() {
 difference() {
  union() {
   translate([-25,-25,50]) cube([50,50,10]);
   translate([-20,-20,0]) cube([40,40,50+eps]);
  }
  square_bore(50);
  for(x=[-20,20],y=[-20,20]) translate([x,y,49]) hole(bolt_d,12);
  translate([0,-21,25]) rotate([-90,0,0]) hole(6.5,42);
 }
}
module assembly() {
 color("DarkSlateGray") translate([-spine_w/2,-spine_w/2,disk_z-55]) cube([spine_w,spine_w,keel_h+55+float_h-70]);
 color("DarkOrange") coupler();
 color("DarkOrange") translate([0,0,float_h-120]) adapter();
 color("Orange") translate([0,0,disk_z]) disk();
 for(a=[0:90:270]) color("Gold") rotate([0,0,a]) translate([root_x,-fin_t/2,fin_z]) fin();
 for(z=[fin_z+hub_h/2,fin_z+fin_h-hub_h/2]) color("DarkOrange") translate([0,0,z]) hub();
 // Replace all following envelopes with confirmed COTS and attachment design.
 color("DimGray") translate([0,0,disk_z-ballast_h-10]) cylinder(d=ballast_d,h=ballast_h);
 color("LightSkyBlue",0.65) difference() {
  cylinder(d=float_d,h=float_h-60);
  translate([-21,-21,-eps]) cube([42,42,float_h]);
  translate([0,0,float_h-120]) cylinder(d=75,h=61);
 }
 color("DarkOrange") translate([0,0,float_h]) import("../../parts/parent/exterior/printed/parent_deck/parent_deck.stl");
 color("LightSteelBlue",0.5) translate([-105,-115,float_h]) import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
 // Lid, camera, GPS and IMU envelopes only; no invented mounting-hole pattern.
 color("LightSteelBlue",0.5) translate([-105,-115,float_h+box_h-4]) cube([210,230,4]);
 color("Black") translate([-35,-145,float_h+35]) cube([70,30,50]);
 color("Silver") translate([40,40,float_h+box_h]) cylinder(d=60,h=18);
 color("SeaGreen") translate([-15,-15,float_h+40]) cube([30,30,6]);
}
if(part=="assembly") assembly();
if(part=="disk") disk();
if(part=="fin") translate([0,fin_h,0]) rotate([90,0,0]) fin();
if(part=="hub") translate([0,0,hub_h/2]) hub();
if(part=="coupler") translate([0,0,40]) coupler();
if(part=="adapter") translate([0,0,60]) rotate([180,0,0]) adapter();
if(part=="packed") {
 color("Orange") disk();
 for(i=[0:3]) color("Gold") translate([disk_d/2+15+i*(fin_w+8),0,0]) rotate([90,0,0]) fin();
 for(i=[0:1]) color("DarkOrange") translate([-hub_w/2+i*(hub_w+10),-disk_d/2-hub_w,hub_h/2]) hub();
}
