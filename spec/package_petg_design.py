from pathlib import Path
import json,zipfile,shutil,hashlib
import numpy as np,trimesh
O=Path(__file__).resolve().parents[1]/'assemblies/child_petg100_design';C=O/'cad';P=O/'delivery';P.mkdir(exist_ok=True)
records=json.loads((C/'manifest.json').read_text());axes={'child_core_frame':'Z','child_jaw_gate':'Z','child_cam_bridge':'Y','td04a_socket':'Z','vertical_light_saddle':'X','vertical_light_cap':'X'}
lines=['# 子機外装 PETG・インフィル100％ 設計案','', '2026-09-10。カメラ1台、右側ライト縦向き、持ち手付き。これは試作設計であり、独立解析・メッシュ収束・締結部の実証まで完了した製造承認版ではありません。','', '## ファイルと印刷方向','', 'STLは有効な単一ソリッドSTEPから生成し、閉じた体積であることを確認。delivery/ のSTLは造形方向へ回転し、底面をZ=0へ移動済み。STEPとSCADは組立座標です。','', '| 部品 | PETG換算 kg | 積層法線（組立座標） |','|---|---:|---|']
for r in records:
 n=r['name'];m=trimesh.load(C/r['stl']);axis=axes[n]
 if axis=='X':m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[0,1,0]))
 if axis=='Y':m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
 m.apply_translation(-m.bounds[0]);assert m.is_volume and max(m.extents)<250
 m.export(P/(n+'.stl'));shutil.copy2(C/(n+'.step'),P/(n+'.step'))
 lines.append(f'| {n} | {r["mass_kg"]:.3f} | {axis} |')
for p in C.glob('*.scad'):shutil.copy2(p,P/p.name)
lines+=['',f'6部品合計：約{sum(x["mass_kg"] for x in records):.2f} kg（密度1.27 g/cm³、サポート・ねじ・搭載機器を除く）。全品250 mm立方の範囲内。','', 'PETG 100％、解析と同じ積層方向を維持してください。実際の温度・速度は使用フィラメントの指定値と造形試験で決めます。水平穴、持ち手上面、張り出し部にサポートが必要です。100％設定だけで解析材料カードの強度が実証されるわけではありません。','', '## 収容・取付','', '- 耐圧容器：外径114.3 mm、胴長200 mmの既存配置。端部・ドームも予約。','- カメラ：中央1台、予約寸法94.7×45.9×84.1 mm。既存カメラマウントを中央へ移設。','- ライト：仮寸法外径40×長さ100 mm、軸Z、中心X80/Y−75。分割クランプ。','- TD04A：仮外径26.4 mm、長さ55 mm、底面Z224.5。底面中央から配線。','- 配線：外径6 mm＋周囲1 mm。TD04A配線を中央穴へ下から通すよう修正。曲げ半径は実ケーブルで確認する必要があります。','- 持ち手：52×30 mmの手差し込み空間と後方からの入口を確保。','- 既存のガードリング、クラウン、ケーブルカバー等は交換対象に含めません。旧左右カメラ用のサイドバンパーは新カメラ取付部へそのまま転用できません。新しいカメラ上部ガードは未設計です。','', '## 検証の範囲','', '- assembly_overlap_1mm.json：6部品同士、および実機器・手・配線の予約空間との1 mm格子検査。重なり0。取付金具そのものを入れる空間と本体の除外領域は区別しています。','- gate_opening_exact.json：STEPで0〜90度を1度刻み、91姿勢で検査。コアと耐圧胴・端部との重なり0。連続角度、配線の追従、周辺ガードを含む開閉試験は未完了。','- verification/：100％充填の実CAD重量とPETG直交異方性カードを用いたFEA。支持面は剛固定の近似で、EVA接触、ねじ締付け、インサート引抜きは表していません。','- 分布自重は実体全体に−Z・3gで適用。赤い矢印は各領域の外力、紫は分布自重の方向表示です。','- search_final/：耐圧容器の全ボアを除外した広い設計空間でのtopopt探索。探索中の密度依存自重更新の制約から探索では自重を省略し、実CADのFEAで評価しています。','- 60反復のquick探索は材料分布の参考であり、最大反復終了を収束と呼びません。加工可能な厚いCADへ再構成しており、最適分布をそのまま印刷する形ではありません。','- CalculiXはメッシュ生成に失敗。独立検証は未完了です。コアのメッシュ収束検査も粗い格子で荷重領域を捕捉できず未完了です。','', '## 実形状のFEA結果（単一メッシュ、収束値ではない）','', '| 部品 | 終了判定 | 最小安全率 | 最小p99.5安全率 | 最大変位 mm |','|---|---|---:|---:|---:|']
for n in axes:
 if n in ['child_core_frame','child_jaw_gate','child_cam_bridge']:
  folder=O/'verification'/n
  if n=='child_core_frame' and (O/'verification/core_089_retry/child_core_frame_print_fea.json').exists():folder=O/'verification/core_089_retry'
 else:folder=O/'fixture_checks'/n
 fs=list(folder.glob('*_fea.json'))
 if not fs:continue
 d=json.loads(fs[0].read_text());cases=d['cases']
 # Schema keys are preserved verbatim in the copied evidence.
 sf=[x.get('min_safety_factor',float('nan')) for x in cases]
 p99=[x.get('safety_factor_p99_5',float('nan')) for x in cases]
 lines.append(f'| {n} | {d.get("pass")} | {min(sf):.2f} | {min(p99):.2f} | {max(x["max_displacement_mm"] for x in cases):.3f} |')
 shutil.copy2(fs[0],P/(n+'_fea.json'))
