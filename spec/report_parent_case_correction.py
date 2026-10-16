"""Publish current fit/slice evidence and invalidate superseded strength claims."""
from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/analysis/case_cad_correction_20261010'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=['switch_tx_access_checks.json','battery_sd_access_checks.json','gnss_access_checks.json','magnetometer_access_checks.json','mount_axis_checks.json','wave_retention_checks.json','wave_assembly_checks.json','stack_spacer_checks.json','stack_spacer_slice_checks.json']
checks={f:read(O/f) for f in files}
checks['case_fit_checks.json']=read(W/'case_fit_checks.json')
checks['bcas_cad_checks.json']=read(R/'parts/parent/exterior/cots/bcas212310g/_work/analysis/cad_correction_20261010/cad_checks.json')
assert all(d['status']=='PASS' for d in checks.values()),{f:d['status'] for f,d in checks.items()}
assert any(q['part']=='floor vertical insertion from above' and q['pass_'] for q in checks['case_fit_checks.json']['checks'])
cad=read(O/'scad_step_checks.json');assembly=read(O/'assembly_checks.json')
assert all(q['status']=='PASS' and q['step_sha256']==sha(O/(q['pose']+'.step')) for q in assembly)
assert all(q['valid_step'] and q['closed_stl'] for q in cad)
slices=read(W/'slicing/after_slicing.json');assert len(slices)==11
for stem,q in slices.items():assert q['exit_code']==0 and q['source_sha256']==sha(R/q['source'])
grams=sum(q['total_filament_g']*q['quantity'] for q in slices.values())
supports=sum(q['support_extrusion_g']*q['quantity'] for q in slices.values())
slice_record=dict(status='PASS',stl_types=11,print_objects=11,assembled_pieces=18,filament_g=grams,support_g=supports,all_parts_actually_resliced=True,results=slices)
write(O/'case_slicing_checks.json',slice_record)
# Keep the native results and the complete pre-change reports in history.
# Current-geometry flags must not qualify changed CAD using those results.
for f in ['wave_rigidity_acceptance.json','print_rigidity_checks.json']:
 d=read(O/f);d.update(status='CURRENT_GEOMETRY_NOT_ANALYZED',manufacturing_release=False,reference_screening_pass=None,wave_reference_screening_pass=None,guarantee='Case correction changed floor, Sony/GNSS geometry and supports; prior calculations are historical. Current stiffness and physical retention unqualified.',current_reference='_work/analysis/case_cad_correction_20261010/before/checks/'+f)
 for q in d.get('runs',[]):q['current_geometry']=False
 write(O/f,d)
p=O/'wave_analysis_geometry_checks.json';h=W/'before/checks/wave_analysis_geometry_checks.json'
if p.exists() and not h.exists():h.write_bytes(p.read_bytes())
write(p,dict(status='STALE_AFTER_CASE_CORRECTION',current_geometry=False,manufacturing_release=False,reason='Floor/upper carriers/supports changed; retained native runs cannot qualify current CAD.',historical_report='_work/analysis/case_cad_correction_20261010/before/checks/wave_rigidity_acceptance.json'))
for f in ['wave_rigidity_report.md','simple_stack_report.md']:
 p=O/f;s=p.read_text(encoding='utf-8')
 if not s.startswith('> 履歴：'):
  p.write_text('> 履歴：2026-10-11の容器訂正前の形状・結果です。現行の床・台・支持位置の剛性根拠に使用しないでください。現行は[case_fit_report.md](case_fit_report.md)を参照。\n\n'+s,encoding='utf-8')
