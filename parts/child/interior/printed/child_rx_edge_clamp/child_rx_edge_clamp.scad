// RX edge retention with M3 only; existing 2.2 mm PCB holes stay unused.
// Right-hand local part: board edge X=34, deck underside Y=-10.
// Mirror X for the left side; mirror local Z for upper mounting stations.
/* [Part] */
include <../../../../../scad/lib/child_interior_mounts.scad>
part="base"; // [base,cap,base_pair,cap_pair]
pair_pitch=34; // Existing stations at assembly Z140.5 and Z174.5.
edge_relief=0.2;
bridge_x=39.2; // Outside the existing X36 +/-2.55 mm cable corridor.
bridge_outer_x=42.2; // 3 mm bridge; inside tube, below upper flange insertion.
screw_x=37.5;
mount_offset=6;
board_edge=34;
edge_gap=0.35;
toe_x=31.8;
pilot_d=2.5;
clear_d=3.4;
head_clear_d=6.6;
$fn=48;
assert(screw_x-head_clear_d/2>board_edge && head_clear_d>=6.6,
       "M3 head reserve must stay outside the PCB edge");
module clamp_base() difference() {
    union() {
        // Deck-facing flat footprint: print RX-90, Y=-10 on the bed.
        translate([board_edge+edge_gap,-16,-3.5]) finished_box([6.15,6,mount_offset+7]);
        translate([board_edge+edge_gap,-18,-3.5]) finished_box([7.15,8,7]);
        // PCB backing ledge: 45 degree inward growth, contacts board Y=-16.
        translate([0,0,-3.5]) linear_extrude(7)
            polygon([[board_edge+edge_gap+0.1,-10],[board_edge+edge_gap+0.1,-16],
                     [toe_x,-16],[toe_x,-13.45]]);
    }
    // Mounting screw and clamp screw use different axes, never collide.
    translate([screw_x,-9.9,mount_offset]) rotate([90,0,0]) cylinder(d=pilot_d,h=4.5);
    translate([screw_x,-18.1,0]) rotate([-90,0,0]) cylinder(d=pilot_d,h=6);
}
module clamp_cap() difference() {
    union() {
        // Flat outside face: print RX90, Y=-20.6 on the bed.
        translate([toe_x,-20.6,-3.5]) finished_box([9.7,2.6,7]);
        translate([toe_x,-18,-3.5]) finished_box([board_edge+edge_gap-toe_x,0.4,7],0.1);
    }
    translate([screw_x,-20.7,0]) rotate([-90,0,0]) cylinder(d=clear_d,h=3);
    // Head remains outside a flat seat; 6.6 mm clear tool/head cylinder.
}

module finished_box(size,c=edge_relief) {
    if(part=="base_pair" || part=="cap_pair") ci_chamfer_box(size,c);
    else cube(size); // Historical individual variants remain unchanged.
}

// A bridge outside the PCB joins each side's two clamps. Original screw axes,
// board bearing faces and the gap to the board are retained.
module paired_clamp(is_base) {
    difference() {
    union() {
        for (upper=[false,true]) translate([0,0,upper ? pair_pitch : 0])
            scale([1,1,upper ? 1 : -1])
                if (is_base) clamp_base(); else clamp_cap();
        if (is_base)
            translate([bridge_x,-16,0])
                ci_chamfer_box([bridge_outer_x-bridge_x,6,pair_pitch],edge_relief);
        else
            translate([bridge_x,-20.6,0])
                ci_chamfer_box([bridge_outer_x-bridge_x,2.6,pair_pitch],edge_relief);
    }
    for (zz=[0,pair_pitch]) {
        translate([screw_x,is_base ? -18.1 : -20.7,zz]) rotate([-90,0,0])
            cylinder(d=is_base ? pilot_d : clear_d,h=is_base ? 6 : 3);
    }
    }
}
if(part=="base") clamp_base();
if(part=="cap") clamp_cap();
if(part=="base_pair") paired_clamp(true);
if(part=="cap_pair") paired_clamp(false);
