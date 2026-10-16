"""Run using FreeCAD Python. Render SCAD independently, compare with STEP, verify both exported poses."""
from parent_access_common import mesh_volume
import FreeCAD as A, Part, Mesh
from pathlib import Path
import json, subprocess, os, runpy, io, contextlib, hashlib, sys
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';P=R/'parts/parent/interior/printed/parent_hand_service'
C=O/'_work/intermediate/scad_check';C.mkdir(parents=True,exist_ok=True)
lid_only='--lid-only' in sys.argv
selected=sys.argv[sys.argv.index('--part')+1] if '--part' in sys.argv else None
assembly_only='--assembly-only' in sys.argv
checks=json.loads((O/'scad_step_checks.json').read_text(encoding='utf-8')) if lid_only or selected or assembly_only else []
files=[]
for it in json.loads((O/'placement.json').read_text(encoding='utf-8'))['items']:
 if '/printed/' not in it['part']:continue
 f=R/it['part']/(it.get('file',Path(it['part']).name)+'.scad')
 skip=json.loads((f.parent/'manufacturing.json').read_text(encoding='utf-8')).get('non_print_files',[])
 if not lid_only and f.exists() and f.stem not in skip and f not in files:files.append(f)
for it in json.loads((O/'print_config.json').read_text(encoding='utf-8')).get('extra_parts',[]):
 f=R/it['part']/(it['file']+'.scad')
 if f not in files and not lid_only:files.append(f)
if selected:files=[f for f in files if f.stem==selected]
if assembly_only:files=[]
for f in sorted(files):
 if f.stem.startswith(('stop_pin','tie_rod','storage_strap','lid_keepout')):continue
 target=C/(f.stem+'.stl')
 result=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(target),str(f)],capture_output=True,text=True,creationflags=0x08000000)
 assert result.returncode==0,(f.name,result.stderr)
 s=Part.read(str(f.with_suffix('.step')));m=Mesh.Mesh(str(target))
 # Generic OCC boxes overestimate trimmed chamfer surfaces; use its precise box.
 exact=s.optimalBoundingBox(False,False)
 delta=max(abs(getattr(exact,k)-getattr(m.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
 vol=abs(s.Volume-mesh_volume(m))/s.Volume
 c=dict(part=f.stem,valid_step=s.isValid(),closed_stl=m.isSolid(),scad_bbox_difference_mm=delta,scad_relative_volume_difference=vol,solid_count=len(s.Solids))
 assert c['valid_step'] and c['closed_stl'] and c['solid_count']==1 and delta<.05 and vol<.02,c
 checks=[old for old in checks if old['part']!=c['part']]+[c];print(f.stem,'PASS',flush=True)
# The reused battery lid is a parameter variant of its original SCAD source.
lp=R/'parts/parent/interior/printed/parent_lipo_retainer';stem='parent_lipo_retainer_lid_narrow';target=C/(stem+'.stl')
if not assembly_only and selected in [None,stem]:
 result=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(target),'-D','part="lid"','-D','west_trim=0.6',str(lp/'parent_lipo_retainer.scad')],capture_output=True,text=True,creationflags=0x08000000)
 assert result.returncode==0,result.stderr
 s=Part.read(str(lp/(stem+'.step')));m=Mesh.Mesh(str(target));b=s.optimalBoundingBox(False,False)
 delta=max(abs(getattr(b,k)-getattr(m.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax']);diff=abs(s.Volume-mesh_volume(m))/s.Volume
 assert s.isValid() and len(s.Solids)==1 and m.isSolid() and delta<.05 and diff<.02
 checks=[c for c in checks if c['part']!=stem]+[dict(part=stem,valid_step=True,closed_stl=True,solid_count=1,scad_bbox_difference_mm=delta,scad_relative_volume_difference=diff,defines={'part':'lid','west_trim':.6})]
 print(stem,'PASS',flush=True)
(O/'scad_step_checks.json').write_text(json.dumps(checks,indent=2))
if lid_only or '--no-assemblies' in sys.argv:sys.exit(0)
poses=[]
for pose,path in [('closed','placement.json'),('service','service_placement.json')]:
 os.environ.update(ASM_JSON=str(O/path),ASM_ROOT=str(R),STEP_IN=str(O/(pose+'.step')))
 log=io.StringIO()
 try:
  with contextlib.redirect_stdout(log):runpy.run_path(str(R/'scad/lib/verify_asm_step.py'),run_name='__main__')
 except SystemExit as e:
  assert e.code in [None,0],(pose,e.code)
 (O/'_work/logs'/(pose+'_verify.log')).write_text(log.getvalue(),encoding='utf-8')
 poses.append(dict(pose=pose,items=len(json.loads((O/path).read_text(encoding='utf-8'))['items']),status='PASS',bbox_tolerance_mm=.5,step_sha256=hashlib.sha256((O/(pose+'.step')).read_bytes()).hexdigest()))
 print(pose,'ASSEMBLY PASS',flush=True)
(O/'assembly_checks.json').write_text(json.dumps(poses,indent=2))
print('PASS independent SCAD/STEP and both assembly poses',flush=True)
