"""Explore thicker splice stock with an unchanged 8 mm washer seat.

No canonical design is promoted by this screen. Run FEA only after the large
frame GPU job has ended; all solvers remain the native topopt CLI.
"""
from pathlib import Path
import argparse,json,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/splice_load_capacity'
OSC=r'C:\Program Files\OpenSCAD\openscad.com'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fea',action='store_true');parser.add_argument('--heights',default='10,12,14');parser.add_argument('--well-diameter',type=float,default=10);parser.add_argument('--width',type=float,default=24);args=parser.parse_args()
    source=PART/'child_exterior_structural_frame.scad'
    for height in [int(h) for h in args.heights.split(',')]:
        suffix='' if args.well_diameter==10 else '_well'+str(args.well_diameter).replace('.','_')
        if args.width!=24:suffix+='_width'+str(args.width).replace('.','_')
        case=CASE/f'screen_thickness_{height}{suffix}';case.mkdir(exist_ok=True)
        cad=case/'splice_screen.scad'
        cad.write_text('use <'+source.as_posix()+'>\n'+f'''$fn=48;
difference() {{
 edge_extrude({height}) rr(-24,{-args.width/2},48,{args.width},3);
 for(x=[-12,12],y=[-6,6]) {{
  translate([x,y,-.02]) cylinder(d=3.5,h={height}+.04,$fn=32);
  translate([x,y,0]) cylinder(d1=4.7,d2=3.5,h=.62,$fn=32);
  translate([x,y,7.4]) cylinder(d1=3.5,d2=4.7,h=.62,$fn=32);
  translate([x,y,8]) cylinder(d={args.well_diameter},h={height}-8+.02);
 }}
}}
''',encoding='utf-8')
        stl=case/'splice_screen.stl'
        if not args.fea:
            with (case/'render.log').open('w') as log:
                subprocess.run([OSC,'--export-format','binstl','-o',str(stl),str(cad)],stdout=log,stderr=subprocess.STDOUT,check=True)
            from clean_stl_degenerates import precision_weld
            precision_weld(stl,case/'precision_weld.json')
            study=json.loads((CASE/'study.json').read_text())
            study['part']=str(stl)
            (case/'study.json').write_text(json.dumps(study,indent=2)+'\n',encoding='utf-8')
        else:
            with (case/'fea.log').open('w') as log:
                p=subprocess.run([sys.executable,str(ROOT/'tools/clamp_bambu_material.py'),'fea',str(case/'study.json'),
                                  '--out',str(case/'fea'),'--voxel','1','--converge'],stdout=log,stderr=subprocess.STDOUT)
            print(height,'native FEA exit',p.returncode,flush=True)


if __name__=='__main__':main()
