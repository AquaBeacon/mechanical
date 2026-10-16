from pathlib import Path
import Part,json
C=Path('C:/Users/ryupc/WorkSpace/Mitou26/AquaBeacon-OSS/mechanical/assemblies/child_petg100_design/cad')
r=[]
for p in C.glob('*.step'):
 s=Part.Shape();s.read(str(p));r.append(dict(part=p.stem,valid=s.isValid(),solids=len(s.Solids),volume_mm3=s.Volume));assert s.isValid() and len(s.Solids)==1
(C/'step_validation.json').write_text(json.dumps(r,indent=2));print(r)
