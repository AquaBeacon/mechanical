"""Reconcile final documentation hashes and validate saved 3MF model positions."""
from pathlib import Path
import hashlib, json, zipfile, re
import xml.etree.ElementTree as ET
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
ASSEMBLY = ROOT / 'assemblies/parent_oneplate'
JOBS = ASSEMBLY / 'print_jobs/repeatable_mount'
WORK = ASSEMBLY / '_work/analysis/repeatable_mount'
NS = {'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02',
      'p':'http://schemas.microsoft.com/3dmanufacturing/production/2015/06'}
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def transform(value):
    numbers = np.array([float(v) for v in value.split()]).reshape(4,3)
    result = np.eye(4)
    result[:3,:3] = numbers[:3,:].T
    result[:3,3] = numbers[3,:]
    return result
def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

manifest = json.loads((JOBS / 'manifest.json').read_text(encoding='utf-8'))
report = json.loads((JOBS / 'slice_report.json').read_text(encoding='utf-8'))
records = []
for plate, sliced in zip(manifest['plates'],report['plates'],strict=True):
    assert plate['plate'] == sliced['plate']
    source = JOBS / plate['stl']
    assert sha(source) == plate['sha256'] == sliced['stl_sha256']
    for part in plate['parts']:
        assert sha(ASSEMBLY / 'parts' / part['file']) == part['source_sha256']
    target = JOBS / sliced['three_mf']
    assert sha(target) == sliced['three_mf_sha256']
    with zipfile.ZipFile(target) as archive:
        model = ET.fromstring(archive.read('3D/3dmodel.model'))
        item = model.find('c:build/c:item',NS)
        component = model.find('c:resources/c:object/c:components/c:component',NS)
        path = component.attrib['{'+NS['p']+'}path'].lstrip('/')
        mesh_xml = ET.fromstring(archive.read(path)).find('c:resources/c:object/c:mesh',NS)
        vertices = [[float(v.attrib[a]) for a in ('x','y','z')] for v in mesh_xml.find('c:vertices',NS)]
        faces = [[int(v.attrib[a]) for a in ('v1','v2','v3')] for v in mesh_xml.find('c:triangles',NS)]
        actual = trimesh.Trimesh(vertices=vertices,faces=faces)
        actual.apply_transform(transform(item.attrib['transform']) @ transform(component.attrib['transform']))
        expected = trimesh.load(source,force='mesh')
        bbox_delta = float(np.max(np.abs(actual.bounds - expected.bounds)))
        volume_error = float(abs(actual.volume - expected.volume)/expected.volume)
        assert actual.is_volume and len(actual.split(only_watertight=False)) == plate['part_count']
        assert bbox_delta < .001 and volume_error < .00001
        assert actual.bounds[0,0] >= 0 and actual.bounds[0,1] >= 28
        assert np.all(actual.bounds[1,:] <= [256,256,256])
        records.append(dict(plate=plate['plate'],part_count=plate['part_count'],
                            saved_3mf_bbox_mm=actual.bounds.tolist(),bbox_delta_mm=bbox_delta,
                            relative_volume_error=volume_error,passed=True))
        images = ASSEMBLY / '_work/images'
        images.mkdir(parents=True,exist_ok=True)
        (images / f"repeatable_plate_{plate['plate']}.png").write_bytes(archive.read('Metadata/plate_1.png'))
manifest['placement_sha256'] = sha(ASSEMBLY / 'placement.json')
manifest['source_manifest_sha256'] = sha(ASSEMBLY / 'parts/manifest.json')
write(JOBS / 'manifest.json',manifest)
report['source_manifest_sha256'] = sha(JOBS / 'manifest.json')
write(JOBS / 'slice_report.json',report)
write(WORK / 'print_job_checks.json',dict(passed=True,plates=records,
    note='Saved model geometry and position match sliced source STLs. Source/3MF hashes verified.'))
logs = ASSEMBLY / '_work/logs'
assembly_log = (logs / 'repeatable_assembly_step_verification.log').read_text(encoding='utf-8-sig',errors='replace')
assert '[verify-asm] 89 item(s), 0 NG' in assembly_log
geometry = json.loads((WORK / 'geometry_checks.json').read_text(encoding='utf-8'))
steps = json.loads((WORK / 'step_checks.json').read_text(encoding='utf-8'))
assert geometry['passed'] and steps['passed']
tests = (logs / 'repeatable_tools_tests.log').read_text(encoding='utf-8-sig',errors='replace')
assert 'Ran 19 tests' in tests and 'FAILED (errors=1)' in tests
global_check = (logs / 'repeatable_print_set_check.log').read_text(encoding='utf-8-sig',errors='replace')
write(WORK / 'verification_summary.json',dict(
    design_status='prototype; real-fit and repeated-attachment trials required',
    geometry_checks='PASS',step_dimensions_and_volumes='PASS',
    assembly_step_placement=dict(items=89,failures=0),print_jobs='PASS',
    target_print_bundle='PASS',workspace_tidy='PASS',
    tools_tests=dict(total=19,passed=18,errors=1,
        error='Existing test refers to missing child_wte4_suspension_clamp/spec/bambu_petg_basic_material.json'),
    global_print_set_failures=[line for line in global_check.splitlines() if line.startswith('FAIL ')],
    evidence=dict(geometry='geometry_checks.json',step='step_checks.json',saved_3mf='print_job_checks.json',
        assembly_log='../../logs/repeatable_assembly_step_verification.log',
        tools_log='../../logs/repeatable_tools_tests.log',global_print_set_log='../../logs/repeatable_print_set_check.log'),
    hashes=dict(placement=sha(ASSEMBLY/'placement.json'),parts_manifest=sha(ASSEMBLY/'parts/manifest.json'),
                job_manifest=sha(JOBS/'manifest.json'),slice_report=sha(JOBS/'slice_report.json'))))
print(json.dumps(dict(passed=True,plates=len(records),parts=sum(r['part_count'] for r in records)),indent=2))
