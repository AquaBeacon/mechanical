// TD04A photo-style bent strap, Rev.6. Canonical editable source, mm.
// X = hole baseline; mounting face XZ at Y=0. Exterior interface Z=0.
// Parent hangs in -Z; child rises in +Z. Only photo metal portion is replaced.
// TD04A broad face is parallel XY, perpendicular to the fixing face XZ.
include <../../../../../scad/lib/td04a_interface.scad>
include <../../../../../scad/lib/child_horizontal_plate_interfaces.scad>
use <../../../../../scad/lib/edge_finished_profiles.scad>

/* [Bracket dimensions - design choices, not measured TD04A dimensions] */
variant="parent_down"; // [parent_down, child_side_up]
bracket_width=26;
foot_depth=42;
strap_length=75; // provisional: exterior contact to free end
wall=5;
sensor_offset=65; // wall (5) + cable clearance (60), measured to flange underside
/* [Exterior attachment - provisional interface] */
exterior_hole_d=5.5; // existing parent exterior M5 support holes
exterior_hole_pitch=20;
exterior_first_y=12;
/* [Child side attachment] */
child_reach=45;
child_side_depth=26;
child_sensor_x=32;
child_hole_y=14;
child_first_z=12;
child_side_pitch=hf_accessory_column_z[2]-hf_accessory_column_z[1];
/* [Edge finishing] */
edge_fillet_r=1.5;
root_fillet_r=3;
edge_chamfer=0.6;
hole_chamfer=0.3;
hole_tip_r=0.15;
/* [Hidden] */
$fn=48;
assert(td04a_mount_pitch==12 && td04a_mount_nominal==4);
assert(sensor_offset-wall==td04a_cable_clearance);
assert(wall>2*edge_fillet_r && wall>2*edge_chamfer);
assert(bracket_width>td04a_mount_pitch+9+2*edge_chamfer);
assert(exterior_first_y>wall+root_fillet_r+exterior_hole_d/2);
assert(foot_depth>exterior_first_y+exterior_hole_pitch+exterior_hole_d/2+edge_fillet_r);

module l_profile() {
    // Closing rounds the inside bend; opening rounds the external corners.
    offset(r=edge_fillet_r) offset(delta=-edge_fillet_r)
    offset(delta=-root_fillet_r) offset(r=root_fillet_r)
        polygon([[0,0],[foot_depth,0],[foot_depth,wall],
                 [wall,wall],[wall,strap_length],[0,strap_length]]);
}
module roof_hole(d) {
    // Compensated circular clearance with a 45-degree roof towards +X.
    // Manufacturing +X maps to build +Z, for BOTH functional hole axes.
    r=d/2;
    offset(r=hole_tip_r) offset(delta=-hole_tip_r) hull() {
        rotate(11.25) circle(r=r/cos(11.25),$fn=16);
        translate([sqrt(2)*r,0]) circle(r=0.001,$fn=12);
    }
}
module upward_strap() {
    difference() {
        // Local profile (u,v) -> world (Y,Z), extrusion -> world +X.
        multmatrix([[0,0,1,-bracket_width/2],[1,0,0,0],
                    [0,1,0,0],[0,0,0,1]])
            ef_profile(bracket_width,edge_chamfer) l_profile();
        for(x=[-td04a_mount_pitch/2,td04a_mount_pitch/2])
            translate([x,0,sensor_offset]) rotate([-90,0,0])
                ef_cut(wall,hole_chamfer) roof_hole(td04a_mount_clearance);
        for(y=[exterior_first_y,exterior_first_y+exterior_hole_pitch])
            translate([0,y,0]) ef_cut(wall,hole_chamfer) roof_hole(exterior_hole_d);
    }
}
module child_side_strap() {
    difference() {
        ef_profile(strap_length,edge_chamfer)
            offset(r=edge_fillet_r) offset(delta=-edge_fillet_r)
            offset(delta=-root_fillet_r) offset(r=root_fillet_r)
                polygon([[0,0],[child_reach,0],[child_reach,wall],
                         [wall,wall],[wall,child_side_depth],[0,child_side_depth]]);
        for(x=[child_sensor_x-td04a_mount_pitch/2,child_sensor_x+td04a_mount_pitch/2])
            translate([x,0,sensor_offset]) rotate([-90,0,0])
                ef_cut(wall,hole_chamfer) rotate(-90) roof_hole(td04a_mount_clearance);
        for(z=[child_first_z,child_first_z+child_side_pitch])
            multmatrix([[0,0,1,0],[1,0,0,child_hole_y],[0,1,0,z],[0,0,0,1]])
                ef_cut(wall,hole_chamfer) rotate(90) roof_hole(hf_m3_clearance);
    }
}
assert(variant=="parent_down" || variant=="child_side_up");
assert(sensor_offset>wall+root_fillet_r+9 && strap_length>sensor_offset+5);
module td04a_bracket_mount() {
    if(variant=="parent_down") mirror([0,0,1]) upward_strap();
    else child_side_strap();
}
td04a_bracket_mount();
