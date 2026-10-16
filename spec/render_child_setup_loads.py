"""Render all study loads, using topopt's own region masks (no FEA here)."""
from pathlib import Path
import sys
import json, html
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh
from PIL import Image, ImageOps, ImageDraw, ImageFont
from topopt.loadcase import load_case_from_json, region_mask
from topopt.cli.setup import prepare

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'assemblies/child_frame2_assembly/topopt_review_20260910'
plt.rcParams.update({'font.family':'Yu Gothic','font.size':11,'axes.unicode_minus':False})
NAMES={'child_core_frame':'コアフレーム','child_jaw_gate':'可動ゲート（最新ラッチ）','child_cam_bridge':'カメラブリッジ'}
TITLES=[['吊り下げ 3g','側面輸送荷重','ヒンジ側への荷重','背面輸送荷重','締付け荷重','着底荷重','持ち手の持上げ（仮条件）','縦向きライトの荷重'],['吊り下げ 3g','前面荷重','ラッチ側への荷重','締付け荷重','前突モーメント'],['吊り下げ 3g','片側前面への荷重','片側側面への荷重','カメラで持上げ']]

class Arrow3D(FancyArrowPatch):
    def __init__(self,start,end,**kwargs):
        super().__init__((0,0),(0,0),**kwargs); self.points=np.array([start,end])
    def draw(self,renderer):
        x,y,z=proj3d.proj_transform(*self.points.T,self.axes.get_proj())
        self.set_positions((x[0],y[0]),(x[1],y[1])); super().draw(renderer)
    def do_3d_projection(self,renderer=None): return -1e9

def arrow(ax,p,v,color,label):
    v=np.array(v,dtype=float); v=v/np.linalg.norm(v)*48
    ax.add_artist(Arrow3D(p,p+v,mutation_scale=22,lw=2.5,arrowstyle='-|>',color=color,zorder=100))
    ax.text(*(p+v*1.12),label,color=color,fontsize=10,weight='bold',bbox={'facecolor':'white','edgecolor':'none','alpha':.9,'pad':1},zorder=110)

def meshplot(ax,mesh,color,alpha):
    # Full triangle surface, never randomly omit faces.
    poly=Poly3DCollection(mesh.triangles,facecolor=color,edgecolor='none',alpha=alpha,rasterized=True)
    ax.add_collection3d(poly)

def box(ax,bounds):
    import itertools
    pts=np.array(list(itertools.product(*zip(*bounds))))
    for i,p in enumerate(pts):
        for q in pts[i+1:]:
            if np.count_nonzero(p!=q)==1: ax.plot(*np.array([p,q]).T,color='#8e99a7',alpha=.4,lw=.8)

