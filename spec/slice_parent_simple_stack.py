"""Offline, identical-profile before/after support and filament comparison.

No printer connection. Source CAD stays canonical; placed meshes/logs live in
the assembly analysis folder. Actual sliced projects are staged there first.
"""
from pathlib import Path
from collections import Counter,defaultdict
import json,subprocess,hashlib,zipfile,re,math,sys
import trimesh
R=Path(__file__).resolve().parents[1]
O=R/'assemblies/parent_hand_service';W=O/'_work/analysis/simple_stack_20261010'
if '--battery-box' in sys.argv:
 sys.argv.remove('--battery-box');W=O/'_work/analysis/battery_box_20261011/slicing'
if '--case-correction' in sys.argv:
 sys.argv.remove('--case-correction');W=O/'_work/analysis/case_cad_correction_20261010/slicing'
if '--corner-mounts' in sys.argv:
 sys.argv.remove('--corner-mounts');W=O/'_work/analysis/corner_mounts_20261011/slicing'
if '--fixed-plates' in sys.argv:
 sys.argv.remove('--fixed-plates');W=O/'_work/analysis/fixed_plates_20261011/slicing'
if '--case-screw-access' in sys.argv:
 sys.argv.remove('--case-screw-access');W=O/'_work/analysis/case_screw_access_20261012/slicing'
if '--battery-slide-lid' in sys.argv:
 sys.argv.remove('--battery-slide-lid');W=O/'_work/analysis/battery_slide_lid_20261012/slicing'
if '--sensor-mounts' in sys.argv:
 sys.argv.remove('--sensor-mounts');W=O/'_work/analysis/sensor_mounts_20261011/slicing'
if '--battery-child-reference' in sys.argv:
 sys.argv.remove('--battery-child-reference');W=O/'_work/analysis/battery_child_reference_20261012/slicing'
if '--battery-tool-nut' in sys.argv:
 sys.argv.remove('--battery-tool-nut');W=O/'_work/analysis/battery_tool_nut_access_20261013/slicing'
if '--battery-side-grooves' in sys.argv:
 sys.argv.remove('--battery-side-grooves');W=O/'_work/analysis/battery_side_grooves_20261013/slicing'
PROFILES=Path('C:/Program Files/Bambu Studio/resources/profiles/BBL')
index={p.stem:p for p in PROFILES.rglob('*.json')}
def resolve(name):
 d=json.loads(index[name].read_text(encoding='utf-8'));a={}
 if d.get('inherits'):a.update(resolve(d['inherits']))
 for name in d.get('include',[]):a.update(resolve(name))
 a.update(d)
 for key in ['inherits','include']:a.pop(key,None)
 return a
machine=resolve('Bambu Lab X1 Carbon 0.4 nozzle');machine['curr_bed_type']='Textured PEI Plate'
process=resolve('0.20mm Standard @BBL X1C')
process.update(print_settings_id='Parent print economy PETG wall4 solid auto support',wall_loops='4',top_shell_layers='5',bottom_shell_layers='5',sparse_infill_density='100%',sparse_infill_pattern='zig-zag',brim_type='outer_only',brim_width='3',enable_support='1',support_type='normal(auto)',support_on_build_plate_only='0',support_threshold_angle='45',support_top_z_distance='0.2',support_bottom_z_distance='0.2',support_object_xy_distance='0.35',support_interface_top_layers='2',support_interface_bottom_layers='2',enable_prime_tower='0',skirt_loops='0',dont_support_bridges='1')
filament=resolve('Generic PETG');filament['filament_density']=['1.27']
W.mkdir(parents=True,exist_ok=True)
for name,data in [('machine',machine),('process',process),('filament',filament)]:
 (W/(name+'.json')).write_text(json.dumps(data,indent=2),encoding='utf-8')
