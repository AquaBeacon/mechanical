// mm. Assembly coordinates and explicit bed orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_bottom_sensors.scad>
if(part=="print"){translate([0,0,75])rotate([90,0,0])carrier();}else{carrier();}
