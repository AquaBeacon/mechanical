// GENERATED: edit parameters.json, spec/over_center_latch/latch_body.scad and generate.py.
use <../../../../scad/lib/util.scad>
part="assembly";
AB_length=8.0;
closed_angle_deg=150;
open_angle=100;
release_angle=18.0;
catch_distance=12.399999999999999;
axis_height=6.0;
catch_height=-2.8;
groove_angle_deg=80.0;
toe_half_height=1.2;
toe_face_x=-2.8;
toe_right=1.2;
lip_end=-1.0;
contact_chamfer=0.15;
receiver_pocket_width=34.0;
keeper_recess_front=16.0;
pocket_floor=-6.0;
epdm_thickness=3.0;
epdm_height=1.8;
epdm_width=30.0;
preload=0.43277625052022883;
design_clamp_force_N=40.0;
design_hand_force_N=100.0;
design_safety_factor=3.0;
host_fixed_floor=6.0;
host_floor=8.0;
host_width=70.0;
host_fixed_back=55.0;
host_moving_tail=37.6;
host_seam_x=2.1;
platform_mount_y=30.0;
platform_base_x1=-26.0;
platform_base_x2=-8.0;
platform_keeper_x=18.6;
mount_diameter=3.5;
tool_diameter=8.0;
pin_diameter=3.0;
pin_clearance=0.3;
print_clearance=0.4;
base_bearing_width=8.0;
link_thickness=3.6;
hood_cheek_thickness=5.5;
eye_radius=4.4;
base_eye_radius=4.3;
hood_top=15.0;
hood_roof_thickness=4.0;
handle_back=-50.0;
handle_front=-14.0;
handle_width=44.0;
hood_width=34.0;
claw_width=30.0;
claw_neck_width=6.0;
edge_chamfer=0.25;
edge_fillet_r=0.6;
hole_chamfer=0.2;
root_fillet=1.2;
closed_height_limit=15.0;
axis_a_length=20.0;
axis_b_length=35.0;
head_diameter=6.2;
head_depth=1.8;
standard_nut_height=2.4;
nut_af=5.5;
socket_head_diameter=5.5;
socket_head_height=3.0;
washer_diameter=7.0;
washer_thickness=0.5;
host_key_y=22.0;
host_key_z=-2.5;
host_key_length=4.0;
host_key_size=3.0;
host_key_tip=1.8;
host_key_fit=0.15;
host_key_end_clearance=0.3;
BC_length=23.18230877438295;
hand_load_x=-47.0;
toe_contact_inset=0.1;
epdm_tangent_offset=-0.2;
claw_outer_underside_relief=0.4;
B_closed=[-6.92820323027551, 10.0];
toe_neck_points=[[9.38840762314984, -4.0], [13.599999999999998, -4.0], [18.4, -3.6], [18.4, 14.5], [12.099999999999998, 14.5], [12.099999999999998, 2.0], [13.599999999999998, -1.5999999999999999], [9.811592376850157, -1.5999999999999999]];
hood_side_points=[[-50.0, 15.0], [18.4, 15.0], [18.4, 1], [-3.9282032302755097, 1], [-3.9282032302755097, 9.0], [-9.92820323027551, 8.0], [-14.0, 4], [-50.0, 0]];
handle_points=[[-50.0, 0], [-47.0, 0], [-47.0, 11.0], [-14.0, 11.0], [-14.0, 15.0], [-50.0, 15.0]];
keeper_void_points=[[-5.935808256012258, -5.8], [-5.771073652153951, -6.0], [15.8, -6.0], [16.0, -5.8], [16.0, 5], [-1.0, 5], [-1.0, -1.45], [-1.15, -1.5999999999999999], [-5.195234937036705, -1.5999999999999999]];
epdm_points=[[-5.519234847638373, -3.437494802553002], [-5.206668127837898, -1.6648408471310279], [-2.6784462756331493, -2.1106345728914544], [-2.991012995433625, -3.8832885283134284]];
A_hardware_sweep=[[-3.593474117082797, 2.7281651736563104], [-3.4068342704295107, 2.8166887406549668], [-3.2259458879369802, 2.9082237365311334], [-3.050728771444597, 3.002486740197349], [-2.88108795457987, 3.0992132372293213], [-2.7169158054983082, 3.198157732943714], [-2.5580940580197256, 3.2990936566337625], [-2.4044957489513425, 3.4018130805946587], [-2.2559870437315066, 3.506126278853567], [-2.1124289368718268, 3.611861150930401], [-1.9736788178584934, 3.7188625355940648], [-1.839591897065385, 3.8269914385669717], [-1.7100224897346088, 3.9361241966009874], [-1.5848251591304585, 4.046151598436003], [-1.4638557225369349, 4.15697798098696], [-1.346972125840849, 4.268520316803779], [-1.2340351940376557, 4.3807073065120425], [-1.124909266148432, 4.493478487654277], [-1.0194627237877452, 4.6067833691765445], [-0.9175684230252505, 4.720580598790089], [-0.8191040392926743, 4.834837168613862], [-0.7239523349566692, 4.949527662887822], [-0.6320013588579263, 5.0646335501446575], [-0.5431445866555151, 5.180142521035131], [-0.45728101025334666, 5.29604787200981], [-0.37431518395984575, 5.412347934252135], [-0.29415723437104724, 5.529045546617146], [-0.21672284029635858, 5.646147570837372], [-0.14193318838365432, 5.763664446892678], [-0.06971490946033398, 5.881609786185646], [0.0, 6.0], [-3.593474117082797, 2.7281651736563104], [-3.7208930294130025, 2.6710736614806043], [-3.8492889195003026, 2.616214611264515], [-3.9786226767127766, 2.5636047336061694], [-4.108854904735095, 2.513260053983946], [-4.239945933569013, 2.465195907874957], [-4.371855831617242, 2.419426936083717], [-4.504544417846994, 2.375967080282404], [-4.637971274029523, 2.3348295787641034], [-4.772095757051899, 2.296026962410285], [-4.906877011297302, 2.2595710508737774], [-5.042273981090032, 2.2254729489783944], [-5.178245423201471, 2.193743043336286], [-5.314749919413166, 2.1643909991840875], [-5.451745889133223, 2.137425757438786], [-5.589191602062155, 2.112855531974235], [-5.727045190904339, 2.090687807119129], [-5.865264664121193, 2.070929335377202], [-6.003807918722217, 2.0535861353703524]];
axis_access_radius=4.2;
closed_angle=150;
lever_half=4.0;
base_inner=0;
base_outer=4.0;
link_inner=4.4;
link_outer=8.0;
hood_inner=8.4;
hood_outer=13.9;
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
