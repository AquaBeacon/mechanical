"""Render a parametric rebuild of the native cage load paths and author FEA.

No solver implementation; all force/material/support inputs are reused verbatim.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
BASE=PART/'_work/analysis/lightweight_epdm_v020'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',default='lightweight_lattice')
    parser.add_argument('--outer',type=float,default=3)
    parser.add_argument('--web',type=float,default=5)
    parser.add_argument('--tie',type=float,default=8)
    parser.add_argument('--rail',type=float,default=8)
    parser.add_argument('--face',type=float,default=0)
    parser.add_argument('--extra',type=float,default=0)
    parser.add_argument('--bolt-x',type=float,default=None)
    parser.add_argument('--brace',type=float,default=0)
    parser.add_argument('--shared-access',type=int,choices=[0,1,2],default=0)
    parser.add_argument('--band-h',type=float,default=32)
    parser.add_argument('--ear-t',type=float,default=24)
    parser.add_argument('--bridge-depth',type=float,default=0)
    parser.add_argument('--bridge-caps',type=int,choices=[0,1],default=0)
    args=parser.parse_args()
    if Path(args.case).name != args.case:
        raise ValueError('case must be a folder name')
    case=PART/'_work/analysis'/args.case
    case.mkdir(parents=True,exist_ok=True)
    final=case/'finished_cage.stl'
    if final.exists():
        raise RuntimeError('Preserve this experiment; select a new case for changed parameters')
    parameters=dict(lattice_outer_t=args.outer,lattice_web_w=args.web,
                    lattice_ear_tie_w=args.tie,lattice_rail_d=args.rail,lattice_face_t=args.face,
                    lattice_radial_extra=args.extra,lattice_brace_d=args.brace,
                    lattice_shared_access=args.shared_access,lattice_band_h=args.band_h,ear_t=args.ear_t,
                    lattice_ear_bridge_depth=args.bridge_depth,lattice_ear_bridge_caps=args.bridge_caps)
    if args.bolt_x is not None:
        parameters['clamp_bolt_x']=args.bolt_x
    (case/'cad_parameters.json').write_text(json.dumps(parameters,indent=2)+'\n',encoding='utf-8')
    cmd=[r'C:\Program Files\OpenSCAD\openscad.com','-o',str(final),'-D','model="cage_lattice"']
    for key,value in parameters.items(): cmd+=['-D',f'{key}={value}']
    cmd.append(str(PART/'child_wte4_suspension_clamp.scad'))
    scad=PART/'child_wte4_suspension_clamp.scad'
    source_hash=hashlib.sha256(scad.read_bytes()).hexdigest()
    shutil.copy2(scad,case/'source_snapshot.scad')
    with (case/'cad_render.log').open('w',encoding='utf-8') as stream:
        subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT,check=True,cwd=ROOT)
    if hashlib.sha256(scad.read_bytes()).hexdigest()!=source_hash:
        raise RuntimeError('CAD source changed during render')
    from clean_stl_degenerates import clean
    clean(final,case/'cad_cleanup.json')
    study=json.loads((BASE/'study_final.json').read_text(encoding='utf-8'))
    log=(case/'cad_render.log').read_text(encoding='utf-8')
    def echo(tag):
        line=next(v[6:] for v in log.splitlines() if v.startswith(f'ECHO: ["{tag}"'))
        values=ast.literal_eval(line)
        return dict(zip(values[1::2],values[2::2]))
    interface=dict(clamp=echo('CLAMP_INTERFACE'),cage=echo('CAGE_INTERFACE'))
    for name,region in study['regions'].items():
        if name.startswith('washer_'):
            region['centre'][0]=(-1 if region['centre'][0]<0 else 1)*interface['clamp']['bolt_x']
            seat=-interface['clamp']['ear_t']-0.8
            region['range']=[seat-0.05,seat+1.05]
    study['part']=str(final)
    study['_part_sha256']=hashlib.sha256(final.read_bytes()).hexdigest()
    study['_reconstruction']='Parametric dual-arc rings, radial webs and three widely spaced columns from the native load paths. Tube, external mounting pattern and rope eye retained. All 11 force cases retained; washer regions follow actual CAD bolt centres.'
    study['_source_scad_sha256']=hashlib.sha256((PART/'child_wte4_suspension_clamp.scad').read_bytes()).hexdigest()
    (case/'study_final.json').write_text(json.dumps(study,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (case/'interface.json').write_text(json.dumps(interface,indent=2)+'\n',encoding='utf-8')
    print(final)


if __name__=='__main__': main()
