// PETG adaptation of official WTE4 Rev C interfaces. Independent source.
include <../../../../../scad/lib/child_horizontal_plate_interfaces.scad>
use <../../../../../scad/lib/edge_finished_profiles.scad>
part="upper_linked"; // [upper_linked,lower_linked,upper,lower]
edge_chamfer=hf_edge_chamfer;
edge_fillet_r=hf_edge_fillet;
link_root_chamfer=hf_clamp_link_root;
$fn=96;
module clamp_outline() {
    ef_plan_finish(edge_fillet_r) union() {
        intersection() {
            circle(r=hf_clamp_r+hf_clamp_wall);
            translate([-84,hf_split_gap/2]) square([168,hf_clamp_mount_plane-hf_split_gap/2]);
        }
        // Flush official mounting face. Ring is locally clipped here; it has
        // no pad/ear extended radially toward the frame.
        translate([0,hf_clamp_mount_plane-3.9]) ef_round_rect(52,7.8,1);
        for(s=[-1,1]) translate([s*hf_ear_x,(hf_split_gap/2+hf_ear_height)/2])
            ef_round_rect(28,hf_ear_height-hf_split_gap/2,2);
    }
}
module mount_nut_channel(x,z,entry) {
    translate([x,hf_mount_nut_radius,z]) rotate([-90,0,0])
        linear_extrude(hf_nut_t) ef_hex(hf_nut_af);
    translate([x,hf_mount_nut_radius,(z+entry)/2]) rotate([-90,0,0])
        linear_extrude(hf_nut_t)
            ef_round_rect(hf_nut_af,abs(z-entry)+hf_nut_af/cos(30),0.25);
}
module clamp_half(lower=false) {
    difference() {
        ef_profile(hf_clamp_width,edge_chamfer) clamp_outline();
        ef_cut(hf_clamp_width,edge_chamfer) circle(r=hf_clamp_r);
        for(x=hf_mount_x,dy=hf_mount_axial) {
            z=hf_clamp_width/2+dy;
            translate([x,hf_clamp_mount_plane,z]) rotate([90,0,0])
                ef_bore(hf_m3_clearance,hf_clamp_mount_plane-53);
            mount_nut_channel(x,z,z<20 ? -4 : hf_clamp_width+4);
        }
        // Official three clamping axes: two on the left, one on the right.
        for(row=hf_ear_rows) {
            translate([row[0],hf_split_gap/2,hf_clamp_width/2+row[1]]) rotate([-90,0,0])
                ef_bore(hf_m3_clearance,hf_ear_height-hf_split_gap/2);
            if(lower)
                translate([row[0],hf_ear_height-hf_nut_t,hf_clamp_width/2+row[1]]) rotate([-90,0,0])
                    ef_cut(hf_nut_t,0.25) ef_hex(hf_nut_af);
        }
    }
}
module linked_half(lower=false) {
    pitch=max(hf_stations)-min(hf_stations);
    length=pitch+hf_clamp_width;
    radius=hf_clamp_r+hf_clamp_wall/2;
    // Two shoulder rails stay inside the original annular wall envelope.
    // The central mounting faces, axial nut entries and split remain accessible.
    assert(len(hf_stations)==2 && pitch>hf_clamp_width);
    assert(hf_clamp_link_t+2*link_root_chamfer<hf_clamp_wall);
    union() {
        for(z=[0,pitch]) translate([0,0,z]) clamp_half(lower);
        for(s=[-1,1])
            translate([s*radius*sin(hf_clamp_link_angle),radius*cos(hf_clamp_link_angle),0])
                rotate([0,0,-s*hf_clamp_link_angle]) {
                    ef_box(hf_clamp_link_width,hf_clamp_link_t,length,edge_fillet_r,edge_chamfer);
                    // Local 45-degree root relief at both inner band faces.
                    translate([0,0,hf_clamp_width-0.3])
                        ef_root(hf_clamp_link_width,hf_clamp_link_t,link_root_chamfer,edge_fillet_r);
                    translate([0,0,pitch+0.3]) rotate([180,0,0])
                        ef_root(hf_clamp_link_width,hf_clamp_link_t,link_root_chamfer,edge_fillet_r);
                }
    }
}
assert(part=="upper" || part=="lower" || part=="upper_linked" || part=="lower_linked");
if(part=="upper_linked" || part=="lower_linked") linked_half(part=="lower_linked");
else clamp_half(part=="lower");
