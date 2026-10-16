// mm. Local +Y points away from the vehicle; light axis Z.
// Installed: rotate Z 180 deg, then translate [0,-82,100].
include <../../../../../scad/lib/child_simple_frame.scad>

/* [Light holder] */
part = "base"; // [base,cap,assembly]
lm_holder_id = 33; // Reference holder bore, NOT a measured light diameter
lm_holder_length = 81;
lm_wall = 4;
lm_split_gap = 1.5;
lm_plate_t = 6;
lm_service_gap = 14;
lm_spine_width = 10;
lm_spine_height = 50;
lm_ear_width = 13;
lm_ear_height = 14;
lm_ear_t = 6;
lm_ear_end_margin = 1;
lm_clamp_clear_d = 3.45;
print_pose = false;

/* [Hidden] */
$fn = 96;
lm_e = 0.02;
lm_ro = lm_holder_id/2+lm_wall;
lm_cy = lm_plate_t+lm_service_gap+lm_ro;
lm_ear_x = lm_ro+lm_ear_width/2-1;
lm_ear_z = lm_holder_length/2-lm_ear_height/2-lm_ear_end_margin;
lm_mount_features = [for(x=[-mount_pitch/2,mount_pitch/2],z=[-mount_pitch/2,mount_pitch/2]) [x,z,5]];
assert(lm_holder_id>0 && lm_wall>=3 && lm_split_gap>0 && lm_split_gap<lm_wall);
assert(lm_spine_width/2+5 < mount_pitch/2,"Mount tool/spine collision");
assert(lm_service_gap>=12,"L-key access gap");
assert(lm_ear_width/2>lm_clamp_clear_d/2+3);
assert(lm_ear_height/2>lm_clamp_clear_d/2+3);
for(a=lm_mount_features) {
    assert(abs(a[0])+a[2] < mount_width/2);
    assert(abs(a[1])+a[2] < mount_height/2);
    for(b=lm_mount_features) if(a!=b)
        assert(norm([a[0]-b[0],a[1]-b[1]])>a[2]+b[2]);
}
module bore_y(x,y,z,d,h) {
    translate([x,y,z]) rotate([-90,0,0]) cylinder(d=d/cos(180/24),h=h,$fn=24);
}
module sleeve() {
    translate([0,lm_cy,-lm_holder_length/2]) cylinder(r=lm_ro,h=lm_holder_length);
}
module half_holder(front=false) {
    difference() {
        union() {
            intersection() {
                sleeve();
                translate([-lm_ro-lm_e,front?lm_cy+lm_split_gap/2:0,-lm_holder_length/2-lm_e])
                    cube([2*lm_ro+2*lm_e,front?lm_ro+lm_e:lm_cy-lm_split_gap/2,lm_holder_length+2*lm_e]);
            }
            for(x=[-lm_ear_x,lm_ear_x],z=[-lm_ear_z,lm_ear_z])
                translate([x-lm_ear_width/2,front?lm_cy+lm_split_gap/2:lm_cy-lm_split_gap/2-lm_ear_t,z-lm_ear_height/2])
                    cube([lm_ear_width,lm_ear_t,lm_ear_height]);
            if(!front) {
                translate([-mount_width/2,0,-mount_height/2]) cube([mount_width,lm_plate_t,mount_height]);
                translate([-lm_spine_width/2,lm_plate_t-lm_e,-lm_spine_height/2])
                    cube([lm_spine_width,lm_cy-lm_plate_t,lm_spine_height]);
            }
        }
        translate([0,lm_cy,-lm_holder_length/2-lm_e]) cylinder(d=lm_holder_id,h=lm_holder_length+2*lm_e);
        for(x=[-lm_ear_x,lm_ear_x],z=[-lm_ear_z,lm_ear_z])
            bore_y(x,lm_cy-lm_ear_t-lm_split_gap,z,lm_clamp_clear_d,2*(lm_ear_t+lm_split_gap));
        if(!front) for(h=lm_mount_features) bore_y(h[0],-lm_e,h[1],m3_clearance_d,lm_plate_t+2*lm_e);
    }
}
module selected() {
    if(part=="base") half_holder(false);
    else if(part=="cap") half_holder(true);
    else if(part=="assembly") {
        color("SteelBlue") half_holder(false);
        color("Orange") half_holder(true);
    } else assert(false,"Unknown part");
}
// Axis vertical: uninterrupted sleeve walls, no supports inside the bore.
if(print_pose) translate([0,0,lm_holder_length/2]) selected();
else selected();
