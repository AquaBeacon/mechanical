// Horizontal child exterior. Dimensions in mm; finished fabrication prototype.
// concept.json retains the visual study. This source defines the bolt-on frame.
// It does not reconstruct or replace either existing topology-optimised part.
include <spec/clamp_interface.scad>
use <../../../../../scad/lib/util.scad>

/* [Variant] */
part = "side_front";
/* [Frame] */
side_x = 150;
panel_t = 12;
frame_half_length = 220;
foot_rail_half_length = 230;
frame_bottom = 10;
frame_top = 225;
rail_height = 26;
middle_height = 60;
joint_gap = 0.4;
shoe_y = 205;
lower_beam_y = 150;
rear_beam_y = -207;
rear_beam_z = 40;
ballast_y = -90;
light_seat_height = 32;
transducer_seat_height = 62;
/* [Fasteners and edge finish] */
m3_d = 3.5;
edge_chamfer = 0.6;
profile_radius = 2;
window_radius = 4;
washer_d = 7;
tool_d = 10;
nut_af = 5.8;
spacer_t = 1;
$fn = 40;

inner_face = side_x-panel_t/2;
clamp_face = abs(clamp_mount_y);
link_face = clamp_face+spacer_t;
link_length = inner_face-link_face;
middle_z = vessel_z;
clamp_y = [for(c=clamp_centres) vessel_y0+c];
clamp_z_offsets = [-clamp_frame_pitch/2,clamp_frame_pitch/2];
clamp_y_offsets = [for(z=clamp_bolt_zs) z-clamp_band_width/2];

assert(edge_chamfer>0 && 2*edge_chamfer<6);
assert(link_length>40 && middle_height>clamp_frame_pitch+12);
assert(joint_gap>0 && panel_t==12);
assert(2*shoe_y+70<=480);

// Local compensated chamfer: erosion before the octahedron keeps functional
// extents, openings and seating planes. This is applied to individual profiles.
module octa(r) {
    polyhedron(points=[[r,0,0],[-r,0,0],[0,r,0],[0,-r,0],[0,0,r],[0,0,-r]],
      faces=[[0,2,4],[2,1,4],[1,3,4],[3,0,4],
             [2,0,5],[1,2,5],[3,1,5],[0,3,5]]);
}
module profile_solid(t,c=edge_chamfer) {
    translate([0,0,c]) minkowski() {
        linear_extrude(height=t-2*c) offset(delta=-c) children();
        octa(c);
    }
}
module rr(w,h,r=profile_radius) {
    offset(r=r) square([w-2*r,h-2*r],center=true);
}
module finished_box(size) {
    profile_solid(size[2]) rr(size[0],size[1]);
}
module nut_slot(size) {
    // Rectangular drop-in access: the smaller edge relief preserves the flat
    // nut contact plane and clears the nut's full hexagonal envelope.
    profile_solid(size[2],0.3) rr(size[0],size[1],0.3);
}
module bore_z(d,t,c=edge_chamfer) {
    translate([0,0,-0.02]) hole(d,t+0.04,fn=24,through=false);
    cylinder(d1=d+2*c,d2=d,h=c+0.02,$fn=32);
    translate([0,0,t-c]) cylinder(d1=d,d2=d+2*c,h=c+0.02,$fn=32);
}
module axis_bore(p,axis,t,d=m3_d,tear=false,peak_y=false) {
    translate(p) rotate(axis=="X"?[0,90,0]:axis=="Y"?[-90,0,0]:[0,0,0]) {
        bore_z(d,t);
        // Compensated circle is the fit surface. Teardrop is extra roof relief.
        if(tear) rotate([0,0,axis=="X"?(peak_y?0:90):180])
            translate([0,0,-0.02]) teardrop(d,t+0.04);
    }
}
module slot_z(w,h,t) {
    translate([0,0,-0.02]) linear_extrude(t+0.04) rr(w,h,min(1,h/3));
    // Both entrance rims, preserving the central slot dimensions.
    hull() {
        translate([0,0,-0.02]) linear_extrude(0.02) rr(w+2*edge_chamfer,h+2*edge_chamfer,1);
        translate([0,0,edge_chamfer]) linear_extrude(0.02) rr(w,h,1);
    }
    hull() {
        translate([0,0,t-edge_chamfer]) linear_extrude(0.02) rr(w,h,1);
        translate([0,0,t]) linear_extrude(0.02) rr(w+2*edge_chamfer,h+2*edge_chamfer,1);
    }
}

function side_holes() = concat(
 [for(y=[-shoe_y,0,shoe_y]) for(dy=[-16,16]) [y+dy,20]],
 [for(y=clamp_y) for(dy=[-10,10]) [y+dy,middle_z]],
 [for(p=[[rear_beam_y,rear_beam_z+12],[lower_beam_y,24],[200,78]])
    for(dy=[-9,9]) [p[0]+dy,p[1]]],
 [for(y=[ballast_y-36,ballast_y+36]) [y,29]],
 [for(y=[-120,-100,-80,-60]) [y,152]],
 [for(y=[-18,18]) for(z=[frame_top-rail_height/2-6,frame_top-rail_height/2+6]) [y,z]],
 [for(y=[-26,26]) for(z=[middle_z-18,middle_z+18]) [y,z]],
 [for(z=[122,158]) [-214,z]]);

