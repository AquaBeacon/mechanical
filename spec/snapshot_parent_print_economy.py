"""Immutable pre-change CAD and print-pack baseline for print economy revision."""
from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parents[1]
D=R/'assemblies/parent_hand_service/_work/analysis/print_economy_20261009/history'
if (D/'COMPLETE.json').exists():raise SystemExit('Baseline already exists; preserve it.')
D.mkdir(parents=True,exist_ok=True)
paths=['spec/build_parent_gnss.py','spec/parent_switch_tx_body.py','spec/update_parent_gnss_metadata.py','scad/lib/parent_gnss.py','assemblies/parent_hand_service/placement.json','assemblies/parent_hand_service/README.md','assemblies/parent_hand_service/print_config.json','assemblies/parent_hand_service/validation_current.json','assemblies/parent_hand_service/wave_rigidity_report.md']
placement=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
for it in placement['items']:
 if '/printed/' not in it['part']:continue
 folder=R/it['part']; stem=it.get('file',folder.name)
 if stem in json.loads((folder/'manufacturing.json').read_text()).get('non_print_files',[]):continue
 paths += [it['part']+'/'+stem+'.'+e for e in ['step','stl','scad']]
 paths += [it['part']+'/'+e for e in ['README.md','manufacturing.json']]
for p in set(paths):
 src=R/p;out=D/p
 if not src.exists():continue
 out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,out)
shutil.copytree(R/'assemblies/parent_hand_service/parts',D/'print_pack',dirs_exist_ok=True)
(D/'COMPLETE.json').write_text(json.dumps({'copied_existing_paths':sorted(set(paths))}),encoding='utf-8')
print(D)
