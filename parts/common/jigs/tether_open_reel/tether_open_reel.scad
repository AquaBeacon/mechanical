// Fathom standard 30 m, single winding chamber, access from BOTH side faces.
// Source dimensions shared by all variants. Units mm. PETG prototype.
/* [Output] */
part = "base"; // [base,lid,stand,cover_half,clip,coupon,assembly,closed,latch_detail]
/* [Cable] */
cable_d = 7.6;
cable_length_m = 30;
min_bend_radius = 75;
packing_factor = 0.65;
/* [Reel] */
core_d = 160;
flange_d = 230;
winding_width = 170;
flange_t = 5;
wall = 3.2;
hand_hole_d = 120;
end_slot_w = 14;
rim_reserve = 9;
/* [Side plate snap] */
spring_l = 30;
spring_t = 1.6;
spring_w = 10;
hook_depth = 1.5;
fit_clear = 0.4;
lip_h = 9;
lip_t = 2.4;
/* [Transport shell and clips] */
shell_clear = 0.6;
shell_wall = 2.4;
cover_lip = 3;
tab_depth = 9;
tab_half_w = 8;
tab_axial_w = 16;
clip_t = 1.2;
clip_gap = 16.4;
clip_l = 12;
clip_hook = 0.6;
/* [Stand] */
stand_w = 220;
stand_d = 190;
stand_floor = 10;
stand_rail_h = 40;
stand_rail_t = 8;
/* [Hidden] */
$fn=128;
eps=0.02;
core_r=core_d/2;
inner_r=core_r-wall;
rim_r=flange_d/2;
full_width=winding_width+2*flange_t;
core_top=flange_t+winding_width;
shell_r=rim_r+shell_clear+shell_wall;
tab_x=shell_r-tab_depth;
tab_z=[30,full_width-30];
spring_x=core_r-13;
boss_x=spring_x-3;
boss_len=core_r-boss_x;
boss_w=spring_w+8;
pocket_x=spring_x-1;
pocket_w=spring_t+6;
catch_print_z=flange_t+spring_l-6;
catch_world_z=full_width-catch_print_z;
window_top=catch_world_z+fit_clear;
window_bottom=full_width-(flange_t+spring_l)+2;
capacity_m=packing_factor*((flange_d-2*rim_reserve)*(flange_d-2*rim_reserve)-core_d*core_d)*winding_width/(cable_d*cable_d)/1000;
assert(core_r>=min_bend_radius);
assert(capacity_m>=cable_length_m,"Storage volume too small");
assert(shell_r*2<237 && full_width<237,"X1C print envelope exceeded");
assert(spring_x-hook_depth>hand_hole_d/2+3,"Latch blocks hand opening");
assert(pocket_x+ pocket_w < core_r-1,"Pocket breaks outer winding surface");
assert(pocket_x-spring_x+hook_depth>0,"No snap engagement");
assert(window_top>window_bottom && spring_l>20);
assert(tab_x>(flange_d-2*rim_reserve)/2+2,"Tabs enter winding volume");
assert(clip_gap>2*tab_half_w && clip_gap-2*clip_hook<2*tab_half_w,"Clip does not retain tabs");
assert(clip_l-clip_t>tab_depth+.5,"Clip pocket too short");
echo(capacity_m=capacity_m, assembled_width=full_width);

