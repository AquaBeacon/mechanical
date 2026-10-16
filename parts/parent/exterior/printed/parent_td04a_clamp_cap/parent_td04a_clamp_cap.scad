// mm. Assembly coordinates and explicit bed orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_bottom_sensors.scad>
if(part=="print"){translate([0,0,46.5])rotate([-90,0,0])td_clamp(true);}else{td_clamp(true);}
