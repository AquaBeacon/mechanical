include <../../../../../scad/lib/child_interior_mounts.scad>
// Printed closed-seat flange brace, bolted revision 2026-10-01.
// Existing pan screws and spacers only; no custom metal sleeves or plates.
/* [Existing interfaces] */
left_x=-22;
right_x=39.5;
board_y=4.6;
left_spacer=30;
right_spacer=12;
arch_z0=22;
flange_face_z=19;
flange_bcd=94;
tube_id=101.6;
/* [Structure] */
rib_t=8;
beam_w=12;
mount_width=10;
left_depth=5.5;
right_depth=5.5;
mount_bore=3.4;
junction_x=0;
junction_y=39.6;
ear_t=12;
ear_od=5.2;
ear_tangent=20;
ear_web_w=24;
ear_bore=3.4;
/* [Hidden] */
mount_z=2.5;
rib_z=flange_face_z-arch_z0;
beam_h=mount_z+rib_t/2-rib_z;
left_seat=board_y+left_spacer;
right_seat=board_y+right_spacer;
left_y=left_seat+left_depth/2;
right_y=right_seat+right_depth/2;
ear_y=flange_bcd/2;
ear_z0=flange_face_z-arch_z0;
$fa=4;
$fs=0.3;
function rad(x,y)=sqrt(x*x+y*y);
assert(ear_t>=10 && mount_width-mount_bore>=2.4);
module bar(a, b, w, h, seat_a=false, seat_b=false) {
    L = rad(b[0]-a[0], b[1]-a[1]);
    ang = atan2(b[1]-a[1], b[0]-a[0]);
    // Taper beside spacer seats: wider beams must not bury the hex end face.
    end_w=4.8;
    wa=seat_a ? end_w : w;
    wb=seat_b ? end_w : w;
    ramp=4;
    translate([a[0],a[1],0]) rotate([0,0,ang]) ci_rounded_extrude(h)
        offset(r=0.6,$fn=24) offset(delta=-0.6) polygon([[0,-wa/2],[ramp,-w/2],[L-ramp,-w/2],
                 [L,-wb/2],[L,wb/2],[L-ramp,w/2],
                 [ramp,w/2],[0,wa/2]]);
    for (p=[a,b]) translate([p[0],p[1],0]) ci_rounded_extrude(h) circle(d=end_w,$fn=32);
}

difference() {
    union() {
        translate([0,0,rib_z]) {
            bar([left_x,left_y],[junction_x,junction_y],beam_w,beam_h,seat_a=true);
            bar([junction_x,junction_y],[30,29],beam_w,beam_h);
            bar([30,29],[right_x,right_y],beam_w,beam_h,seat_b=true);
            // The free elbow is structural, not a spacer seat: no 4.8 mm neck.
            translate([30,29,0]) ci_rounded_extrude(beam_h) circle(d=beam_w,$fn=64);
            translate([junction_x,junction_y,0]) ci_rounded_extrude(beam_h) circle(d=16,$fn=64);
        }
        for (p=[[left_x,left_seat,left_depth],[right_x,right_seat,right_depth]])
            translate([p[0]-mount_width/2,p[1],rib_z])
                edge_round_box([mount_width,p[2],beam_h]);
        intersection() {
            union() {
                for (xx=[-ear_tangent/2,ear_tangent/2])
                    translate([xx,ear_y,ear_z0]) ci_rounded_extrude(ear_t) circle(d=ear_od,$fn=64);
                translate([-ear_tangent/2,ear_y-ear_od/2,ear_z0])
                    edge_round_box([ear_tangent,ear_od,ear_t]);
                translate([-ear_web_w/2,junction_y,ear_z0])
                    edge_round_box([ear_web_w,ear_y-junction_y,ear_t]);
            }
            translate([0,0,ear_z0]) cylinder(r=tube_id/2-1,h=ear_t,$fn=180);
        }
    }
    // Closed M3 hole with a flat pan-head bearing seat.
    translate([0,ear_y,ear_z0-0.1]) cylinder(d=ear_bore,h=ear_t+0.2,$fn=64);

    // Existing J_PWR1 XH9 plug reaches X34.45/Y19/world Z28.375.
    // 0.65/0.70 mm clearance; keep the M3 head and spacer bearing centre.
    // Through-height relief adds no roof or unsupported bridge.
    translate([-50,-30,rib_z-1]) linear_extrude(beam_h+2)
        offset(r=0.6,$fn=24) offset(delta=-0.6) square([85.1,49.7]);

    for (p=[[left_x,left_seat,left_depth],[right_x,right_seat,right_depth]]) {
        translate([p[0],p[1]-0.1,mount_z])
            roof_bore_y(mount_bore,20);
        // Clear the hex end faces, so preload always reaches metal.
        translate([p[0]-mount_width/2-1,p[1]-10,rib_z-0.1])
            cube([mount_width+2,10,beam_h+0.2]);
        translate([p[0]-mount_width/2-1,p[1]+p[2],rib_z-0.1])
            cube([mount_width+2,20,beam_h+0.2]);
    }
}

// Point of horizontal M3 hole faces build +Z; flat bearing seats remain.
module roof_bore_y(d,h) {
    rotate([-90,0,0]) linear_extrude(h) union() {
        circle(d=d,$fn=64);
        polygon([[-d/sqrt(8),-d/sqrt(8)],[0,-d/sqrt(2)],[d/sqrt(8),-d/sqrt(8)]]);
    }
}

// R0.6 external edge rounds, kept inside the original interface envelope.
module edge_round_box(size) {
    r=min(0.6,min(size)/4);
    translate([r,r,r]) minkowski() {
        cube(size-[2*r,2*r,2*r]);
        sphere(r=r,$fn=16);
    }
}
