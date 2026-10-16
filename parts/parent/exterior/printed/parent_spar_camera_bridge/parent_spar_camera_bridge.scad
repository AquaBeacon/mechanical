// mm. part=print is the intended X1C orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_spar_bolted.scad>
if(part=="print") { translate([0,0,225]) rotate([-90,0,0]) camera_bridge(); } else { camera_bridge(); }
