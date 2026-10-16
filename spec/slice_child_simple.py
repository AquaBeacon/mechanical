"""Offline X1C/PETG slicing of r2. Exports one Bambu Studio 3MF per part.

Reads installed system presets, uses a task-local data directory, and never
connects to a printer. Preserve the documented orientation and hash each source.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import shutil
import zipfile
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'print_jobs/child_simple'
WORK=OUT/'slice_validation'
WORK.mkdir(exist_ok=True)
PROFILES=Path(r'C:\Program Files\Bambu Studio\resources\profiles\BBL')
CLI=Path(r'C:\Program Files\Bambu Studio\bambu-studio.exe')
index={p.stem:p for p in PROFILES.rglob('*.json')}

def resolve(name):
    data=json.loads(index[name].read_text(encoding='utf-8'))
    result={}
    if data.get('inherits'): result.update(resolve(data['inherits']))
    for inc in data.get('include',[]): result.update(resolve(inc))
    result.update(data)
    for key in ['inherits','include']: result.pop(key,None)
    return result

machine=resolve('Bambu Lab X1 Carbon 0.4 nozzle')
process=resolve('0.20mm Standard @BBL X1C')
filament=resolve('Generic PETG')
machine['curr_bed_type']='Textured PEI Plate'
process.update(print_settings_id='Child simple r2 PETG 0.20 wall6 solid support',wall_loops='6',top_shell_layers='6',bottom_shell_layers='6',sparse_infill_density='100%',sparse_infill_pattern='zig-zag',brim_type='outer_only',brim_width='3',enable_support='1',support_type='normal(auto)',support_on_build_plate_only='0',support_threshold_angle='45',support_top_z_distance='0.2',support_bottom_z_distance='0.2',support_object_xy_distance='0.35',support_interface_top_layers='2',support_interface_bottom_layers='2',enable_prime_tower='0',skirt_loops='0')
for label,data in [('machine',machine),('process',process),('filament',filament)]:
    (WORK/(label+'.json')).write_text(json.dumps(data,indent=2),encoding='utf-8')

records={}
report=WORK/'results.json'
if report.exists(): records=json.loads(report.read_text())
names=sys.argv[1:] or ['front','rear','guard']
for suffix in names:
    name='child_simple_'+suffix
    source=OUT/(name+'_print.stl')
    dest=WORK/suffix
    dest.mkdir(exist_ok=True)
    mesh=trimesh.load(source,force='mesh')
    assert mesh.is_watertight and len(mesh.split())==1
    mesh.apply_translation([136-mesh.bounds[:,0].mean(),128-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
    # Nominal XY bounds + brim avoid the X1C front-left exclusion and bed edge.
    assert mesh.bounds[0,0]-3>18 and mesh.bounds[1,0]+3<253
    assert mesh.bounds[0,1]-3>3 and mesh.bounds[1,1]+3<253
    staged=dest/'placed.stl'
    mesh.export(staged)
    project=OUT/(name+'_x1c_petg.3mf')
    cmd=[str(CLI),'--debug','2','--datadir',str(dest/'studio_data'),'--load-settings',str(WORK/'machine.json')+';'+str(WORK/'process.json'),'--load-filaments',str(WORK/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf',project.name,'--outputdir',str(dest),str(staged)]
    print('Slicing',suffix,flush=True)
    r=subprocess.run(cmd,capture_output=True,text=True,errors='replace',cwd=str(dest))
    (dest/'slice.log').write_text(r.stdout+r.stderr,encoding='utf-8')
    result=json.loads((dest/'result.json').read_text(encoding='utf-8')) if (dest/'result.json').exists() else {}
    record=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),placed_bounds_mm=mesh.bounds.tolist(),returncode=r.returncode,result=result,project=str(project.relative_to(ROOT)))
    records[suffix]=record
    report.write_text(json.dumps(records,indent=2),encoding='utf-8')
    if r.returncode!=0 or result.get('return_code')!=0:
        print((r.stdout+r.stderr)[-4000:],flush=True)
        raise RuntimeError(f'Slice failed: {suffix}: {result}')
    shutil.copy2(dest/project.name,project)
    with zipfile.ZipFile(project) as z:
        assert 'Metadata/slice_info.config' in z.namelist()
        assert any(n.startswith('Metadata/plate_') and n.endswith('.gcode') for n in z.namelist())
        assert z.testzip() is None
    plate=result['sliced_plates'][0]
    print(suffix,'PASS',round(sum(f['total_used_g'] for f in plate['filaments']),1),'g',round(plate['total_predication']/3600,2),'h',plate.get('warning_message',''),flush=True)
