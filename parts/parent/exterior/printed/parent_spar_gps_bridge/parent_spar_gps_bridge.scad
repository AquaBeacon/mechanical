// mm. part=print is the intended X1C orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_spar_bolted.scad>
if(part=="print") { translate([0,0,10]) rotate([0,90,0]) gps_bridge(); } else { gps_bridge(); }
