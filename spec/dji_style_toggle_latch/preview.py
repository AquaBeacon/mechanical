"""Generate reproducible CAD opening animation, not a physical simulation."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image
import json

ROOT=Path(__file__).resolve().parents[2]
ASM=ROOT/'assemblies/dji_style_toggle_latch'
CAD=ROOT/'parts/common/jigs/dji_style_toggle_latch/dji_style_toggle_latch.scad'
OUT=ASM/'_work/images/motion'
OUT.mkdir(parents=True,exist_ok=True)
WORK=ASM/'_work/intermediate'
OSC=r'C:\Program Files\OpenSCAD\openscad.exe'
report=json.loads((ASM/'_work/analysis/geometry/report.json').read_text(encoding='utf-8'))
closed_angle=report['motion'][0]['link_angle_deg']
open_angle=next(p['free_lever_angle_deg'] for p in report['motion'] if p['free_lever_angle_deg'] is not None)
release_angle=min(p['link_angle_deg'] for p in report['motion'])
angles=list(np.linspace(closed_angle,release_angle,12))
states=[(t,None) for t in angles]+[(release_angle,p) for p in np.linspace(open_angle,30,10)]

def frame(row):
    i,(theta,phi)=row
    scad=WORK/f'motion_{i:02d}.scad'
    scad.write_text(f'use <{CAD.as_posix()}>\nlatch_assembly(theta={theta},free_angle={"undef" if phi is None else phi});\n',encoding='utf-8')
    dest=OUT/f'frame_{i:02d}.png'
    cmd=[OSC,'-o',str(dest),'--imgsize=1000,760','--projection=o',
         '--camera=12,0,30,65,0,25,230',str(scad)]
    subprocess.run(cmd,capture_output=True,check=True)
    return dest

with ThreadPoolExecutor(max_workers=3) as pool:
    frames=list(pool.map(frame,enumerate(states)))
images=[Image.open(p).convert('RGB') for p in frames]
images[0].save(ASM/'_work/images/assembly.png')
images[-1].save(ASM/'_work/images/open.png')
sequence=[images[0]]*5+images+ [images[-1]]*5 +list(reversed(images))
sequence[0].save(ASM/'_work/images/open_close.gif',save_all=True,append_images=sequence[1:],duration=110,loop=0)
print('Created open_close.gif')

# Exact CAD cross-section shows the undercut and sheet location, not an image mockup.
catch_x=report['closed_catch_distance_mm']
sheet_t=report['epdm']['sheet_thickness_mm']
section=''
for stem,color,body in [
    ('keeper','SteelBlue',f'translate([{catch_x},0,0]) latch_keeper();'),
    ('epdm','SeaGreen',f'translate([{catch_x},0,0]) latch_epdm();'),
    ('lever','DimGray','translate(latch_b()) rotate([0,-latch_phi(),0]) latch_lever();')]:
    source=WORK/f'epdm_section_{stem}.scad'
    mesh=WORK/f'epdm_section_{stem}.stl'
    source.write_text(f'use <{CAD.as_posix()}>\nintersection() {{ {body} translate([18,-0.5,0]) cube([24,1,19]); }}\n',encoding='utf-8')
    subprocess.run([OSC,'-o',str(mesh),str(source)],capture_output=True,check=True)
    section+=f'color("{color}") import("{mesh.as_posix()}");\n'
details=[
 ('epdm_keeper', 'color("SteelBlue") latch_keeper(); color("SeaGreen") latch_epdm(uncompressed=true);', '0,0,8,65,0,135,115'),
 ('epdm_contact_section', section, '29,0,9,90,0,0,64')]
for name,body,camera in details:
    source=WORK/(name+'.scad')
    source.write_text(f'use <{CAD.as_posix()}>\n{body}\n',encoding='utf-8')
    subprocess.run([OSC,'-o',str(ASM/'_work/images'/(name+'.png')),
        '--imgsize=1100,760','--projection=o','--camera='+camera,str(source)],capture_output=True,check=True)
