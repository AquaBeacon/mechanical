"""Publish Rev.7 printing notes and derived mesh/support views."""
from pathlib import Path
import json,math,subprocess,sys,shutil,hashlib
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
from prepare_parent_exterior_print_job import saved_mesh
from review_parent_exterior_slices import paths

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
JOB='removable_locators_20261022'
FRAME_DOC='''# 親機・後付け位置決め用の下側プレート Rev.7

2026-10-22。正本はspec/prepare_parent_oneplate.pyとspec/parent_oneplate_frame_sources.py。主面232×134 mm、公称厚20 mm、主面Z=-20..-0.8、三点支持のみZ=0。ロープタブ込み240×134×20 mm。位置決め部4個は別体とし、印刷後にねじ止めする。印刷済みの上側押さえ・脚の取合いを維持。

左右レール：XY=(±110,±8)、上からM4×20ソケット4本。下面の六角穴は天井Z=-12.3、ナット底Z=-15.5。ねじ先端Z=-18.7で脚より1.3 mm上。下面からナットを入れ、レールを締結してから脚を付ける。ナット上面を天井で受けるため締付時に上へ抜けない。

前後アーム：XY=(94,52),(94,62),(-94,-52),(-94,-62)、下からM4×25ソケット4本。ナット底Z=-7.3、頭座面Z=-27.3、先端Z=-2.3で箱底へ出ない。箱を載せる前に上面へナットを入れる。M4普通ナットは計8個。ねじ長さを変更した場合は再検査する。

径10.5 mmの縦ロープ穴4個（X=±111.5/Y=±23）、M5ロッド穴、TD04AとカメラCメス、予備M4穴15箇所を維持。穴配置はspec/parent_oneplate_mounting_pattern.json。厚7 mm・径12 mm治具とM4×25の取付例は先端Z=-2。未知の治具全体は別途検査する。

下面をベッドへ。PETG Basic・X1C・0.4 mm・0.2 mm層・8壁・100%・2 mmブリム。45°自動支持・モデル上も許可したスライスでは、下面ナット座の天井に少量の支持材が残る。六角穴から除去しナットが天井まで入ることを確認する。外周R3・縁0.4 mm・穴入口0.3 mm、機能座面を保持する。

実ねじ・工具・ロープ・印刷済み脚の検査と印刷入口はassemblies/parent_exterior/README.md。実印刷・嵌合・締結・強度・クリープ・浮力は未認定。
'''
LOCATOR_DOC='''# 親機箱の後付け位置決め部 Rev.7

2026-10-22。side_left/side_right/end_fixed/end_pushの4個を主プレートへ後からねじ止めする。正本はspec/prepare_parent_oneplate.pyとspec/parent_oneplate_frame_sources.py。既存バリアントを更新し、旧一体版を現行印刷物へ混ぜない。

左右レールは長さ98 mm・幅15/14.5 mm。固定基準X=-105、押しねじ中心Z=12/Y=±38を維持。主プレート上面Z=-0.8へ載せ、上からM4×20ソケット各2本。頭座面Z=1.3。ロープ穴を迂回する約3.2 mm以上の外側背骨を残し、内側の薄い三日月部分を開放。小さな分断片を作らない。根元の局所補強は0.7 mm。

前後アームは幅20 mm・長さ74/80 mm・厚12 mm、下面Z=-32、接触面Z=-20。固定端Y=115、押しねじ高さZ=9を維持。下からM4×25ソケット各2本、頭座面Z=-27.3。ナットはプレート上面へ。既存の脚は変更しない。

左右は底面を下、前後はY=90°で側面を下に印刷。ねじ穴と前後アームのナット屋根は、その印刷上向きへ55°形状を向ける。外周R1〜2、縁0.4 mm・穴入口0.3 mm。PETG Basic・0.4 mm・0.2 mm層・8壁・100%・ブリム3 mm。自動支持では縁・補強部に少量が残るため、印刷ジョブの図で確認して除去する。座面・基準面へ残さない。

pressure_padは従来のM4ねじ頭径7×高さ4 mm用カップを3個継続し、独立した固定ねじは不要。底を下、0.2 mm層。箱を外すと脱落し得るため回収する。

取付金具はM4×20が4本・M4×25が4本・M4普通ナット（二面幅7×厚3.2）8個。横押し調整ねじとは別。ナットと位置決め部を締結してから脚と箱を装着する。実箱の補正値は未実測のまま0。実印刷・強度・反復位置決めは未認定。検査と印刷入口はassemblies/parent_exterior/README.md。
'''

