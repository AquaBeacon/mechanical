// Metal stock / cut sleeves, reference solids, NOT printed.
kind="sleeve"; // [sleeve, plate]
length=12.2;
od=5;
id=3.2;
plate_w=5;
plate_l=12;
plate_t=1.5;
plate_hole=3.4;
$fn=64;
difference() {
    if(kind=="sleeve") cylinder(d=od,h=length);
    else union() {
        for(y=[-(plate_l-plate_w)/2,(plate_l-plate_w)/2])
            translate([0,y,0]) cylinder(d=plate_w,h=plate_t);
        translate([-plate_w/2,-(plate_l-plate_w)/2,0])
            cube([plate_w,plate_l-plate_w,plate_t]);
    }
    translate([0,0,-0.1]) cylinder(d=kind=="sleeve" ? id : plate_hole,
                                  h=(kind=="sleeve" ? length : plate_t)+0.2);
}
