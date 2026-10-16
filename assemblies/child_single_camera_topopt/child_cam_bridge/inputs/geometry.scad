// Single-camera adapter: GENERATIVE SETUP, not a finished component.
// HP4/HP5 interfaces retained; central camera shifted +9 mm to clear column.
part="reference";
lens_x=0; lens_y=129; lens_z=125;
case_w=94.7; case_d=45.9; case_h=84.1;
wing=60; deck_bot=44.95; deck_top=52.95; hp_y=74.35;
column_front=80.35; hp_z=[100,170]; $fn=48;
module box(lo,hi){translate(lo)cube(hi-lo);}
module preserve(){
    box([-25,hp_y,75],[25,column_front,195]);
    box([-17,lens_y-case_d/2-22,deck_bot],[17,lens_y-case_d/2+22,deck_top]);
    for(s=[-1,1]){
        box([s>0?54:-60,67,deck_bot],[s>0?60:-54,lens_y+8,80]);
        box([s>0?30:-60,lens_y+2,deck_bot],[s>0?60:-30,lens_y+8,80]);
    }
}
module forbidden(){
    box([-case_w/2,lens_y-case_d,82.95],[case_w/2,lens_y,82.95+case_h]);
    box([-17,lens_y-case_d/2-22,deck_top],[17,lens_y-case_d/2+22,82.95]);
    translate([lens_x,lens_y,lens_z])rotate([-90,0,0])cylinder(r1=0,r2=12*tan(77.5),h=12);
    for(z=hp_z)box([-25,62.35,z-25],[25,hp_y,z+25]);
    for(x=[-20,20],z=[80,120,150,190])translate([x,column_front,z])rotate([-90,0,0])cylinder(d=12,h=lens_y+10-column_front);
}
module design_space(){box([-wing,67,deck_bot],[wing,lens_y+8,195]);}
module cuts(){
    forbidden();
    for(x=[-20,20],zc=hp_z,dz=[-20,20])translate([x,hp_y-1,zc+dz])rotate([-90,0,0])cylinder(d=5.4,h=8);
    for(x=[-11,11],dy=[-16,16]){
        translate([x,lens_y-case_d/2+dy,deck_bot-1])cylinder(d=5.4,h=10);
        translate([x,lens_y-case_d/2+dy,deck_bot-1])cylinder(d=8.2/cos(30),h=5,$fn=6);
    }
    for(s=[-1,1],y=[80,125])translate([s*(wing+1),y,65])rotate([0,-90*s,0])cylinder(d=5.4,h=8);
}
assert(lens_y-case_d-column_front>=2.7,"Camera back must clear adapter column");
assert(lens_y+8+110<=250,"Operating depth exceeds 250 mm");
assert(lens_z-80>8*tan(77.5),"Bumper clips optical field");
if(part=="preserve")preserve();
else if(part=="obstacle")difference(){intersection(){forbidden();box([-wing-3,64,deck_bot-3],[wing+3,lens_y+11,198]);}preserve();}
else if(part=="design_space")design_space();
else if(part=="preserve_cuts")cuts();
else{color("green")preserve();color("red",.25)forbidden();%design_space();}
