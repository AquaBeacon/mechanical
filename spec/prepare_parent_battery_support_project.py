"""Attach the canonical local support blocker, then reslice with Bambu Studio."""
from pathlib import Path
import copy,json,hashlib,shutil,subprocess,uuid,zipfile,sys,xml.etree.ElementTree as E
import trimesh
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
W=O/'_work/analysis/battery_tool_nut_access_20261013/slicing'
if '--battery-side-grooves' in sys.argv:W=O/'_work/analysis/battery_side_grooves_20261013/slicing'
P=R/'parts/parent/interior/printed/parent_hand_service'
src=W/'after/battery_base/battery_base.3mf';dest=W/'blocked';dest.mkdir(exist_ok=True)
with zipfile.ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
if E.fromstring(data['Metadata/model_settings.config']).find("object/part[@subtype='support_blocker']") is not None:
    with zipfile.ZipFile(dest/'unblocked.3mf') as z:data={n:z.read(n) for n in z.namelist()}
core='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';prod='http://schemas.microsoft.com/3dmanufacturing/production/2015/06'
E.register_namespace('',core);E.register_namespace('p',prod)
model=E.fromstring(data['3D/3dmodel.model']);component=model.find('.//{'+core+'}component');assert component is not None
childpath=component.attrib['{'+prod+'}path'].lstrip('/');child=E.fromstring(data[childpath])
base=trimesh.load(P/'battery_base.stl',force='mesh')
settings=E.fromstring(data['Metadata/model_settings.config']);host=settings.find('object')
matrix=host.find("part/metadata[@key='matrix']").attrib['value']
modifiers=[m for m in json.loads((O/'print_config.json').read_text(encoding='utf-8')).get('modifiers',[]) if m['host']=='battery_base']
for index,modifier in enumerate(modifiers,3):
 block=trimesh.load(R/modifier['source'],force='mesh');block.apply_translation(-base.bounds.mean(axis=0))
 obj=E.SubElement(child.find('{'+core+'}resources'),'{'+core+'}object',id=str(index),type='model')
 m=E.SubElement(obj,'{'+core+'}mesh');vertices=E.SubElement(m,'{'+core+'}vertices');faces=E.SubElement(m,'{'+core+'}triangles')
 for v in block.vertices:E.SubElement(vertices,'{'+core+'}vertex',**{k:format(float(a),'.9g') for k,a in zip('xyz',v)})
 for f in block.faces:E.SubElement(faces,'{'+core+'}triangle',**{k:str(int(a)) for k,a in zip(['v1','v2','v3'],f)})
 extra=copy.deepcopy(component);extra.attrib['objectid']=str(index);extra.attrib['{'+prod+'}UUID']=str(uuid.uuid4());model.find('.//{'+core+'}components').append(extra)
 part=E.SubElement(host,'part',id=str(index),subtype='support_blocker',uuid=str(uuid.uuid4()))
 E.SubElement(part,'metadata',key='name',value=Path(modifier['source']).stem);E.SubElement(part,'metadata',key='matrix',value=matrix)
for key,value in [('3D/3dmodel.model',model),(childpath,child),('Metadata/model_settings.config',settings)]:data[key]=E.tostring(value,encoding='utf-8',xml_declaration=True)
inputpath=dest/'battery_base_support_project.3mf'
with zipfile.ZipFile(inputpath,'w',zipfile.ZIP_DEFLATED) as z:
 for n,b in data.items():z.writestr(n,b)
cmd=['C:/Program Files/Bambu Studio/bambu-studio.exe','--debug','2','--datadir',str(dest/'studio_data'),'--load-settings',str(W/'machine.json')+';'+str(W/'process.json'),'--load-filaments',str(W/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf','battery_base.3mf','--outputdir',str(dest),str(inputpath)]
run=subprocess.run(cmd,capture_output=True,text=True,errors='replace',cwd=dest,creationflags=0x08000000)
(dest/'slice.log').write_text(run.stdout+run.stderr,encoding='utf-8');result=json.loads((dest/'result.json').read_text())
assert run.returncode==0 and result['return_code']==0,(run.returncode,result)
output=dest/'battery_base.3mf'
with zipfile.ZipFile(output) as z:
 config=E.fromstring(z.read('Metadata/model_settings.config'));assert len(config.findall("object/part[@subtype='support_blocker']"))==len(modifiers)
 assert len(config.findall("object/part[@subtype='normal_part']"))==1
with zipfile.ZipFile(src) as z:already=E.fromstring(z.read('Metadata/model_settings.config')).find("object/part[@subtype='support_blocker']") is not None
if not already:shutil.copy2(src,dest/'unblocked.3mf')
shutil.copy2(output,src)
records=json.loads((W/'after_slicing.json').read_text());rec=records['battery_base'];rec.update(result=result,local_support_blocker_sha256=hashlib.sha256((P/'battery_lid_nut_support_blocker.stl').read_bytes()).hexdigest(),blocked_project_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),total_filament_g=sum(f['total_used_g'] for f in result['sliced_plates'][0]['filaments']))
rec.pop('feature_extrusion_g',None);rec.pop('support_extrusion_g',None)
(W/'after_slicing.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print('PASS resliced with local support blocker',rec['total_filament_g'],'g')
