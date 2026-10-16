// Non-print ideal hardware proxies, directly using the canonical C-twist.
use <../../../jigs/quick_release_prototypes/quick_release_prototypes.scad>
part="lock_bolt"; // [lock_bolt,lock_nut,lock_washer,rubber_pads]
if(part=="lock_bolt") through_bolt("twist",include_washer=false);
else if(part=="lock_nut") fixed_nut("twist");
else if(part=="lock_washer") difference() {
    through_bolt("twist",include_washer=true);
    through_bolt("twist",include_washer=false);
}
else if(part=="rubber_pads") twist_pad_reference(compressed=true);
else assert(false,"Unknown hardware");
