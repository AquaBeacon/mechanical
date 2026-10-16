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

/* [Support reduction / modest lightening] */
lm_plate_window_w = 20;
lm_plate_window_h = 30;
lm_side_window_w = 14;
lm_side_window_h = 46;
lm_side_window_offset = 10;
lm_ramp_rise = 1.4; // Steeper than 45 degrees for slicer/process margin

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
    // Peaked roof steeper than 45 degrees; full M3 circle remains clear.
    r=d/2/cos(180/24);
    translate([x,0,z]) prism_y([[-r/sqrt(2),r/sqrt(2)],[r/sqrt(2),r/sqrt(2)],[0,r*1.7]],y,h);
}
module prism_y(points,y,h) {
    translate([0,y+h,0]) rotate([90,0,0]) linear_extrude(h) polygon(points);
}
module diamond_y(x,z,w,h,y,depth) {
    translate([x,0,z]) prism_y([[-w/2,0],[0,-h/2],[w/2,0],[0,h/2]],y,depth);
}
assert(lm_plate_window_h>=lm_plate_window_w && lm_side_window_h>=lm_side_window_w,"Window roof must be at least 45 degrees");
assert(17-lm_plate_window_w/2>lm_spine_width/2,"Keep central spine");
assert(lm_side_window_h/2<lm_ear_z-lm_ear_height/2,"Keep clamp bands");
module sleeve() {
    translate([0,lm_cy,-lm_holder_length/2]) cylinder(r=lm_ro,h=lm_holder_length);
}
// Integral fixtures reuse the identical shell, ears, bore and clamp locations.
// The legacy plate/spine is optional; existing base/cap branches keep it.
module half_holder(front=false,mount_plate=true) {
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
            for(sign=[-1,1]) {
                // Upper ears grow out of the cylinder at about 54 degrees.
                scale([sign,1,1]) prism_y([
                    [lm_ro-3,lm_ear_z-lm_ear_height/2-lm_ramp_rise*(lm_ear_x+lm_ear_width/2-(lm_ro-3))],
                    [lm_ear_x+lm_ear_width/2,lm_ear_z-lm_ear_height/2],
                    [lm_ro-3,lm_ear_z-lm_ear_height/2+lm_e]],
                    front?lm_cy+lm_split_gap/2:lm_cy-lm_split_gap/2-lm_ear_t,lm_ear_t);
                // Lower ears start on the bed, rather than 1 mm above it.
                translate([sign*lm_ear_x-lm_ear_width/2,front?lm_cy+lm_split_gap/2:lm_cy-lm_split_gap/2-lm_ear_t,-lm_holder_length/2])
                    cube([lm_ear_width,lm_ear_t,lm_ear_end_margin+lm_e]);
            }
            if(!front && mount_plate) {
                translate([-mount_width/2,0,-mount_height/2]) cube([mount_width,lm_plate_t,mount_height]);
                // Foot joins plate, spine and sleeve on the first layer.
                foot_drop=(lm_holder_length-mount_height)/2;
                prism_y([[-mount_width/2+foot_drop/lm_ramp_rise,-lm_holder_length/2],
                         [mount_width/2-foot_drop/lm_ramp_rise,-lm_holder_length/2],
                         [mount_width/2,-mount_height/2+lm_e],[-mount_width/2,-mount_height/2+lm_e]],0,lm_plate_t);
                translate([-lm_spine_width/2,lm_plate_t-lm_e,-lm_holder_length/2])
                    cube([lm_spine_width,lm_cy-lm_plate_t,(lm_holder_length+lm_spine_height)/2]);
            }
        }
        translate([0,lm_cy,-lm_holder_length/2-lm_e]) cylinder(d=lm_holder_id,h=lm_holder_length+2*lm_e);
        for(x=[-lm_ear_x,lm_ear_x],z=[-lm_ear_z,lm_ear_z])
            bore_y(x,lm_cy-lm_ear_t-lm_split_gap,z,lm_clamp_clear_d,2*(lm_ear_t+lm_split_gap));
        if(!front && mount_plate) for(h=lm_mount_features) bore_y(h[0],-lm_e,h[1],m3_clearance_d,lm_plate_t+2*lm_e);
        if(!front && mount_plate) for(x=[-17,17]) diamond_y(x,0,lm_plate_window_w,lm_plate_window_h,-lm_e,lm_plate_t+2*lm_e);
        // Side windows leave the full-diameter upper/lower clamping bands.
        for(y=[-lm_side_window_offset,lm_side_window_offset])
            translate([-lm_ro-lm_e,lm_cy,0]) rotate([90,0,90]) linear_extrude(2*lm_ro+2*lm_e)
                polygon([[y-lm_side_window_w/2,0],[y,-lm_side_window_h/2],[y+lm_side_window_w/2,0],[y,lm_side_window_h/2]]);
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
