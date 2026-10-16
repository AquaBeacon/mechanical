"""Read native results without replacing FEM or acceptance criteria."""
from pathlib import Path
import json,csv,hashlib,sys
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';D=O/'_work/analysis/wave_rigidity_20261009'
jobs={
 'gnss_frame':('wave_switch_clearance','ccx_converged_surface5'),
 'antenna_rack':('wave_release','ccx_converged_surface5_circle16'),
 'main_carrier':('reinforced_02','ccx_converged'),
 'sony_carrier':('reinforced_02','ccx_converged_h4_surface5_circle16'),
 'floor_plate':('wave_floor_budget','ccx_converged_surface5_floorsmallfaces'),
}
if '--current' in sys.argv:
 jobs=json.loads((O/'wave_analysis_jobs.json').read_text())
 if any(tag.startswith('print_economy') for tag,out in jobs.values()):
  import runpy
  runpy.run_path(str(R/'spec/report_parent_print_rigidity.py'),run_name='__main__')
  raise SystemExit(0)
elif len(sys.argv)>1:
 jobs={name:(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else 'ccx_converged_surface5') for name in jobs}
data={};lines=[]
for name,(tag,out) in jobs.items():
 p=D/tag/name;f=p/out/'ccx_summary.json';e=p/(out+'_execution.json')
 s=json.loads(f.read_text()) if f.exists() else {};execution=json.loads(e.read_text()) if e.exists() else {'completed':False}
 study=json.loads((p/'study.json').read_text())
 data[name]=dict(summary=f.relative_to(O).as_posix(),execution=execution,mesh_convergence=s.get('mesh_convergence'),payload_mass_kg=study['_payload_mass_kg'],printed_mass_kg=study['_self_mass_kg'],runs=[])
 if not s:lines.append(f'| {name} | — | 未完了 | — | — | — | — | — |')
 summaries=sorted(p.glob('ccx_*/ccx_summary.json'))
 data[name]['all_attempts']=[dict(path=q.relative_to(O).as_posix(),execution=json.loads(q.read_text())) for q in sorted(p.glob('ccx_*_execution.json'))]
 for r in [dict(run,source_summary=q.relative_to(O).as_posix()) for q in summaries for run in json.loads(q.read_text()).get('runs',[])]:
  waves=[c for c in r['cases'] if c['case'].startswith('wave_')];ports=[c for c in r['cases'] if c['case'].startswith('port')]
  def maxd(cases):
   return max(c['max_disp_mm'] for c in cases) if cases and all(c.get('max_disp_mm') is not None for c in cases) else None
  wave,port=maxd(waves),maxd(ports)
  sf=[c.get('safety_factor_p99_5') for c in r['cases']];worst=[c.get('worst_element_safety_factor') for c in r['cases']]
  sfmin=min(sf) if sf and all(v is not None for v in sf) else None;wmin=min(worst) if worst and all(v is not None for v in worst) else None
  row=dict(source_summary=r['source_summary'],mesh_mm=r['mesh_target_mm'],native_pass=r.get('pass'),mesh_quality=r.get('mesh_quality'),wave_cases_complete=len(waves)==6 and wave is not None,wave_max_displacement_mm=wave,port_max_displacement_mm=port,p99_5_min_sf=sfmin,worst_min_sf=wmin,
   force_balance=[c.get('equilibrium') for c in r['cases']],moment_balance=[c.get('moment_error') for c in r['cases']])
  data[name]['runs'].append(row)
  fmt=lambda v:'—' if v is None else f'{v:.4f}'
  lines.append(f"| {name} | {r['mesh_target_mm']:g} | {'PASS' if r.get('pass') else 'FAIL'} | {fmt(wave)} | {fmt(port)} | {fmt(sfmin)} | {fmt(wmin)} | {'PASS' if r.get('mesh_quality',{}).get('pass') else 'FAIL'} |")
all_done=all(q['execution'].get('completed') for q in data.values())
out=dict(status='VALIDATION_INCOMPLETE' if all_done else 'ANALYSIS_IN_PROGRESS',guarantee='NOT_ESTABLISHED',manufacturing_release=False,date='2026-10-09',cases='Resultant 2g on +/-X,+/-Y,+/-Z separately, including gravity; no fall/5g certification',reference_max_displacement_mm=.2,existing_port_target=dict(force_N=20,case_relative_mm=.2,status='NOT_ESTABLISHED',reason='Printed bearing fixtures are modeled; compliant PCB, sockets, case and physical joints are not'),native_results=data,
 unresolved=['Mesh convergence/mesh quality and complete solver results are required; a single-level PASS is not release','Case boss height10mm and effective insert depth unmeasured; M4x8 length provisional','Generic dense dry23C PETG, not measured for this printer/material; creep/fatigue not modeled','Actual payloads must be weighed within design budgets; floor budget includes printed fixtures/fasteners','Actual screw preload/loosening, foam compression, lacing and retention under waves are untested','The six axial load cases do not certify every simultaneous oblique/dynamic load'],physical_tests='wave_retention_physical_tests.csv')