def archive_printed_job():
    """Preserve the user's three-body project outside the managed STL set."""
    original=A/'parts/parent_oneplate_bar.3mf'
    dest=A/'print_jobs/printed_upper_and_skids_20261021/parent_oneplate_bar.3mf'
    source=original if original.exists() else dest
    if not source.exists():return
    actual,settings=saved_mesh(source);components=actual.split()
    assert len(components)==3
    records=[];counts={}
    for component in components:
        stem='parent_oneplate_bar' if component.volume>200000 else 'parent_oneplate_stand'
        reference=trimesh.load(A/'parts'/(stem+'.stl'),force='mesh')
        def angle(mesh):
            _,axes=np.linalg.eigh(mesh.moment_inertia[:2,:2])
            return math.atan2(axes[1,0],axes[0,0])
        rotation=angle(component)-angle(reference);errors=[]
        for extra in (0,math.pi):
            trial=reference.copy()
            trial.apply_transform(trimesh.transformations.rotation_matrix(rotation+extra,[0,0,1]))
            trial.apply_translation(component.center_mass-trial.center_mass)
            distance=max(float(trimesh.proximity.closest_point(component,trial.vertices)[1].max()),
                         float(trimesh.proximity.closest_point(trial,component.vertices)[1].max()))
            errors.append(distance)
        error=min(errors);assert error<.001,(stem,error)
        counts[stem]=counts.get(stem,0)+1
        records.append(dict(part=stem,maximum_bidirectional_vertex_surface_distance_mm=error,passed=True))
    assert counts==dict(parent_oneplate_bar=1,parent_oneplate_stand=2)
    dest.parent.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    if original.exists():
        assert original.resolve().is_relative_to(ROOT) and dest.resolve().is_relative_to(ROOT)
        assert not dest.exists()
        shutil.move(str(original),str(dest))
    report=dict(original_path='assemblies/parent_exterior/parts/parent_oneplate_bar.3mf',
                sha256=digest,quantity=counts,layer_height=settings.get('layer_height'),
                geometry_matches_current_parts=True,checks=records)
    (dest.parent/'manifest.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (dest.parent/'README.md').write_text('# 印刷済み上側押さえと脚のプロジェクト\n\n'
        '2026-10-22にparts/から履歴へ移動。元の3MFを変更せず保持。上側押さえ1個・脚2個を含み、保存メッシュを現行STLと照合して形状一致を確認。'
        'ユーザー申告の印刷済み部品を維持するための記録で、今回の下側プレート用ジョブではありません。保存された層厚は0.28 mm。'
        '\n\n[保存プロジェクト](parent_oneplate_bar.3mf)／[移動元・SHA-256・形状照合](manifest.json)\n',encoding='utf-8')
    print('Archived printed upper/skids project; all three saved bodies match current geometry',flush=True)