text=['# 親機：防水容器CADと内装嵌合の訂正','','2026-10-11。メーカーPDF/DXFを読み直した参照CADで、床・ボス・四隅と本体／ふたの誤りを修正した。メーカー製STEPではなく、未図示の成形勾配と実物公差は未確認。原本は[メーカー図面](https://www.takachi-el.co.jp/assets/attachments/images/BCAS212310G.pdf)、再生成元はspec/build_bcas212310g.py。','','| 訂正 | 現行 |','|---|---|','| 床 | 厚3 mm。誤っていた中央中実台を撤去 |','| 内側ボス | 床上7 mm、上面Z10。インサート4＋タップ12 |','| 四隅・壁 | DXFのC形隔壁と断面の側壁勾配 |','| ふた | 本体と別体、屋根下面Z97.1 |','| 内装床 | 四隅0.5 mm逃げ、全ボス逃げ、4座面がZ10へ接触 |','| 固定 | M4×12ボタン4本、公称ねじ込み5.2 mm。型番・実深さ要確認 |','| 配置 | LiPo北3.6、TX南4、GNSS後左脚東2.6 mm。基板高さ維持 |','| GNSS工具 | 後左脚と磁気センサの支柱の間に上方工具逃げ |','','![床と容器の平面確認](_work/images/case_floor_top.png)','','## 検証','','図面由来CADに対し、部品の実STEP干渉、床板の上からの連続挿入、本体／ふたの閉鎖、4接触座、LiPoと蓋の取り出し、両SD・両電源スイッチ、TX実装全外形の上20 mm、箱外MAIN USB、GNSS／LIS3MDL操作、取付穴・工具、組立順、8本ランナーを検査しPASS。結果はvalidation_current.jsonと個別JSON。実物の嵌合や配線の把持を保証するものではない。','','M3ナット座は床格子下面までつながる。Sony後左座の下面の一部は近傍タップボスを逃がし、残る3方向は格子下面まで連続、ボス上面より上は4方向とも連続。床自体は1連結ソリッド。旧「4方向とも全高」の検査は必須ボス逃げを不具合と数えたため、実ボス高さで区切って検証する。剛性の認定には使用しない。','','## 印刷','','入口は[parts/PRINT.md](parts/PRINT.md)。11種類各1個、ランナー切離し後18部品。PETG・0.4 mmノズル・0.2 mm積層・4周壁・100%インフィル。全11形状を実スライスし、STLハッシュを照合した。',f'使用量合計{grams:.2f} g、うちサポート{supports:.2f} g。8本スペーサセットのサポートは0 g。首の2層の押出し経路を確認。結果・3MF・ログは_work/analysis/case_cad_correction_20261010/slicing/。','','## 適用限界','','今回変更した床・Sony／GNSS台・支持位置の剛性解析は未実施。旧2g解析を現行合格として表示しない。旧Sony20Nの変位・強度不合格は履歴に保持し、解消済みと扱わない。メッシュ収束、実締結・緩み・クリープ・波浪試験も未完了。製造リリースは取合い試作。','','ユーザーはメーカーSTEPを所有していないと確認済み。四隅の未図示断面・成形公差、実インサートとねじ、XH・LiPo実寸とリード、5 m同軸の実巻きは現物照合が必要。容器モデルを共有する他の旧内装・外装構成は今回再検証していない。旧CAD・入力・検査は各_work/analysis/内のbeforeに保持。']
(O/'case_fit_report.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
validation=dict(revision='case_cad_correction_20261011',status='CAD_FIT_AND_PRINT_CHECKS_PASS',manufacturing_release=False,checks=checks,scad_step_checks=cad,assemblies=assembly,slicing=slice_record,structural_qualification=dict(status='CURRENT_GEOMETRY_NOT_ANALYZED',wave_reference_screening_pass=None,manufacturing_release=False,reference='wave_rigidity_report.md'),cad_sha256={f:sha(O/f) for f in ['placement.json','closed.step','service.step','parts/manifest.json']},limitations=['Drawing-derived case, not manufacturer STEP; unsectioned molding details and physical fit unverified.','Current stiffness, real bolt/joint retention, creep and wave-cycle tests not qualified.'])
failures=[s for s in (W/'all_packs.log').read_text(encoding='utf-8').splitlines() if s.startswith('FAIL')]
unit=(W/'unittest.log').read_text(encoding='utf-8');ran=re.search(r'Ran (\d+) tests',unit);errors=re.search(r'FAILED \(errors=(\d+)\)',unit)
validation['workspace_checks']=dict(parent_print_pack='PASS',tidy_workspace='PASS',all_print_packs=dict(status='FAIL_OUTSIDE_PARENT_SCOPE' if failures else 'PASS',issues=failures),tools_unittest=dict(status='ERROR_OUTSIDE_PARENT_SCOPE' if errors else 'PASS',tests=int(ran[1]) if ran else None,errors=int(errors[1]) if errors else 0,reason='Existing missing child_wte4_suspension_clamp/spec/bambu_petg_basic_material.json' if errors else None))
write(O/'validation_current.json',validation)
print('PASS current fit/print evidence; current stiffness unqualified',round(grams,2),'g',round(supports,2),'g support')
