"""CLI CAD review previews and a contact sheet; outputs stay with the assembly."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[2]
images = root / 'assemblies/child_interior/_work/images'
images.mkdir(parents=True, exist_ok=True)
osc = r'C:\Program Files\OpenSCAD\openscad.exe'
for name, stem in [('child_vtray_deck','child_vtray_deck_t200'),
                   ('child_flange_brace','child_flange_brace'),
                   ('child_vtray_batt_box','child_vtray_batt_box'),
                   ('child_vtray_batt_floor','child_vtray_batt_floor')]:
    part = root / 'parts/child/interior/printed' / name
    view = part / '_work/intermediate/bolted_preview.scad'
    view.parent.mkdir(parents=True, exist_ok=True)
    view.write_text('import("' + (part / (stem+'.stl')).as_posix() + '");\n', encoding='utf-8')
    preview = part / '_work/images' / (stem+'_preview.png')
    subprocess.run([osc, '-o', str(preview), '--imgsize=1400,1050',
                    '--camera=0,0,0,65,0,210,0', '--viewall', '--autocenter',
                    '--colorscheme=Tomorrow', str(view)],
                   check=True, creationflags=subprocess.CREATE_NO_WINDOW)
sheet = Image.new('RGB', (1800, 1440), '#eef0f4')
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 25)
for index, (name, stem, caption) in enumerate([
    ('child_vtray_deck', 'child_vtray_deck_t200', 'Deck: wider 80 mm roots'),
    ('child_flange_brace', 'child_flange_brace', 'Flange brace: 12 mm beams'),
    ('child_vtray_batt_box', 'child_vtray_batt_box', 'Battery bay: M3 nut pockets'),
    ('child_vtray_batt_floor', 'child_vtray_batt_floor', 'Service floor: wider bolted tab'),
]):
    image = Image.open(root / 'parts/child/interior/printed' / name / '_work/images' / (stem + '_preview.png')).convert('RGB')
    image.thumbnail((880, 660))
    x, y = (index % 2) * 900, (index // 2) * 720
    sheet.paste(image, (x + (900-image.width)//2, y+45+(660-image.height)//2))
    draw.text((x+20, y+12), caption, font=font, fill='#222c38')
sheet.save(images / 'bolted_mount_parts.png')
print(images / 'bolted_mount_parts.png')
