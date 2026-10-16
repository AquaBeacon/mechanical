"""Measure real frame A output; CAD hole/hand reservations are acceptance inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'

def main():
    ap=argparse.ArgumentParser();group=ap.add_mutually_exclusive_group();group.add_argument('--inputs',action='store_true');group.add_argument('--splice-only',action='store_true');args=ap.parse_args()
    dims=json.loads((PART/'spec/design_parameters.json').read_text(encoding='utf-8'))
    results={}
    if args.inputs:
        names=['domain','preserve']; paths=[CASE/(n+'.stl') for n in names]
    elif args.splice_only:
        previous=json.loads((CASE/'final_geometry_checks.json').read_text())
        assert previous['pass_geometry'],'Only a passed frame may be reused'
        results=previous['parts']
        for n,row in results.items():
            if n=='splice':continue
            p=PART/f'child_exterior_structural_frame_{n}.stl'
            assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],'Cached frame geometry changed'
        names=['splice'];paths=[PART/'child_exterior_structural_frame_splice.stl']
    else:
        names=['full','lower_minus','lower_plus','upper_minus','upper_plus','splice']
        paths=[PART/f'child_exterior_structural_frame_{n}.stl' for n in names]
    for n,p in zip(names,paths):
        m=trimesh.load(p,force='mesh')
        row=dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),watertight=bool(m.is_watertight),
                 winding_consistent=bool(m.is_winding_consistent),extents_mm=m.extents.tolist(),
                 volume_mm3=float(m.volume),mass_g_provisional=float(m.volume*1.25/1000),
                 positive_bodies=int(sum(s.volume>0 for s in m.split(only_watertight=False))))
        row['pass_mesh']=row['watertight'] and row['winding_consistent'] and (n=='preserve' or row['positive_bodies']==1)
        if n not in ['splice']:
            # Entire 270x100 through-board rectangle, not a thin centreline.
            pts=np.array([[x,y,z] for x in np.linspace(-135,135,31)
                          for y in np.linspace(-82,18,15) for z in [0.1,3,6,9,11.9,24,36,dims['max_depth']-.1]])
            row['hand_clear_270x100']=not bool(m.contains(pts).any())
            finger=np.array([[x,y,z] for x in np.linspace(-45,45,11) for y in np.linspace(215,245,7)
                             for z in [.1,6,12,24,36,dims['max_depth']-.1]])
            row['finger_clear_90x30']=not bool(m.contains(finger).any())
        if n not in ['full','domain','preserve']:
            row['fit_conservative_250_with_5mm_brim']=bool(np.all(m.extents+[10,10,0] <= [250,250,250]))
        if n=='full':
            foil=np.array([[s*x,140,z] for s in [-1,1] for x in [147.98,148,148.02] for z in np.linspace(14,44,31)])
            row['no_old_rim_boundary_foil']=not bool(m.contains(foil).any())
            holes=[]
            angles=np.linspace(0,2*np.pi,24,endpoint=False)
            for kind in ['clamp_holes_yz','c_holes_yz','joint_holes_yz']:
                for x,y in dims[kind]:
                    pts=np.array([[x+1.5*np.cos(a),y+1.5*np.sin(a),z]
                                  for a in angles for z in np.linspace(0.05,dims['max_depth']-.05,36)])
                    holes.append(dict(kind=kind,centre_yz_mm=[x,y],m3_shank_clear=not bool(m.contains(pts).any())))
            row['holes']=holes; row['all_M3_shanks_clear']=all(h['m3_shank_clear'] for h in holes)
            vertices=np.array([[np.cos(a),np.sin(a)] for a in np.arange(6)*np.pi/3])*(5.5/np.sqrt(3))
            nut_xy=np.array([(1-t)*vertices[i]+t*vertices[(i+1)%6]
                             for i in range(6) for t in np.linspace(0,1,9)])
            nuts=[]
            for x,y in dims['joint_holes_yz']:
                pts=np.array([[x+u,y+v,z] for u,v in nut_xy for z in [4.01,4.8,5.6,6.39]])
                nuts.append(not bool(m.contains(pts).any()))
            row['all_joint_nuts_fit_AF5_5']=all(nuts)
            outer=dims['joint_seat_depth']+dims['splice_seat_depth']+.5
            row['joint_screw_tip_inside_frame_face']=outer-dims['joint_screw_length']>=0
            row['joint_screw_full_nut_engagement']=outer-dims['joint_screw_length'] < dims['nut_pocket_depth']-2.4
            tools=[]
            for x,y in dims['clamp_holes_yz']+dims['c_holes_yz']:
                if y>=254: continue
                pts=np.array([[x+5*np.cos(a),y+5*np.sin(a),z] for a in angles
                              for z in np.linspace(12.1,dims['max_depth']+.1,20)])
                tools.append(not bool(m.contains(pts).any()))
            row['recessed_mount_tool_D10_clear']=all(tools)
            recess=dims['eye_recess']
            pts=np.array([[x,y,z] for x in np.linspace(-recess['width']/2+1,recess['width']/2-1,9)
                          for y in np.linspace(recess['centre_y']-recess['height']/2+1,recess['centre_y']+recess['height']/2-1,11)
                          for z in [.1,recess['depth']/2,recess['depth']-.05]])
            row['clamp_eye_recess_clear']=not bool(m.contains(pts).any())
        if n=='splice':
            pts=np.array([[x+1.5*np.cos(a),y+1.5*np.sin(a),z]
                          for x in [-12,12] for y in [-6,6]
                          for a in np.linspace(0,2*np.pi,24,endpoint=False)
                          for z in np.linspace(.05,dims['splice_thickness']-.05,12)])
            row['splice_M3_shanks_clear']=not bool(m.contains(pts).any())
            pts=np.array([[x+4.5*np.cos(a),y+4.5*np.sin(a),z]
                          for x in [-12,12] for y in [-6,6]
                          for a in np.linspace(0,2*np.pi,24,endpoint=False)
                          for z in np.linspace(dims['splice_seat_depth']+.1,dims['splice_thickness']+.1,12)])
            row['splice_tool_D9_clear']=not bool(m.contains(pts).any())
        results[n]=row
    checks=[v for r in results.values() for k,v in r.items()
            if k in ['pass_mesh','hand_clear_270x100','finger_clear_90x30','fit_conservative_250_with_5mm_brim','all_M3_shanks_clear',
                     'all_joint_nuts_fit_AF5_5','joint_screw_tip_inside_frame_face','joint_screw_full_nut_engagement',
                     'splice_M3_shanks_clear','splice_tool_D9_clear','recessed_mount_tool_D10_clear','clamp_eye_recess_clear','no_old_rim_boundary_foil']]
    result=dict(pass_geometry=all(checks),parts=results,
                limits='Discrete geometric checks only; no bolt/joint strength, ergonomics or mesh convergence claim.')
    out=CASE/('input_geometry_checks.json' if args.inputs else 'final_geometry_checks.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(pass_geometry=result['pass_geometry'],parts={n:{k:r[k] for k in ['extents_mm','mass_g_provisional','pass_mesh']} for n,r in results.items()}),ensure_ascii=False))
    raise SystemExit(0 if result['pass_geometry'] else 1)

if __name__=='__main__':
    main()
