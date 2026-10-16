// Photo-inspired reusable draw latch; NOT a DJI replacement part. mm.
// All dimensions provisional. Bambu Lab PETG Basic prototype; metal M3 axles.
use <../../../../scad/lib/util.scad>
/* [Output] */
part = "lever"; // [base,link,lever,keeper,epdm,axle_a,axle_b,assembly,open]
/* [Interface dimensions - provisional] */
link_length = 12;
closed_angle = 185;
catch_distance = 26;
axis_height = 10.5;
pad_thickness = 5;
pad_width = 46;
base_left = -17;
base_right = 9;
keeper_left = -16;
keeper_right = 3; // Cavity back is flush with the mounting plate edge.
keeper_pad_width = 48;
mount_y = 18;
keeper_mount_x = -12;
keeper_mount_x2 = -4;
keeper_mount_y = 19;
mount_d = 3.45;
keeper_adjust = 1.5;
/* [Moving parts] */
center_width = 8;
link_thickness = 4.8;
cheek_thickness = 4.8;
side_gap = 0.4;
eye_radius = 5.5;
roof_bottom = 10.5;
roof_thickness = 4.8;
hook_wall = 4.8;
hook_width = 20;
hook_depth = -2; // Raise the main jaw belly; separate reinforced toe sits below.
hook_tip_fillet = 2.5;
hook_tip_round = 0.8;
hook_back_clearance = 1;
root_fillet = 3;
lever_fillet = 2.5;
edge_round = 1;
/* [Integral printed keeper] */
catch_height = 8.5;
keeper_height = 16.5; // 4 mm lip above the lined cavity.
keeper_top_round = 1.2;
keeper_ridge_width = 30;
keeper_web_thickness = 14; // Groove leaves a 10 mm solid neck.
keeper_groove_depth = 4;
keeper_groove_bottom = 0; // Open to the plate edge: no floor beneath the hook.
keeper_groove_top = 12.5;
keeper_groove_radius = 3;
hook_toe_bottom = 6.4;
hook_toe_top = 10.6;
release_angle = 115;
/* [EPDM lining the complete FIXED cavity: back, roof and both sides] */
epdm_thickness = 1.0; // User's sheet. Assume solid EPDM; confirm foam/adhesive thickness before use.
epdm_precompression = 0.15; // Nominal closed squeeze, not material certification.
base_relief_thickness = 2.5;
/* [Metal hardware - verify purchased parts] */
axle_d = 3;
axle_hole = 3.45;
catch_clearance = 0.5;
axle_a_length = 25;
axle_b_length = 35;
/* [Hidden] */
$fn=64;
eps=0.02;
link_y = center_width/2+side_gap;
cheek_y = link_y+link_thickness+side_gap;
outer_y = cheek_y+cheek_thickness;
roof_top = roof_bottom+roof_thickness;
catch_r = keeper_web_thickness/2+catch_clearance;
bx = link_length*cos(closed_angle);
bz = link_length*sin(closed_angle);
lever_length = sqrt(pow(catch_distance-bx,2)+pow(catch_height-axis_height-bz,2));
stop_z = axis_height+bz-eye_radius;
epdm_closed_thickness = epdm_thickness-epdm_precompression;
keeper_groove_width = hook_width+2*(epdm_thickness+side_gap);
epdm_width = keeper_groove_width-2*epdm_thickness;
epdm_main_length = keeper_groove_top-keeper_groove_radius
    +PI/2*(keeper_groove_radius-epdm_thickness/2)
    +keeper_groove_depth-keeper_groove_radius;
hook_underlap = keeper_groove_depth-epdm_closed_thickness;
hook_tip_x = keeper_web_thickness/2-hook_underlap;
assert(stop_z>base_relief_thickness && roof_bottom>eye_radius);
assert(epdm_precompression>0 && epdm_precompression<epdm_thickness);
assert(keeper_right==keeper_web_thickness/2-keeper_groove_depth);
assert(keeper_groove_radius>epdm_thickness);
assert(hook_toe_bottom>keeper_groove_bottom && hook_toe_top<keeper_groove_top);
assert(hook_underlap>0 && hook_underlap<keeper_groove_depth);
assert(keeper_ridge_width>hook_width+2*side_gap && keeper_ridge_width<pad_width);
assert(keeper_height>catch_height && catch_height>=pad_thickness+root_fillet);
assert(closed_angle>180 && closed_angle<210);

