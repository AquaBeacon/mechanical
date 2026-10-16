"""Create delivery docs, oriented STL files and a self-contained source ZIP."""
import json
import math
import zipfile
from pathlib import Path
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
ASM=ROOT/'assemblies/child_simple_assembly'
PRINT=ROOT/'print_jobs/child_simple'
PRINT.mkdir(exist_ok=True)
checks=json.loads((ASM/'mesh_checks.json').read_text())
cad=json.loads((ASM/'cad_checks.json').read_text())
assert cad['pass'], 'Do not package a model with CAD collisions'
assert cad.get('revision')=='r2_exposed_nuts', 'Do not package stale CAD validation'
rows=[]
for suffix in ['front','rear','guard']:
    name='child_simple_'+suffix
    folder=ROOT/'parts/child/exterior/printed'/name
    mesh=trimesh.load(folder/(name+'.stl'),force='mesh')
    angle=math.pi/2 if suffix=='front' else -math.pi/2 if suffix=='rear' else 0
    matrix=trimesh.transformations.rotation_matrix(angle,[1,0,0])
    mesh.apply_transform(matrix)
    mesh.apply_translation(-mesh.bounds[0])
    assert mesh.is_watertight and max(mesh.extents)<250
    mesh.export(PRINT/(name+'_print.stl'))
    record=checks['parts'][name]
    dims=' × '.join(f'{x:g}' for x in record['bbox_mm'])
    role={'front':'前枠。カメラ用ブリッジのM3 40×40穴を前面中央に設置。','rear':'後枠。TD04Aの後付けL字マウント用M3 40×40穴を背面上部に設置。','guard':'下部配線ガードr2。4支柱の段差で枠を支え、M3×35の8本と外付けナットで固定。埋め込み・先入れ不要。'}[suffix]
    text=f'''# {name}

{role}

## 主要寸法・インタフェース

- 外形：{dims} mm。樹脂実体の体積：{record['volume_cm3']:.1f} cm³。
- 設計の正本：[共有パラメータ](../../../../../scad/lib/child_simple_frame.scad)。
- 対象：WTE4 Ø114.3×200の縦置き子機。2026-09-16ユーザー確認済み。
- 寸法と穴座標・ねじ一覧：[組立仕様](../../../../../assemblies/child_simple_assembly/README.md)。

## 印刷向き

[印刷条件と配置済みSTL](../../../../../print_jobs/child_simple/PRINT.md)。PETG、サポートあり。最新のスライス状況はリンク先を参照。実機印刷は未実施。

## 検証・荷重ケース

STL閉メッシュ、単一連結体。STEPソリッド検査と容器・ねじの干渉検査は通過。
100 Nのマウント荷重、300 Nの保持／着底・輸送荷重のうち該当ケースをFEAで検査した。
**メッシュ収束は不合格。要求安全率4を下回る最悪要素もあり、強度合格品ではない。**
たわみ・安全率と境界条件の限界：[検証結果](../../../../../assemblies/child_simple_assembly/verification.md)。

## 部品外の考慮・要確認

ナット、工具、配線用の空間を確保。ガードのナットは外付けで、容器の装着後でも交換できる。
ドームリング実寸、EVA締め代、実配線、ねじの緩み対策、吊り状態は現物確認が必要。
カメラ・TD04Aと専用マウント、バラスト、ケーブルの最終配置は未反映。
'''
    (folder/(name+'.md')).write_text(text,encoding='utf-8')
    convergence=json.loads((ASM/('fea_'+suffix+'_final')/(name+'_fea_convergence.json')).read_text())
    for case,info in convergence['cases'].items():
        f=info['runs'][-1]
        rows.append(f"| {suffix} / {case} | {f['max_disp_mm']:.3f} | {f['min_safety_factor']:.2f} | {f['safety_factor_p99_5']:.2f} | 不合格 |")

