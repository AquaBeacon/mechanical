"""Two derived inspection views; original CAD/placement stays authoritative."""
from pathlib import Path
import json,subprocess,runpy
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';I=O/'_work/images';C=O/'_work/intermediate'
ops=runpy.run_path(str(R/'scad/lib/asm_gen.py'))['ops_to_scad'];osc='C:/Program Files/OpenSCAD/openscad.exe'
for pose,file in [('closed','placement.json'),('service','service_placement.json')]:
 subprocess.run(['C:/Python313/python.exe',str(R/'scad/lib/asm_gen.py'),str(O/file),str(O/(pose+'_view.scad'))],check=True)
d=json.loads((O/'placement.json').read_text(encoding='utf-8'));lines=['// Exploration only; TX perimeter is open.']
for it in d['items']:
 if it['label'] not in ['tx_improved','sony_upper_carrier','spresense'] and not it['label'].startswith('sony_column_'):continue
 p=R/it['part']/(it.get('file',Path(it['part']).name)+'.stl');color='#32a58d' if '/printed/' in it['part'] else '#526f9e'
 lines.append(f'color("{color}") '+ops(it['ops'])+f' import("{p.as_posix()}",convexity=20);')
f=C/'simple_tx_stack.scad';f.write_text('\n'.join(lines),encoding='utf-8')
subprocess.run([osc,'-o',str(I/'simple_tx_stack.png'),'--imgsize=1400,1100','--projection=o','--viewall','--camera=320,-100,160,170,174,45',str(f)],check=True,capture_output=True,creationflags=0x08000000)
p=R/'parts/common/interior/printed/stack_spacers/parent_stack_spacer_set.stl'
f=C/'stack_spacer_set_view.scad';f.write_text(f'// Inspection, as printed.\ncolor("#32a58d") import("{p.as_posix()}",convexity=20);',encoding='utf-8')
subprocess.run([osc,'-o',str(I/'stack_spacer_set.png'),'--imgsize=1600,900','--projection=o','--viewall','--camera=180,-170,150,62,12,14',str(f)],check=True,capture_output=True,creationflags=0x08000000)
print('Updated assembly views and rendered stack/runner')
