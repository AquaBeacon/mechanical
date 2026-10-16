from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'parts/parent/exterior/printed'
def save(name,s):
    d=P/name;d.mkdir(exist_ok=True);(d/(name+'.scad')).write_text(s,encoding='utf-8')
s=(P/'parent_open_frame/parent_open_frame.scad').read_text()
s=s.replace('lug_y=85; lug_pitch=16;','lug_y=85; lug_hole=10.5; lug_z=-26;')
s=s.replace(' union(){',' union(){\n  // Four integral downward lugs, below the box for nut/rope access.\n  for(x=[-118,110],y=[-lug_y,lug_y])translate([x,y-16,-42])cube([8,32,32]);',1)
s=s.replace('  for(c=[-lug_y,lug_y],dy=[-lug_pitch/2,lug_pitch/2])translate([x,c+dy,-thick-.02])hole(5.5,thick+.04);','')
s=s.replace(' for(x=carrier_x){',' for(x=[-118,110],y=[-lug_y,lug_y])translate([x-.02,y,lug_z])rotate([0,90,0])hole(lug_hole,8.04);\n // Through-windows leave 7 mm ribs; keep bolt-bearing zones solid.\n for(x=[-111,101])translate([x,-30,-thick-.02])cube([10,60,thick+.04]);\n for(y=[-clamp_y,clamp_y])translate([-54,y-5,-thick-.02])cube([108,10,thick+.04]);\n for(x=carrier_x){')
save('parent_light_frame',s)
s=(P/'parent_clamp_bar/parent_clamp_bar.scad').read_text().replace(' for(x=[-rod_pitch/2,rod_pitch/2])',' // Solid ends and twin 8 mm side ribs remain.\n translate([-80,-4,-.02])cube([160,8,thickness+.04]);\n for(x=[-rod_pitch/2,rod_pitch/2])',1)
save('parent_light_bar',s)
s=(P/'parent_compact_carrier/parent_compact_carrier.scad').read_text()
s=s.replace(' for(x=frame_x)', ''' // Flange windows retain ribs between wall and the mounting row.
 for(x=[-50,-8,34])translate([x,-43,top_z-wall-.02])cube([20,27,wall+.04]);
 // Preserve camera bolt pads and TD bracket landing; remove unloaded sheet.
 for(c=[[-97,-92,24,62],[-20,-92,42,50],[26,-92,69,39]])
  translate([c[0],-wall-.02,c[1]])cube([c[2],wall+.04,c[3]]);
 translate([-51,-wall-.02,-73])cube([6,wall+.04,14]);
 for(x=frame_x)''')
s=s.replace('for(z=[-35,-60])','for(z=[-35])')
save('parent_light_carrier',s)
print('Prepared 3 lightweight parts; existing camera mount is reused.')
