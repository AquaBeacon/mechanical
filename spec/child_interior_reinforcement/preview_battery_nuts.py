"""Render actual battery nut pockets, assembled and insertion positions."""
import json, subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[2]
w=root/'assemblies/child_interior/_work'
items=json.loads((root/'assemblies/child_interior/placement.json').read_text(encoding='utf-8'))['items']
def src(i,c):
 p=root/i['part']/(i.get('file',Path(i['part']).name)+'.stl')
 ops=''.join(f'{k}({json.dumps(v)}) ' for op in i.get('ops',[]) for k,v in op.items())
 return f'color({json.dumps(c)}) {ops} import("{p.as_posix()}");'
box=next(i for i in items if i['label']=='vtray_batt_box')
nuts=[i for i in items if i['label'].startswith('bolted_nut_') and i['ops'][0]['translate'][0]>0]
nut=min(nuts,key=lambda i:abs(i['ops'][0]['translate'][2]-32))
panels=[]
for name,shift in [('seated',0),('side_insertion',8)]:
 body='intersection(){'+src(box,[.95,.57,.2])+'translate([19,-22,25]) cube([10,14,14]);}'
 body+=f'translate([{shift},0,0]) '+src(nut,[.35,.45,.56])
 f=w/'intermediate'/('battery_nut_'+name+'.scad');f.write_text(body,encoding='utf-8')
 out=w/'images'/('battery_nut_'+name+'.png')
 subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(out),'--imgsize=900,700','--camera=27,-15,32,115,0,35,55','--colorscheme=Tomorrow',str(f)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 panels.append(out)
im=Image.new('RGB',(1800,760),'white');d=ImageDraw.Draw(im);font=ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',28)
for j,p in enumerate(panels):
 im.paste(Image.open(p).convert('RGB'),(900*j,60));d.text((900*j+20,15),['Seated nut (local crop)','Insert from outer side (8 mm away)'][j],fill='black',font=font)
im.save(w/'images/battery_nut_insertion.png')
