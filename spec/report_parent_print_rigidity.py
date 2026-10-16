"""Read native solver verdicts and compare the existing0.2mm design target.

No solver, constitutive model or native acceptance rule is implemented here.
All unsuccessful design trials remain visible in the report.
"""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/analysis/wave_rigidity_20261009'
selection={'floor_plate':'print_economy_final','main_carrier':'print_economy_adjusted','sony_carrier':'print_economy_adjusted'}
sources={'floor_plate':'parent_hand_service/floor_plate','main_carrier':'parent_hand_service/main_lower_carrier','sony_carrier':'parent_hand_service/sony_upper_carrier'}
# Preserve pre-revision current pointers/reports before publishing new sources.
history=O/'_work/analysis/print_economy_20261009/history/assemblies/parent_hand_service'
for name in ['wave_analysis_jobs.json','wave_rigidity_acceptance.json','wave_analysis_geometry_checks.json']:
 if not (history/name).exists():shutil.copy2(O/name,history/name)
(O/'wave_analysis_jobs.json').write_text(json.dumps({name:[tag,'ccx_screen_h3_circle16'] for name,tag in selection.items()},indent=2),encoding='utf-8')
records=[]
for tag in ['print_economy','print_economy_adjusted','print_economy_final']:
 for file in sorted((W/tag).glob('*/ccx_*/ccx_summary.json')):
  data=json.loads(file.read_text());name=file.parent.parent.name
  actual=R/'parts/parent/interior/printed'/(sources[name]+'.step')
  analyzed=file.parent.parent/(name+'.step')
  current=tag==selection[name] and analyzed.read_bytes()==actual.read_bytes()
  for run in data['runs']:
   cases=run.get('cases',[]);wave=[c for c in cases if c['case'].startswith('wave_2g')];port=[c for c in cases if c['case'].startswith('port20N')]
   maximum=lambda rows:max((c['max_disp_mm'] for c in rows if c.get('max_disp_mm') is not None),default=None)
   wave_max=maximum(wave);port_max=maximum(port)
   records.append(dict(part=name,tag=tag,current_geometry=current,summary=file.relative_to(R).as_posix(),mesh_mm=run['mesh_target_mm'],native_pass=run['pass'],mesh_quality_pass=run['mesh_quality']['pass'],wave_mm=wave_max,port20N_mm=port_max,p995_sf=run['safety_factor_p99_5'],worst_sf=run['worst_element_safety_factor'],target_0_2mm_met=len(wave)==6 and max(q for q in [wave_max,port_max] if q is not None)<=.2,mesh_convergence=data.get('mesh_convergence','not evaluated; single mesh stage'),step_sha256=hashlib.sha256(analyzed.read_bytes()).hexdigest()))
current=[r for r in records if r['current_geometry']]
assert {r['part'] for r in current}==set(selection),('Missing current solver data',current)
out=dict(status='VALIDATION_INCOMPLETE',manufacturing_release=False,guarantee='Not established: new split joints, whole enclosure compliance, mesh convergence and physical wave/creep tests unqualified.',reference_screening_pass=all(r['native_pass'] and r['mesh_quality_pass'] and r['target_0_2mm_met'] for r in current),runs=records,conditions='Same six resultant2g directions, floor1510g payload budget plus CAD self-mass; unchanged20N SD/USB cases on MAIN/Sony; generic dry23C dense PETG Z-axis,4walls,100%infill, SF3 and native worst-element minimum1.5; bolted interfaces ideal fixed',limitations=['Native PASS concerns native material/equilibrium/mesh criteria.0.2mm is the preexisting displacement target shown separately, never hidden behind native PASS.','Initial floor6mm grid and MAIN all-through pockets exceeded0.2mm and were revised.','GNSS upper frame/columns and antenna tower/ring joint behavior have not been mechanically requalified. Previous integral-frame results are historical.','Single-stage solve convergence is not mesh-density convergence. Do not infer enclosure-level displacement from separate fixtures.'])
(O/'print_rigidity_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'wave_rigidity_acceptance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 印刷削減改訂の剛性検討','','全体保証・製造リリースは未成立。床板・MAIN/Sony台の現行形状を既存Gmsh/CalculiX経路で再計算した。分割したGNSS支柱とアンテナ台／リングの接合、実ケースと基板の変形、予圧・すべり・緩み、使用温度でのクリープ・実波浪での繰返し保持は未実測。','','条件は重力込み暫定2gを±X/±Y/±Zへ個別に適用。床の搭載質量予算1510 gと実CAD自重を維持。MAIN/Sonyは従来のSD/USB20Nも維持。汎用乾燥23℃の直交異方性PETG、積層Z、0.2 mm・4周壁・100%インフィル、中実相当。理想締結。SF3、最悪要素下限1.5、メッシュ収束5%の条件は変更していない。今回の単一3mm段階はメッシュ密度収束を認定しない。材料定数・自重入力の詳細は改訂前の記録`_work/analysis/print_economy_20261009/history/assemblies/parent_hand_service/wave_rigidity_report.md`。','','| 形状 | 部品 | メッシュmm | ネイティブ判定 | 波2g最大mm | 20N最大mm | 0.2mm目標 | p99.5 SF / 最悪SF |','|---|---|---:|---|---:|---:|---|---|']
for r in records:
 fmt=lambda q:'—' if q is None else f'{q:.4f}'
 lines.append(f"| {'現行' if r['current_geometry'] else '改訂過程・履歴'} | {r['part']} ({r['tag']}) | {r['mesh_mm']} | {'PASS' if r['native_pass'] else 'FAIL'} | {fmt(r['wave_mm'])} | {fmt(r['port20N_mm'])} | {'達成' if r['target_0_2mm_met'] else '超過／未完了'} | {r['p995_sf']:.2f} / {r['worst_sf']:.2f} |")
lines += ['','ネイティブPASSと変位目標は別に表示する。最初の格子と貫通ポケット案の目標超過も保持した。最終床は格子幅7.5 mm、MAINは操作部の下側支持板を残した。詳細・各ケースと実行入力は[print_rigidity_checks.json](print_rigidity_checks.json)から元のネイティブ記録を参照する。改訂前の一体GNSS・アンテナ台などの数値を現在の分割構造へ転用しない。','','実物の受入記録は`wave_retention_physical_tests.csv`。分割キーの嵌合、床側16ナット、長ねじ、4ケースボスの実寸を確認し、組立後の揺動と緩み・変位を測る。印刷／アクセスの検証結果は[print_economy_report.md](print_economy_report.md)。']
(O/'wave_rigidity_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(out['status'],'current screening',out['reference_screening_pass'])
