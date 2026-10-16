"""Offline comparison of r1/r2 with identical X1C PETG settings."""
from pathlib import Path
import hashlib,json,subprocess,shutil,zipfile
import trimesh
ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_simple_light_mount'
OUT=ROOT/'print_jobs/child_simple_light_mount'
WORK=OUT/'slice_validation';WORK.mkdir(exist_ok=True)
PRE=ROOT/'print_jobs/child_simple/slice_validation'
CLI=r'C:\Program Files\Bambu Studio\bambu-studio.exe'
for name in ['machine','filament']:
    shutil.copy2(PRE/(name+'.json'),WORK/(name+'.json'))
records={}
for case,support in [('r1_auto','1'),('r2_auto','1'),('r2_no_support','0')]:
    dest=WORK/case;dest.mkdir(exist_ok=True)
    process=json.loads((PRE/'process.json').read_text())
    process.update(print_settings_id='Light mount PETG 0.20 6 walls solid',enable_support=support,brim_width='5')
    (dest/'process.json').write_text(json.dumps(process,indent=2))
    meshes=[]; hashes={}
    for key,x in [('base',92),('cap',174)]:
        src=(PART/'ref/r1' if case.startswith('r1') else PART)/('child_simple_light_mount_'+key+'.stl')
        mesh=trimesh.load(src);assert mesh.is_watertight and len(mesh.split())==1
        hashes[key]=hashlib.sha256(src.read_bytes()).hexdigest()
        mesh.apply_translation([x,128-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
        meshes.append(mesh)
    combined=trimesh.util.concatenate(meshes);combined.export(dest/'placed.stl')
    cmd=[CLI,'--debug','2','--datadir',str(dest/'studio_data'),'--load-settings',str(WORK/'machine.json')+';'+str(dest/'process.json'),'--load-filaments',str(WORK/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf','light_mount.3mf','--outputdir',str(dest),str(dest/'placed.stl')]
    print('Slicing',case,flush=True)
    r=subprocess.run(cmd,capture_output=True,text=True,errors='replace',cwd=dest)
    (dest/'slice.log').write_text(r.stdout+r.stderr,encoding='utf-8')
    result=json.loads((dest/'result.json').read_text())
    assert r.returncode==0 and result['return_code']==0,(case,result)
    plate=result['sliced_plates'][0]
    with zipfile.ZipFile(dest/'light_mount.3mf') as z:
        assert z.testzip() is None
        gc=z.read('Metadata/plate_1.gcode').decode()
    supports=[ln for ln in gc.splitlines() if ln.startswith('; FEATURE:') and 'Support' in ln]
    records[case]={'seconds':plate['total_predication'],'grams':sum(f['total_used_g'] for f in plate['filaments']),'warning':plate.get('warning_message',''),'support_feature_sections':len(supports),'source_sha256':hashes}
    (WORK/'comparison.json').write_text(json.dumps(records,indent=2))
    print(case,records[case],flush=True)
    if case=='r2_no_support':shutil.copy2(dest/'light_mount.3mf',OUT/'child_simple_light_mount_x1c_petg.3mf')