(O/'wave_rigidity_acceptance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
text='''# 波揺れに対する現行内装の剛性・固定検証

**全体保証は未成立、製造リリースなし。** 現行CADに補強・固定・留め穴を反映した取合い試作。下表の数値は理想締結における単体の参考応答で、実ケース／基板／ねじを含む保証値ではない。旧rigidity_report.mdは昇降キャリアの履歴。

## 条件と適用範囲

ユーザーの「大きな衝撃より、波に揺られて動かないこと」を受け、落下・5g条件は使用しない。重力込み2gを±X／±Y／±Zの6方向へ個別に与える暫定条件。複合斜方向・動的共振・実波高／周期の認定ではない。各部品の質量予算と自重はstudy.jsonに記録する。床の質量予算はMAIN270／Sony150／アンテナ・巻き束450／GNSS140／PWR100／TX100／電池保持具込み300 g、合計1510 g＋床自身。実物の質量は未測定。

Gmshによる実STEP面の独立再メッシュ、CalculiXの既存topopt経路を使用。ソルバ・材料判定・収束基準は改変しない。表面アルゴリズム／円周最少点数の変更はmesher_override.json、実行・終了コードは各runの入力／execution JSONへ保持する。自重はCAD体積×1270kg/m³を全体積に分配するCLOAD。ネイティブのmoment_errorがDLOAD自重を含めないための入力表現で、負荷を省いたものではない。

PETG汎用直交異方性カードpetg_generic_fff_orthotropic_v1（乾燥23℃、機種固有実測なし）。Ex/Ey/Ez=2100/1750/1150MPa、Gxy/Gyz/Gzx=700/420/420MPa、Xt/Yt/Zt=42/33/25MPa、Xc/Yc/Zc=50/42/35MPa、Sxy/Syz/Szx=20/14/14MPa。要求SF3、ネイティブの最悪要素下限1.5とメッシュ収束5%を維持。部品形状の積層軸Z、PETG・0.2mm・4周壁・100%インフィルがこの中実近似の条件。疎なインフィルへ結果を転用しない。

各台は4本の床側取付部を理想固定。床はケースM4ボスの4支持面を理想固定。樹脂ねじ山、予圧・すべり、PCBとコネクタ、実ケースABS壁／ボス、フォーム接触、鋼板によるラックの剛性増加は含めない。簡略ケースCADは実物より厚い有効内寸壁の代理形状なので、ケース全体FEAの根拠には使わない。

従来のUSB／SD20N・ケース相対変位0.2mm目標は残す。今回の20Nケースは実プリント支持面に与えており、実コネクタの変位ではない。台だけが0.2mmを下回っても全体目標の達成とはしない。

## 現行形状のネイティブ結果

全メッシュ段階を表示。欠損結果をゼロとして扱わず、未完了／不合格を除いて都合のよい段階だけ選ばない。波2g欄は6ケースが揃った段階だけ表示する。

| 部品 | メッシュmm | ネイティブ判定 | 波2g最大mm | 20N最大mm | p99.5最小SF | 最悪要素最小SF | メッシュ品質 |
|---|---:|---|---:|---:|---:|---:|---|
'''+ '\n'.join(lines)+'''

収束判定の詳細・釣合い・全ケースは[wave_rigidity_acceptance.json](wave_rigidity_acceptance.json)とそこに示す元ccx_summary.json。単一段階PASSを収束済みと呼ばない。未完了やメッシュ生成失敗、結果欠損の試行も_work/analysis/wave_rigidity_20261009に保持する。

## 幾何と実物の受入

[wave_analysis_geometry_checks.json](wave_analysis_geometry_checks.json)で解析STEPと現行STEPの外形・体積・対称差を照合。STEP再書出しのヘッダ日時差を形状一致と混同しない。電池／SD／スイッチ／TX／GNSS／LIS3MDLと締結具・工具は各access_checks、ケース固定はwave_retention_checks.jsonを参照する。

4点M4固定、床側16個の上入れM3ナット、各キャリアの長ねじ、基板4穴、GNSS前後押さえ＋4側面ストッパー、LiPo六面フォーム保持、巻き束の編糸留め、GNSS配線留めを組立に反映。長ねじの金属軸による剛性増加と実締結の予圧・すべりは解析へ算入していない。ねじとナットの締付け量を実物で確認し、過締めで樹脂やPCBを変形させず、合いマークを付けて緩みを追跡する。薬剤の適合性は未確認で、任意のねじ止め剤を指定しない。組立順序と連続経路はwave_assembly_checks.jsonを参照。

wave_retention_physical_tests.csvは未記入の実測様式。実重量、ボス高さ／ねじ深さ、実セル・フォームの予圧、糸込みの巻き束寸法を確認し、実使用相当の角度・周期・加速度・回数を記録して揺動前後のずれ／ねじ緩み／コネクタ抜けを測る。USB／SD20Nの実コネクタ・ケース基準変位、使用温度での長時間クリープも別途実測する。未測定欄を仮定で埋めていない。
'''
(O/'wave_rigidity_report.md').write_text(text,encoding='utf-8')
test=O/'wave_retention_physical_tests.csv'
if not test.exists():
 with test.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['case','target','actual_mass_g','temperature_C','angle_period_acceleration_cycles','case_relative_displacement_mm','screw_or_connector_movement','result','notes'])
  for a in 'XYZ':
   for sign in ['-','+']:w.writerow(['wave_'+a+sign,'Record actual wave-like conditions; design reference resultant2g','','','','','','',''])
  for port in ['MAIN_USB','MAIN_SD','SONY_SD']:
   for a in 'XYZ':
    for sign in ['-','+']:w.writerow([port+'_'+a+sign,'20N; case-relative displacement<=0.2mm','','','','','','',''])
print(out['status'])
