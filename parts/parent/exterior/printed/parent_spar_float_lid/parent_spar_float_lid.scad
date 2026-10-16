// mm. part=print is the intended X1C orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_spar_bolted.scad>
if(part=="print") { translate([0,0,6]) rotate([180,0,0]) float_lid(); } else { float_lid(); }
