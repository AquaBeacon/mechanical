// Camera-only rotary joint, mm. Legacy light quick-release remains untouched.
// Female assembled face z=18.5; male face z=6. Male is flipped onto female.
use <../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes.scad>
use <edge_finished_profiles.scad>
$fn=48;
camera_qr_ear_center=52;
camera_qr_ear_width=10;
camera_qr_ear_inner=12;
camera_qr_ear_end=57;
camera_qr_ear_chamfer=.4;
camera_qr_screw_clearance=3.5;
camera_qr_nut_af=5.8;
camera_qr_nut_bottom=2;
camera_qr_nut_top=4.8;
camera_qr_screw_bottom=.5;
module camera_qr_ear(z,h,s) {
 translate([0,s*(camera_qr_ear_inner+camera_qr_ear_end)/2,z])
  ef_box(camera_qr_ear_width,camera_qr_ear_end-camera_qr_ear_inner,h,2,camera_qr_ear_chamfer);
}
// Round concave joins of the ears to the existing pad. The inner exclusion
// protects mating surfaces. 0.1 mm overlap avoids coincident boolean faces.
module camera_qr_roots(foot_width,z,h,round_foot=false) {
 difference() {
  translate([0,0,z]) ef_profile(h,.3) ef_plan_finish(1) union() {
   if(round_foot) circle(d=foot_width,$fn=64);
   else ef_round_rect(foot_width,foot_width,3);
   for(s=[-1,1])
    translate([0,s*(camera_qr_ear_inner+camera_qr_ear_end)/2])
     ef_round_rect(camera_qr_ear_width,camera_qr_ear_end-camera_qr_ear_inner,2);
  }
  translate([0,0,z-.1]) linear_extrude(h+.2)
   if(round_foot) circle(d=foot_width-.2,$fn=64);
   else ef_round_rect(foot_width-.2,foot_width-.2,2.9);
 }
}
module camera_qr_female_cuts() {
 for(s=[-1,1]) {
  translate([0,s*camera_qr_ear_center,camera_qr_screw_bottom])
   ef_poly_bore(camera_qr_screw_clearance,8-camera_qr_screw_bottom+.02,.25,8);
  // Allow a fully unthreaded shank to slide outward; retain hex shoulders.
  translate([0,0,4.92]) ef_cut(3.2,.15) hull() {
   translate([0,s*camera_qr_ear_center]) circle(d=3.6,$fn=48);
   translate([0,s*(camera_qr_ear_end+1)]) circle(d=3.6,$fn=48);
  }
  translate([0,s*camera_qr_ear_center,camera_qr_nut_bottom+.1])
   ef_cut(camera_qr_nut_top-camera_qr_nut_bottom-.2,.2)
    hull() {
     ef_hex(camera_qr_nut_af);
     translate([0,s*7]) square([camera_qr_nut_af,1],center=true);
    }
 }
}
module camera_qr_female() {
 difference() {
  union() {
   twist_female();
   for(s=[-1,1]) camera_qr_ear(0,8,s);
   camera_qr_roots(28,0,8,true);
   // Raise the annular land 0.5 mm to preserve the existing z=24.5
   // camera datum. Entry slots must remain open through the raised land.
   difference() {
    translate([0,0,17.98]) cylinder(d=28,h=.52);
    translate([0,0,17.97]) cylinder(d=14.6,h=.55);
    for(a=[80,260]) rotate([0,0,a])
     translate([0,-3.3,17.97]) cube([10.8,6.6,.55]);
   }
  }
  camera_qr_female_cuts();
 }
}
module camera_qr_male() {
 difference() {
  union() {
   twist_male();
   camera_qr_roots(40,0,6);
   camera_qr_roots(60,-6,6);
   for(s=[-1,1]) {
    camera_qr_ear(-6,12,s);
    // Fill old rubber recesses; rigid lands carry the clamping force.
    translate([s*10.5,0,5.7]) cube([5.5,8.5,.6],center=true);
   }
  }
  for(s=[-1,1]) translate([0,0,-6.01])
   ef_cut(12.02,.25) hull() {
    translate([0,s*camera_qr_ear_center]) circle(d=3.6,$fn=48);
    translate([0,s*(camera_qr_ear_end+1)]) circle(d=3.6,$fn=48);
   }
  // Clearance beneath lug bearing faces permits the rigid faces to close:
  // legacy nominal gap 0.5 mm plus 0.3 mm clearance; preserve 2.2 mm lug.
  difference() {
   translate([0,0,10.99]) cylinder(d=24,h=.81);
   translate([0,0,10.98]) cylinder(d=14,h=.85);
  }
 }
}

// Removable slotted spacer; open slot faces +X for both sides.
module camera_qr_spacer() {
 difference() {
  ef_box(14,10,10.5,1.2,.4);
  translate([0,0,-.01]) ef_cut(10.52,.25)
   hull() { circle(d=3.6,$fn=48); translate([8,0]) circle(d=3.6,$fn=48); }
 }
}
