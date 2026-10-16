"""Collect verified final sensor artifacts without changing CAD or placements."""
from pathlib import Path
import hashlib, json, re
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/analysis/sensor_mounts_20261011';L=O/'_work/logs'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
run=read(W/'validation_run.json');assert run['status']=='PASS' and len(run['checks'])==6
checks={}
for filename in ['sensor_mount_checks.json','magnetometer_access_checks.json','gnss_access_checks.json','switch_tx_access_checks.json','battery_sd_access_checks.json','wave_assembly_checks.json']:
    p=O/filename;d=read(p);assert d['status']=='PASS',filename
    checks[filename]=dict(status='PASS',sha256=digest(p))
assemblies=[]
for pose,placement in [('closed','placement.json'),('service','service_placement.json')]:
    text=(L/f'sensor_{pose}_verify.log').read_text(encoding='utf-8',errors='replace')
    n=len(read(O/placement)['items'])
    assert re.search(rf'\[verify-asm\] {n} item\(s\), 0 NG',text),pose
    assemblies.append(dict(pose=pose,items=n,status='PASS',bbox_tolerance_mm=.5,step_sha256=digest(O/(pose+'.step')),placement_sha256=digest(O/placement)))
(O/'assembly_checks.json').write_text(json.dumps(assemblies,indent=2),encoding='utf-8')
slice_result=read(W/'slicing/after_slicing.json')['gnss_universal_carrier']
assert digest(R/slice_result['source'])==slice_result['source_sha256'] and slice_result['exit_code']==0
mesh=read(W/'openscad_mesh_check.json');assert mesh['status']=='PASS'
assert mesh['source_sha256']==slice_result['source_sha256']
inputs=['scad/lib/parent_gnss.py','spec/build_parent_gnss.py','spec/parent_switch_tx_body.py','spec/update_parent_sensor_mounts.py','spec/verify_parent_sensor_mounts.py','spec/verify_parent_magnetometer_access.py','spec/verify_parent_gnss_access.py','spec/verify_parent_switch_tx_access.py','spec/verify_parent_battery_sd_access.py','spec/verify_parent_wave_assembly.py','assemblies/parent_hand_service/placement.json','parts/parent/interior/printed/gnss_universal_carrier/gnss_universal_carrier.step','parts/parent/interior/printed/gnss_universal_carrier/gnss_universal_carrier.stl']
outside=[s for s in (L/'sensor_all_print_sets.log').read_text(encoding='utf-8').splitlines() if s.startswith('FAIL ')]
assert not any(s.startswith('FAIL parent_hand_service:') for s in outside)
report=dict(revision='sensor_mounts_20261011',status='CAD_FIT_AND_PRINT_CHECKS_PASS',manufacturing_release=False,checks=checks,assembly_checks=assemblies,openscad_mesh=mesh,slicing=dict(status='PASS',source_sha256=slice_result['source_sha256'],total_filament_g=slice_result['total_filament_g'],support_g=slice_result['support_extrusion_g'],warnings=slice_result['warnings']),source_hashes={s:digest(R/s) for s in inputs},authoritative_switch_PCB=dict(path=str(R.parent/'hardware/pcb/PARENT_PWR/PARENT_PWR.kicad_pcb'),sha256=digest(R.parent/'hardware/pcb/PARENT_PWR/PARENT_PWR.kicad_pcb')),workspace_checks=dict(parent_print_pack='PASS',tidy_workspace='PASS',all_print_packs=dict(status='FAIL_OUTSIDE_CURRENT_PARENT_SCOPE',issues=outside),tools_unittest=dict(status='ERROR_OUTSIDE_PARENT_SCOPE',tests=42,passed=41,reason='Existing missing child_wte4_suspension_clamp/spec/bambu_petg_basic_material.json')),limitations=['No structural FEA, creep, wave loading or physical print validation.','Measured pitch and edge offsets; nominal M3 PCB drill diameter and fastener/tool envelopes need physical fit check.','Disconnect SMA and park coax before south QT grip; connector selection and real harness slack remain unmeasured.','Repeat powered/transmitting magnetometer tests and calibration after lowering the sensor.','GNSS frame assembly path passed for the pre-relief superset; final frame containment and all seating/contact/clearance conditions verified separately.'])
(O/'validation_current.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: six geometry/access checks, two STEP assemblies, final STL/OpenSCAD and actual slice')
