// Template: parameters and derived XZ profiles are written by generate.py.
// DJI layout: two identical short links + B-mounted hood with integral toe.
$fn=48; eps=.01;
module prism(h,c=edge_chamfer) {
    assert(h>2*c);
    // Local feature finishing: preserves concave toe/handle profiles. A hull
    // over a concave profile would erase its notch and collide with the keeper.
    translate([0,0,c]) minkowski() {
        linear_extrude(h-2*c) offset(delta=-c) children();
        // Exact axis vertices give flat seating planes and true edge chamfers.
        polyhedron(points=[[c,0,0],[-c,0,0],[0,c,0],[0,-c,0],[0,0,c],[0,0,-c]],
            faces=[[0,2,4],[2,1,4],[1,3,4],[3,0,4],[2,0,5],[1,2,5],[3,1,5],[0,3,5]]);
    }
}
module xz(y,t) { translate([0,y+t,0]) rotate([90,0,0]) linear_extrude(t) children(); }
module xzp(y,t,c=edge_chamfer) { translate([0,y+t,0]) rotate([90,0,0]) prism(t,c) children(); }
module finished2d(r=edge_fillet_r) { offset(r=r) offset(delta=-r) children(); }
module bore(h,d=pin_diameter+pin_clearance) {
    cd=d/cos(180/48);
    translate([0,0,-eps]) hole(d,h+2*eps,fn=48);
    cylinder(d1=cd+2*hole_chamfer,d2=cd,h=hole_chamfer);
    translate([0,0,h-hole_chamfer]) cylinder(d1=cd,d2=cd+2*hole_chamfer,h=hole_chamfer+eps);
}
module bore_y(y,h,x=0,z=0) { translate([x,y,z]) rotate([-90,0,0]) bore(h); }
module key(extra=0,extension=0) {
    hull() {
        translate([host_seam_x-.02,0,host_key_z]) rotate([0,90,0]) linear_extrude(.04)
            finished2d(.25) square(host_key_size+2*extra,center=true);
        translate([host_seam_x+host_key_length+extension-.02,0,host_key_z]) rotate([0,90,0]) linear_extrude(.04)
            finished2d(.25) square(host_key_tip+2*extra,center=true);
    }
}
module platform(fixed=true) {
    x0=fixed?-host_fixed_back:host_seam_x-catch_distance;
    x1=fixed?host_seam_x:host_moving_tail;
    thick=fixed?host_fixed_floor:host_floor;
    translate([0,0,-thick]) prism(thick) finished2d()
        translate([x0,-host_width/2]) square([x1-x0,host_width]);
}
module platform_bores(fixed=true) {
    thick=fixed?host_fixed_floor:host_floor;
    for(x=fixed?[platform_base_x1,platform_base_x2]:[platform_keeper_x],y=[-platform_mount_y,platform_mount_y])
        translate([x,y,-thick]) bore(thick,d=mount_diameter);
}
module base_profile() {
    difference() {
    finished2d() union() {
        translate([-base_eye_radius,-.3]) square([2*base_eye_radius,axis_height+.3]);
        translate([0,axis_height]) circle(r=base_eye_radius);
        polygon([[-9,-.3],[-base_eye_radius+1,-.3],[-base_eye_radius+1,2],[-6,2]]);
    }
    translate([host_seam_x-print_clearance,-1]) square([20,1]);
    }
}
module base() {
    difference() {
        union() {
            platform();
            xzp(-base_bearing_width/2,base_bearing_width) base_profile();
            // 0.8 mm root fillets along the sides of the A pedestal. The
            // links' lowest eye surface is z=1.6 mm, above these fillets.
            for(sign=[-1,1]) translate([-8,0,0]) rotate([0,90,0]) linear_extrude(9.5)
                scale([1,sign]) difference() {
                    translate([-.8,base_bearing_width/2-.2]) square([1.,1.]);
                    translate([-.8,base_bearing_width/2+.8]) circle(r=.8);
                }
            for(y=[-host_key_y,host_key_y]) translate([0,y,0]) key();
        }
        bore_y(-base_bearing_width/2-eps,base_bearing_width+2*eps,z=axis_height);
        platform_bores();
    }
}
// Link design coordinates A=(0,0), B=(AB_length,0). Same part, two copies.
module bail() {
    difference() {
        xzp(0,link_thickness) hull() for(x=[0,AB_length]) translate([x,0]) circle(r=eye_radius);
        for(x=[0,AB_length]) bore_y(-eps,link_thickness+2*eps,x=x);
        // The identical right copy has this recess on its inner face; its
        // outer face stays flat beneath the nut. Keep a straight bearing land.
        translate([0,0,0]) rotate([-90,0,0])
            cylinder(d1=head_diameter,d2=pin_diameter+pin_clearance,h=head_depth);
    }
}
// Profiles use closed-world XZ coordinates; output is local to closed B.
module hood_closed() {
    difference() {
        union() {
            for(y=[-hood_outer,hood_inner]) xzp(y,hood_cheek_thickness)
                finished2d() offset(delta=-root_fillet) offset(r=root_fillet) union() {
                    polygon(hood_side_points);
                    translate(B_closed) circle(r=eye_radius);
                    // Form the neck/rib junction as one filleted XZ profile,
                    // rather than leaving a sharp union edge at the claw root.
                    polygon(toe_neck_points);
                }
            xzp(-claw_width/2,claw_width,.15)
                offset(delta=-root_fillet) offset(r=root_fillet) polygon(toe_neck_points);
            translate([0,0,hood_top-hood_roof_thickness]) prism(hood_roof_thickness)
                finished2d() translate([handle_back,-hood_width/2])
                    square([catch_distance+claw_neck_width-handle_back,hood_width]);
            xzp(-handle_width/2,handle_width) finished2d() polygon(handle_points);
        }
        bore_y(-handle_width/2-eps,handle_width+2*eps,x=B_closed[0],z=B_closed[1]);
        // At a higher closed B position the roof reaches the real washer,
        // cap and nut. Relieve only outside the cheek bearing surfaces.
        for(y=[-handle_width/2-eps,hood_outer])
            xzp(y,handle_width/2-hood_outer+eps,.15)
                translate(B_closed) circle(r=washer_diameter/2+print_clearance);
        // The inside of the hood clears the entire two-link sweep, including
        // lifting the released claw. Side cheeks remain outside these slots.
        // Slightly enter the cheek instead of ending exactly on its inner
        // plane: coincident CGAL cut/union planes created collinear facets.
        xzp(-hood_inner-.15,2*(hood_inner+.15),.15)
            union() for(q=A_hardware_sweep) hull() {
                translate(q) circle(r=eye_radius+print_clearance);
                translate(B_closed) circle(r=eye_radius+print_clearance);
            }
        // Clearance for real A head, nut and projecting shaft over the sweep.
        for(y=[-hood_outer-eps,hood_inner-eps]) xzp(y,hood_cheek_thickness+2*eps,.15)
            union() for(q=A_hardware_sweep) translate(q) circle(r=axis_access_radius);
    }
}
module lever() { translate([-B_closed[0],0,-B_closed[1]]) hood_closed(); }
module keeper() {
    difference() {
        platform(false);
        xz(-receiver_pocket_width/2,receiver_pocket_width) polygon(keeper_void_points);
        // Side entrances have explicit 45-degree relief; do not alter 80deg face.
        for(y=[-receiver_pocket_width/2-edge_chamfer,receiver_pocket_width/2])
            xz(y,edge_chamfer) offset(delta=edge_chamfer) polygon(keeper_void_points);
        for(y=[-host_key_y,host_key_y]) translate([-catch_distance,y,0]) key(host_key_fit,host_key_end_clearance);
        platform_bores(false);
    }
}
// Installed geometric envelope of three purchased EPDM sheets, not printable.
module epdm() { xz(-epdm_width/2,epdm_width) polygon(epdm_points); }
module rod(y,l,d=pin_diameter) { translate([0,y,0]) rotate([-90,0,0]) cylinder(d=d,h=l); }
module nut(y,h) { translate([0,y,0]) rotate([-90,0,0]) cylinder(d=nut_af/cos(30),h=h,$fn=6); }
module washer(y) {
    translate([0,y,0]) rotate([-90,0,0]) difference() {
        cylinder(d=washer_diameter,h=washer_thickness);
        cylinder(d=pin_diameter+.3,h=washer_thickness+eps);
    }
}
module axis_a() {
    rod(-link_outer,axis_a_length);
    translate([0,-link_outer,0]) rotate([-90,0,0]) cylinder(d1=head_diameter-.1,d2=pin_diameter,h=head_depth);
    nut(link_outer,standard_nut_height);
}
module axis_b() {
    start=-hood_outer-washer_thickness;
    rod(start,axis_b_length);rod(start-socket_head_height,socket_head_height,socket_head_diameter);
    washer(start);washer(hood_outer);nut(hood_outer+washer_thickness,standard_nut_height);
}
assert(groove_angle_deg==80 && design_clamp_force_N==40);
assert(host_floor+pocket_floor>=2 && host_fixed_floor>=4);
assert(hood_width>2*hood_outer && receiver_pocket_width>claw_width+2*print_clearance);
assert(preload>0 && preload<epdm_thickness*.5);
assert(host_key_size+2*host_key_fit<host_fixed_floor-1);
assert(hood_top-hood_roof_thickness>axis_height+base_eye_radius+print_clearance);
assert(handle_back<B_closed[0]-20);
if(part=="base") base();
else if(part=="bail") bail();
else if(part=="lever") lever();
else if(part=="keeper") keeper();
else if(part=="epdm") epdm();
else if(part=="axis_a") axis_a();
else if(part=="axis_b") axis_b();
else if(part=="assembly") {
    color("SlateGray") base();
    for(y=[-link_outer,link_inner]) color("Orange") translate([0,y,axis_height]) rotate([0,-closed_angle_deg,0]) bail();
    color("SteelBlue") translate([B_closed[0],0,B_closed[1]]) lever();
    color("SeaGreen") translate([catch_distance,0,0]) keeper();
    color("Black") translate([catch_distance,0,0]) epdm();
    color("Silver") {translate([0,0,axis_height]) axis_a();translate([B_closed[0],0,B_closed[1]]) axis_b();}
} else assert(false,"Unknown part");