module ring(ro,ri,h) { difference() { cylinder(r=ro,h=h); translate([0,0,-eps]) cylinder(r=ri,h=h+2*eps); } }
module flange() {
 difference() {
  ring(rim_r,hand_hole_d/2,flange_t);
  // Open radial lead slot: installed connector need not fit through a hole.
  translate([hand_hole_d/2-1,-end_slot_w/2,-eps]) cube([rim_r-hand_hole_d/2+2,end_slot_w,flange_t+2*eps]);
 }
}
module receiver() {
 difference() {
  translate([boss_x,-boss_w/2,flange_t-eps]) cube([boss_len,boss_w,winding_width+eps]);
  // Open top pocket guides the spring. Window is reachable from central hole.
  translate([pocket_x,-spring_w/2-fit_clear,full_width-flange_t-spring_l-fit_clear])
   cube([pocket_w,spring_w+2*fit_clear,spring_l+2*fit_clear]);
  translate([boss_x-eps,-spring_w/2-fit_clear,window_bottom]) cube([pocket_x-boss_x+1,spring_w+2*fit_clear,window_top-window_bottom]);
 }
}
module base() {
 union() {
  flange();
  translate([0,0,flange_t-eps]) difference() {
   ring(core_r,inner_r,winding_width+eps);
   // Matching full-depth side-entry slot: inner cable lead remains accessible.
   translate([inner_r-1,-end_slot_w/2,-eps]) cube([wall+3,end_slot_w,winding_width+2*eps]);
  }
  for(a=[90,270]) rotate([0,0,a]) receiver();
 }
}
module spring() {
 // Beam bends outward; catch faces the hand opening, so it is finger-accessible.
 translate([spring_x,-spring_w/2,flange_t-eps]) cube([spring_t,spring_w,spring_l+eps]);
 translate([0,spring_w/2,0]) rotate([90,0,0]) linear_extrude(spring_w)
  polygon([[spring_x,catch_print_z],[spring_x-hook_depth,catch_print_z],
    [spring_x-hook_depth,catch_print_z+2],[spring_x,flange_t+spring_l-1]]);
}
module lid() {
 union() {
  flange();
  // Locating lip is interrupted at cable opening and two receiver columns.
  translate([0,0,flange_t-eps]) difference() {
   ring(inner_r-fit_clear,inner_r-fit_clear-lip_t,lip_h+eps);
   for(a=[90,270]) rotate([0,0,a]) translate([boss_x-1,-boss_w/2-fit_clear,-eps]) cube([boss_len+2,boss_w+2*fit_clear,lip_h+2*eps]);
   translate([inner_r-lip_t-2,-end_slot_w/2-fit_clear,-eps]) cube([wall+lip_t+5,end_slot_w+2*fit_clear,lip_h+2*eps]);
  }
  // Lid rotates 180 about X in assembly; 90/270 swap and remain matched.
  for(a=[90,270]) rotate([0,0,a]) spring();
 }
}
module cover_half() {
 // Printed at Z=0. Assembly shifts down by cover_lip + fit_clear.
 translate([0,0,cover_lip+fit_clear]) cover_geometry();
}
module cover_geometry() {
 difference() {
 union() {
  intersection() {
   union() {
    translate([0,0,-cover_lip-fit_clear]) ring(shell_r,rim_r+shell_clear,full_width+2*(cover_lip+fit_clear));
    // End stops enclose both side flanges with axial clearance; cover cannot slide off.
    for(z=[-cover_lip-fit_clear,full_width+fit_clear]) translate([0,0,z]) ring(shell_r,rim_r-2.5,cover_lip);
   }
   translate([-shell_r,0,-cover_lip-fit_clear]) cube([2*shell_r,shell_r,full_width+2*(cover_lip+fit_clear)]);
  }
  for(s=[-1,1],z=tab_z) {
   if(s==1) translate([tab_x,0,z-tab_axial_w/2]) cube([tab_depth,tab_half_w,tab_axial_w]);
   else translate([-shell_r,0,z-tab_axial_w/2]) cube([tab_depth,tab_half_w,tab_axial_w]);
  }
 }
 // Relief around clip arms: curved shell must not block the two jaws.
 for(s=[-1,1],z=tab_z) translate([s==1 ? tab_x : -shell_r-1,tab_half_w,z-tab_axial_w/2-fit_clear])
  cube([tab_depth+1,2*clip_t+fit_clear,tab_axial_w+2*fit_clear]);
 }
}
module clip() {
 // XY flexure printed flat; four removable clips join the two half shells.
 union() {
  for(s=[-1,1]) {
   translate([0,s==1 ? clip_gap/2 : -clip_gap/2-clip_t,0]) cube([clip_l,clip_t,tab_axial_w]);
   linear_extrude(tab_axial_w) polygon(s==1 ?
    [[0,clip_gap/2+eps],[1,clip_gap/2-clip_hook],[1.6,clip_gap/2-clip_hook],[1.6,clip_gap/2+eps]] :
    [[0,-clip_gap/2-eps],[1,-clip_gap/2+clip_hook],[1.6,-clip_gap/2+clip_hook],[1.6,-clip_gap/2-eps]]);
  }
  translate([clip_l-clip_t,-clip_gap/2-clip_t,0]) cube([clip_t,clip_gap+2*clip_t,tab_axial_w]);
 }
}
module stand() {
 union() {
  translate([-stand_w/2,-stand_d/2,0]) cube([stand_w,stand_d,stand_floor]);
  for(s=[-1,1]) difference() {
   translate([-stand_w/2,s==1 ? full_width/2-stand_rail_t : -full_width/2,stand_floor-eps]) cube([stand_w,stand_rail_t,stand_rail_h+eps]);
   translate([0,stand_d/2+1,stand_floor+shell_r]) rotate([90,0,0]) cylinder(r=shell_r+fit_clear,h=stand_d+2);
  }
 }
}
module coupon() {
 // Short upper core/receiver section, only one snap; matching local lid.
 if(coupon_side=="socket") intersection() {
  translate([-boss_x+3,0,-core_top+36]) receiver();
  translate([0,-boss_w/2-3,0]) cube([boss_len+7,boss_w+6,36]);
 }
 else union() {
  translate([0,-boss_w/2,0]) cube([boss_len+7,boss_w,flange_t]);
  translate([-boss_x+3,0,0]) spring();
 }
}
module reel() {
 color("SlateGray") base();
 color("Orange") translate([0,0,full_width]) rotate([180,0,0]) lid();
}
module transport() {
 color("LightSteelBlue") for(a=[0,180]) rotate([0,0,a]) translate([0,0,-cover_lip-fit_clear]) cover_half();
 for(s=[-1,1],z=tab_z) color("Tomato") {
  if(s==1) translate([shell_r-clip_l+clip_t,0,z-tab_axial_w/2]) clip();
  else rotate([0,0,180]) translate([shell_r-clip_l+clip_t,0,z-tab_axial_w/2]) clip();
 }
}
module assembly(closed=false) {
 color("DarkSlateGray") stand();
 translate([0,full_width/2,stand_floor+(closed ? shell_r : rim_r)]) rotate([90,0,0]) {
  reel(); if(closed) transport();
 }
}
coupon_side="socket"; // [socket,spring]
if(part=="base") base();
else if(part=="lid") lid();
else if(part=="stand") stand();
else if(part=="cover_half") cover_half();
else if(part=="clip") clip();
else if(part=="coupon") coupon();
else if(part=="assembly") assembly();
else if(part=="closed") assembly(true);
else if(part=="latch_detail") intersection() { reel(); translate([-12,boss_x-3,core_top-38]) cube([24,boss_len+8,45]); }
else assert(false,"Unknown part");
