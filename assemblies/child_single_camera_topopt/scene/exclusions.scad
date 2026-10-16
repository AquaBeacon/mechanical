// AUTHORISED: one central camera, one +X vertical light. 2026-09-10.
// Setup review: solid exclusion envelopes, not production parts.
// World frame: mm; X right, Y front, Z up. Provisional component sizes.
use <C:/Users/ryupc/WorkSpace/Mitou26/AquaBeacon-OSS/mechanical/assemblies/child_single_camera_topopt/child_core_frame/inputs/geometry.scad>
$fn=48;
part="all";
light_d=40; light_length=100; cable_d=6; cable_clearance=1;
module box(lo,hi){translate(lo)cube(hi-lo);}
module link(a,b,r){hull(){translate(a)sphere(r=r,$fn=16);translate(b)sphere(r=r,$fn=16);}}
module route(points,r){for(i=[0:len(points)-2])link(points[i],points[i+1],r);}
module pressure_vessel(){
    translate([0,0,-8])cylinder(r=57.15,h=216);
    translate([0,0,-13.8])cylinder(r=60.15,h=5.8);
    translate([0,0,208])cylinder(r=60.15,h=6.5);
    translate([0,0,214])intersection(){sphere(r=47.25);box([-50,-50,0],[50,50,50]);}
}
module cameras(){box([-47.35,83.1,82.95],[47.35,129,167.05]);}
module light_forward(){} // Removed by user request.
module light_vertical(){
    box([44,-100,75],[80,-50,125]);
    translate([80,-75,50])cylinder(d=light_d+2,h=light_length);
}
module td04a(){
    // Body seated on socket floor: 218.5 + 6, not placed on socket rim.
    translate([0,-85,224.5])cylinder(d=26.4,h=55);
}
module td04a_socket(){box([-25,-110,218.5],[25,-60,256.5]);}
module hand_clearance(){
    hand_room();
    // Approach from the rear through the 52x30 finger opening.
    box([-26,-150,115],[26,-103,145]);
}
module cables(){
    // Swept routing corridors. Bend radius and service loops remain to be sized.
    for(s=[-1,1])route([[s*18,-97,-40],[s*18,-97,75],
        [s*34,-79,105],[s*34,-79,187],[s*18,-92,202],[s*18,-92,228]],cable_d/2+cable_clearance);
    // TD04A feed to its bottom opening; follow the left-side reserved bypass.
    route([[-18,-92,202],[-18,-85,214],[0,-85,224]],cable_d/2+cable_clearance);
    // Vertical-light lead returns to the right-side cable channel; bend radius remains provisional.
    route([[80,-75,50],[80,-75,28],[42,-79,28],[34,-79,75],[18,-97,75]],cable_d/2+cable_clearance);
    // Five penetrators and the lower wiring volume (provisional 20mm protrusion).
    for(a=[-90,-18,54,126,198])translate([28*cos(a),28*sin(a),-33.8])cylinder(d=14,h=20);
    box([-38,-45,-48],[38,38,-34]);
}
if(part=="pressure_vessel")pressure_vessel();
else if(part=="cameras")cameras();
else if(part=="light_forward")light_forward();
else if(part=="light_vertical")light_vertical();
else if(part=="td04a")td04a();
else if(part=="td04a_socket")td04a_socket();
else if(part=="hand_clearance")hand_clearance();
else if(part=="cables")cables();
else {color([.25,.65,.95,.3])pressure_vessel();color("orange")cameras();
color("gold",.5){light_forward();light_vertical();}color("purple")td04a();
color("red")cables();color("cyan",.4)hand_clearance();}
