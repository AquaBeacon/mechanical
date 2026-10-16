// DJI osmo Action 6固定部品 — integrated revision, provisional case contact surfaces.
// mm; X camera width / screw axis, +Y front, Z up. One printable solid.
show_case = false;
tab_t=3;
tab_gap=3;
case_hole=5;
body_to_axis=12.5;
fit=0.3;
base_w=104;
base_d=54;
base_t=8;
axis_z=24;
wall_t=8;
wall_y=19;
wall_span=84;
contact_w=16;
contact_d=6;
contact_raise=4;
shim_gap=0.3;
lug_r=7;
nut_side_t=6;
head_side_t=3;
nut_af=8.2;
nut_depth=4.2;
tool_r=14; // assumed knob/tool radial envelope, not measured
case_w=95;
case_d=45.9;
case_h=75;
$fn=64;
eps=0.02;
middle_t=tab_gap-fit;
slot=tab_t+fit;
stack=nut_side_t+2*slot+middle_t+head_side_t;
left=-(slot+middle_t/2+nut_side_t);
body_z=axis_z+body_to_axis;
contact_z=body_z-shim_gap;
wall_top=contact_z-contact_raise;
assert(middle_t>0 && nut_depth<nut_side_t-1);
assert(wall_y-wall_t/2>tool_r);
assert(axis_z-tool_r>base_t);
assert(wall_span/2<base_w/2 && wall_y+wall_t/2<base_d/2);
assert(contact_z< body_z && wall_top>base_t);
module hole(d,h) { cylinder(d=d/cos(180/32),h=h,$fn=32); }
module ribs() {
    // Broad front/rear shear walls, tied by side webs into a closed frame.
    for(s=[-1,1]) translate([-wall_span/2,s*wall_y-wall_t/2,base_t])
        cube([wall_span,wall_t,wall_top-base_t]);
    for(s=[-1,1]) translate([s*(wall_span/2-wall_t/2)-wall_t/2,-wall_y,base_t])
        cube([wall_t,2*wall_y,wall_top-base_t]);
}
module body() {
    difference() {
        union() {
            translate([-base_w/2,-base_d/2,0]) cube([base_w,base_d,base_t]);
            difference() {
                ribs();
                // Keep the complete screw insertion/knob corridor open.
                translate([-base_w,0,axis_z]) rotate([0,90,0]) cylinder(r=tool_r,h=2*base_w);
            }
            for(p=[[-30,wall_y],[30,wall_y],[0,-wall_y]])
                translate([p[0]-contact_w/2,p[1]-contact_d/2,wall_top])
                    cube([contact_w,contact_d,contact_raise]);
            for(i=[0:2]) {
                starts=[left,-middle_t/2,middle_t/2+slot];
                ts=[nut_side_t,middle_t,head_side_t];
                translate([starts[i],-lug_r,base_t]) cube([ts[i],2*lug_r,axis_z-base_t]);
                translate([starts[i],0,axis_z]) rotate([0,90,0]) cylinder(r=lug_r,h=ts[i]);
            }
        }
        translate([left-eps,0,axis_z]) rotate([0,90,0]) hole(case_hole+0.2,stack+2*eps);
        translate([left-eps,0,axis_z]) rotate([0,90,0]) cylinder(d=nut_af/cos(30),h=nut_depth+eps,$fn=6);
        for(x=[-11,11],y=[-16,16]) {
            translate([x,y,-eps]) hole(5.4,base_t+2*eps);
            // Head/driver access through wall, leaves an 8 mm base bearing surface.
            translate([x,y,base_t]) hole(10.4,body_z);
        }
    }
}
color("SteelBlue") body();
if(show_case) %translate([-case_w/2,-case_d/2,body_z]) cube([case_w,case_d,case_h]);
