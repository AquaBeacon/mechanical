"""Publish the current corner-support fit/print evidence, without strength claims."""
from pathlib import Path
import hashlib,json,re,sys
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/analysis/fixed_plates_20261011'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=['switch_tx_access_checks.json','battery_sd_access_checks.json','gnss_access_checks.json','magnetometer_access_checks.json','mount_axis_checks.json','wave_retention_checks.json','wave_assembly_checks.json','stack_spacer_checks.json','stack_spacer_slice_checks.json']
checks={f:read(O/f) for f in files};checks['case_fit_checks.json']=read(W/'case_fit_checks.json')
assert all(q['status']=='PASS' for q in checks.values()),{f:q['status'] for f,q in checks.items()}
cad=read(O/'scad_step_checks.json');assemblies=read(O/'assembly_checks.json')
assert all(q['valid_step'] and q['closed_stl'] and q['solid_count']==1 for q in cad)
assert not any(q['part'] in ['main_lower_carrier','sony_upper_carrier','main_offset_corner']+[f'sony_corner_{i}' for i in range(4)] for q in cad)
assert all(q['status']=='PASS' and q['step_sha256']==sha(O/(q['pose']+'.step')) for q in assemblies)
slices=read(W/'slicing/after_slicing.json');assert len(slices)==11
for stem,q in slices.items():assert q['exit_code']==0 and q['source_sha256']==sha(R/q['source']),(stem,'stale slicing')
assert (W/'pack_check.log').read_text(encoding='utf-8').strip()=='PASS parent_hand_service'
assert 'PASS:' in (W/'tidy.log').read_text(encoding='utf-8')
grams=sum(q['total_filament_g']*q['quantity'] for q in slices.values())
support=sum(q['support_extrusion_g']*q['quantity'] for q in slices.values())
old=read(W/'before/validation_current.json')['slicing']['filament_g']
if '--validation-only' not in sys.argv:
 p=O/'fixed_plate_report.md';s=p.read_text(encoding='utf-8')
 s+='\n## 検証結果\n\n'
 s+='図面由来容器CADと閉蓋、部品間干渉、4点の実取付穴、床固定、連続した組立経路、工具経路、LiPo・両SD・両電源スイッチ、箱外MAIN USB、GNSS取出し、TX上方20 mm、同軸収納包絡を再検査しPASS。実物の公差・配線把持を保証するものではない。\n\n'
 s+='OpenSCAD独立レンダリングとSTEP/STL外形・体積、閉メッシュ、2つの組立STEP、12本のランナー部品と切離し後13連結成分（廃棄ランナー含む）も確認。首の0.2/0.4 mm両層に実G-codeの押出しを確認した。\n\n'
 s+=f'X1 Carbon・0.4 mmノズル・PETG・0.2 mm積層・4周壁・100%インフィルで全11形状を実スライス。合計{grams:.2f} g（固定板を追加する前の{old:.2f} gとの差は{grams-old:+.2f} g）、サポート{support:.2f} g。12本ランナーのサポートは{slices["parent_stack_spacer_set"]["support_extrusion_g"]:.2f} g。結果・3MF・設定は_work/analysis/fixed_plates_20261011/slicing/。\n\n'
 s+='両固定板は平らな下面をベッドに向ける。MAIN板のサポートは0 g、Sony板は局所に約0.04 g、柱セットは0 g。固定板の穴は一定幅の矩形肉抜きで、部品・ピン形状に沿う加工ではない。基板裏面と板の公称余裕はMAIN1.745 mm、Sony0.55 mm。CAD形状・操作と印刷姿勢の検証であり、実物の公差を保証しない。\n\n'
 s+='現行支持の剛性解析・メッシュ収束、実締結・波浪・クリープは未実施。旧解析は現行の合格根拠に使用しない。取合い試作の状態を維持する。前の独立支持具と検証は_work/analysis/fixed_plates_20261011/before/へ保存。\n'
 p.write_text(s,encoding='utf-8')
failures=[q for q in (W/'all_packs.log').read_text(encoding='utf-8').splitlines() if q.startswith('FAIL')]
unit=(W/'unittest.log').read_text(encoding='utf-8');ran=re.search(r'Ran (\d+) tests',unit)
validation=dict(revision='fixed_plates_20261011',status='CAD_FIT_AND_PRINT_CHECKS_PASS',manufacturing_release=False,checks=checks,scad_step_checks=cad,assemblies=assemblies,
 slicing=dict(status='PASS',stl_types=11,print_objects=11,assembled_pieces=22,runner_members=12,filament_g=grams,support_g=support,previous_filament_g=old,all_parts_actually_resliced=True,results=slices),
 structural_qualification=dict(status='CURRENT_GEOMETRY_NOT_ANALYZED',manufacturing_release=False,wave_reference_screening_pass=None,reference='wave_rigidity_report.md'),
 cad_sha256={f:sha(O/f) for f in ['placement.json','closed.step','service.step','parts/manifest.json']},
 source_sha256={f:sha(R/f) for f in ['spec/build_parent_hand_service.py','spec/parent_switch_tx_body.py','scad/lib/parent_corner_mounts.py','spec/build_parent_stack_spacers.py','spec/parent_access_common.py']},
 workspace_checks=dict(parent_print_pack='PASS',tidy_workspace='PASS',all_print_packs=dict(status='FAIL_OUTSIDE_CURRENT_PARENT_SCOPE' if failures else 'PASS',issues=failures),tools_unittest=dict(status='ERROR_OUTSIDE_PARENT_SCOPE' if 'FAILED' in unit else 'PASS',tests=int(ran[1]) if ran else None,reason='Existing missing child_wte4_suspension_clamp/spec/bambu_petg_basic_material.json' if 'FAILED' in unit else None)),
 limitations=['Drawing-derived case; physical molding details/tolerances unverified.','Current stiffness, screw retention, creep and wave cycles unqualified.'])
(O/'validation_current.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS current fixing-plate fit/print evidence',round(grams,2),'g; current stiffness unqualified')
