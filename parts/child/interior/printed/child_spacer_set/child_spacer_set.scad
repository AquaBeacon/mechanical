// Hexagonal slip spacers. M3 metal through-studs and nuts are separate COTS.
use <../../../../../scad/lib/child_interior_mounts.scad>

/* [Output] */
part = "set"; // [set,body10,body12,body30]
/* [Functional dimensions, mm] */
lengths = [10,10,12,30];
body_af = 5.5; // Across flats, within the original purchased hex envelope.
clear_d = 3.5; // Inscribed diameter: M3 slides through, no tapping.
hole_sides = 12;
corner_fillet = 0.2;
edge_chamfer = 0.2;
/* [Sacrificial connections] */
pitch = 10;
runner_y = -5;
runner_width = 2;
runner_height = 0.6;
neck_width = 0.8;
neck_height = 0.4; // Two layers at 0.2 mm; deliberately sharp fracture edges.
neck_overlap = 0.15;
$fn=64;

module body(h) {
    assert(h>2*edge_chamfer && edge_chamfer>0);
    assert((body_af-clear_d/cos(180/hole_sides))/2>0.9);
    difference() {
        hull() {
            linear_extrude(0.001) outline(edge_chamfer);
            translate([0,0,edge_chamfer]) linear_extrude(h-2*edge_chamfer) outline();
            translate([0,0,h-0.001]) linear_extrude(0.001) outline(edge_chamfer);
        }
        // Compensated dodecagon contains a true 3.5 mm circle throughout.
        translate([0,0,-0.01]) cylinder(d=clear_d/cos(180/hole_sides),h=h+0.02,$fn=hole_sides);
        translate([0,0,-0.01]) cylinder(d1=(clear_d+2*edge_chamfer+0.02)/cos(180/hole_sides),d2=clear_d/cos(180/hole_sides),h=edge_chamfer+0.01,$fn=hole_sides);
        translate([0,0,h-edge_chamfer]) cylinder(d1=clear_d/cos(180/hole_sides),d2=(clear_d+2*edge_chamfer+0.02)/cos(180/hole_sides),h=edge_chamfer+0.01,$fn=hole_sides);
    }
}

module outline(inset=0) {
    offset(delta=-inset) offset(r=corner_fillet) offset(delta=-corner_fillet)
        circle(d=body_af/cos(30),$fn=6);
}

if (part=="set") {
    assert(neck_height<runner_height && neck_height>edge_chamfer);
    union() {
        for(i=[0:len(lengths)-1]) {
            translate([i*pitch,0,0]) body(lengths[i]);
            // Neck reaches inside the bottom chamfer, keeping the first layer connected.
            translate([i*pitch-neck_width/2,runner_y+runner_width/2-neck_overlap,0])
                cube([neck_width,-body_af/2+edge_chamfer+neck_overlap-(runner_y+runner_width/2-neck_overlap),neck_height]);
        }
        translate([-body_af/2,runner_y-runner_width/2,0])
            ci_chamfer_box([(len(lengths)-1)*pitch+body_af,runner_width,runner_height],0.1);
    }
} else if(part=="body10") body(lengths[0]);
else if(part=="body12") body(lengths[2]);
else if(part=="body30") body(lengths[3]);
else assert(false,"Unknown spacer output");
