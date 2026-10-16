// mm. part=print is the intended X1C orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_spar_bolted.scad>
if(part=="print") { translate([0,0,8]) rotate([180,0,0]) float_end(false); } else { float_end(false); }
