"""Re-render immutable parent stock and front clamp into isolated candidates."""
from pathlib import Path
import sys, subprocess, time, json, hashlib, os
import trimesh, numpy as np
from scipy.spatial import cKDTree
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools'))
from prepare_child_horizontal_plate_frame import verify_printed_render
osc=r'C:\Program Files\OpenSCAD\openscad.exe'
out=root/'assemblies/parent_exterior/_work/analysis/camera_rotary_20261029/immutable_regression'
out.mkdir(parents=True,exist_ok=True)
parts=root/'parts/parent/exterior/printed'
jobs=[]
for name in ['parent_oneplate_frame','parent_oneplate_bar','parent_oneplate_stand']:
 d=parts/name;jobs.append((d/(name+'.scad'),d/(name+'.stl'),None))
d=parts/'parent_oneplate_box_locator'
for variant in ['pressure_pad','side_left','side_right','end_fixed','end_push']:
 jobs.append((d/'parent_oneplate_box_locator.scad',d/('parent_oneplate_box_locator_'+variant+'.stl'),variant))
d=root/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
jobs.append((d/'camera_front_clamp.scad',d/'camera_front_clamp.stl',None))
def raw_equivalence(original,candidate):
 a=trimesh.load(original,force='mesh');b=trimesh.load(candidate,force='mesh')
 error=max(float(cKDTree(x.vertices).query(y.vertices)[0].max()) for x,y in [(a,b),(b,a)])
 report=dict(original=original.relative_to(root).as_posix(),candidate=candidate.relative_to(root).as_posix(),
  method='raw render; bidirectional vertices, bounding box, volume, Euler and watertightness',
  bidirectional_vertex_error_mm=error,bounds_error_mm=float(np.abs(a.bounds-b.bounds).max()),
  volume_error_mm3=abs(float(a.volume-b.volume)),original_watertight=bool(a.is_volume),candidate_watertight=bool(b.is_volume),original_euler=int(a.euler_number),candidate_euler=int(b.euler_number),original_components=len(a.split()),candidate_components=len(b.split()),
  original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),candidate_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest())
 if error>1e-4 or report['bounds_error_mm']>1e-4 or report['volume_error_mm3']>.1 or not a.is_volume or not b.is_volume or b.euler_number!=a.euler_number or len(a.split())!=1 or len(b.split())!=1:
  raise RuntimeError('Raw render requires cleanup or differs: '+json.dumps(report))
 os.utime(original,None)
 candidate.with_suffix('.equivalence.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 return report
results=[]
for src,original,variant in jobs:
 candidate=out/(original.stem+'.stl')
 args=[osc,'-o',str(candidate)]
 if variant: args+=['-D','part="'+variant+'"']
 args.append(str(src))
 if original.stem=='parent_oneplate_frame' and candidate.exists():
  report=raw_equivalence(original,candidate)
  results.append(report);print('passed',original.stem,'error',report['bidirectional_vertex_error_mm'],flush=True);continue
 p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 print('task-owned OpenSCAD pid',p.pid,'start',time.strftime('%Y-%m-%d %H:%M:%S'),'part',original.stem,flush=True)
 try: log,_=p.communicate(timeout=360)
 except subprocess.TimeoutExpired:
  p.kill(); log,_=p.communicate(); raise RuntimeError('timeout '+original.stem)
 (out/(original.stem+'.log')).write_text(log,encoding='utf-8')
 if p.returncode or 'ERROR' in log or 'WARNING' in log: raise RuntimeError('OpenSCAD failed '+original.stem+': '+log)
 try:
  report=raw_equivalence(original,candidate)
 except RuntimeError:
  report=verify_printed_render(original,candidate)
 results.append(report)
 print('passed',original.stem,'error',report['bidirectional_vertex_error_mm'],flush=True)
(out/'report.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
