"""Screen a deeper integral handle using the native FEA, without changing CAD.

All trials live in the original case's analysis directory. This is a design
comparison, not a production mesh or an independent solver implementation.
"""
from pathlib import Path
import argparse,json,subprocess,sys
import trimesh

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_hand_access'
OSC=r'C:\Program Files\OpenSCAD\openscad.com'


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--depth',type=float,required=True)
    ap.add_argument('--rails',action='store_true'); args=ap.parse_args()
    out=CASE/f'handle_{"U_" if args.rails else ""}depth_{args.depth:g}'; out.mkdir(exist_ok=True)
    d=json.loads((PART/'spec/design_parameters.json').read_text())
    points=d['clamp_holes_yz']+d['c_holes_yz']+d['joint_holes_yz'] if args.rails else [p for p in d['c_holes_yz']+d['joint_holes_yz'] if p[1]>=254]
    # Same compensated R0.6 edge construction as the canonical stock.
    extra=''
    if args.rails:
        extra='''
union() {
 difference() { rr(-170,-132,340,408,3); rr(-166,-128,332,400,3); }
 difference() { rr(-152,-92,304,350,3); rr(-148,-88,296,342,3); }
 for(y=[-110,70,190,264]) rr(-24,y-12,48,24,3);
 for(x=[-158,158]) rr(x-11,56,22,48,3);
}
'''
    profile='translate([-167,257]) offset(r=3) square([334,16]);'
    if args.rails: profile='union() { '+profile+extra+' }'
    code=f'''$fn=48;
module rr(x,y,w,h,r) {{ translate([x+r,y+r]) offset(r=r) square([w-2*r,h-2*r]); }}
module stock() {{ minkowski() {{
 translate([0,0,.6]) linear_extrude({args.depth} - 1.2)
  offset(delta=-.6) {profile}
 sphere(r=.6,$fn=16);
}} }}
module cuts() {{ for(p={json.dumps(points)}) translate([p[0],p[1],-1]) cylinder(d=3.5,h={args.depth+2}); }}
if(model=="stock") stock(); else cuts();
'''
    src=out/'reinforcement.scad'; src.write_text(code)
    for name in ['stock','cuts']:
        r=subprocess.run([OSC,'-o',str(out/(name+'.stl')),'-D',f'model="{name}"',str(src)],capture_output=True,text=True)
        (out/(name+'_render.log')).write_text(r.stdout+r.stderr,encoding='utf-8'); r.check_returncode()
    base=trimesh.load(PART/'child_exterior_structural_frame_full.stl',force='mesh')
    extra=trimesh.load(out/'stock.stl',force='mesh'); cuts=trimesh.load(out/'cuts.stl',force='mesh')
    mesh=trimesh.boolean.union([base,extra],engine='manifold')
    mesh=trimesh.boolean.difference([mesh,cuts],engine='manifold')
    if not mesh.is_watertight or not mesh.is_winding_consistent: raise RuntimeError('Trial mesh invalid')
    mesh.export(out/'trial.stl')
    (out/'geometry.json').write_text(json.dumps(dict(volume_mm3=mesh.volume,extents=mesh.extents.tolist(),mass_g_PETG=mesh.volume*.00125),indent=2))
    study=json.loads((CASE/'study_frame_a.json').read_text())
    for k in ['geometry','design','finish']: study.pop(k,None)
    study['part']=str(out/'trial.stl'); study['regions']['handle']['max'][2]=args.depth
    # A 9 mm washer footprint still contains material after a 3.5 mm bore at
    # the 2 mm screening grid. The original r3.1 footprint disappears there.
    for region in study['regions'].values():
        if region.get('type')=='cylinder': region['r']=4.5
    study['printer']['build_volume_mm'][2]=args.depth+10
    study['_what']=f'Handle reinforcement screening at depth {args.depth} mm; support spans full handle thickness, washer footprint radius4.5. Not a production mesh.'
    study['cases']=[c for c in study['cases'] if c['name']=='handling_lateral_positive_2g']
    study['required_cases']=[c['name'] for c in study['cases']]
    (out/'study.json').write_text(json.dumps(study,indent=2)+'\n')
    with (out/'fea.log').open('w') as log:
        r=subprocess.run([sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py'),'fea',str(out/'study.json'),'--out',str(out/'fea'),'--voxel','2'],stdout=log,stderr=subprocess.STDOUT)
    print('Screen complete',args.depth,'native exit',r.returncode,flush=True)


if __name__=='__main__': main()
