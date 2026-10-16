// mm. Assembly coordinates and explicit bed orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_bottom_sensors.scad>
if(part=="print"){cartridge();}else{cartridge();}
