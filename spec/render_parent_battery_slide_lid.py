"""Inspection views of the one-screw battery lid; not an assembly source."""
from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/intermediate';I=O/'_work/images';I.mkdir(exist_ok=True)
base=(R/'parts/parent/interior/printed/parent_hand_service/battery_base.stl').as_posix()
lid=(R/'parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer_lid_slide.stl').as_posix()
screw=(R/'parts/common/interior/cots/screw/screw_m3x12.stl').as_posix()
for name,shift,z in [('closed',0,29),('released',-55,29),('open',-108,40)]:
    text=f'// exploration_only: local inspection view\ncolor("DarkOrange") import("{base}",convexity=20);\ncolor("Gold",.7) translate([{shift},0,{z}]) import("{lid}",convexity=20);'
    if name=='closed':text+=f'\ncolor("Silver") translate([12,5,32]) import("{screw}");'
    scad=W/f'battery_slide_lid_{name}.scad';scad.write_text(text,encoding='utf-8')
    subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(I/f'battery_slide_lid_{name}.png'),'--imgsize=1200,900','--projection=o','--viewall','--camera=160,-130,140,52,27,20',str(scad)],check=True,capture_output=True,creationflags=0x08000000)
text=f'// exploration_only: side groove section at local X60\ncolor("DarkOrange") intersection(){{import("{base}");translate([59.9,-5,20]) cube([.2,65,15]);}}\ncolor("Gold") intersection(){{translate([0,0,29]) import("{lid}");translate([59.9,-5,20]) cube([.2,65,15]);}}'
scad=W/'battery_slide_lid_section.scad';scad.write_text(text,encoding='utf-8')
subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(I/'battery_slide_lid_section.png'),'--imgsize=1200,800','--projection=o','--camera=140,27,28,60,27,28','--render',str(scad)],check=True,capture_output=True,creationflags=0x08000000)
print('Rendered closed/released/open and hook section',flush=True)
for name,cam,section in [('nut_mouth','12,-35,35,12,5,24',False),('nut_section','12,-35,25,12,5,25',True),('tool_hole','52,27,150,52,27,0',False)]:
    body=f'import("{base}",convexity=20);'
    if section:body=f'intersection(){{{body} translate([5,4.9,19]) cube([14,.2,12]);}}'
    scad=W/f'battery_{name}.scad';scad.write_text('// exploration_only: battery access inspection\ncolor("DarkOrange") '+body,encoding='utf-8')
    subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(I/f'battery_{name}.png'),'--imgsize=1200,900','--projection=o','--camera='+cam,'--render',str(scad)],check=True,capture_output=True,creationflags=0x08000000)
