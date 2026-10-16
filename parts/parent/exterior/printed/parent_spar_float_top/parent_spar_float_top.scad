// mm. part=print is the intended X1C orientation.
part="assembly"; // [assembly,print]
use <../../../../../scad/lib/parent_spar_bolted.scad>
if(part=="print") { float_end(true); } else { float_end(true); }
