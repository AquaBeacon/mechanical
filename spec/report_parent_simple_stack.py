"""Publish current geometry/slice records and native verdicts without hiding fails."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';W=O/'_work/analysis/simple_stack_20261010';F=O/'_work/analysis/wave_rigidity_20261009'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
if (O/'case_fit_report.md').exists():
 raise RuntimeError('Historical geometry only. Use spec/report_parent_case_correction.py for current case-corrected CAD.')
write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=read(O/'_work/analysis/print_economy_20261009/after_slicing.json');new=read(W/'after_slicing.json')
for name in ['machine','process','filament']:assert read(W/(name+'.json'))==read(O/'_work/analysis/print_economy_20261009'/(name+'.json'))
for stem,d in new.items():assert hashlib.sha256((R/d['source']).read_bytes()).hexdigest()==d['source_sha256'] and d['exit_code']==0
before=sum(d['total_filament_g']*d['quantity'] for d in old.values())
before_support=sum(d['support_extrusion_g']*d['quantity'] for d in old.values())
unchanged={stem:d for stem,d in old.items() if stem not in ['floor_plate','sony_upper_carrier','gnss_column_front','gnss_column_rear']}
# Unchanged bodies must still be byte-identical to the previous sliced meshes.
for stem,d in unchanged.items():assert hashlib.sha256((R/d['source']).read_bytes()).hexdigest()==d['source_sha256'],('Reslice changed source',stem)
after=sum(d['total_filament_g']*d['quantity'] for d in [*unchanged.values(),*new.values()])
support=sum(d['support_extrusion_g']*d['quantity'] for d in [*unchanged.values(),*new.values()])
slice_out=dict(status='PASS_CAD_AND_SLICING',before_g=before,after_g=after,before_support_g=before_support,after_support_g=support,filament_reduction_percent=100*(before-after)/before,printed_stl_types=11,print_objects=11,assembled_printed_pieces=18,set_contents=8,changed_sources=new,unchanged_slice_sources=unchanged)
write(O/'simple_stack_checks.json',slice_out)
selection={'floor_plate':['simple_stack_final','ccx_screen_h3_circle16'],'main_carrier':['print_economy_adjusted','ccx_screen_h3_circle16'],'sony_carrier':['simple_stack','ccx_screen_h3_circle16']};write(O/'wave_analysis_jobs.json',selection)
records=[]
for name,(tag,run) in selection.items():
 p=F/tag/name/run/'ccx_summary.json';data=read(p)
 for stage in data['runs']:
  waves=[c for c in stage['cases'] if c['case'].startswith('wave_2g')];ports=[c for c in stage['cases'] if c['case'].startswith('port20N')]
  records.append(dict(part=name,tag=tag,current_geometry=True,summary=p.relative_to(R).as_posix(),mesh_mm=stage['mesh_target_mm'],native_pass=stage['pass'],wave_native_pass=len(waves)==6 and all(c['pass'] for c in waves),wave_mm=max(c['max_disp_mm'] for c in waves),port20N_mm=max((c['max_disp_mm'] for c in ports),default=None),port20N_native_pass=all(c['pass'] for c in ports),p995_sf=stage['safety_factor_p99_5'],worst_sf=stage['worst_element_safety_factor'],mesh_quality_pass=stage['mesh_quality']['pass'],mesh_convergence=data.get('mesh_convergence','not evaluated; one stage')))
fea=dict(status='VALIDATION_INCOMPLETE',manufacturing_release=False,reference_screening_pass=all(r['native_pass'] and max(r['wave_mm'],r['port20N_mm'] or 0)<=.2 for r in records),wave_reference_screening_pass=all(r['wave_native_pass'] and r['wave_mm']<=.2 and r['mesh_quality_pass'] for r in records),guarantee='Physical joints, creep/wave cycling and mesh-density convergence unqualified. Sony20N criteria fail; retained as explicit limitation.',runs=records,conditions='Six resultant2g directions; floor1510g payload plus CAD self-mass, Sony40g plus adapter/column self-mass, MAIN150g. Same generic dry23C dense PETG Z, walls4, infill100%, SF3 / absolute worst1.5. Sony actual printed stack seats are ideally bonded; real steel bolt stiffness/preload/slip omitted.',limitations=['Sony20N case retains original0.2mm and native strength criteria; failed cases are not waived or reduced.','GNSS/rack split interfaces and case/PCB/actual bolt compliance are not qualified.','No physical print, neck break-force, wave-cycle or creep tests. Single3mm stage is not mesh-density convergence.'])
write(O/'wave_rigidity_acceptance.json',fea);write(O/'print_rigidity_checks.json',fea)
lines=['# スペーサ積み上げ改訂の参考剛性解析','','製造リリース・全体剛性保証は未成立。Sonyは実際の上台＋4本の印刷スペーサの接触面を理想接合して計算した。床は現行形状で再計算、MAINは形状一致を検証した前回解析。実ボルトの剛性・予圧・すべり・緩み、ケース／基板変形、樹脂クリープと実波浪は未検証。','','暫定重力込み2gを±X/±Y/±Zへ適用。床搭載質量1510g、Sony基板40g、MAIN150gと実CAD自重。乾燥23℃の汎用直交異方性PETG、積層Z、0.2 mm・4周壁・100%インフィル、中実相当。従来のSD/USB20N、変位目標0.2 mm、SF3、最悪要素下限1.5を維持。Gmsh/CalculiX既存経路の3mm単一段階で、メッシュ密度収束は未認定。','','| 現行モデル | 2g最大変位mm | 2gネイティブ判定 | 20N最大変位mm | 全ケースのネイティブ判定 |','|---|---:|---|---:|---|']
for r in records:
 port='—' if r['port20N_mm'] is None else f"{r['port20N_mm']:.5f}"
 lines.append(f"| {r['part']} | {r['wave_mm']:.5f} | {'PASS' if r['wave_native_pass'] else 'FAIL'} | {port} | {'PASS' if r['native_pass'] else 'FAIL'} |")
lines+=['','Sonyの20Nでは横方向の変位が約1.13 mmとなり0.2 mm目標を超え、一部ケースは最悪要素SFも下限未達。波2gの結果と20Nの結果を分けて表示し、強く押す操作の剛性保証へ転用しない。今回の4本スペーサ構成は操作・嵌合試作として扱い、実締結状態での操作と保持を測定する。','','詳細・全ケース・未達は[print_rigidity_checks.json](print_rigidity_checks.json)と各ネイティブccx_summary.json。幾何一致は[wave_analysis_geometry_checks.json](wave_analysis_geometry_checks.json)。改訂前の壁付きモデルは`_work/analysis/simple_stack_20261010/history/`、ケース干渉を修正する前の床入力は`wave_rigidity_20261009/simple_stack/floor_plate`に履歴として保持し、現行床の解析へ使用しない。']
(O/'wave_rigidity_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
lines=['# 親機：ナット座とスペーサ積み上げ改訂','','2026-10-10。ナット座下面の隙間をなくし、基板高さを維持。Sonyの3面壁を外して印刷スペーサ4本と上台へ分割した。位置決め突起と既存M3×45の共締めを使用する。GNSS既存4支柱と合わせ8本を1枚の切離しランナーで印刷する。','','印刷は11種類・各1個、切離し後18部品。ランナーは組立に使用しない。側面接続部1.2×0.4×自由長1 mm。首をCADで切ると8支柱＋ランナーの9連結成分となり、各支柱の元形状・座面・キーを欠損しないことを検査する。実切離し力は未測定。','','| 変更部品 | 使用量g | サポートg |','|---|---:|---:|']
for name,d in new.items():lines.append(f"| {name} | {d['total_filament_g']:.2f} | {d['support_extrusion_g']:.2f} |")
lines+=['',f'同じローカルX1C／0.4 mm／PETG／0.2 mm・4周壁・100%インフィル設定。前版合計{before:.2f} g→今回{after:.2f} g（{slice_out["filament_reduction_percent"]:.2f}%削減）、サポート{before_support:.2f}→{support:.2f} g。今回変更した3種を実スライスし、残る8種はSTLハッシュ一致を確認して前回の同設定結果を参照した。スペーサセットのサポートは0 g、全体には局所支持が残る。', '', '入口は[parts/PRINT.md](parts/PRINT.md)。実際の解析・3MF・ログは`_work/analysis/simple_stack_20261010/`、集約は[simple_stack_checks.json](simple_stack_checks.json)。3MFは比較用の解析出力で、印刷入口は同梱STL。前版の結果は履歴。', '', '参考剛性ではSonyの波2gは約0.070 mm、20Nは約1.13 mmで旧目標未達。予圧・すべり・メッシュ密度収束と実物試験は未完了。詳細は[wave_rigidity_report.md](wave_rigidity_report.md)。']
(O/'simple_stack_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('slice PASS; wave reference',fea['wave_reference_screening_pass'],'all loads',fea['reference_screening_pass'])
