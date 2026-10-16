"""One-time recorded revision: move contact to 7.5 mm from the plate seam."""
from pathlib import Path
import json, shutil
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'parts/common/jigs/over_center_latch'
CASE=P/'_work/analysis/dji_groove40N_near_seam_20261010'
def main():
    before=CASE/'before'
    if before.exists(): raise RuntimeError('Revision snapshot already exists')
    for directory in [ROOT/'spec/over_center_latch',P,ROOT/'assemblies/over_center_latch']:
        for f in directory.rglob('*'):
            if not f.is_file() or '_work' in f.relative_to(directory).parts or '__pycache__' in f.parts: continue
            dest=before/f.relative_to(ROOT); dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(f,dest)
    path=P/'parameters.json';v=json.loads(path.read_text(encoding='utf-8'))
    mount_world=v['catch_distance']+v['platform_keeper_x']
    end_world=v['catch_distance']+v['host_moving_tail']
    v['catch_distance']=v['host_seam_x']+7.5-v['toe_face_x']
    v['platform_keeper_x']=mount_world-v['catch_distance']
    v['host_moving_tail']=end_world-v['catch_distance']
    path.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    import dji_geometry as g
    v['preload']=g.calibrate_preload(v)
    print('catch_distance',v['catch_distance'],'dead_angle',g.dead_angle(v),'closed',g.load_at(v,170))
if __name__=='__main__':main()
