// mm. U=side-front, V=up, N=out. Geometry in the assembled locked pose.
include <../../../../../scad/lib/child_horizontal_twist_interface.scad>
include <../../../../../scad/lib/child_horizontal_plate_interfaces.scad>
use <../../../../../scad/lib/edge_finished_profiles.scad>
use <../../../../common/jigs/quick_release_prototypes/quick_release_prototypes.scad>
use <../child_simple_light_mount/child_simple_light_mount.scad>
part="frame_receiver"; // [frame_receiver,light_twist]
frame_width=24;
frame_end_margin=12;
frame_plate_t=qr_pad_t; // co-planar with the existing 4 mm twist foot
receiver_n=0; // inner guard leaves the outside side face clear
receiver_u=20; // existing Y=60 column -> light Y=80
receiver_v=0;
dock_rotation=0; // lock axis U: horizontal beside the upright light in the locked pose
cradle_embed=qr_twist_plate_t; // overlap the non-mating outer plate with the shell wall
edge_fillet_r=2;
edge_chamfer=.6;
hole_chamfer=.3;
qr_bore_relief=.02; // only the C plate cut; legacy shell retains the nominal 33 bore
$fn=96;
frame_pitch=hf_accessory_column_z[len(hf_accessory_column_z)-1]-hf_accessory_column_z[0];
adapter_height=frame_pitch+2*frame_end_margin;
light_r=chlm_holder_id/2+chlm_wall;
legacy_cy=chlm_plate_t+chlm_service_gap+light_r;
male_outer=qr_locked_height;
cradle_shift=male_outer-cradle_embed-(legacy_cy-light_r);
light_centre_n=male_outer-cradle_embed+light_r;
// The two new parts are single connected solids. Never alter C contact profiles.
echo(["SIDE_TWIST_R4",frame_width,adapter_height,frame_pitch,frame_plate_t,
      receiver_n,receiver_u,receiver_v,dock_rotation,cradle_shift,light_centre_n,
      chlm_holder_id,chlm_holder_length]);
module frame_receiver() {
    difference() {
        union() {
            // Finish the concave junctions of the flat foot and the existing C
            // pad as one local planar profile. C mating surfaces above it stay
            // in the canonical twist module; restore its mounting holes last.
            ef_profile(frame_plate_t,edge_chamfer) ef_plan_finish(edge_fillet_r) union() {
                ef_round_rect(frame_width,adapter_height,edge_fillet_r);
                translate([receiver_u,receiver_v]) rotate(dock_rotation)
                    ef_round_rect(qr_pad,qr_pad,qr_plate_corner_r);
            }
            // Replace only the non-mating pad below N=4. Keeping two nearly
            // coincident finished pads creates microscopic sliver triangles.
            // All C walls, cam paths and lock bore above the floor stay stock.
            translate([receiver_u,receiver_v,receiver_n]) rotate([0,0,dock_rotation]) difference() {
                twist_female();
                // 0.05 mm overlap joins the replacement foot volumetrically.
                translate([-50,-50,-1]) cube([100,100,qr_pad_t+1-.05]);
                // Keep that overlap only beneath the central C body. The old
                // rounded pad corners must not reappear as coincident rims.
                for(s=[-1,1]) scale([1,s,1])
                    translate([-50,qr_pad/2-5.9,-1]) cube([100,50,qr_pad_t+1]);
            }
        }
        for(v=[-frame_pitch/2,frame_pitch/2]) translate([0,v,0])
            ef_poly_bore(hf_m3_clearance,frame_plate_t,hole_chamfer,sides=8);
        translate([receiver_u,receiver_v,receiver_n]) rotate([0,0,dock_rotation])
            mounting_holes(thickness=qr_pad_t);
    }
}
module light_twist() {
    union() {
        difference() {
            translate([0,0,male_outer]) rotate([0,0,dock_rotation]) rotate([180,0,0]) twist_male();
            // Trim only the non-mating upper C plate before union. A local
            // 0.02 radial relief avoids coincident tessellations with the shell.
            // The shell restores the original 33 bore and retains ~4 mm of
            // rear plate; C mating/pad faces are below this cut.
            translate([0,chlm_holder_length/2+.1,light_centre_n]) rotate([90,0,0])
                cylinder(d=chlm_holder_id+2*qr_bore_relief,h=chlm_holder_length+.2,$fn=96);
        }
        translate([0,0,cradle_shift]) rotate([90,0,180]) half_holder(false,false);
    }
}
if(part=="frame_receiver") frame_receiver();
else if(part=="light_twist") light_twist();
else assert(false,"Unknown part");
