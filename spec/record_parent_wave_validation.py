"""Record completed geometry/pack checks separately from structural qualification."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
read=lambda name:json.loads((O/name).read_text(encoding='utf-8'))
names=['switch_tx_access_checks','battery_sd_access_checks','gnss_access_checks','magnetometer_access_checks','mount_axis_checks','wave_retention_checks','wave_assembly_checks','wave_analysis_geometry_checks']
checks={n:read(n+'.json')['status'] for n in names};assert all(v=='PASS' for v in checks.values()),checks
economy=read('print_economy_checks.json');assert economy['status']=='PASS_CAD_AND_SLICING'
types=economy['after']['types'];pieces=economy['after']['pieces']
scad=read('scad_step_checks.json');assert len(scad)==types and all(q['valid_step'] and q['closed_stl'] and q['solid_count']==1 for q in scad)
poses=read('assembly_checks.json');assert [(q['pose'],q['items'],q['status']) for q in poses]==[('closed',len(read('placement.json')['items']),'PASS'),('service',len(read('service_placement.json')['items']),'PASS')]
pack=(O/'_work/logs/print_economy_pack_check.log').read_text(encoding='utf-8-sig');assert 'PASS parent_hand_service' in pack and 'FAIL' not in pack
global_log=(O/'_work/logs/print_economy_workspace_pack_check.log').read_text(encoding='utf-8-sig')
issues=[q for q in global_log.splitlines() if q.startswith('FAIL')];assert not any('parent_hand_service' in q for q in issues),issues
tidy=(O/'_work/logs/print_economy_tidy.log').read_text(encoding='utf-8-sig');assert tidy.startswith('PASS')
fea=read('wave_rigidity_acceptance.json');assert fea['manufacturing_release'] is False
assert fea['reference_screening_pass'] is True
data=dict(status='PASS_PARENT_GEOMETRY_AND_PACK_CHECKS',manufacturing_release=False,date='2026-10-09',
 checks={**checks,'independent_scad_step':dict(status='PASS',parts=types),'assembly_step':poses,'remeshed_print_sources':dict(status='PASS',parts=len(read('remesh_checks.json'))),'assembly_path_count':len(read('wave_assembly_checks.json')['checks']),'real_slicing':dict(status='PASS',warnings=economy['warnings'],before=economy['before'],after=economy['after'],reductions=economy['reduction_percent'])},
 structural_qualification=dict(status=fea['status'],guarantee=fea['guarantee'],reference='wave_rigidity_report.md',physical_wave_tests='Not performed; blank record retained'),
 workspace_checks=dict(parent_print_pack=f'PASS, {types} STL types / {pieces} pieces',tidy_workspace='PASS',all_print_packs=dict(status='FAIL_OUTSIDE_PARENT_SCOPE' if issues else 'PASS',issues=issues),tools_unittest=dict(status='ERROR_OUTSIDE_PARENT_SCOPE',tests=16,successful=15,errors=1,reason='test_clamp_bambu_material references absent child_wte4_suspension_clamp/spec/bambu_petg_basic_material.json')),
 cad_sha256={n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in ['placement.json','closed.step','service.step','parts/manifest.json']},
 verification_sha256={n+'.json':hashlib.sha256((O/(n+'.json')).read_bytes()).hexdigest() for n in names})
(O/'validation_current.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(data['status'],data['structural_qualification']['status'])
