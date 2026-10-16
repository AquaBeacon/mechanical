"""Prepare the no-box-hole clamp variant; preserve previous simple design."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'parts/parent/exterior/printed'
base=(P/'parent_simple_deck/parent_simple_deck.scad').read_text(encoding='utf-8')
base=base.replace('/* [Existing BCAS212310G mounting] */\nbox_pitch_x=192;\nbox_pitch_y=212;\nbox_hole=4.5;\nnut_access_d=10;\nnut_access_depth=4;',
'''/* [External clamp rods - no box holes used] */
box_pitch_x=224;
box_pitch_y=110;
box_hole=5.5;''')
base=base.replace('assert(plate_t-nut_access_depth>=6);','assert(box_pitch_x/2-box_hole/2>105);')
base=base.replace('   // Open underside recess for standard M4 nut and small socket driver.\n   translate([x,y,-plate_t-eps])hole(nut_access_d,nut_access_depth+eps);\n','')
base=base.replace('// Simple parent exterior.', '// Clamped parent exterior; external M5 rods at X=+-112, Y=+-55.')
base=base.replace('/* [Rope eyes outside box footprint] */\nrope_x=112;\nrope_y=75;\nrope_d=8;', '/* [Float lug attachment: two M5 screws per lug] */\nrope_x=112;\nrope_y=85;\nrope_d=5.5;\nlug_pitch=16;')
base=base.replace('for(x=[-rope_x,rope_x],y=[-rope_y,rope_y])translate', 'for(x=[-rope_x,rope_x],cy=[-rope_y,rope_y],dy=[-lug_pitch/2,lug_pitch/2])let(y=cy+dy)translate')
d=P/'parent_clamped_deck';d.mkdir(exist_ok=True)
(d/'parent_clamped_deck.scad').write_text(base,encoding='utf-8')
d=P/'parent_clamp_bar';d.mkdir(exist_ok=True)
(d/'parent_clamp_bar.scad').write_text('''// Two identical upper clamp bars. Flat underside Z=0. mm.
/* [Dimensions] */
width=236;
depth=24;
thickness=12;
rod_pitch=224;
rod_hole=5.5;
$fn=48;
assert((width-rod_pitch-rod_hole)/2>=3);
assert(depth>=20 && thickness>=10);
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
difference(){
 translate([-width/2,-depth/2,0])cube([width,depth,thickness]);
 for(x=[-rod_pitch/2,rod_pitch/2])translate([x,0,-0.02])hole(rod_hole,thickness+0.04);
}
''',encoding='utf-8')
print('Prepared clamped deck and upper bar')
