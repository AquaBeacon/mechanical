"""Collect verified geometry, print provenance and preserved child/floor sources."""
from pathlib import Path
import hashlib,json,sys

R=Path(__file__).resolve().parents[1]
O=R/'assemblies/parent_hand_service'
W=O/'_work/analysis/battery_child_reference_20261012'
side='--battery-side-grooves' in sys.argv
current='--battery-tool-nut' in sys.argv or side
if current:W=O/'_work/analysis/battery_tool_nut_access_20261013'
if side:W=O/'_work/analysis/battery_side_grooves_20261013'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

names=['battery_slide_lid_checks.json','battery_sd_access_checks.json','case_screw_access_checks.json']
if current:names.append('battery_nut_print_checks.json')
checks={n:dict(status=read(O/n)['status'],sha256=sha(O/n)) for n in names}
assert all(c['status']=='PASS' for c in checks.values())
meshes=read(W/'mesh_checks.json');assert meshes['status']=='PASS'
scad=[c for c in read(O/'scad_step_checks.json') if c['part'] in ['battery_base','parent_lipo_retainer_lid_slide']]
assert len(scad)==2 and all(c['valid_step'] and c['closed_stl'] and c['solid_count']==1 for c in scad)
poses=read(O/'assembly_checks.json')
assert len(poses)==2 and all(c['status']=='PASS' and c['step_sha256']==sha(O/(c['pose']+'.step')) for c in poses)
slicing=read(W/'slicing/after_slicing.json')
assert all(c['exit_code']==0 and c['result']['return_code']==0 and c['source_sha256']==sha(R/c['source']) for c in slicing.values())
baseline=read(W/'baseline.json')
protected=[p for p in baseline if p.startswith('parts/child/') or '/floor_plate.' in p or '/main_mount_plate.' in p or (current and '/ann_mb1_' in p and p.endswith(('.step','.stl','.scad')))]
assert protected and all(sha(R/p)==baseline[p] for p in protected)
unchanged=[p for p,h in baseline.items() if p.endswith(('.scad','.step','.stl')) and (R/p).exists() and sha(R/p)==h]
sources=['spec/build_parent_hand_service.py','spec/export_parent_lipo_retainer.py','spec/parent_switch_tx_body.py','scad/lib/parent_battery_slide.py','spec/verify_parent_battery_slide_lid.py','spec/verify_parent_battery_sd_access.py','spec/verify_parent_case_screw_access.py','spec/report_parent_battery_child_reference.py','assemblies/parent_hand_service/placement.json','assemblies/parent_hand_service/service_placement.json','assemblies/parent_hand_service/print_config.json','parts/child/interior/printed/child_vtray_batt_floor/child_vtray_batt_floor.scad']
if current:sources+=['scad/lib/parent_case_access.py','spec/verify_parent_battery_nut_print.py','spec/prepare_parent_battery_support_project.py','parts/parent/interior/printed/parent_hand_service/battery_lid_nut_support_blocker.stl']
if side:sources+=['parts/parent/interior/printed/parent_hand_service/battery_slide_rail_support_blocker.stl']
data=dict(revision='battery_child_reference_20261012',status='CAD_FIT_AND_PRINT_CHECKS_PASS',manufacturing_release=False,checks=checks,scad_checks=scad,mesh_checks=meshes,assembly_checks=poses,slicing=slicing,protected_unchanged_files=protected,unchanged_original_geometry_files=unchanged,source_hashes={p:sha(R/p) for p in sources},limitations=['Physical PETG fit, repeated slide cycles, real leads/foam and single-screw retention strength unverified.','Parent print set and workspace tidiness pass. Existing unrelated print-set failures remain in _work/logs/battery_child_all_printsets.log. Tool tests previously ran 42 tests with one error for a missing child_wte4_suspension_clamp material card; see _work/logs/battery_slide_tools_tests.log.'])
if current:
    data['revision']='battery_tool_nut_access_20261013'
    data['limitations'][1]='Parent print set and workspace tidiness pass. Repository-wide checks retain existing failures in other print sets and a missing child_wte4_suspension_clamp material card; see _work/analysis/battery_tool_nut_access_20261013/all_printsets.log and tools_tests.log.'
if side:
    data['revision']='battery_side_grooves_20261013'
    data['limitations'].append('Full-length lid withdrawal requires raising the battery module after removing its four mount screws; no installed in-case lid extraction.')
(O/'validation_current.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(data['status'],'protected',len(protected),'files unchanged')