module side_profile() {
    difference() {
        union() {
            translate([0,(frame_bottom+frame_top)/2]) rr(2*frame_half_length,frame_top-frame_bottom);
            translate([0,frame_bottom+rail_height/2]) rr(2*foot_rail_half_length,rail_height);
        }
        translate([0,(frame_bottom+rail_height+middle_z-middle_height/2)/2])
            rr(2*(frame_half_length-rail_height),middle_z-middle_height/2-frame_bottom-rail_height,window_radius);
        translate([0,(middle_z+middle_height/2+frame_top-rail_height)/2])
            rr(2*(frame_half_length-rail_height),frame_top-rail_height-middle_z-middle_height/2,window_radius);
    }
}
module side_panel(front) {
    hs=side_holes();
    for(i=[0:len(hs)-1]) for(j=[0:len(hs)-1]) if(j>i)
        assert(norm(hs[i]-hs[j])>=washer_d+0.5,"Fastener seats overlap");
    difference() {
        profile_solid(panel_t) intersection() {
            side_profile();
            translate([front?joint_gap/2:-500,0]) square([500-joint_gap/2,500]);
        }
        for(p=hs) if(front?p[0]>0:p[0]<0) translate([p[0],p[1],0]) bore_z(m3_d,panel_t);
        // The cage screws are fitted after the side plates: straight driver
        // passages continue through the side panel and central splice plate.
        for(y=clamp_y) for(dy=clamp_y_offsets) for(dz=clamp_z_offsets)
            if(front?y+dy>0:y+dy<0) translate([y+dy,middle_z+dz,0]) bore_z(tool_d+0.5,panel_t);
        for(y=[-125,-45,45,125]) if(front?y>0:y<0)
            translate([y,18,0]) slot_z(14,4,panel_t);
    }
}
module splice(mid=false) {
    h=mid?52:26;
    difference() {
        finished_box([68,h,6]);
        for(x=mid?[-26,26]:[-18,18]) for(y=mid?[-18,18]:[-6,6]) translate([x,y,0]) bore_z(m3_d,6);
        if(mid) for(x=[-10,10]) translate([x,0,0]) bore_z(m3_d,6);
        if(mid) for(x=clamp_y_offsets) for(y=clamp_z_offsets)
            translate([x,y,0]) bore_z(tool_d+0.5,6);
    }
}

// Native connector coordinates: +X outward, Y vessel axis, Z vertical relative
// to vessel centre. Four cage holes, plus two independent frame screws.
module link() {
    difference() {
        translate([0,16,0]) rotate([90,0,0]) profile_solid(32) difference() {
            translate([(link_face+inner_face)/2,0]) rr(link_length,52);
            translate([(link_face+inner_face)/2,0]) rr(link_length-30,16,3);
        }
        for(y=clamp_y_offsets) for(z=clamp_z_offsets) {
            axis_bore([link_face,y,z],"X",8,m3_d,true,true);
            axis_bore([link_face+8,y,z],"X",inner_face-link_face-8+0.1,tool_d,true,true);
            echo(["HOLETABLE","cage",[link_face,y,z],[1,0,0],m3_d]);
        }
        for(y=[-10,10]) {
            axis_bore([inner_face-4,y,0],"X",4,m3_d,true,true);
            // Drop-in M3 nut, AF5.8. Flat nut seat at X=inner_face-4.
            translate([inner_face-6.1,y,-4.2]) nut_slot([4.2,7.4,33]);
            echo(["HOLETABLE","frame",[inner_face,y,0],[1,0,0],m3_d]);
        }
    }
}
module shoe() {
    difference() {
        // U section: 0.2 mm clearance per side; 5 mm floor and 8.8 mm cheeks.
        translate([0,35,0]) rotate([90,0,0]) profile_solid(70) difference() {
            translate([0,12]) rr(30,24);
            translate([0,30]) rr(panel_t+0.4,50,0.3);
        }
        for(y=[-16,16]) {
            axis_bore([-15,y,15],"X",30,m3_d,true);
            translate([-15.02,y,15]) rotate([0,90,0])
                linear_extrude(4.52) circle(d=nut_af/cos(30),$fn=6);
            translate([-15.02,y,15]) rotate([0,90,0]) cylinder(d1=8,d2=6.8,h=0.5,$fn=32);
            translate([-10.5,y,15]) rotate([0,90,0]) cylinder(d1=m3_d+0.8,d2=m3_d,h=0.4,$fn=32);
        }
    }
}

