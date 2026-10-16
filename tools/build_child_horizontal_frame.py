"""Render only the horizontal frame source, preserving unrelated print sets."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import trimesh
from prepare_child_horizontal_frame import ROOT,PART,OUT,OSC,STEM,VARIANTS


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--variant',action='append');ap.add_argument('--measure-only',action='store_true');args=ap.parse_args()
    names=args.variant or VARIANTS
    logdir=PART/'_work/logs';logdir.mkdir(parents=True,exist_ok=True)
    def build(v):
        path=PART/(STEM+'_'+v+'.stl')
        if not args.measure_only:
            with (logdir/(v+'.log')).open('w',encoding='utf-8') as log:
                result=subprocess.run([str(OSC),'--export-format','binstl','-D','part="'+v+'"',
                      '-o',str(path),str(PART/(STEM+'.scad'))],stdout=log,stderr=subprocess.STDOUT)
            if result.returncode:raise RuntimeError(v+' render failed; see '+str(logdir/(v+'.log')))
        m=trimesh.load(path,force='mesh')
        row=dict(sha256=hashlib.sha256(path.read_bytes()).hexdigest(),watertight=bool(m.is_watertight),
                 winding_consistent=bool(m.is_winding_consistent),volume_mm3=float(m.volume),
                 bounds_mm=m.bounds.tolist(),faces=len(m.faces),
                 positive_bodies=int(sum(s.volume>0 for s in m.split(only_watertight=False))))
        if not row['watertight'] or not row['winding_consistent'] or row['positive_bodies']!=1:
            raise RuntimeError('Invalid manufactured solid: '+v+' '+str(row))
        print(v,round(m.volume),'mm3',len(m.faces),'faces',flush=True)
        return v,row
    with ThreadPoolExecutor(max_workers=2) as pool:records=dict(pool.map(build,names))
    if not args.measure_only:
        # Existing audited numerical cleanup, sequential MeshLab operations.
        from clean_stl_degenerates import precision_weld,clean
        raw=PART/'_work/intermediate/openscad_raw';raw.mkdir(parents=True,exist_ok=True)
        for v in names:
            path=PART/(STEM+'_'+v+'.stl');shutil.copy2(path,raw/path.name)
            report=PART/'_work/analysis'/('cleanup_'+v+'.json')
            weld=precision_weld(path,allow_collinear=True)
            flipped=clean(path,binary=True)
            report.write_text(json.dumps(dict(weld=weld,edge_flip=flipped),indent=2)+'\n',encoding='utf-8')
        # Measure again without re-rendering the now validated print mesh.
        args.measure_only=True
        records=dict(build(v) for v in names)
    report=PART/'_work/analysis/manufacturing_geometry.json';report.parent.mkdir(parents=True,exist_ok=True)
    if args.variant and report.exists():
        previous=json.loads(report.read_text(encoding='utf-8'));previous.update(records);records=previous
    report.write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
