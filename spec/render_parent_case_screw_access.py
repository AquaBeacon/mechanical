"""Derived inspection views only; canonical placements remain unchanged."""
from pathlib import Path
import json,subprocess,math,runpy,os
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/intermediate';I=O/'_work/images';I.mkdir(exist_ok=True)
data=json.loads((O/'placement.json').read_text(encoding='utf-8'))
ops=runpy.run_path(str(R/'scad/lib/asm_gen.py'))['ops_to_scad']
removed=['lipo','lipo_ret_lid','lipo_ret_pads']+['lipo_ret_bolt_'+str(i) for i in range(4)]
for name,cam,subset in [('top','105,115,450,105,115,25',None),('sw','-100,-150,130,25,25,28',['plate','main_mount_plate','coax_ring','antenna_rack','p_main','gnss_antenna','antenna_ground_plate']),('se','340,-100,140,185,25,32',['plate','lipo_tray'])]:
    lines=['// exploration_only: battery/lid/top foam removed for access demonstration.']
    for it in data['items']:
        if it['label'] in removed or it['label'] in ['lid_keepout','box_bcas212310g','tx_top_keepout','coax_coil_keepout']:continue
        if subset and it['label'] not in subset:continue
        p=R/it['part']/(it.get('file',Path(it['part']).name)+'.stl')
        lines.append(f'color("{it.get("color","Gray")}") '+ops(it['ops'])+f'import("{p.as_posix()}",convexity=20);')
    for i,(x,y) in enumerate([[25,25],[185,25],[25,205]]):
        if name=='sw' and i!=0 or name=='se' and i!=1:continue
        axis=[-math.sin(math.radians(10))/math.sqrt(2),-math.sin(math.radians(10))/math.sqrt(2),math.cos(math.radians(10))] if i==0 else [-math.sin(math.radians(10)),0,math.cos(math.radians(10))] if i==2 else [0,0,1]
        end=[x+axis[0]*(110-19)/axis[2],y+axis[1]*(110-19)/axis[2],110]
        lines.append('color("LimeGreen",.65) hull(){'+f'translate([{x},{y},19]) sphere(r=1.75,$fn=24);translate({end}) sphere(r=1.75,$fn=24);'+'}')
        lines.append(f'color("Red") translate([{x},{y},19]) sphere(r=2,$fn=24);')
    scad=W/f'case_screw_access_{name}.scad';scad.write_text('\n'.join(lines),encoding='utf-8')
    subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(I/f'case_screw_access_{name}.png'),'--imgsize=1400,1100','--projection=o','--viewall','--camera='+cam,str(scad)],check=True,capture_output=True,creationflags=0x08000000)
print('Rendered case screw access views',flush=True)
