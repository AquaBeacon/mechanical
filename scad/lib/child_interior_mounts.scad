// Confirmed t200 battery/deck interfaces; mm. Plain purchased M3 nut AF5.5/t2.4.
// Shared by bay, removable floor and deck. No printed threads or metal inserts.
ci_box_hx=24;
ci_box_hz=[12,90];
ci_service_x=22.5;
ci_service_z=16;
ci_clear_d=3.4;
ci_nut_af=5.7; // 0.2 mm total clearance over the existing AF5.5 nut model
ci_nut_t=2.6;
ci_ear_depth=8;
ci_ear_outer_x=27.7; // cable rail starts at X28; do not enlarge further
ci_ear_half_z=7;
ci_service_half_z=7;
ci_service_outer_x=26;
ci_service_depth=9.0;
ci_service_nut_y=-36.5;
ci_edge_chamfer=0.3;
ci_edge_fillet_r=0.6;

// Nut flats face +/-X. Axis +Y, pocket is inserted from the outward X side.
module ci_nut_y(af=ci_nut_af,depth=ci_nut_t) {
    rotate([-90,0,0]) rotate([0,0,30])
        cylinder(d=af/cos(30),h=depth,$fn=6);
}

// Rectangular block with 0.3 mm edge relief, preserving its bounding box.
// The central flat faces retain the specified mounting planes.
module ci_chamfer_box(size,c=ci_edge_chamfer) {
    assert(min(size)>2*c);
    hull() {
        translate([c,c,0]) cube([size[0]-2*c,size[1]-2*c,size[2]]);
        translate([c,0,c]) cube([size[0]-2*c,size[1],size[2]-2*c]);
        translate([0,c,c]) cube([size[0],size[1]-2*c,size[2]-2*c]);
    }
}

// Finish an individual prism, with shrink/expand compensation preserving bounds.
// Apply to structural profiles before assembly booleans, never the full model.
module ci_rounded_extrude(h,r=ci_edge_chamfer) {
    assert(h>2*r);
    translate([0,0,r]) minkowski() {
        linear_extrude(h-2*r) offset(delta=-r) children();
        // OpenSCAD's faceted sphere has flattened poles. Compensate along the
        // extrusion axis so flat flange seats remain exactly at Z0 and Zh.
        scale([1,1,1/cos(180/12)]) sphere(r=r,$fn=12);
    }
}
