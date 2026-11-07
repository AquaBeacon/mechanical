"""Bounded build of the canonical frame/spacers, using CadService snapshots."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'assemblies/parent_hand_service/_work/analysis/frame_spacers_20261024'

def main():
    sys.path.insert(0,str(ROOT/'tools/cad_foundation'))
    from service import CadService
    rows=json.loads((ROOT/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))['items']
    deps=['scad/lib/parent_service_retrofit.py','scad/lib/parent_corner_mounts.py','scad/lib/parent_gnss.py','scad/lib/cad_edge_finish.py','scad/lib/parent_case_access.py',
          'assemblies/parent_hand_service/placement.json','assemblies/parent_hand_service/_work/analysis/retrofit_20261024/interfaces.json',
          'parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring.step']
    for row in rows:
        folder=Path(row['part']);deps.append((folder/(row.get('file',folder.name)+'.step')).as_posix())
    WORK.mkdir(parents=True,exist_ok=True)
    result=CadService().build_native('spec/build_parent_frame_spacers.py',parameters={'diagnostic':'--diagnostic' in sys.argv},dependencies=sorted(set(deps)),timeout=240)
    (WORK/'build_run.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