fine=O/'verification/core_089_retry/child_core_frame_print_fea.json'
fine_status='0.89 mm再解析の結果を上表へ反映済み。単一メッシュの再解析であり、メッシュ収束の証明ではありません。' if fine.exists() else '0.89 mm再解析は未完了です。現在の表は1.33 mmの結果です。初回の細分化解析はGPUエラーで停止し、再実行のログは verification/core_089_retry.log と .err にあります。'
lines+=['',fine_status,'','追加の輸送500 N（全備10 kg・5g相当）は verification/*_transport500/ で確認。両部品とも強度・変位基準は満たしましたが、コアの1.33 mmメッシュ解像度は未合格です。主要構造の通常荷重と締結予荷重も別ケースです。','topopt分布との比較では、CAD化により一部ケースでコンプライアンスが増えています。材料量最小の収束解を達成したとは主張しません。','','検査出力の最悪要素とp99.5の両方を確認してください。これらは材料試験・実荷重試験の代わりにはなりません。']
(O/'README.md').write_text('\n'.join(lines),encoding='utf-8');shutil.copy2(O/'README.md',P/'README.md')
for name in ['manifest.json','step_validation.json']:shutil.copy2(C/name,P/name)
for name in ['assembly_overlap_1mm.json','gate_opening_exact.json']:shutil.copy2(O/name,P/name)
h=(O/'review.html').read_text(encoding='utf-8').replace('<img src="design.png">','<img src="design_front.png"><img src="design_rear.png">')
h=h.replace('<h2>除外領域</h2>','<p><a href="README.md">設計条件と検証結果</a> ／ <a href="child_petg100_design.zip">STEP・STL・SCAD一式</a></p><h2>除外領域</h2>')
h=h.replace('<h2>除外領域</h2>','<h2>搭載状態（機器は寸法の予約モデル）</h2><img src="assembly_loaded.png"><h2>除外領域</h2>')
h='<!doctype html><meta charset="utf-8"><title>PETG100 子機外装</title><style>body{font-family:sans-serif;max-width:1100px;margin:30px auto;background:#f4f6f8}img{max-width:100%}p{line-height:1.7}</style><h1>PETG 100% 子機外装・試作設計</h1><p>独立解析・メッシュ収束・締結部の検証は未完了です。力の矢印は方向を示し、長さは力の大きさに比例しません。</p><p><a href="README.md">設計条件と検証結果</a> ／ <a href="child_petg100_design.zip">STEP・STL・SCAD一式</a></p><img src="design_front.png"><img src="design_rear.png"><h2>搭載状態（機器は寸法の予約モデル）</h2><img src="assembly_loaded.png">'+h[h.index('<h2>除外領域</h2>'):]
(O/'review.html').write_text(h,encoding='utf-8')
with zipfile.ZipFile(O/'child_petg100_design.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in P.iterdir():z.write(p,p.name)
 for fn in ['review.html','design_front.png','design_rear.png','assembly_loaded.png','reservations.png']:
  z.write(O/fn,fn)
 for p in O.glob('forces_*.png'):z.write(p,p.name)
 for p in (O/'verification').glob('*_transport500/*_fea.json'):z.write(p,'analysis/'+p.parent.name+'/'+p.name)
 for p in (O/'search_final').glob('*/opt/study_topo.png'):z.write(p,'topopt/'+p.parent.parent.name+'/'+p.name)
 for p in (O/'search_final').glob('*/opt/study.json'):z.write(p,'topopt/'+p.parent.parent.name+'/'+p.name)
print('Packaged',len(records),'parts')
