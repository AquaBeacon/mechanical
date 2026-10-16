from pathlib import Path
import json,zipfile,hashlib
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service'
assert json.loads((O/'verification.json').read_text(encoding='utf-8'))['status']=='PASS'
assert json.loads((O/'verification.json').read_text(encoding='utf-8'))['lid_closure']['minimum_clearance_mm']>=3
assert all(x['status']=='PASS' and hashlib.sha256((O/(x['pose']+'.step')).read_bytes()).hexdigest()==x['step_sha256'] for x in json.loads((O/'assembly_checks.json').read_text()))
tool=json.loads((O/'service_tool_access.json').read_text())
assert tool['status']=='PASS' and tool['service_step_sha256']==hashlib.sha256((O/'service.step').read_bytes()).hexdigest()
assert len(json.loads((O/'scad_step_checks.json').read_text()))==12
files=set(f for f in O.iterdir() if f.suffix in ['.step','.png','.json','.md','.scad','.log','.csv'])
files.update(f for f in (O/'rigidity').rglob('*') if f.is_file() and f.suffix in ['.json','.log','.step','.stl','.py'])
data=json.loads((O/'service_placement.json').read_text(encoding='utf-8'))
for item in data['items']:
 folder=R/item['part'];stem=item.get('file',folder.name)
 for suffix in ['.step','.stl','.scad','.md','.json']:
  f=folder/(stem+suffix)
  if f.exists():files.add(f)
files.update((R/'parts/parent/interior/printed/parent_hand_service').glob('*.*'))
files.update((R/'parts/parent/interior/printed/parent_hand_service/ref').glob('*.html'))
ref=R/'parts/parent/interior/cots/spresense_logger/ref'
files.update(f for f in ref.iterdir() if f.suffix in ['.stp','.html'])
files.update((R/'parts/parent/interior/cots/spresense_service_stack').glob('*.json'))
files.add(R/'parts/parent/interior/printed/parent_lipo_retainer/dimensions.json')
files.add(R/'assemblies/parent_service_review/placement.json')
files.add(R/'parts/parent/exterior/cots/bcas212310g/ref/BCAS212310G.dxf')
for name in ['build_parent_hand_service.py','verify_parent_hand_service.py','preview_parent_hand_service.py','package_parent_hand_service.py','check_parent_rigidity.py','render_parent_hand_service.py','prepare_parent_rigidity_study.py','prepare_parent_revised_study.py','run_parent_rigidity.py','run_ccx_delaunay.py','run_ccx_native_step.py','parent_rigidity_acceptance.py','collect_parent_rigidity_evidence.py','verify_parent_service_tools.py']:files.add(R/'spec'/name)
for name in ['verify_asm_step.py','asm_gen.py']:files.add(R/'scad/lib'/name)
# Include authoritative PCB input for rebuilding support-hole coordinates after extraction.
pcb=[]
for name in ['PARENT_MAIN','PARENT_PWR','TX_improved']:pcb.append(R.parent/'hardware/pcb'/name/(name+'.kicad_pcb'))
with zipfile.ZipFile(O/'parent_hand_service.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(files):
  if f.is_file():z.write(f,'mechanical/'+f.relative_to(R).as_posix())
 for f in pcb:z.write(f,f.relative_to(R.parent).as_posix())
print('PACKAGED',len(files),'files',round((O/'parent_hand_service.zip').stat().st_size/1e6,1),'MB')
