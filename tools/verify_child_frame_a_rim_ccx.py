"""Try native independent CCX on geometry-checked coplanar STEP input."""
from pathlib import Path
import json,subprocess,sys,psutil
from compact_coplanar_mesh import compact

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'


def main():
    source=PART/'child_exterior_structural_frame_full.stl'
    target=CASE/'ccx_input.stl'
    compact(source,target,CASE/'ccx_input_geometry.json')
    cmd=[sys.executable,str(ROOT/'tools/clamp_bambu_material.py'),'ccx',str(target),
         '--study',str(CASE/'study_final.json'),'--out',str(CASE/'ccx'),
         '--mesh-mm','4','--converge','--map','volume']
    with (CASE/'ccx.log').open('w') as log:
        child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
        try:
            code=child.wait(timeout=600);status=dict(status='finished',exit_code=code)
        except subprocess.TimeoutExpired:
            for p in reversed(psutil.Process(child.pid).children(recursive=True)):
                try:p.kill()
                except psutil.NoSuchProcess:pass
            child.kill();child.wait();status=dict(status='timeout',seconds=600)
    (CASE/'ccx_status.json').write_text(json.dumps(status,indent=2)+'\n')
    print(status)


if __name__=='__main__':main()
