// Float attachment lug. Four copies; mirror X for the left side.
// Assembly coordinates for right side, Y=0. mm.
/* [Bracket] */
deck_edge=118;
deck_t=12;
foot_inset=16;
wall_t=8;
foot_t=8;
width=32;
top_z=24;
/* [Float attachment] */
float_hole=10.5; // M10 clearance hole, not a printed thread
float_z=10;
/* [Two M5 deck bolts] */
bolt_x=112;
bolt_pitch=16;
bolt_d=5.5;
/* [Hidden] */
$fn=48;
eps=0.02;
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
assert(width/2-float_hole/2>=8);
assert(top_z-float_z-float_hole/2>=8);
assert(deck_edge-bolt_x-bolt_d/2>=3);
assert(width/2-bolt_pitch/2-bolt_d/2>=5);
difference(){
 union(){
  translate([deck_edge-foot_inset,-width/2,-deck_t-foot_t])cube([foot_inset+wall_t,width,foot_t]);
  translate([deck_edge,-width/2,-deck_t-foot_t])cube([wall_t,width,top_z+deck_t+foot_t]);
 }
 translate([deck_edge-eps,0,float_z])rotate([0,90,0])hole(float_hole,wall_t+2*eps);
 for(y=[-bolt_pitch/2,bolt_pitch/2])translate([bolt_x,y,-deck_t-foot_t-eps])hole(bolt_d,foot_t+2*eps);
}
