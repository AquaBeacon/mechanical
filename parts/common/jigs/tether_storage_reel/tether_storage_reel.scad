// Fathom 4-pair, purchased 30 m. Units: mm. See companion md for sources.
/* [Output] */
part = "base"; // [base,lid,assembly]
/* [Cable and capacity] */
cable_d = 7.6;
cable_length_m = 30;
min_bend_radius = 75; // Conservative static-radius interpretation
packing_factor = 0.65;
/* [Reel] */
core_d = 160;
flange_d = 240;
winding_width = 140;
flange_t = 4;
wall = 3.2;
hand_hole_d = 110;
rim_reserve = 8;
/* [Fasteners and locating lip] */
bolt_d = 4;
bolt_clearance = 0.5;
boss_d = 20;
boss_overlap = 1.2;
lip_h = 3;
lip_wall = 2.4;
lip_clearance = 0.4; // radial
/* [Band slots and edges] */
band_slot_w = 4;
band_slot_l = 18;
slot_edge = 3;
edge_chamfer = 0.5;
/* [Hidden] */
$fn = 192;
eps = 0.02;
inner_d = core_d - 2*wall;
bolt_r = inner_d/2 - boss_d/2 + boss_overlap;
slot_r = flange_d/2-slot_edge-band_slot_w/2;
capacity_m = packing_factor*((flange_d-2*rim_reserve)*(flange_d-2*rim_reserve)-core_d*core_d)*winding_width/(cable_d*cable_d)/1000;
assert(core_d/2 >= min_bend_radius);
assert(capacity_m >= cable_length_m, "Insufficient storage volume");
assert(bolt_r-boss_d/2 > hand_hole_d/2+2);
assert(bolt_r+boss_d/2 < core_d/2);
assert(flange_t > 2*edge_chamfer && wall >= 2.4);
assert(lip_wall > 0 && lip_h < winding_width);
assert(slot_r-band_slot_w/2 > (flange_d-2*rim_reserve)/2);
assert(part=="base" || part=="lid" || part=="assembly");
echo(capacity_m=capacity_m, assembled_height=winding_width+2*flange_t);

// Compensated polygon: flats lie on specified clearance diameter.
module hole(d,h,n=24) { cylinder(r=d/2/cos(180/n),h=h,$fn=n); }
module bolts(h,extra=0) {
    for(a=[0,120,240]) rotate([0,0,a]) translate([bolt_r,0,-eps])
        hole(bolt_d+bolt_clearance+extra,h+2*eps);
}
module flange() {
    difference() {
        union() {
            cylinder(d1=flange_d-2*edge_chamfer,d2=flange_d,h=edge_chamfer);
            translate([0,0,edge_chamfer]) cylinder(d=flange_d,h=flange_t-2*edge_chamfer);
            translate([0,0,flange_t-edge_chamfer]) cylinder(d1=flange_d,d2=flange_d-2*edge_chamfer,h=edge_chamfer);
        }
        translate([0,0,-eps]) cylinder(d=hand_hole_d,h=flange_t+2*eps);
        translate([0,0,-eps]) cylinder(d1=hand_hole_d+2*edge_chamfer,d2=hand_hole_d,h=edge_chamfer+eps);
        translate([0,0,flange_t-edge_chamfer]) cylinder(d1=hand_hole_d,d2=hand_hole_d+2*edge_chamfer,h=edge_chamfer+eps);
        for(a=[60,180,300]) rotate([0,0,a]) translate([slot_r-band_slot_w/2,-band_slot_l/2,-eps]) cube([band_slot_w,band_slot_l,flange_t+2*eps]);
        bolts(flange_t);
    }
}
module base() {
    difference() {
        union() {
            flange();
            translate([0,0,flange_t-eps]) difference() {
                cylinder(d=core_d,h=winding_width+eps);
                translate([0,0,-eps]) cylinder(d=inner_d,h=winding_width+3*eps);
            }
            for(a=[0,120,240]) rotate([0,0,a]) translate([bolt_r,0,flange_t-eps]) cylinder(d=boss_d,h=winding_width+eps);
        }
        bolts(flange_t+winding_width);
    }
}
module lid() {
    union() {
        flange();
        translate([0,0,flange_t-eps]) difference() {
            cylinder(d=inner_d-2*lip_clearance,h=lip_h+eps);
            translate([0,0,-eps]) cylinder(d=inner_d-2*(lip_clearance+lip_wall),h=lip_h+3*eps);
            for(a=[0,120,240]) rotate([0,0,a]) translate([bolt_r,0,-eps]) cylinder(d=boss_d+2*lip_clearance,h=lip_h+3*eps);
        }
    }
}
if(part=="base") base();
if(part=="lid") lid();
if(part=="assembly") {
    color("SlateGray") base();
    color("LightSteelBlue") translate([0,0,winding_width+2*flange_t]) rotate([180,0,0]) lid();
}
