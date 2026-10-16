"""Build the one-piece direct M3 mount from the retained fitted source."""
from pathlib import Path
import subprocess, json, hashlib
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount'
OUT=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
OSC=r'C:\Program Files\OpenSCAD\openscad.exe'

def run(src,dest,*args):
    p=subprocess.run([OSC,'-o',str(dest),*args,str(src)],capture_output=True,text=True)
    (dest.with_suffix(dest.suffix+'.log')).write_text(p.stdout+p.stderr,encoding='utf-8')
    assert p.returncode==0 and 'ERROR' not in p.stderr,p.stderr

def main():
    src=(OLD/'dji_osmo_action6_mount.scad').read_text(encoding='utf-8')
    src=src.replace('base_w=104;', 'base_w=100;')
    src=src.replace('gusset_t=8; gusset_x=30;', 'gusset_t=6; gusset_x=38;')
    src=src.replace('front_y=19; front_wall_t=8;', 'front_wall_t=8; front_shift=front_wall_t; front_y=19+front_shift;')
    src=src.replace('$fn=64; eps=0.02;', '''// CHILD-SIMPLE-M3-40x40 Rev.1: direct rear attachment.
mount_pitch=40; mount_center_z=40; mount_d=3.45;
head_d=6.8; head_depth=3.6; rear_clear_half=31;
$fn=64; eps=0.02;
assert(gusset_x-gusset_t/2>rear_clear_half);
assert(plate_t-head_depth>=4);
assert(mount_center_z-mount_pitch/2-head_d/2>base_t);
assert(mount_center_z+mount_pitch/2+head_d/2<84.5);
// Polygon roof points up in the Z print direction; circular clearance retained.
module roof_bore_y(x,y,z,d,depth) {
 r=d/2/cos(180/24);
 translate([x,y+eps,z]) rotate([90,0,0]) linear_extrude(depth+eps)
 polygon(concat([for(a=[135:15:405]) [r*cos(a),r*sin(a)]],[[0,r*sqrt(2)]]));
}
module rear_bore(x,z,d,depth) { roof_bore_y(x,rear_face,z,d,depth); }''')
    src=src.replace('module body() {', '''// Modest reliefs: roof slopes exceed 55 degrees above the bed.
module roof_window_y(w,z0,shoulder) {
 translate([0,rear_back-eps,0]) rotate([90,0,0])
 linear_extrude(plate_t+2*eps,center=true)
 polygon([[-w/2,z0],[w/2,z0],[w/2,shoulder],[0,shoulder+w*0.8],[-w/2,shoulder]]);
}
module body() {''')
    # The through-window is centered within the original plate thickness.
    src=src.replace('translate([0,rear_back-eps,0])', 'translate([0,rear_back+plate_t/2,0])')
    src=src.replace('  translate([left-eps,0,axis_z]) roof_hole_x', '''  roof_window_y(36,34,43);
  // Clear the original rear base overhang so the rear face sits flush on the frame.
  translate([-rear_clear_half,base_y0-eps,-eps])
   cube([2*rear_clear_half,rear_back-base_y0+eps,base_t+2*eps]);
  for(x=[-mount_pitch/2,mount_pitch/2],z=[mount_center_z-mount_pitch/2,mount_center_z+mount_pitch/2]) {
   rear_bore(x,z,mount_d,plate_t+2*eps);
   // Recess M3 socket heads below the existing camera contact surface.
   rear_bore(x,z,head_d,head_depth);
  }
  // Straight hex-key access to the lower mounting bolts, camera removed.
  for(x=[-mount_pitch/2,mount_pitch/2])
   roof_bore_y(x,front_y+front_wall_t/2,mount_center_z-mount_pitch/2,5,front_wall_t+2*eps);
  // Two vertical base slots, clear of ribs, screw pads and support contacts.
  for(s=[-1,1]) translate([s*42-4,-15,-eps]) cube([8,30,base_t+2*eps]);
  // A peaked opening under the front support; retains a continuous top rail.
  translate([0,front_y,0]) rotate([90,0,0]) linear_extrude(front_wall_t+2*eps,center=true)
   polygon([[-12,base_t-0.01],[12,base_t-0.01],[12,9],[0,28.2],[-12,9]]);
  translate([left-eps,0,axis_z]) roof_hole_x''')
    src=src.replace('''  for(x=[-11,11],y=[-16,16]) {
   translate([x,y,-eps]) hole(5.4,base_t+2*eps);
   translate([x,y,base_t]) hole(10.4,plate_top);
  }''', '  // Obsolete underside M5 attachment and its tool recesses removed.')
    # use<> must not render the original source's top-level body.
    src=src.replace('color("SteelBlue") body();','module camera_mount() { body(); }\ncolor("SteelBlue") camera_mount();')
    (OUT/'camera_mount.scad').write_text(src,encoding='utf-8')
    for name in ['camera_mount','assembly']:
        run(OUT/(name+'.scad'),OUT/(name+'.stl'))
        run(OUT/(name+'.scad'),OUT/(name+'.png'),'--imgsize=1200,900','--viewall','--autocenter','--projection=o','--camera=0,0,0,65,0,35,0')
    run(OUT/'frame_view.scad',OUT/'frame_view.png','--imgsize=1200,900','--viewall','--autocenter','--projection=o','--camera=0,0,0,65,0,145,0')
    data={}
    for name,p in [('original',OLD/'dji_osmo_action6_mount.stl'),('camera_mount',OUT/'camera_mount.stl')]:
        m=trimesh.load(p,force='mesh')
        data[name]=dict(bounds=m.bounds.tolist(),volume_cm3=m.volume/1000,watertight=m.is_watertight,components=len(m.split()),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        assert m.is_watertight and len(m.split())==1
    data['mount_volume_reduction_percent']=100*(1-data['camera_mount']['volume_cm3']/data['original']['volume_cm3'])
    (OUT/'mesh_checks.json').write_text(json.dumps(data,indent=2))
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