def main():
    for part,doc in [('parent_oneplate_frame',FRAME_DOC),('parent_oneplate_box_locator',LOCATOR_DOC)]:
        (ROOT/'parts/parent/exterior/printed'/part/'README.md').write_text(doc,encoding='utf-8')
    root=A/'print_jobs'/JOB
    stats=json.loads((root/'validation.json').read_text())
    labels={'parent_oneplate_frame':'下側プレート','parent_oneplate_box_locator_side_left':'左レール',
            'parent_oneplate_box_locator_side_right':'右レール','parent_oneplate_box_locator_end_fixed':'固定側アーム',
            'parent_oneplate_box_locator_end_push':'押し側アーム'}
    support_g=0;panels=[]
    for row in stats:
        stem=row['file'][:-4];project=root/stem/(stem+'.3mf')
        mesh,settings=saved_mesh(project)
        density=float(settings['filament_density'][0]);diameter=float(settings['filament_diameter'][0])
        row['support_g_estimate']=row['support_filament_mm']*math.pi*(diameter/2)**2*density/1000
        support_g+=row['support_g_estimate']
        panels.append((stem,mesh,[p for z,f,p in paths(project.parent/'plate_1.gcode') if f.startswith('Support')]))
    fig=plt.figure(figsize=(17,5))
    for i,(stem,mesh,support) in enumerate(panels):
        ax=fig.add_subplot(1,5,i+1,projection='3d')
        ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolor='#bdcdd1' if i==0 else '#45a475',edgecolors='none',alpha=.8))
        ax.add_collection3d(Line3DCollection(support,colors='#f04a18',linewidths=1.7))
        lo,hi=mesh.bounds;extent=hi-lo;mid=(lo+hi)/2;size=max(extent)*.6
        ax.set(xlim=(mid[0]-size,mid[0]+size),ylim=(mid[1]-size,mid[1]+size),zlim=(mid[2]-size,mid[2]+size))
        ax.set_box_aspect([1,1,1]);ax.view_init(-20,225);ax.set_axis_off()
        ax.set_title(stem.replace('parent_oneplate_box_locator_','').replace('parent_oneplate_',''),fontsize=11)
    fig.suptitle('Rev.7 print poses / orange = actual automatic support toolpaths (underside view)')
    fig.tight_layout();fig.savefig(A/'_work/images'/f'{JOB}_supports.png',dpi=150);plt.close(fig)
    def time(s):
        m=round(s/60);return f'{m//60}時間{m%60:02d}分'
    rows=['# 後付け位置決め Rev.7：変更分5個の印刷','',
          '2026-10-22。印刷入口は[parts/PRINT.md](../../parts/PRINT.md)。**上側押さえ1個と脚2個は印刷済みで再印刷不要です。**',
          '今回の変更分は下側プレート1個・左右レール各1個・前後アーム各1個。以下の3MFを各1回ずつ印刷します。カメラ・TD04A・QR等の未印刷部品はこの5ファイルには含みません。',
          '',f'X1 Carbon／0.4 mm／Bambu PETG Basic／Textured PEI Plate、0.20 mm層・8壁・100%充填。変更分合計 **{sum(r["grams"] for r in stats):.1f} g・{time(sum(r["seconds"] for r in stats))}**。スライサー見積りで、実測ではありません。',
          '', '| 3MF（各1個入り） | 見積り | 時間 | 支持材見積り |','|---|---:|---|---:|']
    for r in stats:
        s=r['file'][:-4];rows.append(f'| [{labels[s]}]({s}/{s}.3mf) | {r["grams"]:.1f} g | {time(r["seconds"])} | {r["support_g_estimate"]:.2f} g |')
    rows += ['',f'支持材は5個の合計約{support_g:.2f} gです。自動支持を45°・モデル上も許可したまま保存しています。支持材0の形状ではありません。平板下面のナット座天井、レールの縁、アームの補強部に少量残ります。支持材は六角穴・外側から除去でき、密閉された空洞へ閉じ込めていません。',
             '', '![印刷姿勢と実支持材の位置](../../_work/images/'+JOB+'_supports.png)',
             '', '## 印刷と組立', '',
             '1. まず左右レールと前後アームを印刷し、支持材とブリムを取り除きます。ナット・ねじ頭・接触面に残さず、手持ちのM4金具が入ることを確認してください。',
             '2. 下側プレートを下面を下に印刷。約696 g使うので残量750 g以上を目安にします。下面の六角穴内の支持材も除去してください。主プレートのブリム2 mm、他3 mmを保存済みです。',
             '3. プレート下面から左右レール用のM4ナット4個を入れ、上からM4×20を4本でレールを固定します。ナット上面がポケット天井へ着座します。',
             '4. プレート上面から前後アーム用のM4ナット4個を入れ、下からM4×25を4本でアームを固定します。指定のねじ先端は箱底より2.3 mm下です。',
             '5. 既存の脚と上側押さえを取り付けます。箱を置く前に、ねじ先端と座面を確認してください。横押し調整ねじ・圧力パッドは既存方式です。',
             '', '3MFはBambu Studioでプロジェクトとして開き、機種・ノズル・プレート・装填PETGの割当を確認します。保存した姿勢と設定を使い、支持材はOFFへ変更しないでください。実印刷・締結・強度・クリープは未確認です。',
             '', '[元STLハッシュとスライス結果](validation.json)／[保存3MFと全層の経路検査](../../_work/analysis/'+JOB+'/slice_checks.json)／[組立とネジ指定](../../README.md)', '']
    (root/'README.md').write_text('\n'.join(rows),encoding='utf-8')
    manifest=dict(date='2026-10-22',changed_part_count=5,grams=sum(r['grams'] for r in stats),seconds=sum(r['seconds'] for r in stats),support_g_estimate=support_g,parts=stats,physical_print_verified=False)
    (root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    config=json.loads((A/'print_config.json').read_text(encoding='utf-8'))
    config.update(status='prototype_removable_locators_r7',note=(
        '**2026-10-22 Rev.7：[変更分5個の3MF・印刷手順](../print_jobs/'+JOB+'/README.md)。上側押さえ1個・脚2個は印刷済みで再印刷不要。下表は全体の総数です。** '
        '下側は240×134×20 mm平板、箱位置決め4個は別体。左右M4×20を4本・前後M4×25を4本・M4普通ナット8個。先にナットと位置決め部を付けてから脚・箱を装着。'
        f'変更分5個はPETG Basic・0.2 mm層・8壁・100%、自動支持の合計見積り約{support_g:.2f} g。下面ナット座と縁・補強部の支持材を除去する。'
        'STLは印刷姿勢済み。前後アームはY=90°、左右・平板は底面下。camera_mount_twistは10/21の小型C一体型と専用3MFを継続し、Generic PETG・0.1 mm層・6壁・15% Gyroid・自動支持。'
        '旧Rev.6の6枚3MFは履歴。今回の5個の3MFはカメラ・TD04A・QR等の残り全品を含まない。実印刷・嵌合・強度は未認定。'))
    (A/'print_config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Derived assembly views use the canonical placement; no second placement authority.
    p=json.loads((A/'placement.json').read_text(encoding='utf-8'))
    p['items']=[r for r in p['items'] if r['label']=='open_frame' or r['label'] in ['bolt_on_'+v for v in ('side_left','side_right','end_fixed','end_push')]]
    inter=A/'_work/intermediate';layout=inter/(JOB+'_view.json');layout.write_text(json.dumps(p,ensure_ascii=False),encoding='utf-8')
    scad=inter/(JOB+'_view.scad')
    subprocess.run([sys.executable,str(ROOT/'scad/lib/asm_gen.py'),str(layout),str(scad)],check=True,cwd=ROOT)
    scad.write_text(scad.read_text(encoding='utf-8').replace('import("../../','import("../../../../'),encoding='utf-8')
    result=subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(A/'_work/images'/f'{JOB}_assembled.png'),'--imgsize=1400,950','--viewall','--autocenter','--projection=o','--camera=0,0,0,60,0,30,500',str(scad)],capture_output=True,cwd=ROOT)
    (A/'_work/logs'/f'{JOB}_preview.log').write_bytes(result.stdout+result.stderr)
    assert result.returncode==0 and b'WARNING' not in result.stderr and b'ERROR' not in result.stderr
    print('Published five print projects, notes and support/assembly previews',flush=True)

if __name__=='__main__':
    main()
    archive_printed_job()
