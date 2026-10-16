"""Measured CAD volumes and real slicer comparison; no strength verdict here."""
from pathlib import Path
from collections import Counter
import json,sys,hashlib
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';W=O/'_work/analysis/print_economy_20261009'
def cad_totals(root):
 placement=json.loads((root/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
 result={}
 for it in placement['items']:
  if '/printed/' not in it['part']:continue
  stem=it.get('file',Path(it['part']).name);folder=root/it['part']
  if stem in json.loads((folder/'manufacturing.json').read_text()).get('non_print_files',[]):continue
  if stem in result:result[stem]['quantity']+=1;continue
  path=folder/(stem+'.step');s=Part.read(str(path));b=s.optimalBoundingBox(False,False)
  result[stem]=dict(quantity=1,volume_mm3=s.Volume,dense_petg_g=s.Volume*.00127,valid=s.isValid(),solids=len(s.Solids),bbox_mm=[b.XLength,b.YLength,b.ZLength],step_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
 return result
before=cad_totals(W/'history');after=cad_totals(R)
slice_before=json.loads((W/'before_slicing.json').read_text());slice_after=json.loads((W/'after_slicing.json').read_text())
assert set(before)==set(slice_before) and set(after)==set(slice_after)
for stem,row in after.items():
 rec=slice_after[stem];source=R/rec['source']
 assert hashlib.sha256(source.read_bytes()).hexdigest()==rec['source_sha256'],stem+' stale slice'
 assert rec['quantity']==row['quantity'] and rec['exit_code']==0 and row['valid'] and row['solids']==1
def totals(cad,slices):
 return dict(types=len(cad),pieces=sum(v['quantity'] for v in cad.values()),cad_dense_petg_g=sum(v['dense_petg_g']*v['quantity'] for v in cad.values()),sliced_filament_g=sum(v['total_filament_g']*v['quantity'] for v in slices.values()),support_extrusion_g=sum(v['support_extrusion_g']*v['quantity'] for v in slices.values()),prediction_hours=sum(v['prediction_hours']*v['quantity'] for v in slices.values()))
b=totals(before,slice_before);a=totals(after,slice_after)
data=dict(status='PASS_CAD_AND_SLICING',before=b,after=a,cad_before=before,cad_after=after,reduction_percent={k:100*(1-a[k]/b[k]) for k in ['cad_dense_petg_g','sliced_filament_g','support_extrusion_g','prediction_hours']},floor_cad_reduction_percent=100*(1-after['floor_plate']['volume_mm3']/before['floor_plate']['volume_mm3']),slice_conditions='Bambu Studio installed X1C0.4, generic PETG density1.27, textured PEI, 0.20mm,4walls,100%infill,3mmbrim,normal auto supports45deg,both sides0.2mm gap,dont_support_bridges enabled; identical before/after settings',support_measure='Positive moving extrusion in G-code feature labels Support/Support interface/Support transition,1.75mm filament x density1.27; excludes retraction and stationary priming. Slicer total includes brim and priming.',warnings={k:v['warnings'] for k,v in slice_after.items() if v['warnings']},limitations=['Printer and filament-specific bridge/overhang performance needs physical print; successful slicing does not prove printable strength.','Short bridges/local overhangs still use supports; do not disable all supports globally.','New split keys and floor lightening invalidate previous full-part FEA. No mechanical guarantee or manufacturing qualification.'])
(O/'print_economy_checks.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:data[k] for k in ['status','before','after','reduction_percent','floor_cad_reduction_percent','warnings']},ensure_ascii=False,indent=2))
