"""Slice the five changed parts with automatic supports enabled for inspection."""
import sys,json,hashlib,zipfile
import numpy as np
from shapely.geometry import LineString,box
from slice_parent_exterior_qr import main,A
from review_parent_exterior_slices import paths
from prepare_parent_exterior_print_job import saved_mesh
import trimesh

JOB='removable_locators_20261022'
STEMS=['parent_oneplate_frame']+['parent_oneplate_box_locator_'+v for v in ('side_left','side_right','end_fixed','end_push')]

def run():
    sys.argv=[sys.argv[0]]+STEMS
    code=main(JOB,detect_supports=True)
    assert code==0,'Slice failed'
    root=A/'print_jobs'/JOB;checks=[]
    for r in json.loads((root/'validation.json').read_text()):
        stem=r['file'][:-4];folder=root/stem;project=folder/(stem+'.3mf');gcode=folder/'plate_1.gcode'
        actual,settings=saved_mesh(project)
        source=trimesh.load(A/'parts'/r['file'],force='mesh')
        source.apply_translation(actual.bounds[0]-source.bounds[0])
        assert np.max(abs(actual.bounds-source.bounds))<.001 and abs(actual.volume-source.volume)/source.volume<1e-5
        assert actual.is_watertight and len(actual.split())==1
        lines=paths(gcode);xy=np.array([p[:,:2] for z,f,p in lines if f!='Custom'])
        lo=xy.min(axis=(0,1));hi=xy.max(axis=(0,1))
        candidates=xy[(xy.min(axis=1)[:,0]<18.25)&(xy.min(axis=1)[:,1]<28.25)]
        hits=sum(LineString(p).intersects(box(0,0,18.25,28.25)) for p in candidates)
        assert np.all(lo>=.25) and np.all(hi<=255.75) and hits==0
        with zipfile.ZipFile(project) as z:
            assert z.testzip() is None and z.read('Metadata/plate_1.gcode')==gcode.read_bytes()
        c=dict(stem=stem,source_sha256=hashlib.sha256((A/'parts'/r['file']).read_bytes()).hexdigest(),
               three_mf_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),
               actual_support_extrusion_moves=sum(f.startswith('Support') for z,f,p in lines),
               extrusion_bounds_xy_mm=[lo.tolist(),hi.tolist()],exclusion_hits=hits,
               automatic_supports_enabled=settings['enable_support'],source_mesh_matches=True,passed=True)
        assert c['automatic_supports_enabled']=='1'
        checks.append(c)
    out=A/'_work/analysis'/JOB/'slice_checks.json'
    out.write_text(json.dumps(dict(passed=True,parts=checks),indent=2)+'\n',encoding='utf-8')
    print('SAVED PROJECTS / ALL-LAYER BED PATHS PASS',flush=True)

if __name__=='__main__':run()