pages=[]; manifest=[]
for ni,(name,jp) in enumerate(NAMES.items()):
    folder=OUT/name
    raw=json.loads((folder/'study.json').read_text(encoding='utf-8'))
    study=load_case_from_json(str(folder/'study.json'))
    setup,report=prepare(study,verbose=False)
    preserved=trimesh.load(folder/'setup/study_preserve.stl',force='mesh')
    # Mesh is exactly the setup voxel surface. Obstacles are on native setup overview;
    # omit opaque forbidden volume on load figures to expose load-bearing interfaces.
    design=trimesh.load(folder/'inputs/design_space.stl',force='mesh')
    images=[]
    for ci,case in enumerate(raw['cases']):
        code=case['name'].split()[0]
        fig=plt.figure(figsize=(13,9),facecolor='#f7f9fb')
        ax=fig.add_axes([.015,.14,.60,.76],projection='3d',computed_zorder=False)
        meshplot(ax,preserved,'#49ac77',.33); box(ax,design.bounds)
        bounds=design.bounds; center=bounds.mean(axis=0); radius=max(np.ptp(bounds,axis=0))/2+57
        ax.set(xlim=(center[0]-radius,center[0]+radius),ylim=(center[1]-radius,center[1]+radius),zlim=(center[2]-radius,center[2]+radius),xlabel='X 左右 [mm]',ylabel='Y 前方 [mm]',zlabel='Z 上方 [mm]')
        ax.set_box_aspect((1,1,1)); ax.view_init(elev=22,azim=(-62 if name=='child_core_frame' else 58))
        ax.set_facecolor('#f7f9fb'); ax.tick_params(labelsize=8)
        texts=[]; marks=[]
        def pts_for(region):
            mask=region_mask(setup.grid,region,study.regions,clip=True)&setup.preserve
            assert mask.any(),region
            return setup.origin+(np.argwhere(mask)+.5)*setup.h
        for si,support in enumerate(case['supports']):
            pts=pts_for(support['region']); p=pts.mean(axis=0)
            ax.scatter(*pts[::max(1,len(pts)//100)].T,s=3,color='#2868bc',alpha=.45,zorder=5)
            ax.text(*p,f'S{si+1}',color='#174e9c',fontsize=9,zorder=105)
        for li,load in enumerate(case['loads']):
            pts=pts_for(load['region']); p=pts.mean(axis=0); v=load['force']
            arrow(ax,p,v,'#d53a38',f'F{li+1}')
            mag=np.linalg.norm(v)
            texts.append(f'F{li+1}  {load["region"]}\n     ({v[0]:g}, {v[1]:g}, {v[2]:g}) N  |F|={mag:g} N')
            marks.append({'id':f'F{li+1}','region':load['region'],'force_N':v,'centroid_mm':p.tolist()})
        if case.get('gravity'):
            gravity=case['gravity']; p=center+[-radius*.66,0,40]
            arrow(ax,p,gravity['direction'],'#c87b00','G')
            texts.append(f'G  自重の方向のみ（矢印位置は作用点ではない）\n     方向 {gravity["direction"]} / {gravity["g_factor"]:g}g')
        fig.text(.045,.95,f'{jp}  /  {code}  {TITLES[ni][ci]}',fontsize=19,weight='bold')
        fig.text(.63,.86,'入力した力（Fx, Fy, Fz）',fontsize=14,weight='bold')
        fig.text(.63,.815,('\n' if len(texts)>5 else '\n\n').join(texts),va='top',fontsize=10 if len(texts)>5 else 11,linespacing=1.25 if len(texts)>5 else 1.45)
        sup='\n'.join(f'S{i+1}  {s["region"]} : {s["fix"]} 固定' for i,s in enumerate(case['supports']))
        fig.text(.63,.28,'支持・固定（青）\n'+sup,va='top',fontsize=10,color='#174e9c')
        fig.text(.045,.085,'緑：残す機能部  /  灰枠：設計空間  /  赤矢印：領域への合計荷重  /  橙：自重',fontsize=11)
        fig.text(.045,.045,'矢印の長さは方向を見せるため一定。領域内へ分布適用し、矢印はその重心に表示。各画像は別の荷重ケース。',fontsize=10,color='#465365')
        path=folder/f'loads_{code}.png'; fig.savefig(path,dpi=145); plt.close(fig)
        images.append(path); manifest.append({'part':name,'case':case['name'],'loads':marks,'gravity':case.get('gravity'),'support_regions':case['supports']})
        pages.append(f'<section><h2>{html.escape(jp)} — {html.escape(code)} {TITLES[ni][ci]}</h2><img src="{name}/{path.name}"></section>')
        print(path.name,flush=True)
    thumbs=[]
    for p in images:
        im=Image.open(p).convert('RGB'); im.thumbnail((1040,720)); thumbs.append(im)
    sheet=Image.new('RGB',(2080,720*((len(thumbs)+1)//2)),'#f7f9fb')
    for i,im in enumerate(thumbs):sheet.paste(im,((i%2)*1040,(i//2)*720))
    sheet.save(OUT/f'{name}_all_loads.png')

(OUT/'load_arrow_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
intro='''<!doctype html><html lang="ja"><meta charset="utf-8"><title>子機外装 — setupと全荷重ケース</title><style>body{font-family:system-ui;background:#edf1f5;color:#203040;margin:32px auto;max-width:1400px}section{background:white;padding:20px;margin:24px 0}img{width:100%}h1{font-size:30px}p{line-height:1.8}a{color:#1265b0}</style><h1>子機外装：setupと全15荷重ケース</h1><p>2026-09-10 / 最適化は未実行。以下は最適化前の設計空間です。緑＝保持、赤＝材料を置けない領域、灰＝設計空間。荷重図の赤は力の矢印です。各ケースは別々に評価し、同時に全ケースの力を加える意味ではありません。</p><p>荷重・支持のボックス領域は保持ボクセルとの重なり部分へ適用されます。領域の一部が保持部から外れる警告があります。支持反力は未知量なので、入力荷重と混同せず青の固定箇所として示しています。保持部をすべて描くため、裏側の矢印も手前に透過表示しています。</p>'''
overview=''.join(f'<section><h2>{jp}：setup全領域</h2><img src="{n}/setup/study_setup.png"><p><a href="{n}/study.json">入力study</a> / <a href="{n}/setup/study_setup.scad">3D setup</a> / <a href="{n}/setup.log">setupログ</a></p></section>' for n,jp in NAMES.items())
intro=intro.replace('全15荷重ケース',f'全{len(manifest)}荷重ケース')
if OUT.name=='child_single_camera_topopt':
    intro=intro.replace('最適化は未実行。','この図はsetup時点の記録です。最適化結果はREADME.mdを参照。')
if (OUT/'scene').exists():
    scene_note='中央カメラ1台、右側縦向きライト1灯。カメラは柱を避けて前へ9mm移動。設計前端137mm、背面−110mmで奥行247mm。ユーザー承認済み構成。最適化の進行結果はREADME.mdを参照。' if OUT.name=='child_single_camera_topopt' else '下図のライト前向き・左右縦向きは選択肢の予約領域です。同時に3灯を搭載する意味ではありません。前向き100mmライトは奥行上限を超過します。'
    intro += '<section><h2>機器・配線・手の除外領域</h2><p>'+scene_note+' 配線は仮の経路包絡で、最小曲げ半径は未確認です。</p><img src="exclusions_front.png"><img src="exclusions_rear.png"><img src="handle_detail.png"></section>'
(OUT/'review.html').write_text(intro+overview+''.join(pages)+'</html>',encoding='utf-8')
print(f'DONE: {len(manifest)} case figures, 3 sheets, review.html',flush=True)