revision=sys.argv[1];assert revision in ['before','after']
base=W/'history' if revision=='before' else R
placement=json.loads((base/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
counts=Counter();items={}
for it in placement['items']:
 if '/printed/' not in it['part'] or it.get('print') is False:continue
 folder=base/it['part'];stem=it.get('file',folder.name)
 if stem in json.loads((folder/'manufacturing.json').read_text()).get('non_print_files',[]):continue
 counts[stem]+=1;items[stem]=it
for it in json.loads((O/'print_config.json').read_text(encoding='utf-8')).get('extra_parts',[]):
 counts[it['file']]+=it['quantity'];items[it['file']]=it
results_path=W/(revision+'_slicing.json')
results=json.loads(results_path.read_text()) if results_path.exists() else {}
def extrusion_stats(gcode):
 # Count positive extrusion only on actual movement; retraction/prime excluded.
 relative=False;eold=0;feature='Unknown';lengths=defaultdict(float)
 for line in gcode.splitlines():
  if line.startswith('; FEATURE: '):feature=line[11:].strip()
  if line.startswith(';TYPE:'):feature=line[6:].strip()
  if line.startswith('M83'):relative=True
  if line.startswith('M82'):relative=False
  if line.startswith('G92 '):
   m=re.search(r'\bE(-?[\d.]+)',line)
   if m:eold=float(m[1])
  if not line.startswith(('G0 ','G1 ','G2 ','G3 ')):continue
  m=re.search(r'\bE(-?[\d.]+)',line)
  if not m:continue
  e=float(m[1]);delta=e if relative else e-eold;eold=e
  if delta>0 and re.search(r'\b[XYIJ][-\d.]',line):lengths[feature]+=delta
 return {k:v*math.pi*(1.75/2)**2*.001*1.27 for k,v in lengths.items()}
for stem in sys.argv[2:] or sorted(items):
 it=items[stem];src=base/it['part']/(stem+'.stl');sha=hashlib.sha256(src.read_bytes()).hexdigest()
 orientation=json.loads((base/it['part']/'manufacturing.json').read_text()).get('print_rotations_deg',{}).get(stem,[0,0,0])
 dest=W/revision/stem;dest.mkdir(parents=True,exist_ok=True)
 mesh=trimesh.load(src,force='mesh');assert mesh.is_watertight
 # Same axis order as assembly_parts.py: X, Y, Z around source origin.
 for axis,angle in zip([[1,0,0],[0,1,0],[0,0,1]],orientation):
  mesh.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),axis))
 mesh.apply_translation([128-mesh.bounds[:,0].mean(),128-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
 assert mesh.bounds[0,:2].min()-3>=3 and mesh.bounds[1,:2].max()+3<=253,(stem,mesh.bounds)
 staged=dest/'placed.stl';mesh.export(staged)
 project=stem+'.3mf'
 cmd=['C:/Program Files/Bambu Studio/bambu-studio.exe','--debug','2','--datadir',str(dest/'studio_data'),'--load-settings',str(W/'machine.json')+';'+str(W/'process.json'),'--load-filaments',str(W/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf',project,'--outputdir',str(dest),str(staged)]
 print('Slice',revision,stem,flush=True)
 run=subprocess.run(cmd,capture_output=True,text=True,errors='replace',cwd=dest,creationflags=0x08000000)
 (dest/'slice.log').write_text(run.stdout+run.stderr,encoding='utf-8')
 data=json.loads((dest/'result.json').read_text()) if (dest/'result.json').exists() else {}
 rec=dict(quantity=counts[stem],source=it['part']+'/'+stem+'.stl',source_sha256=sha,orientation_deg=orientation,exit_code=run.returncode,result=data)
 if run.returncode==0 and data.get('return_code')==0:
  with zipfile.ZipFile(dest/project) as z:
   gcode=z.read(next(n for n in z.namelist() if n.startswith('Metadata/plate_') and n.endswith('.gcode'))).decode('utf-8')
   rec['feature_extrusion_g']=extrusion_stats(gcode)
  plate=data['sliced_plates'][0]
  rec.update(total_filament_g=sum(f['total_used_g'] for f in plate['filaments']),support_extrusion_g=sum(v for k,v in rec['feature_extrusion_g'].items() if k.lower().startswith('support')),prediction_hours=plate['total_predication']/3600,warnings=plate.get('warning_message',''))
 results[stem]=rec;results_path.write_text(json.dumps(results,indent=2),encoding='utf-8')
 assert run.returncode==0 and data.get('return_code')==0,(stem,data,(run.stdout+run.stderr)[-1800:])
 print(stem,round(rec['total_filament_g'],2),'g; support',round(rec['support_extrusion_g'],2),'g;',rec['warnings'],flush=True)
