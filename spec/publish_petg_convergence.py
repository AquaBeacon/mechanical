from pathlib import Path
import json,subprocess,html
O=Path(__file__).resolve().parents[1]/'assemblies/child_petg100_design'
panels=[];report=[]
for n,label,cam in [('child_core_frame','コア（持ち手側）','-400,-550,380,0,0,100'),('child_jaw_gate','ゲート','400,550,380,0,0,100')]:
 stage='continuation_mma' if (O/f'search_final/{n}/continuation_mma/opt/study.json').exists() else 'continuation'
 pending=(O/f'search_final/{n}/continuation_mma/study.json').exists() and stage!='continuation_mma'
 rel=f'search_final/{n}/{stage}/opt';out=O/rel
 d=json.loads((out/'study.json').read_text());hist=d['history'];term=d['termination_reason']
 sc=O/f'converged_{n}.scad';sc.write_text(f'color("{ "SteelBlue" if n=="child_core_frame" else "SeaGreen" }")import("{rel}/study_final.stl");')
 png=f'converged_{n}.png'
 subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(O/png),'--imgsize=1100,950','--viewall','--autocenter','--camera='+cam,'--projection=o',str(sc)],check=True,capture_output=True)
 report.append({'part':n,'termination_reason':term,'iterations':len(hist),'last_criteria':hist[-1].get('criteria'),'checks':d.get('checks'),'optimization_summary_pass':d.get('pass')})
 failed=sorted({c['name'] for f in d.get('final_fea',[]) for c in f.get('checks',[]) if not c['pass']})
 failure_text='、'.join({'mesh resolution':'解析格子の解像度','strength':'強度','stiffness':'剛性'}.get(x,x) for x in failed)
 fea_note=('出力形状のFEAは未合格：'+failure_text) if failed else '出力形状の単一格子FEAは合格（メッシュ収束・独立解析の完了を意味しません）'
 pending_note='<p><strong>MMAで継続計算中です。以下は直前の未収束結果です。</strong></p>' if pending else ''
 panels.append(f'<section><h2>{label}</h2>{pending_note}<p>終了理由：{html.escape(term)} ／ 今回{len(hist)}反復</p><p>{html.escape(fea_note)}</p><img src="{png}"><p><a href="{rel}/study_final.stl">最適化出力STL</a> ／ <a href="{rel}/study.json">判定と全履歴JSON</a></p><img src="{rel}/study_topo.png"></section>')
(O/'convergence_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
header='<!doctype html><meta charset="utf-8"><title>トポロジー最適化の収束結果</title><style>body{max-width:1150px;margin:32px auto;font-family:sans-serif;background:#f4f6f8;line-height:1.8}img{max-width:100%}section{background:white;padding:20px;margin:24px 0}</style><h1>トポロジー最適化の結果</h1><p>前回の結果形状を初期形状として再最適化した直接出力です。内部状態の復元ではありません。密度場は再初期化され、ケース正規化係数もツールで再計算されるため、前回と今回の正規化目的関数の数値は直接比較できません。材料・荷重・除外領域・3 mm格子・体積率は維持しています。</p><p>penal=3、beta=16、造形方向の制約は最初から最終設定を適用。収束閾値は緩めていません。自由設計領域に残す材料の体積率35％と、造形物内部のインフィル100％は別の指定です。最適化の収束と強度検証の合格は別です。この出力は印刷用完成品ではありません。</p>'
(O/'topology_result.html').write_text(header+''.join(panels),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
