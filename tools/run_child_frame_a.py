"""Logged native topology pipeline for frame A; no solver implementation.

Queues behind the running clamp GPU job. Does not modify the clamp's files.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import psutil

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
CLI=[sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py')]
STUDY=CASE/'study_frame_a.json'
OSC=r'C:\Program Files\OpenSCAD\openscad.com'
FC=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def run(stage,cmd,allowed=(0,),env=None,timeout=None):
    save(CASE/'pipeline_status.json',dict(stage=stage,status='running',started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())))
    print('START',stage,flush=True)
    with (CASE/(stage+'.log')).open('w',encoding='utf-8') as stream:
        try:
            result=subprocess.Popen(cmd,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,env=env)
            code=result.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            # Stop only this owned stage and its descendants, including Gmsh.
            children=psutil.Process(result.pid).children(recursive=True)
            for child in reversed(children):
                try: child.kill()
                except psutil.NoSuchProcess: pass
            result.kill(); result.wait()
            save(CASE/(stage+'_status.json'),dict(status='timeout',seconds=timeout))
            raise
    save(CASE/(stage+'_status.json'),dict(status='finished',exit_code=code))
    print('END',stage,code,flush=True)
    if code not in allowed: raise RuntimeError(f'{stage} exited {code}; read its log')
    return code

def wait_gpu():
    start=time.monotonic()
    while True:
        busy=[]
        for p in psutil.process_iter(['cmdline']):
            cmd=p.info['cmdline'] or []
            if p.pid!=os.getpid() and any(a.endswith('clamp_bambu_material.py') for a in cmd) and any(a in ('opt','extract','fea') for a in cmd):
                busy.append(p.pid)
        if not busy: return
        save(CASE/'pipeline_status.json',dict(stage='waiting_for_existing_gpu_analysis',status='waiting',other_pids=busy))
        if time.monotonic()-start>7200: raise RuntimeError('Existing GPU analysis still running after two hours')
        time.sleep(10)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--reuse-opt',action='store_true'); ap.add_argument('--reuse-extract',action='store_true'); ap.add_argument('--reuse-render',action='store_true'); args=ap.parse_args()
    os.environ['PYTHONIOENCODING']='utf-8'; os.environ['OMP_NUM_THREADS']='4'
    inputs=read(CASE/'input_identity.json'); source=PART/'child_exterior_structural_frame.scad'
    assert digest(source)==inputs['source'],'Frame CAD changed after preparation'
    if not args.reuse_opt:
        wait_gpu()
        run('opt',CLI+['opt',str(STUDY),'--out',str(CASE/'opt'),'--voxel','3','--iters','50'],allowed=(0,1))
    opt=read(CASE/'opt/study_frame_a.json')
    save(CASE/'optimisation_verdict.json',dict(pass_check=opt.get('pass'),termination_reason=opt.get('termination_reason'),checks=opt.get('checks')))
    if not args.reuse_extract:
        run('extract',CLI+['extract',str(CASE/'opt'),'--study',str(STUDY),'--out',str(CASE/'extract'),'--levels','0.4,0.5,0.6'],allowed=(0,1))
    ext=read(CASE/'extract/study_frame_a_extract.json'); level=ext['chosen_level']
    native=CASE/f'extract/study_frame_a_t{round(level*100):02d}_finish.stl'
    from finish_child_clamp_smooth import repair_surface
    surface=PART/'spec/frame_a_density_surface.stl'
    repair=repair_surface(native,surface,CASE/'surface_repair.json')
    if not args.reuse_render:
        from finish_child_frame_a import finish
        finish()
        for name in ['full','lower_minus','lower_plus','upper_minus','upper_plus','splice']:
            cmd=[OSC,'--export-format','binstl','-o',str(PART/f'child_exterior_structural_frame_{name}.stl'),'-D',f'model="{name}"']
            if name not in ['full','splice']: cmd+=['-D','tile_use_rendered_full=true']
            run('render_'+name,cmd+[str(source)])
            if name=='splice':
                from clean_stl_degenerates import precision_weld
                precision_weld(PART/f'child_exterior_structural_frame_{name}.stl',CASE/'splice_precision_weld.json')
            import trimesh,numpy as np
            exported=trimesh.load(PART/f'child_exterior_structural_frame_{name}.stl',force='mesh')
            if np.any(exported.area_faces<1e-12): raise RuntimeError(f'OpenSCAD export degenerate: {name}')
    run('geometry',[sys.executable,str(ROOT/'tools/verify_child_frame_a.py')])
    final=read(STUDY)
    for key in ['geometry','design','finish','voxel_mm']: final.pop(key,None)
    full=PART/'child_exterior_structural_frame_full.stl'
    final['part']=str(full); final['_part_sha256']=digest(full)
    save(CASE/'study_final.json',final)
    same=['material','build_axis','raster_axis','infill','walls','safety_factor','max_deflection_mm','regions','cases']
    assert all(final[k]==read(STUDY)[k] for k in same)
    save(CASE/'final_provenance.json',dict(condition_identity_keys=same,all_equal=True,native_surface=digest(native),
        smoothed_surface=digest(surface),full=digest(full),repair=repair,chosen_level=level,
        source='Native density smoothing plus exact CAD stock/holes/window, no simple rib reconstruction'))
    run('final_fea',CLI+['fea',str(CASE/'study_final.json'),'--out',str(CASE/'final_fea'),'--voxel','2','--converge'],allowed=(0,1))
    # Try independent analysis once. A numerical/meshing failure remains visible.
    try:
        run('ccx',CLI+['ccx',str(full),'--study',str(CASE/'study_final.json'),'--out',str(CASE/'ccx'),'--mesh-mm','4','--converge','--map','surface'],allowed=(0,1,2,3),timeout=600)
    except subprocess.TimeoutExpired:
        print('Independent analysis timed out; finished strength remains unqualified',flush=True)
    for name in ['lower_minus','lower_plus','upper_minus','upper_plus','splice']:
        p=PART/f'child_exterior_structural_frame_{name}.stl'
        from compact_coplanar_mesh import compact
        step_input=CASE/f'step_mesh_{name}.stl'
        compact(p,step_input,CASE/f'step_coplanar_{name}.json')
        env=os.environ.copy(); env['STL_IN']=str(step_input); env['STEP_OUT']=str(p.with_suffix('.step'))
        run('step_'+name,[FC,str(ROOT/'scad/lib/stl_to_step.py')],env=env)
        axis='1,0,0' if name=='splice' else '0,1,0'
        run('print_'+name,CLI+['print',str(p),'--printer','X1C','--keep-flat','Z','--load-axis',axis],allowed=(0,1))
    save(CASE/'pipeline_status.json',dict(stage='geometry_and_analysis_complete',status='finished',
         note='Read verdicts. Full continuum success never qualifies the split M3 joints or the upstream clamp.'))

if __name__=='__main__':
    try: main()
    except Exception as e:
        save(CASE/'pipeline_failure.json',dict(error=repr(e),status='not_complete'))
        raise
