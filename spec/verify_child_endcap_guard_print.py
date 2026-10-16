"""Verify rendered mesh and print geometry; --slice checks the complete STL offline."""
import argparse
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_endcap_guard'
ASM = ROOT/'assemblies/child_endcap_guard'
LOG = PART/'_work/logs'
WORK = ASM/'_work/analysis/printability_slice'
parser = argparse.ArgumentParser()
parser.add_argument('--slice', action='store_true')
args = parser.parse_args()
report = {'scope': 'upper main cage, local Z>12 mm, radius<73 mm; provisional hinge excluded from area comparison'}
for stem in ('child_endcap_guard_integrated', 'child_endcap_guard_hinge_reference'):
    output = PART/'_work/intermediate'/(stem+'_openscad_check.stl')
    r = subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe', '-o', str(output),
                        str(PART/(stem+'.scad'))], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    m = trimesh.load(output, force='mesh')
    native = trimesh.load(PART/(stem+'.stl'), force='mesh')
    delta = abs(m.volume-native.volume)/native.volume
    bounds_delta = float(abs(m.bounds-native.bounds).max())
    assert m.is_watertight and m.is_winding_consistent and len(m.split()) == 1
    assert delta < 1e-5 and bounds_delta < .001  # ASCII STL coordinate rounding
    report[stem] = {'watertight': True, 'components': 1, 'volume_mm3': float(native.volume),
                    'roundtrip_volume_difference_fraction': float(delta),
                    'roundtrip_bounds_difference_mm': bounds_delta}
areas = {}
for label, source in (
    ('baseline', PART/'_work/analysis/printability_baseline/child_endcap_guard_integrated.stl'),
    ('current', PART/'child_endcap_guard_integrated.stl')):
    m = trimesh.load(source, force='mesh')
    c = m.triangles_center
    scope = (c[:,2] > 12) & (np.linalg.norm(c[:,:2],axis=1) < 73)
    areas[label] = float(m.area_faces[scope & (m.face_normals[:,2] < -.75)].sum())
report['steep_downward_upper_cage_area_mm2'] = areas
report['area_reduction_fraction'] = 1-areas['current']/areas['baseline']
assert areas['current'] < areas['baseline']*.1
report['limitation'] = 'Area is a geometric proxy, not support volume or a guarantee of support-free printing.'
LOG.mkdir(exist_ok=True)
(LOG/'printability_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS: closed meshes and reduced steep underside area:', areas, flush=True)
if args.slice:
    WORK.mkdir(parents=True,exist_ok=True)
    presets = ROOT/'print_jobs/child_simple/slice_validation'
    for name in ('machine','filament'):
        shutil.copy2(presets/(name+'.json'),WORK/(name+'.json'))
    settings = json.loads((presets/'process.json').read_text(encoding='utf-8'))
    settings.update(enable_support='1',support_type='normal(auto)',brim_width='5',
                    wall_loops='6',top_shell_layers='6',bottom_shell_layers='6',
                    sparse_infill_density='40%',layer_height='0.2')
    (WORK/'process.json').write_text(json.dumps(settings,indent=2),encoding='utf-8')
    source = ASM/'parts/child_endcap_guard_integrated.stl'
    mesh = trimesh.load(source,force='mesh')
    assert mesh.is_watertight and max(mesh.extents)<250
    mesh.apply_translation([128-mesh.bounds[:,0].mean(),128-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
    placed = WORK/'placed.stl'
    mesh.export(placed)
    cmd = [r'C:\Program Files\Bambu Studio\bambu-studio.exe','--debug','2',
           '--datadir',str(WORK/'studio_data'),'--load-settings',
           str(WORK/'machine.json')+';'+str(WORK/'process.json'),'--load-filaments',
           str(WORK/'filament.json'),'--arrange','0','--orient','0','--slice','0',
           '--export-3mf','slice_check.3mf','--outputdir',str(WORK),str(placed)]
    r = subprocess.run(cmd,capture_output=True,text=True,errors='replace',cwd=WORK,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    (WORK/'slice.log').write_text(r.stdout+r.stderr,encoding='utf-8')
    result = json.loads((WORK/'result.json').read_text(encoding='utf-8'))
    assert r.returncode==0 and result['return_code']==0, result
    with zipfile.ZipFile(WORK/'slice_check.3mf') as archive:
        assert archive.testzip() is None
        gcode = archive.read('Metadata/plate_1.gcode').decode()
        assert '; FEATURE:' in gcode
    report['slice'] = {'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                       'plate':result['sliced_plates'][0],
                       'analysis_only':True,
                       'note':'Offline complete STL with auto support; includes support below provisional hinge and main foot.'}
    (LOG/'printability_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PASS: full STL slices with PETG/0.20/6 walls and auto support.',flush=True)
