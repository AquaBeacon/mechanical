// Local positive primitives are finished before functional cuts.
use <util.scad>
module ef_round_rect(w,l,r) {
    safe_r=min(r,w/2-0.01,l/2-0.01);
    translate([-w/2,-l/2]) projection(cut=true) rrect_prism(w,l,1,safe_r);
}
module ef_capsule(w,l) {
    assert(l>=w && w>0);
    hull() for(s=[-1,1]) translate([0,s*(l-w)/2]) circle(d=w,$fn=48);
}
module ef_profile(t,c=0.6) {
    // Compensated local profile, exact extrema and thickness. This is not a
    // blanket Minkowski of a completed part or assembly. Cuts are restored last.
    assert(t>2*c && c>0);
    minkowski() {
        translate([0,0,c]) linear_extrude(t-2*c) offset(delta=-c) children();
        union() {
            translate([0,0,-c]) cylinder(r1=0,r2=c,h=c,$fn=16);
            cylinder(r1=c,r2=0,h=c,$fn=16);
        }
    }
}
module ef_convex_profile(t,c=0.6) {
    // Exact offset loft for convex profiles: avoids unnecessary 3D Minkowski
    // triangulation on large plates and bosses. Nonconvex profiles use ef_profile.
    assert(t>2*c && c>0);
    hull() {
        linear_extrude(0.01) offset(delta=-c) children();
        translate([0,0,c]) linear_extrude(t-2*c) children();
        translate([0,0,t-0.01]) linear_extrude(0.01) offset(delta=-c) children();
    }
}
module ef_cut(t,c=0.6) {
    translate([0,0,-0.1]) linear_extrude(t+0.2) children();
    hull() {
        translate([0,0,-0.01]) linear_extrude(0.01) offset(delta=c) children();
        translate([0,0,c]) linear_extrude(0.01) children();
    }
    hull() {
        translate([0,0,t-c-0.01]) linear_extrude(0.01) children();
        translate([0,0,t]) linear_extrude(0.01) offset(delta=c) children();
    }
}
module ef_bore(d,t,c=0.3) { ef_cut(t,c) circle(d=d,$fn=32); }
// Diameter is the inscribed circle: polygon flats preserve the shaft clearance.
module ef_poly_bore(d,t,c=0.3,sides=8) {
    assert(sides>=6 && sides==floor(sides));
    ef_cut(t,c) rotate(180/sides) circle(r=d/2/cos(180/sides),$fn=sides);
}
module ef_box(w,l,t,r=2,c=0.6) { ef_convex_profile(t,c) ef_round_rect(w,l,r); }
module ef_hex(af) { rotate(30) circle(d=af/cos(30),$fn=6); }
module ef_plan_finish(r=2) {
    // Closing rounds concave roots; opening rounds convex corners. Exact planar
    // extrema and straight functional flats are retained.
    offset(r=r) offset(delta=-r) offset(delta=-r) offset(r=r) children();
}
module ef_root(w,l,r=1,corner=2) {
    // Local 45-degree relief where a boss meets a plate (place at plate top).
    hull() {
        linear_extrude(0.01) ef_round_rect(w+2*r,l+2*r,corner+r);
        // End strictly inside the boss. An exact tangent match of the two
        // independently tessellated rounded profiles creates microscopic lips.
        translate([0,0,r+0.3]) linear_extrude(0.01)
            offset(delta=-0.3) ef_round_rect(w,l,corner);
    }
}
