"""Compare TD print poses with actual automatic support generation (offline)."""
from pathlib import Path
import json
import sys
import numpy as np
import trimesh
from topopt import slicer
from topopt.cli import slice as native

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_exterior/_work/analysis/support_reduction/pose_trials'

def main(final=False):
    original=native._write_presets
    slicer.FILAMENT_FAMILY['PETG']='Bambu PETG Basic'
    def inputs(*a,**kw):
        files=original(*a,**kw);p=Path(files['process']);d=json.loads(p.read_text())
        d.update(wall_loops='8',sparse_infill_density='100%',sparse_infill_pattern='alignedrectilinear',
                 support_threshold_angle='45',support_on_build_plate_only='0',brim_width='6',brim_type='outer_only')
        p.write_text(json.dumps(d));return files
    native._write_presets=inputs
    results=[]
    cases=[('td_support',*c) for c in [(-135,15,0),(-135,30,0),(-135,45,0),(-135,30,1.5),(-135,45,1.5),(0,90,0),(0,-90,0)]]
    if final:cases=[('td_support',0,-90,0),('camera_stop',-90,0,0)]
    for name,rx,ry,clip in cases:
        p=OUT/f'{name}_x{rx}_y{ry}_clip{clip:g}';p.mkdir(parents=True,exist_ok=True)
        stem='parent_oneplate_'+name
        m=trimesh.load(ROOT/'parts/parent/exterior/printed'/stem/(stem+'.stl'),force='mesh')
        m.apply_transform(trimesh.transformations.euler_matrix(*np.radians([rx,ry,0])))
        if clip:m=m.slice_plane([0,0,m.bounds[0,2]+clip],[0,0,1],cap=True)
        m.apply_translation(-m.bounds[0]);m.export(p/'posed.stl',file_type='stl_ascii')
        code=native.main([str(p/'posed.stl'),'--out',str(p/'slice'),'--printer','X1C','--material','PETG',
                          '--layer-mm','0.2','--supports','auto','--orient','keep','--bed-type','Textured PEI Plate','--quiet'])
        d=json.loads((p/'slice/slice.json').read_text())
        row=dict(part=stem,rotation=[rx,ry,0],clip_mm=clip,exit_code=code,error=d.get('error'),support_mm=slicer.support_mm(d.get('filament_by_feature_mm',{})),grams=d.get('filament_g'))
        results.append(row);print(row,flush=True)
    (OUT/('results_final.json' if final else 'results.json')).write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main('--final' in sys.argv)
