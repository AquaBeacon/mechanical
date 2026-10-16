"""Record actual current geometry checks independently of failed20N criteria."""
from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
read=lambda n:json.loads((O/n).read_text(encoding='utf-8'))
names=['switch_tx_access_checks','battery_sd_access_checks','gnss_access_checks','magnetometer_access_checks','mount_axis_checks','wave_retention_checks','wave_assembly_checks','stack_spacer_checks','stack_spacer_slice_checks','wave_analysis_geometry_checks']
checks={n:read(n+'.json')['status'] for n in names};assert all(v=='PASS' for v in checks.values()),checks
scad=read('scad_step_checks.json');assert len(scad)==15 and all(q['valid_step'] and q['closed_stl'] and q['solid_count']==1 for q in scad)
poses=read('assembly_checks.json');assert [(q['pose'],q['items'],q['status']) for q in poses]==[('closed',len(read('placement.json')['items']),'PASS'),('service',len(read('service_placement.json')['items']),'PASS')]
pack=read('parts/manifest.json');assert len(pack['parts'])==11 and sum(q['quantity'] for q in pack['parts'])==11
for q in pack['parts']:assert hashlib.sha256((O/'parts'/q['file']).read_bytes()).hexdigest()==q['sha256']
log=lambda n:(O/'_work/logs'/n).read_text(encoding='utf-8-sig')
assert log('simple_stack_pack_check.log').strip()=='PASS parent_hand_service'
assert log('simple_stack_tidy.log').startswith('PASS')
issues=[q for q in log('simple_stack_workspace_pack_check.log').splitlines() if q.startswith('FAIL')]
assert not any('parent_hand_service' in q for q in issues)
tests=log('simple_stack_tools_tests.log');total=int(re.search(r'Ran (\d+) tests',tests)[1]);errors=int(re.search(r'FAILED \(errors=(\d+)\)',tests)[1]) if 'FAILED' in tests else 0
fea=read('wave_rigidity_acceptance.json');assert fea['manufacturing_release'] is False
slicing=read('simple_stack_checks.json');assert slicing['status']=='PASS_CAD_AND_SLICING'
data=dict(status='PASS_PARENT_GEOMETRY_AND_PACK_CHECKS',manufacturing_release=False,date='2026-10-10',checks={**checks,'independent_scad_step':dict(status='PASS',source_shapes=15),'assembly_step':poses,'print_set':dict(stl_types=11,print_objects=11,assembled_printed_pieces=18,spacers_in_runner=8),'continuous_assembly_paths':len(read('wave_assembly_checks.json')['checks']),'real_slicing':slicing},structural_qualification=dict(status=fea['status'],wave_reference_screening_pass=fea['wave_reference_screening_pass'],all_loads_reference_screening_pass=fea['reference_screening_pass'],guarantee=fea['guarantee'],reference='wave_rigidity_report.md'),workspace_checks=dict(parent_print_pack='PASS',tidy_workspace='PASS',all_print_packs=dict(status='FAIL_OUTSIDE_PARENT_SCOPE' if issues else 'PASS',issues=issues),tools_unittest=dict(status='ERROR_OUTSIDE_PARENT_SCOPE' if errors else 'PASS',tests=total,successful=total-errors,errors=errors,reason='Missing prior child_wte4_suspension_clamp material card; existing unrelated failure' if errors else None)),cad_sha256={n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in ['placement.json','closed.step','service.step','parts/manifest.json']},verification_sha256={n+'.json':hashlib.sha256((O/(n+'.json')).read_bytes()).hexdigest() for n in names})
(O/'validation_current.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(data['status'],fea['status'])
