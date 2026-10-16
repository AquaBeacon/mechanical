"""Render current CAD details, keeping all images and view sources in _work."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[2]
work = root / 'assemblies/child_interior/_work'
views = work / 'intermediate'
images = work / 'images'
views.mkdir(exist_ok=True, parents=True)
images.mkdir(exist_ok=True, parents=True)
items = json.loads((root/'assemblies/child_interior/placement.json').read_text(encoding='utf-8'))['items']
osc = r'C:\Program Files\OpenSCAD\openscad.exe'
def item_source(it, color):
    path = root/it['part']/(it.get('file', Path(it['part']).name)+'.stl')
    ops = ''.join(f'{k}({json.dumps(v)}) ' for op in it.get('ops', []) for k,v in op.items())
    return f'color({json.dumps(color)}) {ops} import("{path.as_posix()}");\n'

flange = ''
for it in items:
    name = it['label']
    if name in ('vtray_deck','flange_brace'):
        flange += 'intersection(){'+item_source(it,[.96,.54,.15])+'translate([-70,-70,0]) cube([140,140,62]);}\n'
    elif name.startswith(('penetrator_', 'flange_screw_', 'flange_spacer_')):
        flange += item_source(it,[.45,.55,.62])
    elif name == 'end_cap_bottom':
        flange += item_source(it,[.7,.75,.8,.4])
clamps = ''.join(item_source(i,[.96,.54,.15] if 'base' in i['label'] else [.35,.63,.74])
                 for i in items if 'rx_clamp_' in i['label'] and '/printed/' in i['part'])
floor = next(i for i in items if i['label']=='vtray_batt_floor')
panels = [('flange_fixed_detail',flange,'Flange roots / WetLink M10 x5'),
          ('paired_clamps_detail',clamps,'RX clamps: 8 parts -> 4'),
          ('floor_strength_detail',item_source(floor,[.96,.54,.15]),'Floor: smaller R3 windows')]
for name,source,caption in panels:
    view=views/(name+'.scad'); view.write_text(source,encoding='utf-8')
    subprocess.run([osc,'-o',str(images/(name+'.png')),'--render','--imgsize=1200,900',
                    '--camera=0,0,0,65,0,35,0','--viewall','--autocenter',
                    '--colorscheme=Tomorrow',str(view)],check=True,
                   creationflags=subprocess.CREATE_NO_WINDOW)
sheet=Image.new('RGB',(1800,510),'#fafafa')
draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',22)
for index,(name,_,caption) in enumerate(panels):
    im=Image.open(images/(name+'.png')).convert('RGB'); im.thumbnail((600,450))
    sheet.paste(im,(600*index,55)); draw.text((600*index+15,15),caption,font=font,fill='#27333d')
sheet.save(images/'print_strength_details.png')
print(images/'print_strength_details.png')