function latch_b(theta=closed_angle) = [link_length*cos(theta),0,axis_height+link_length*sin(theta)];
function latch_cx(theta=closed_angle) = link_length*cos(theta)+sqrt(lever_length*lever_length-pow(catch_height-axis_height-link_length*sin(theta),2));
function latch_phi(theta=closed_angle) = asin((catch_height-axis_height-link_length*sin(theta))/lever_length);

// XZ profile extruded along +Y. Local 2D Y maps to world Z.
module profile_y(y,t) { translate([0,y+t,0]) rotate([90,0,0]) linear_extrude(t) children(); }
module axle_cut(y,len) { translate([0,y,0]) rotate([-90,0,0]) hole(axle_hole,len,fn=24); }
module rounded_pad(x0,length,width=pad_width) {
    translate([x0,-width/2,0]) box_rounded(length,width,pad_thickness,2,0.3);
}
// Concave circular root fillets, additive, not merely a cosmetic outer round.
module root_haunches(y,t,half=eye_radius,sides=[-1,1]) {
    for(s=sides) scale([s,1,1]) profile_y(y,t)
        difference() {
            translate([half-eps,pad_thickness-eps]) square([root_fillet+eps,root_fillet+eps]);
            translate([half+root_fillet,pad_thickness+root_fillet]) circle(r=root_fillet);
        }
}
module softened_profile() {
    // Close concave corners by adding R2.5 material, then round convex R1 edges.
    offset(r=edge_round) offset(delta=-edge_round)
        offset(delta=-lever_fillet) offset(r=lever_fillet) children();
}
// For host integration use with_pad=false and merge root down to z=0.
module latch_base(with_pad=true,with_holes=true) {
    difference() {
        union() {
            if(with_pad) difference() {
                rounded_pad(base_left,base_right-base_left);
                // Rear relief allows B to sit below the pad top. Mounting strips
                // and the central A bearing keep the full 5 mm mounting pad.
                translate([base_left-eps,-outer_y-0.5,base_relief_thickness])
                    cube([1-base_left+eps,2*(outer_y+0.5),pad_thickness]);
            }
            translate([-eye_radius,-center_width/2,0]) cube([2*eye_radius,center_width,axis_height]);
            translate([0,-center_width/2,axis_height]) rotate([-90,0,0]) cylinder(r=eye_radius,h=center_width);
            root_haunches(-center_width/2,center_width);
            // Closed-position stop: both link eye bottoms rest here.
            translate([base_left,-link_y-link_thickness,0]) cube([-6-base_left,2*(link_y+link_thickness),stop_z]);
        }
        translate([0,0,axis_height]) axle_cut(-center_width/2-eps,center_width+2*eps);
        if(with_pad && with_holes) for(x=[-10,3],y=[-mount_y,mount_y])
            translate([x,y,-eps]) hole(mount_d,pad_thickness+2*eps,fn=24);
    }
}
// A at origin, B at +X. Thickness runs +Y; print with axle holes vertical.
module latch_link() {
    difference() {
        union() {
            profile_y(0,link_thickness) translate([0,-eye_radius]) square([link_length,2*eye_radius]);
            for(x=[0,link_length]) translate([x,0,0]) rotate([-90,0,0]) cylinder(r=eye_radius,h=link_thickness);
        }
        for(x=[0,link_length]) translate([x,0,0]) axle_cut(-eps,link_thickness+2*eps);
    }
}
// Rounded outside profile; underside/root fillets are formed by the groove cut.
module keeper_profile(bottom=0) {
    w=keeper_web_thickness/2;
    offset(r=keeper_top_round) offset(delta=-keeper_top_round)
        translate([-w,bottom]) square([2*w,keeper_height-bottom]);
}
// Swept socket for a FIXED keeper, retaining the reinforced rear jaw.
// The positive retaining toe is added separately after this clearance is cut.
module keeper_socket() {
    intersection() {
        union() for(t=[release_angle:1:closed_angle-1]) hull() for(a=[t,min(t+1,closed_angle)])
            rotate(-latch_phi(a)) translate([catch_distance-latch_cx(a),-catch_height]) union() {
                offset(delta=catch_clearance) keeper_profile(bottom=-30);
                translate([0,-30]) square([keeper_web_thickness/2+hook_back_clearance,
                    keeper_height+catch_clearance+30]);
            }
        // Limit rear clearance so the structural jaw retains its wall thickness.
        rotate(-latch_phi(closed_angle)) translate([-100,-100])
            square([100+keeper_web_thickness/2+hook_back_clearance,200]);
    }
}
// B at origin; catch reference C at +X. U-shaped roof resembles photo lever.
module latch_lever() {
    union() {
    difference() {
        union() {
            for(y=[-outer_y,cheek_y]) profile_y(y,cheek_thickness) softened_profile()
                polygon([[-eye_radius,0],[-3,-eye_radius],[4,-eye_radius],[7,roof_bottom],
                    [lever_length+catch_r+hook_wall,roof_bottom],[lever_length+catch_r+hook_wall,roof_top],
                    [lever_length-4,roof_top],[-3,roof_top],[-eye_radius,6]]);
            translate([-3,-outer_y,roof_bottom]) cube([lever_length+3,2*outer_y,roof_thickness]);
            // Main hook body; positive undercut toe is added below separately.
            profile_y(-hook_width/2,hook_width) softened_profile()
                translate([lever_length-catch_r-hook_wall,-hook_depth])
                    square([2*(catch_r+hook_wall),roof_top+hook_depth]);
            // R3 hook-to-roof gussets in XZ, across the hook width.
            for(s=[-1]) translate([lever_length,0,0]) scale([s,1,1])
                profile_y(-hook_width/2,hook_width) difference() {
                    translate([catch_r+hook_wall-eps,roof_bottom-root_fillet]) square([root_fillet+eps,root_fillet+eps]);
                    translate([catch_r+hook_wall+root_fillet,roof_bottom-root_fillet]) circle(r=root_fillet);
                }
        }
        axle_cut(-outer_y-eps,2*outer_y+2*eps);
        profile_y(-hook_width/2-eps,hook_width+2*eps)
            translate([lever_length,0]) keeper_socket();
    }
    // Positive hook toe, under the keeper ledge. Add AFTER the socket cut so
    // the release clearance cannot erase the retaining feature.
    translate([lever_length,0,0]) rotate([0,latch_phi(closed_angle),0])
        profile_y(-hook_width/2,hook_width)
            offset(r=hook_tip_round) offset(delta=-hook_tip_round)
                offset(delta=-hook_tip_fillet) offset(r=hook_tip_fillet)
                polygon([[hook_tip_x,hook_toe_bottom-catch_height],
                    [catch_r+hook_wall,hook_toe_bottom-catch_height],
                    [catch_r+hook_wall,8],
                    [keeper_web_thickness/2+hook_back_clearance,8],
                    [keeper_web_thickness/2+hook_back_clearance,hook_toe_top-catch_height],
                    [hook_tip_x,hook_toe_top-catch_height]]);
    }
}
// Open-ended cavity profile; bottom rounding is below the mounting plane.
module keeper_groove_profile() {
    offset(r=keeper_groove_radius) offset(delta=-keeper_groove_radius)
        translate([keeper_right,-keeper_groove_radius-1])
            square([keeper_groove_depth+root_fillet+1,
                keeper_groove_top+keeper_groove_radius+1]);
}
module liner_clip() {
    translate([keeper_right,0]) square([keeper_groove_depth,keeper_groove_top]);
}
// Low rectangular ridge: full-width material directly joins the host.
module latch_keeper(with_pad=true,with_holes=true) {
    difference() {
        union() {
            if(with_pad) rounded_pad(keeper_left,keeper_right-keeper_left,keeper_pad_width);
            profile_y(-keeper_ridge_width/2,keeper_ridge_width) keeper_profile();
            root_haunches(-keeper_ridge_width/2,keeper_ridge_width,half=keeper_web_thickness/2,sides=[-1]);
        }
        // Central undercut: solid neck remains, side cheeks resist Y escape.
        profile_y(-keeper_groove_width/2,keeper_groove_width) keeper_groove_profile();
        if(with_pad && with_holes) for(y=[-keeper_mount_y,keeper_mount_y]) {
            // X-adjustable two-hole pattern, deliberately beyond pin supports.
            for(x=[keeper_mount_x,keeper_mount_x2]) hull() for(dx=[-keeper_adjust,keeper_adjust])
                translate([x+dx,y,-eps]) hole(mount_d,pad_thickness+2*eps,fn=24);
        }
    }
}
// Three purchased sheet pieces in KEEPER coordinates. Never print them.
module liner_nominal() {
    // Main bent strip covers the complete back and ceiling, between side sheets.
    profile_y(-epdm_width/2,epdm_width) intersection() {
        liner_clip();
        difference() { keeper_groove_profile(); offset(delta=-epdm_thickness) keeper_groove_profile(); }
    }
    for(y=[-keeper_groove_width/2,epdm_width/2])
        profile_y(y,epdm_thickness) intersection() { liner_clip(); keeper_groove_profile(); }
}
module latch_epdm(theta=closed_angle,free_angle=undef,uncompressed=false) {
    phi=is_undef(free_angle)?latch_phi(theta):free_angle;
    difference() {
        liner_nominal();
        // Geometric installed envelope only, not an elastomer constitutive model.
        if(!uncompressed) translate(latch_b(theta)-[catch_distance,0,0])
            rotate([0,-phi,0]) latch_lever();
    }
}
// Reserved metal envelopes, not printable hardware. Head + shank + nut space.
module metal_axle(span,length) {
    translate([0,-span/2,0]) rotate([-90,0,0]) {
        cylinder(d=axle_d,h=length);
        translate([0,0,-3]) cylinder(d=5.5,h=3);
        translate([0,0,span+0.5]) cylinder(d=6.4,h=4);
    }
}
module latch_assembly(theta=closed_angle,free_angle=undef) {
    b=latch_b(theta);
    phi=is_undef(free_angle)?latch_phi(theta):free_angle;
    color("SlateGray") latch_base();
    color("SteelBlue") translate([catch_distance,0,0]) latch_keeper();
    // Rubber is an envelope, not a constitutive deformation simulation.
    color("SeaGreen") translate([catch_distance,0,0]) latch_epdm(theta,free_angle);
    for(y=[-link_y-link_thickness,link_y]) color("Orange")
        translate([0,y,axis_height]) rotate([0,-theta,0]) latch_link();
    color("DimGray") translate(b) rotate([0,-phi,0]) latch_lever();
    color("Silver") {
        translate([0,0,axis_height]) metal_axle(2*(link_y+link_thickness),axle_a_length);
        translate(b) metal_axle(2*outer_y,axle_b_length);
    }
}
if(part=="base") latch_base();
else if(part=="link") latch_link();
else if(part=="lever") latch_lever();
else if(part=="keeper") latch_keeper();
else if(part=="epdm") latch_epdm();
else if(part=="epdm_nominal") liner_nominal();
else if(part=="epdm_side_template") translate([-keeper_right,0]) intersection() { liner_clip(); keeper_groove_profile(); }
else if(part=="epdm_main_template") square([epdm_main_length,epdm_width]);
else if(part=="axle_a") metal_axle(2*(link_y+link_thickness),axle_a_length);
else if(part=="axle_b") metal_axle(2*outer_y,axle_b_length);
else if(part=="assembly") latch_assembly();
else if(part=="open") latch_assembly(theta=release_angle,free_angle=30);
else if(part=="metrics") echo(METRICS=[link_length,closed_angle,catch_distance,axis_height,link_y,link_thickness,outer_y,keeper_ridge_width,keeper_web_thickness,lever_length,pad_thickness,mount_y,keeper_mount_x,catch_height,axle_a_length,axle_b_length,keeper_height,keeper_top_round,catch_clearance,epdm_thickness,epdm_precompression,epdm_width,keeper_groove_top,0,0,release_angle,keeper_groove_depth,keeper_groove_bottom,keeper_groove_top,hook_underlap,hook_toe_bottom,hook_toe_top,hook_width,hook_tip_fillet,hook_tip_round,keeper_groove_radius,keeper_left,keeper_right,keeper_pad_width,keeper_mount_y,keeper_mount_x2,keeper_groove_width,epdm_main_length]);
else assert(false,"Unknown part");
