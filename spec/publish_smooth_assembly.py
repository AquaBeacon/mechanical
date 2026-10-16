from pathlib import Path
import json, shutil, zipfile, html

root = Path(__file__).resolve().parents[1]
out = root / 'assemblies/child_petg100_design/smooth_assembly'
records = json.loads((out / 'manifest.json').read_text(encoding='utf-8'))
for part in ('child_core_frame', 'child_jaw_gate'):
    shutil.copy2(out / 'extraction' / part / 'study_t50_smooth.stl', out / f'{part}_smooth.stl')

readme = '''# TO_printing スムース結果とアセンブリ

青のコアと緑のゲートは、収束したトポロジー最適化の密度結果から、TO_printing の topopt extract で生成したスムース形状です。手作業で再構成した厚肉CADではありません。

## 処理

- 元データ: search_final/<part>/continuation_mma/opt。コア374反復、ゲート207反復で収束。
- コマンド: python -m topopt extract <opt> --study <study.json> --out <extraction> --levels 0.5 --pick 0.5 --no-fea
- 3 mmボクセル、しきい値0.5。TO_printingのGaussian平滑化（既定sigma 1 voxel）とmarching cubesを使用。
- child_core_frame_smooth.stl と child_jaw_gate_smooth.stl は処理出力をそのままコピー。単位mm。
- PETG・インフィル100%は元の設計条件。平滑化後のFEAは未実施。

## アセンブリ

assembly.scad をOpenSCADで開くと色分けされた配置を確認できます。meshesフォルダを隣に置いてください。
23項目を収録。輸送用ドームキャップは通常表示では非表示（show_transport=trueで表示）。
圧力容器、上下フランジ、底蓋、ドーム、ガード、クラウン、ケーブルカバー、カメラ取付部、ライト取付部、TD04Aソケット、左右バンパーを配置しました。
カメラ1台・縦向きライト・TD04Aは外形モデル、赤色は配線の予約空間です。ライトは仮寸法Ø40×100 mm。内部電子部品と締結ねじはモデルに含みません。
左右バンパーは既存SCADを一眼配置に合わせて変更した配置案です。パラメータは同梱SCADとmanifest.jsonに記載。
assembly_preview.stl は予約空間を含む表示用の重ね合わせであり、一体印刷用データではありません。

## 残っている確認事項

- コアのスムースSTLは4つの閉じたシェルを含みます。約0.293 mm³の微小な孤立片と負の符号付き体積を持つ2シェルがあります。後者は内部空洞境界の可能性があるため削除していません。extractは複数シェル警告で終了コード1でした。ゲートは1シェルです。
- 精密CAD接合面の復元処理は適用していません。3 mm格子由来の穴・接合面を含みます。
- 平滑化後の干渉、開閉軌跡、配線クリアランス、強度は未検証。別途作成した厚肉CADでの検証結果はこの形状には適用できません。
- カメラブリッジの側面締結穴には約1 mmの底が残る構成で、バンパー締結部は修正・確認が必要です。
- 元の最適化は収束していますが、最終FEAのメッシュ解像度判定は不合格です。この一式は配置確認用で、印刷・使用承認済みの設計ではありません。

## 収録部品

'''
readme += '\n'.join('- ' + r['name'] for r in records) + '\n'
(out / 'README.md').write_text(readme, encoding='utf-8')
rows = ''.join(f'<tr><td>{html.escape(r["name"])}</td><td><a href="meshes/{r["name"]}.stl">STL</a></td><td>{r["triangles"]:,}</td></tr>' for r in records)
page = '''<!doctype html><html lang="ja"><meta charset="utf-8"><title>スムース結果・アセンブリ</title>
<style>body{font:16px/1.7 system-ui;margin:32px auto;max-width:1100px;padding:0 20px;background:#f4f6f8;color:#18242d}img{width:49%;vertical-align:top}a{color:#075ba3}table{border-collapse:collapse;width:100%;background:white}td,th{padding:8px;border-bottom:1px solid #ddd;text-align:left}.note{padding:16px;background:#fff0d4}</style>
<h1>TO_printing スムース結果とアセンブリ</h1>
<p>青：収束したコア（374反復）／緑：収束したゲート（207反復）。TO_printing の <code>topopt extract</code> で実際の密度結果を平滑化しています。</p>
<p><a href="child_core_frame_smooth.stl">コア・スムースSTL</a>　<a href="child_jaw_gate_smooth.stl">ゲート・スムースSTL</a>　<a href="smooth_assembly.zip">アセンブリ一式 ZIP</a>　<a href="assembly.scad">OpenSCAD</a></p>
<img src="front.png" alt="前方から見たアセンブリ"><img src="rear.png" alt="後方から見たアセンブリ">
<p>外装と搭載機器の配置モデルです。カメラは1台、ライトは縦向き。カメラ・ライト・TD04Aは外形モデル、赤は配線予約空間です。内部電子部品と締結ねじは含みません。輸送キャップは同梱し、画像では非表示です。</p>
<p class="note">配置確認用：コアには微小な孤立片を含む複数シェルが残っています。平滑化後の接合面・干渉・開閉・強度は未検証です。バンパー締結穴にも修正が必要です。<a href="README.md">処理条件・残課題</a></p>
<h2>部品データ（mm）</h2><p>STLはアセンブリ座標に配置済みです。assembly_preview.stl は表示用で、一体印刷用ではありません。</p>
<table><tr><th>部品</th><th>データ</th><th>三角形数</th></tr>'''+rows+'</table></html>'
(out / 'review.html').write_text(page, encoding='utf-8')
with zipfile.ZipFile(out / 'smooth_assembly.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for p in sorted(out.rglob('*')):
        if p.is_file() and p.suffix != '.zip':
            archive.write(p, 'smooth_assembly/' + p.relative_to(out).as_posix())
print(json.dumps({'parts': len(records), 'zip_bytes': (out/'smooth_assembly.zip').stat().st_size, 'review': str(out/'review.html')}))
