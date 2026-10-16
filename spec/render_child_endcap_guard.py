"""Every revision: closed/open views and a fixed-camera opening/closing GIF."""
import copy
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scad/lib'))
from asm_gen import ops_to_scad

ASM = ROOT / 'assemblies/child_endcap_guard'
data = json.loads((ASM / 'placement.json').read_text(encoding='utf-8'))
params = json.loads((ROOT/'parts/child/exterior/printed/child_endcap_guard/parameters.json').read_text(encoding='utf-8'))
hy, hz = params['hinge_y'], params['hinge_z']
images = ASM / '_work/images'
intermediate = ASM / '_work/intermediate'
images.mkdir(parents=True, exist_ok=True)
intermediate.mkdir(parents=True, exist_ok=True)
def scene(angle):
    lines = ['// GENERATED preview from placement.json. Do not edit.']
    for item in data['items']:
        item = copy.deepcopy(item)
        if angle and item['label'].startswith('latch_'):
            continue  # removed for opening
        if angle and item['label'] == 'guard_integrated':
            item['ops'] += [{'translate':[0,hy,hz]}, {'rotate':[-angle,0,0]}, {'translate':[0,-hy,-hz]}]
        source = (ROOT / item['part'] / (item['file']+'.stl')).as_posix()
        lines.append('color("'+item['color']+'") '+ops_to_scad(item['ops'])+' import("'+source+'");')

    return '\n'.join(lines)+'\n'

oscad = r'C:\Program Files\OpenSCAD\openscad.exe'
print_view = intermediate/'print_pose_preview.scad'
print_source = (ROOT/'parts/child/exterior/printed/child_endcap_guard/child_endcap_guard_integrated.stl').as_posix()
print_view.write_text('color("Orange") import("'+print_source+'");\n',encoding='utf-8')
subprocess.run([oscad,'-o',str(images/'print_pose.png'),'--imgsize=1100,1000',
                '--viewall','--autocenter','--projection=o','--camera=0,0,0,60,0,25,0',
                '--colorscheme=Tomorrow',str(print_view)],check=True)
subprocess.run([oscad,'-o',str(images/'root_fillet_closeup.png'),'--imgsize=900,760',
                '--projection=o','--camera=45,-45,9,60,0,25,125',
                '--colorscheme=Tomorrow',str(print_view)],check=True)
for angle, name in ((0,'closed'),(85,'open')):
    path = intermediate / (name+'_preview.scad')
    path.write_text(scene(angle), encoding='utf-8')
    subprocess.run([oscad,'-o',str(images/(name+'.png')),
                    '--imgsize=1200,1000','--viewall','--autocenter','--projection=o',
                    '--camera=0,0,0,125,0,25,0','--colorscheme=Tomorrow',str(path)],check=True)

# Fixed framing: no per-frame autocenter or viewall, so the vessel stays still.
frame_dir = images/'animation_frames'
frame_csg = intermediate/'animation'
frame_dir.mkdir(exist_ok=True)
frame_csg.mkdir(exist_ok=True)
font = ImageFont.truetype(r'C:\Windows\Fonts\meiryo.ttc',20)
forward = []
for angle in range(0,111,5):
    path = frame_csg/('angle_%03d.scad'%angle)
    png = frame_dir/('angle_%03d.png'%angle)
    path.write_text(scene(angle),encoding='utf-8')
    subprocess.run([oscad,'-o',str(png),'--imgsize=900,760','--projection=o',
                    '--camera=0,-85,-60,125,0,25,650','--colorscheme=Tomorrow',str(path)],check=True)
    frame = Image.open(png).convert('RGB')
    draw = ImageDraw.Draw(frame)
    draw.rectangle((0,0,900,43),fill='white')
    draw.text((20,8),'開閉 %d°'%angle,font=font,fill='#303030')
    draw.text((20,725),'橙: 一体ガード / 青: 固定側蝶番の仮配置',font=font,fill='#303030')
    forward.append(frame)
    print('GIF frame %d/110 degrees'%angle,flush=True)

# Use a common palette to keep identical part colours in every frame.
samples = Image.new('RGB',(2300,85),'white')
for i,frame in enumerate(forward):
    small = frame.copy()
    small.thumbnail((100,85))
    samples.paste(small,(i*100,0))
palette = samples.quantize(colors=128)
sequence = forward+forward[-2:0:-1]
indexed = [frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in sequence]
durations = [100]*len(indexed)
durations[0] = 1000
durations[len(forward)-1] = 1000
gif = images/'opening_closing.gif'
indexed[0].save(gif,save_all=True,append_images=indexed[1:],duration=durations,
                loop=0,disposal=2,optimize=False)
with Image.open(gif) as check:
    assert check.n_frames == len(indexed)
    assert check.size == (900,760)
(ASM/'_work/logs').mkdir(exist_ok=True)
(ASM/'_work/logs/animation.json').write_text(json.dumps({
    'gif':gif.relative_to(ROOT).as_posix(),'frames':len(indexed),
    'angle_range_degrees':[0,110],'sequence':'closed-open-closed',
    'camera':'0,-85,-60,125,0,25,650','fixed_camera':True,
    'hinge_axis_local':[0,hy,hz],'source':'placement.json'},indent=2)+'\n',encoding='utf-8')
print('Wrote '+str(gif),flush=True)

# Actual filleted BRep section, to make the two tab-only recesses visible.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Meiryo'
section = json.loads((ROOT/'parts/child/exterior/printed/child_endcap_guard/_work/intermediate/key_section.json').read_text(encoding='utf-8'))
fig, ax = plt.subplots(figsize=(8,7))
for name, colour in (('guard','#e78b20'),('cap','#657785')):
    for i, points in enumerate(section[name]):
        xs, ys = zip(*points)
        ax.plot(xs,ys,color=colour,lw=2,label=('一体受け' if name=='guard' else 'エンドキャップ') if i==0 else None)
for sign in (-1,1):
    ax.annotate('突起部だけ凹む',xy=(sign*60.7,0),xytext=(sign*39,29),
                ha='center',arrowprops={'arrowstyle':'->','color':'#444444'})
ax.annotate('その他は内側へ張り出す',xy=(0,-57.7),xytext=(0,-32),
            ha='center',arrowprops={'arrowstyle':'->','color':'#444444'})
ax.set(xlim=(-73,73),ylim=(-73,73),aspect='equal',xlabel='X [mm]',ylabel='Y [mm]',
       title='方向合わせ用受けの実形状断面（キャップ面の下側）')
ax.legend(loc='upper right')
ax.grid(alpha=.2)
fig.tight_layout()
fig.savefig(images/'key_receiver_section.png',dpi=160)
plt.close(fig)
