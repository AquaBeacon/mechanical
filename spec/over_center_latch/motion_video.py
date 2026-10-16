"""Render actual generated CAD poses; no physics or real print footage."""
from pathlib import Path
import json,math,subprocess
from geometry import layout,dimensions,pose,over_center,contact_geometry,compression_samples,dead_angle
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio.v2 as imageio

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'parts/common/jigs/over_center_latch'
ASM=ROOT/'assemblies/over_center_latch'
out=ASM/'_work/images';out.mkdir(parents=True,exist_ok=True)
frames=out/'motion_frames';frames.mkdir(exist_ok=True)
logs=ASM/'_work/logs';logs.mkdir(exist_ok=True)
v=json.loads((P/'parameters.json').read_text())
closed=dimensions(v)['closed_angle']
op=v['open_angle'];rel=v['release_angle'];fps=8
font=ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc',22)
small=ImageFont.truetype('C:/Windows/Fonts/meiryo.ttc',16)
phases=[]
def hold(label,angle,hook,sep,n=8):
    phases.extend([(label,angle,hook,sep)]*n)
def move(label,start,end,n):
    for q in np.linspace(0,1,n):
        phases.append((label,*[x+(y-x)*(q*q*(3-2*q)) for x,y in zip(start,end)]))
hold(f'Closed: 40 N target / {closed-dead_angle(v):.1f} deg beyond dead point',closed,0,0)
move('1. Raise lever; release EPDM preload at claw',(closed,0,0),(op,0,0),20)
hold('Open: preload released',op,0,0,6)
move('2. Lift the hood and simple trapezoidal claw',(op,0,0),(op,rel,0),16)
move('3. Separate hosts; A/B screws stay attached',(op,rel,0),(op,rel,20),16)
hold('Detached: bare-hand operation',op,rel,20,8)
move('4. Return receiver',(op,rel,20),(op,rel,0),16)
move('5. Place the printed hook into the receiver',(op,rel,0),(op,0,0),16)
move('6. Lower lever past dead center',(op,0,0),(closed,0,0),20)
hold('Closed: cover folded fully onto the flat host plate',closed,0,0,10)
unique={};gif_frames=[]
intermediate=ASM/'_work/intermediate';intermediate.mkdir(exist_ok=True)
def view_source(angle,hook,sep):
    result='// Verified STL surfaces.\n'
    for item in layout(v,angle,hook,sep):
        if item['label']=='epdm':
            B,C,K,Q,n,u=contact_geometry(v)
            wall=Q-n*(v['epdm_thickness']-v['preload'])
            xs=np.linspace(-v['epdm_height']/2,v['epdm_height']/2,21)+v.get('epdm_tangent_offset',0.)
            if hook or sep or not pose(v,angle)['contact_active']:
                thickness=np.full(len(xs),v['epdm_thickness'])
            else:
                positions,compress,gap,points=compression_samples(v,angle)
                thickness=np.interp(xs,positions,np.minimum(v['epdm_thickness'],gap))
            rear=wall+xs[:,None]*u
            front=rear+thickness[:,None]*n
            poly=np.concatenate([rear,front[::-1]])
            poly[:,0]+=sep
            result+=f'color("Black") translate([0,{v["epdm_width"]/2},0]) rotate([90,0,0]) linear_extrude({v["epdm_width"]}) polygon({json.dumps(poly.tolist())});\n'
            continue
        path=(P/(item['file']+'.stl')).as_posix();pos=json.dumps(item['ops'][0]['translate']);rot=json.dumps(item['ops'][1]['rotate']);col=item['color']
        result+=f'color("{col}") translate({pos}) rotate({rot}) import("{path}");\n'
    return result
writer=imageio.get_writer(out/'operation.mp4',fps=fps,codec='libx264',quality=8,macro_block_size=16)
try:
    for i,(label,angle,hook,sep) in enumerate(phases):
        key=tuple(round(x,5) for x in (angle,hook,sep))
        if key not in unique:
            path=frames/f'cad_{len(unique):03d}.png'
            scene=intermediate/'motion_view.scad';scene.write_text(view_source(angle,hook,sep),encoding='utf-8')
            args=[r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(path),'--imgsize=960,640','--camera=0,0,8,65,0,25,240','--projection=o',str(scene)]
            r=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace')
            if r.returncode or not path.exists() or 'WARNING:' in r.stderr: raise RuntimeError(r.stderr)
            unique[key]=path
        img=Image.open(unique[key]).convert('RGB');draw=ImageDraw.Draw(img)
        draw.rectangle([0,0,960,76],fill='#162b39');draw.text((20,12),label,font=font,fill='white')
        draw.text((20,45),'CAD動作アニメーション／実物動画ではありません',font=small,fill='#b6d6e8')
        draw.rectangle([0,588,960,640],fill='#162b39')
        draw.text((20,596),f'オレンジ：左右リンク　青：爪付き操作レバー　緑：溝付きの台　ゴムは幾何包絡',font=small,fill='white')
        writer.append_data(np.asarray(img));gif_frames.append(img.resize((720,480)))
        if i%20==0: print(f'FRAME {i+1}/{len(phases)}',flush=True)
finally: writer.close()
gif_frames[0].save(out/'operation.gif',save_all=True,append_images=gif_frames[1:],duration=round(1000/fps),loop=0,optimize=False)
(logs/'motion_video.json').write_text(json.dumps(dict(frames=len(phases),fps=fps,duration_s=len(phases)/fps,method='Final STL surfaces, prescribed contact/release poses. Rubber is a geometric envelope, not a deformation solution.',outputs=['operation.mp4','operation.gif']),indent=2)+'\n')
print('VIDEO',out/'operation.mp4',flush=True)