report='''# 検証結果 — 2026-09-16 r2（外付けナット）

## 結論

**形状・組立確認用の試作設計。構造強度の合格判定は得られていない。**

## 形状

- 3個のSTLは閉メッシュ、法線整合、単一連結体。各部品STEPも有効な単一ソリッド。
- 耐圧容器との15組＋新規部品間3組、合計18組で交差体積0.01 mm³未満。
- M3マウント8穴、前後締結4本、ガード8本とナット／工具の合計32領域で不要な交差なし。
- ガードの受け面4か所は各320 mm²。枠下面・支柱上面の双方が受け面を形成することをCADで確認。
- ガードのナット厚4 mm、両側ワッシャ、外径10 mm工具の進入経路を容器装着状態で検査。埋め込み・熱圧入・先入れは不要。
- 組立STEPは8部品、欠落0。読み戻し配置検査も8部品すべて一致。
- 根拠：`cad_checks.json`、`mesh_checks.json`、`build_assembly.log`、`step_vs_stl.log`。
- 新規3部品のチューブ参照はユーザー確認内容で固定済み。リポジトリ全体の参照検査は40件中34件の既存未確認／変更検出で不合格（`interface_check.log`）。新規3件の指摘はない。

## 造形

X1C実用250³に3部品とも収まる。最小肉厚の自動検査は合格。
前後枠はY軸方向に積層し、機体Z方向の引張りを層面内に置く。
ただし3部品ともサポート面積15%の自動基準を超え、造形判定全体は不合格。
サポートを有効にしてスライス・造形確認する。ガードはZ荷重と積層方向の一致も警告される。
圧縮荷重でも横荷重による層間曲げがあるため、この警告を強度合格に読み替えない。

## FEA：未収束の参考値

PETG異方性モデル、前後枠build_axis=Y、ガードbuild_axis=Z、要求安全率4、許容変位2 mm。
3段階（4 / 2 / 1 mm）で検査。以下は最細1 mmの出力であり、**最終強度値ではない**。
最悪要素とp99.5を併記する。p99.5だけでは合格判定しない。

| 部品／ケース | 最大変位mm | 最悪要素の安全率 | p99.5安全率 | メッシュ収束 |
|---|---:|---:|---:|---|
'''+ '\n'.join(rows)+'''

### 荷重と限界

- マウント：前後締結のボルト周辺を固定し、取付板に面外100 N。後付けマウントの質量が未定のため設計用仮定。
- 容器保持：各半枠の吊り穴周辺を固定し、下側保持帯へ300 N下向き。全備約6 kg×5gを各半枠に単独で掛ける保守的なケース。
- ガード：8個の取付ボルト周辺を固定し、下のリングへ着底300 N、横X/Y各300 N。段差の面接触による荷重分担は計算に入れず、ボルト拘束だけで検査する。
- ボルト周辺の固定パッチによる応力集中、細いM3穴の離散化、対称な応力集中点の入れ替わりが含まれる。
  これらは今回解消・検証しておらず、低い最悪要素安全率を無視する根拠にはできない。
- EVAの面接触、ねじ予荷重、部品間の滑り、衝撃、水中・長期使用は未計算。
- r1のナット先入れ型は`revisions/r1_captive_nut/`へ記録。以下のFEAはr2の形状で再実行した結果。未収束の数値から旧版との改善率は算出しない。

**実運用前に残る作業**：ドームリング実測、実物合わせ、最終マウント荷重の定義、締結接触を含む強度再検証と荷重試験。
解析入力は`child_simple_*_study.json`、結果は`fea_*_final/`に保存してある。
'''
# Keep count tied to the actual checker output.
report=report.replace('合計32領域',f"合計{len(cad['hardware'])}領域")
(ASM/'verification.md').write_text(report,encoding='utf-8')

zip_path=PRINT/'child_simple_print_pack.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
    z.write(ROOT/'scad/lib/child_simple_frame.scad','sources/child_simple_frame.scad')
    for suffix in ['front','rear','guard']:
        name='child_simple_'+suffix
        z.write(PRINT/(name+'_print.stl'),name+'_print.stl')
        z.writestr('sources/'+name+'.scad',f'include <child_simple_frame.scad>\n{name}();\n')
        folder=ROOT/'parts/child/exterior/printed'/name
        z.write(folder/(name+'.step'),'step/'+name+'.step')
    z.write(ASM/'verification.md','verification.md')
    z.writestr('README.txt','Simple child enclosure r2 PROTOTYPE. 3 parts, M3 mounts 40x40 mm.\nGuard: four bearing shoulders, eight M3x35 through bolts, exposed nuts. NO embedded inserts or captive nuts.\nSTLs are oriented for printing. Enable supports, PETG, 100% infill.\nSources are standalone: open sources/child_simple_front.scad etc.\nStructural FEA has NOT passed mesh convergence or all worst-element strength criteria.\nSee verification.md; confirm dimensions and loads before operational use.\n')
print(zip_path)