// Half beam: local X=joint gap/2..144; Y +/-19; Z=0..24. End nuts
// enter from +Z. The same geometry serves the lower and camera beams.
module cross_half() {
    difference() {
        translate([(joint_gap/2+inner_face)/2,0,0]) finished_box([inner_face-joint_gap/2,38,24]);
        for(y=[-9,9]) {
            // Tip relief beyond the captive nut, with the nut seat unchanged.
            axis_bore([inner_face-8,y,12],"X",8,m3_d,true);
            translate([inner_face-5.7,y,7.8]) nut_slot([3.4,7.4,18]);
        }
        for(z=[6,18]) axis_bore([18,-19,z],"Y",38,m3_d,true);
        // Optional camera deck. Both holes are outside the camera's base face.
        for(y=[-2,8]) translate([24,y,0]) bore_z(m3_d,24);
    }
}
module cross_splice() {
    difference() {
        finished_box([68,24,6]);
        for(x=[-18,18]) for(y=[-6,6]) translate([x,y,0]) bore_z(m3_d,6);
    }
}
module tray_half() {
    difference() {
        translate([(joint_gap/2+inner_face)/2,0,0]) finished_box([inner_face-joint_gap/2,106,10]);
        for(y=[-36,36]) {
            axis_bore([inner_face-8,y,5],"X",8,m3_d,true);
            translate([inner_face-5.7,y,0.8]) nut_slot([3.4,7.4,12]);
        }
        for(y=[-30,30]) translate([18,y,0]) bore_z(m3_d,10);
        for(x=[32,120]) for(y=[-18,18]) translate([x,y,0]) bore_z(m3_d,10);
        for(x=[68,98]) for(y=[-30,30]) translate([x,y,0]) slot_z(14,4,10);
    }
}
module tray_splice() {
    difference() {
        // Clear the inner ballast stop nuts at X=+/-32.
        finished_box([48,90,6]);
        for(x=[-18,18]) for(y=[-30,30]) translate([x,y,0]) bore_z(m3_d,6);
    }
}
module weight_stop() {
    difference() {
        finished_box([8,58,12]);
        for(y=[-18,18]) translate([0,y,0]) bore_z(m3_d,12);
    }
}
module camera_deck() {
    difference() {
        finished_box([90,68,12]);
        for(x=[-24,24]) for(y=[-31,-21]) translate([x,y,0]) bore_z(m3_d,12);
        for(x=[-38,38]) translate([x,3,0]) slot_z(5,22,12);
    }
}
module equipment_seat(riser=false) {
    top=riser?transducer_seat_height:light_seat_height;
    difference() {
        translate([0,19,0]) rotate([90,0,0]) profile_solid(38)
            offset(r=profile_radius) offset(delta=-profile_radius)
                polygon([[0,0],[12,0],[36,top-12],[60,top-12],[60,top],[0,top]]);
        for(y=[-10,10]) {
            axis_bore([0,y,8],"X",12,m3_d,true,true);
            axis_bore([12,y,8],"X",49,tool_d,true,true);
        }
        if(!riser) for(x=[20,48]) translate([x,0,top-12]) slot_z(5,24,12);
        if(riser) for(y=[-10,10]) translate([45,y,top-12]) bore_z(m3_d,12);
    }
}
module equipment_bridge() {
    difference() {
        finished_box([60,90,6]);
        for(y=[-34,-14]) translate([-9,y,0]) bore_z(m3_d,6);
        for(x=[-15,15]) translate([x,16,0]) slot_z(5,30,6);
    }
}
module bumper_half() {
    difference() {
        profile_solid(12) difference() {
            intersection() {
                rr(2*inner_face,82,3);
                translate([joint_gap/2,-100]) square([200,200]);
            }
            rr(200,46,4);
        }
        for(y=[-32,32]) translate([18,y,0]) bore_z(m3_d,12);
        // Native XY = world XZ, native thickness = world -Y.
        for(y=[-18,18]) {
            axis_bore([inner_face-8,y,6],"X",8,m3_d,true,true);
            translate([inner_face-5.7,y,2]) nut_slot([3.4,7.4,12]);
        }
    }
}
module bumper_splice() {
    difference() {
        finished_box([68,18,6]);
        for(x=[-18,18]) translate([x,0,0]) bore_z(m3_d,6);
    }
}

if(part=="side_front") side_panel(true);
else if(part=="side_rear") side_panel(false);
else if(part=="splice_upper") splice(false);
else if(part=="splice_middle") splice(true);
else if(part=="clamp_link") link();
else if(part=="shoe") shoe();
else if(part=="cross_half") cross_half();
else if(part=="cross_splice") cross_splice();
else if(part=="tray_half") tray_half();
else if(part=="tray_splice") tray_splice();
else if(part=="weight_stop") weight_stop();
else if(part=="camera_deck") camera_deck();
else if(part=="equipment_seat") equipment_seat(false);
else if(part=="equipment_riser") equipment_seat(true);
else if(part=="equipment_bridge") equipment_bridge();
else if(part=="bumper_half") bumper_half();
else if(part=="bumper_splice") bumper_splice();
else if(part=="foam_reference") translate([0,0,-17]) finished_box([54,148,34]);
else assert(false,"Unknown part variant");
