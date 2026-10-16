"""Validate delivered STEP BReps and tessellate them for robust printable meshes."""
import os,json
from pathlib import Path
import Part,MeshPart
folder=Path(os.environ['CAD_FOLDER']);records=[]
for p in folder.glob('*.step'):
 s=Part.Shape();s.read(str(p));s=s.removeSplitter()
 rec={'part':p.stem,'valid':s.isValid(),'solids':len(s.Solids),'volume_mm3':s.Volume}
 if rec['valid'] and rec['solids']==1:
  m=MeshPart.meshFromShape(Shape=s,LinearDeflection=.12,AngularDeflection=.15,Relative=False)
  m.write(str(p.with_name(p.stem+'_print.stl')))
 records.append(rec);print(rec,flush=True)
(folder/'step_validation.json').write_text(json.dumps(records,indent=2))
