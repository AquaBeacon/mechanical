from pathlib import Path
import sys,json,copy,os
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'spec'));sys.path.insert(0,str(ROOT/'scad/lib'))
from build_parent_spar_bolted import run,OSC
from check_asm_contacts import load
OUT=ROOT/'assemblies/parent_bottom_sensors'
asm=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
lower=copy.deepcopy(asm)
lower['items']=[it for it in asm['items'] if it['group'] in ['exterior','hardware','reference','envelope'] and (load(ROOT,it).bounds[1,2]<-225 or it['label']=='beam_lower')]
(OUT/'lower_placement.json').write_text(json.dumps(lower,indent=2),encoding='utf-8')
run([sys.executable,ROOT/'scad/lib/asm_gen.py',OUT/'lower_placement.json',OUT/'lower_view.scad'],OUT/'lower_view.log')
for name,scad,angle in [('lower_preview',OUT/'lower_view.scad',145),('preview_alternate',OUT/'parent_bottom_sensors_view.scad',145)]:
 run([OSC,'--imgsize=1400,1400','--viewall','--autocenter',f'--camera=0,0,0,68,0,{angle},1100','-o',OUT/(name+'.png'),scad],OUT/(name+'.log'))
print('Previews rendered',flush=True)
