// mm. Assembly coordinates and explicit bed orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_bottom_sensors.scad>
if(part=="print"){rotate([90,0,0])td_clamp(false);}else{td_clamp(false);}
