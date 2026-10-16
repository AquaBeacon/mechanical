"""Readable CAD section and open-frame views, always from placement.json."""
import hashlib,json
import subprocess
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from prepare_child_horizontal_plate_frame import OUT,ROOT,OSC,load_world

plt.rcParams['font.family']='Yu Gothic'
placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
world=load_world(placement)
# Assembly STL is a view of all placement instances, never a print job.
assembly=OUT/'child_horizontal_plate_frame.stl'
trimesh.util.concatenate([mesh for _,mesh in world]).export(assembly)
provenance={'purpose':'assembly view only; print the separate portable parts',
    'items':len(world),'placement_sha256':hashlib.sha256((OUT/'placement.json').read_bytes()).hexdigest(),
    'output_sha256':hashlib.sha256(assembly.read_bytes()).hexdigest()}
(OUT/'_work/analysis/layout/assembly_stl.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
colors=dict(frame='#397c95',clamp='#778995',vessel='#67a6b7',ballast='#424952',ballast_cap='#c58a3d')
fig=plt.figure(figsize=(16,10),facecolor='#f4f3ef')
fig.text(.04,.95,'固定部とバラストの構成',fontsize=25,color='#29464f',weight='bold')
fig.text(.04,.91,'配置の正本から描画  /  右側板と容器を省略した説明図 + 実メッシュの断面',fontsize=12,color='#62727a')
ax=fig.add_axes([.025,.15,.50,.69],projection='3d',facecolor='#f4f3ef')
light=LightSource(azdeg=30,altdeg=60)
for row,mesh in world:
    if row['group'] in ('fasteners','vessel') or row['label'] in ('right_side_frame','right_front_guard','right_rear_guard'): continue
    color='#c58a3d' if row['label']=='lowest_ballast_frame' or row.get('role')=='detachable_clamp_support' else colors[row['group']]
    collection=Poly3DCollection(mesh.triangles,facecolors=color,shade=True,lightsource=light,rasterized=True)
    collection.set_edgecolor('none');ax.add_collection3d(collection)
ax.set_xlim(-140,140);ax.set_ylim(-190,190);ax.set_zlim(0,240)
ax.set_box_aspect([280,380,240]);ax.view_init(elev=30,azim=34);ax.set_axis_off()
fig.text(.07,.135,'容器を置く前：Cは底板の受けと押さえで固定',fontsize=12,color='#62727a')
for i,(station,title) in enumerate([(-60,'容器支持部  /  Y = −60 mm'),(-24,'円筒バラスト胴部  /  Y = −24 mm')]):
    a=fig.add_axes([.56,.50 if i==0 else .10,.39,.36],facecolor='#f4f3ef')
    for row,mesh in world:
        if row['group']=='fasteners': continue
        section=mesh.section(plane_origin=[0,station,0],plane_normal=[0,1,0])
        if section is None: continue
        color='#c58a3d' if row['label']=='lowest_ballast_frame' or row.get('role')=='detachable_clamp_support' else colors[row['group']]
        for loop in section.discrete:
            a.plot(loop[:,0],loop[:,2],color=color,linewidth=1.1)
    a.set_xlim(-128,128);a.set_ylim(-3,237);a.set_aspect('equal')
    a.set_xticks([-110,0,110]);a.set_yticks([0,75.2,138,200.8,230])
    a.tick_params(labelsize=8,colors='#62727a');a.grid(alpha=.15)
    a.set_title(title,fontsize=13,color='#29464f',loc='left')
    for spine in a.spines.values(): spine.set_color('#d0d7d7')
    if i==0:
        a.annotate('上部へM3固定',xy=(20,200.8),xytext=(48,220),fontsize=9,color='#526975',arrowprops=dict(arrowstyle='-',color='#526975'))
        a.annotate('独立支持治具へ固定',xy=(-20,75.2),xytext=(-100,100),fontsize=9,color='#526975',arrowprops=dict(arrowstyle='-',color='#526975'))
    else:
        a.annotate('C押さえ ×2本/個',xy=(54,62),xytext=(20,105),fontsize=9,color='#91682d',arrowprops=dict(arrowstyle='-',color='#91682d'))
fig.text(.04,.045,'主4枚 + 延長4個 + 回転止め2個 + 支持治具4個 + クランプ2個 + C押さえ4個 = 20個。嵌合・荷重試験前。',fontsize=11,color='#91682d')
fig.savefig(OUT/'_work/images/assembly_details.png',dpi=140);plt.close(fig)
print('Wrote assembly_details.png')

# OpenSCAD's depth-buffer preview keeps the ballast visible behind compound
# frame parts; this derivative view is regenerated from the same placement.
for stem,opened in [('open_frame',True),('protected_frame',False),('linked_clamps',False),('ballast_mount',False)]:
    commands=['// Generated review only; authority is ../../placement.json']
    for row,_ in world:
        if stem=='ballast_mount' and not (row['group'] in ('ballast','ballast_cap') or row['label']=='lowest_ballast_frame'
                or row['label'].startswith(('plate_mount_','ballast_join_'))): continue
        if stem=='linked_clamps' and row['group']!='clamp': continue
        if opened and (row['group']=='vessel' or row['label'] in ('right_side_frame','right_front_guard','right_rear_guard')): continue
        color='#c58a3d' if row['label']=='lowest_ballast_frame' or row.get('role')=='detachable_clamp_support' else '#a0a4a9' if row['group']=='fasteners' else colors[row['group']]
        ops=' '.join(f'{kind}({json.dumps(values)})' for op in row.get('ops',[]) for kind,values in op.items())
        if stem=='linked_clamps' and row['label']=='clamp_linked_upper':
            ops='translate([0,0,25]) '+ops
            color='#397c95'
        source=(ROOT/row['part']/(row['file']+'.stl')).as_posix()
        # Acrylic is translucent in this review, never in the manufacturing data.
        if row['label']=='acrylic_tube_200': color=[.4,.65,.72,.3]
        commands.append(f'color({json.dumps(color)}) {ops} import({json.dumps(source)});')
    view=OUT/f'_work/intermediate/{stem}_view.scad';view.write_text('\n'.join(commands)+'\n',encoding='utf-8')
    result=subprocess.run([str(OSC),'--imgsize=1200,1000','--projection=o','--viewall','--autocenter',
        '--camera=470,370,360,0,0,115','-o',str(OUT/f'_work/images/{stem}.png'),str(view)],
        capture_output=True,text=True,encoding='utf-8',errors='replace')
    (OUT/f'_work/logs/{stem}_preview.log').write_text(result.stdout+result.stderr,encoding='utf-8')
    if result.returncode: raise RuntimeError(f'OpenSCAD preview failed: {stem}')
    print(f'Wrote {stem}.png')

fig,axes=plt.subplots(1,2,figsize=(12,7),facecolor='#f4f3ef')
for ax,limits,title in zip(axes,[(-71,-49),(49,71)],['左の突起受け','右の突起受け']):
    ax.set_facecolor('#f4f3ef')
    for row,mesh in world:
        if row['label'] not in ('end_cap_bottom','left_rotation_key','right_rotation_key'): continue
        section=mesh.section(plane_origin=[0,-111,0],plane_normal=[0,1,0])
        if section is None: continue
        for loop in section.discrete:
            ax.plot(loop[:,0],loop[:,2],color='#b66e32' if row['group']=='vessel' else '#397c95',linewidth=2)
    ax.set_xlim(*limits);ax.set_ylim(110,154);ax.set_aspect('equal');ax.grid(alpha=.2)
    ax.set_title(title,fontsize=15);ax.set_xlabel('X / mm');ax.set_ylabel('Z / mm')
fig.suptitle('蓋外周の実CADに沿う窪み  /  Y = −111 mm',fontsize=20,color='#29464f')
fig.text(.08,.05,'茶：エンドキャップ、青：側板へ直接ねじ止めする独立した受け。片側隙間0.55 mm。\n上から挿入。元の突起が180°対称のため、蓋の穴配列を見て上下を合わせる。',fontsize=12,color='#62727a')
fig.subplots_adjust(bottom=.2,top=.85,wspace=.35)
fig.savefig(OUT/'_work/images/endcap_key_sections.png',dpi=140);plt.close(fig)
print('Wrote endcap_key_sections.png')

# Orthographic sections and hole centres of the real side mesh.
fig,ax=plt.subplots(figsize=(10,10),facecolor='#f4f3ef')
ax.set_facecolor('#f4f3ef')
side=next(m for r,m in world if r['label']=='left_side_frame')
section=side.section(plane_origin=[-116,0,0],plane_normal=[1,0,0])
for loop in section.discrete:
    ax.plot(loop[:,1],loop[:,2],color='#397c95',linewidth=1.3)
holes=np.array(placement['attachment_interface']['hole_centres_yz_mm'])
ax.scatter(holes[:,0],holes[:,1],s=30,color='#c58a3d',label='M3 accessory holes (22 / side)')
key_z=placement['protection']['key_mount_z_mm']; key_y=placement['protection']['key_mount_y_mm']
ax.scatter([key_y]*len(key_z),key_z,s=65,color='#af4c31',marker='s',label='Direct key mount (2 x M3 / side)')
support=placement['clamp_support']
points=np.array([[station+dy,z] for station in placement['clamp_connection']['stations_mm']
                 for dy in support['joint_axial_offsets_mm'] for z in support['joint_z_mm']])
ax.scatter(points[:,0],points[:,1],s=65,color='#29464f',marker='+',label='Clamp supports (8 x M3 / side)')
ax.set_xlim(-125,125);ax.set_ylim(-5,240);ax.set_aspect('equal');ax.grid(alpha=.2)
ax.set_xlabel('Y / mm');ax.set_ylabel('Z / mm');ax.legend(loc='lower center',bbox_to_anchor=(.5,-.16))
ax.set_title('側面フレーム / M3追加取付穴と独立回転止め',fontsize=18,pad=20)
fig.text(.10,.03,'側板は印刷済み。回転止め：M3×25各2本。支持治具：M3×25各4本・開放ナット。',fontsize=11,color='#62727a')
fig.subplots_adjust(bottom=.21,top=.9)
fig.savefig(OUT/'_work/images/side_attachments.png',dpi=150);plt.close(fig)
print('Wrote side_attachments.png')

# Close view of the side-frame fastening, using saved mesh placements.
commands=['// Generated close review from placement.json']
for row,_ in world:
    if row['label'] not in ('left_side_frame','left_rotation_key','left_rear_guard') and not row['label'].startswith('key_join_-1_'):
        continue
    color=([.72,.48,.22,.45] if row['label']=='end_cap_bottom' else
           '#d19043' if row['label']=='left_rotation_key' else
           '#a0a4a9' if row['group']=='fasteners' else '#397c95')
    ops=' '.join(f'{kind}({json.dumps(values)})' for op in row.get('ops',[]) for kind,values in op.items())
    source=(ROOT/row['part']/(row['file']+'.stl')).as_posix()
    commands.append(f'color({json.dumps(color)}) {ops} import({json.dumps(source)});')
view=OUT/'_work/intermediate/rotation_key_mount_view.scad'
view.write_text('\n'.join(commands)+'\n',encoding='utf-8')
result=subprocess.run([str(OSC),'--imgsize=1200,1000','--projection=o',
    '--camera=40,-220,200,-95,-100,134','-o',str(OUT/'_work/images/rotation_key_mount.png'),str(view)],
    capture_output=True,text=True,encoding='utf-8',errors='replace')
(OUT/'_work/logs/rotation_key_mount_preview.log').write_text(result.stdout+result.stderr,encoding='utf-8')
if result.returncode: raise RuntimeError('Independent key mount preview failed')
print('Wrote rotation_key_mount.png')

# New independent lower clamp bracket and its four side fasteners.
commands=['// Generated detachable bracket review from placement.json']
for row,_ in world:
    if row['label'] not in ('left_side_frame','left_clamp_support_-60') and not row['label'].startswith('support_join_-1_-60_'):
        continue
    color='#c58a3d' if row.get('role')=='detachable_clamp_support' else '#a0a4a9' if row['group']=='fasteners' else '#397c95'
    ops=' '.join(f'{kind}({json.dumps(values)})' for op in row.get('ops',[]) for kind,values in op.items())
    source=(ROOT/row['part']/(row['file']+'.stl')).as_posix()
    commands.append(f'color({json.dumps(color)}) {ops} import({json.dumps(source)});')
view=OUT/'_work/intermediate/clamp_support_mount_view.scad'
view.write_text('\n'.join(commands)+'\n',encoding='utf-8')
result=subprocess.run([str(OSC),'--imgsize=1200,1000','--projection=o',
    '--camera=40,-180,120,-75,-60,61','-o',str(OUT/'_work/images/clamp_support_mount.png'),str(view)],
    capture_output=True,text=True,encoding='utf-8',errors='replace')
(OUT/'_work/logs/clamp_support_mount_preview.log').write_text(result.stdout+result.stderr,encoding='utf-8')
if result.returncode: raise RuntimeError('Independent clamp support preview failed')
print('Wrote clamp_support_mount.png')

# Functional fastener sections, from full-resolution placed meshes.
fig,axes=plt.subplots(1,3,figsize=(16,7),facecolor='#f4f3ef')
specs=[('支持治具 / 上段の開放部',[-100,-70,0],[0,1,0],
        ('left_side_frame','left_clamp_support_-60'),('support_join_-1_-60_-10_66_',),(-115,-85),(55,80)),
       ('回転止め / 開放ナット',[-100,-98,0],[0,1,0],
        ('left_side_frame','left_rotation_key'),('key_join_-1_122_',),(-115,-85),(110,135)),
       ('上部フレーム / 上から工具',[-95,-80,0],[0,1,0],
        ('left_side_frame','removable_upper_frame'),('frame_join_-1_-80_205.8_',),(-115,-75),(197,218))]
for ax,(title,point,normal,labels,prefixes,xlim,zlim) in zip(axes,specs):
    ax.set_facecolor('#f4f3ef')
    for row,mesh in world:
        if row['label'] not in labels and not row['label'].startswith(prefixes): continue
        section=mesh.section(plane_origin=point,plane_normal=normal)
        if section is None:continue
        color='#84919a' if row['group']=='fasteners' else '#397c95' if row['label']=='left_side_frame' else '#c58a3d'
        for loop in section.discrete: ax.plot(loop[:,0],loop[:,2],color=color,lw=1.4)
    ax.set_xlim(*xlim);ax.set_ylim(*zlim);ax.set_aspect('equal');ax.grid(alpha=.18)
    ax.set_title(title,fontsize=14,color='#29464f');ax.set_xlabel('X / mm');ax.set_ylabel('Z / mm')
fig.suptitle('埋込み六角溝を廃止 / 貫通ボルト＋開放部の普通M3ナット',fontsize=21,color='#29464f')
fig.text(.06,.16,'青：印刷済み側板   橙：変更した未印刷部品   灰：M3ねじ・ナット・両側ワッシャ\n支持治具と回転止めは側端から、上部は上からナットをスパナで押さえる。ねじ先端の穴も通す。',fontsize=12,color='#62727a',linespacing=1.7)
fig.text(.06,.065,'印刷済み：側板2・底板1・上下クランプ各1を保持。残り15個だけ追加印刷。\n未印刷のM3穴は内接円径3.5 mmの八角形。材質強度と実工具の嵌合は実物確認が必要。',fontsize=11,color='#91682d',linespacing=1.6)
fig.subplots_adjust(top=.85,bottom=.30,wspace=.30)
fig.savefig(OUT/'_work/images/open_nut_fastening.png',dpi=160);plt.close(fig)
print('Wrote open_nut_fastening.png')
