from pathlib import Path
import json,os,runpy
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
a=json.loads((O/'placement.json').read_text(encoding='utf-8'));ops=runpy.run_path(str(R/'scad/lib/asm_gen.py'))['ops_to_scad']
s='// Generated fixed interior. Parameters and sources are canonical in placement.json.\n/* [Inspection] */\nshow_case=true;\nshow_lid_keepout=false;\nshow_tx_keepout=true;\nout_of_case=false;\n'
for it in a['items']:
 p=R/it['part']/(it.get('file',Path(it['part']).name)+'.stl');rel=os.path.relpath(p,O).replace('\\','/')
 prefix=''
 if it['group']=='vessel':prefix='if(show_case) '
 if it['label']=='lid_keepout':prefix='if(show_lid_keepout && !out_of_case) '
 if it['label']=='tx_top_keepout':prefix='if(show_tx_keepout && !out_of_case) '
 if it['label'] in a['moving_labels']:prefix+='translate(out_of_case ? [230,0,0] : [0,0,0]) '
 s+=prefix+f'color("{it.get("color","Gray")}",{it.get("alpha",1)}) '+ops(it['ops'])+f' import("{rel}",convexity=20); // {it["label"]}\n'
(O/'parent_hand_service.scad').write_text(s,encoding='utf-8')
print('Generated fixed interior inspection and out-of-case pose')
