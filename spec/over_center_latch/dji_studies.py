"""Write strength-screening studies for the current final STL, no solver edits."""
from pathlib import Path
import argparse,json,hashlib,math
import numpy as np,trimesh
from geometry import *

ROOT=Path(__file__).resolve().parents[2];P=ROOT/'parts/common/jigs/over_center_latch'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',default='dji_groove40N_20261010');args=parser.parse_args()
    v=json.loads((P/'parameters.json').read_text(encoding='utf-8'))
    report=json.loads((ROOT/'assemblies/over_center_latch/_work/analysis/kinematics/report.json').read_text())
    out=P/'_work/analysis'/args.case/'studies';out.mkdir(parents=True,exist_ok=True)
    closed={i['label']:i for i in layout(v)};parts={}
    for name,label in [('base','base'),('bail','link_left'),('lever','lever'),('keeper','keeper')]:
        i=closed[label];m=trimesh.load(P/(i['file']+'.stl'))
        m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(i['ops'][1]['rotate'][1]),[0,1,0]));m.apply_translation(i['ops'][0]['translate'])
        assert m.is_volume and m.is_watertight,name
        path=out/(name+'_closed.stl');path.write_text(m.export(file_type='stl_ascii'),encoding='ascii');parts[name]=path
    def cylinder(c,r,yrange=None):
        d=dict(type='cylinder',axis='Y',centre=list(c),r=r)
        if yrange is not None:d['range']=yrange
        return d
    def box(lo,hi):return dict(type='box',min=list(lo),max=list(hi))
    def save(name,regions,cases):
        d=dict(units='mm_N_MPa',part=str(parts[name]),material='BAMBU-PETG-BASIC-V3',
            build_axis='Y',raster_axis='X',printer='X1C',infill=1.,walls=6,safety_factor=3.,max_deflection_mm=.5,
            regions=regions,cases=cases,_source_sha256=hashlib.sha256(parts[name].read_bytes()).hexdigest(),
            _canonical_source_sha256=hashlib.sha256((P/('over_center_latch_'+name+'.stl')).read_bytes()).hexdigest(),
            _limits='Linear elastic screening. Clamped bore collars approximate metal pins; local contact pressure, rubber/PETG coupling, friction, creep and fatigue unmeasured. Rear z restraint is maintained compressive seating only. Normal operating and retained 100N direct hand-press cases.')
        (out/(name+'_study.json')).write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    B0,C0,K,Q0,n,u=contact_geometry(v);B3=np.array([B0[0],0,B0[1]]);A=[0,0,v['axis_height']]
    cl=report['closed'];peak=report['peak_link'];hand=report['peak_hand']
    regions={'B':cylinder(B3,2.35,[-dimensions(v)['hood_outer']-.1,dimensions(v)['hood_outer']+.1]),
             'rear':box([v['handle_back']-.1,-v['handle_width']/2,-.1],[v['handle_back']+3.1,v['handle_width']/2,1.]),
             'press':box([v['hand_load_x']-2,-20,v['hood_top']-1],[v['hand_load_x']+2,20,v['hood_top']+.1])}
    cases=[]
    for key,q in [('peak_link',peak),('peak_hand',hand),('closed',cl)]:
        R=rotation(-q['delta_deg'])
        def vec3(f):
            a=R@np.array(f)[[0,2]];return [float(a[0]),0,float(a[1])]
        def point3(p):
            a=B0+R@(np.array(p)[[0,2]]-np.array(q['B'])[[0,2]]);return [float(a[0]),0,float(a[1])]
        qp=point3(q['rubber_point']);kp=point3(q['K'])
        regions[key+'_rubber']=cylinder(qp,1.6,[-v['epdm_width']/2,v['epdm_width']/2])
        regions[key+'_lip']=cylinder(kp,1.,[-v['epdm_width']/2,v['epdm_width']/2])
        loads=[dict(region=key+'_rubber',force=vec3(q['rubber_force_on_hook'])),dict(region=key+'_lip',force=vec3(q['lip_force_on_hook']))]
        supports=[dict(region='B',fix='xyz')]
        if key=='closed':
            supports.append(dict(region='rear',fix='z'))
            loads.append(dict(region='press',force=[0,0,-v['design_hand_force_N']]))
        else:loads.append(dict(region='press',force=vec3([0,0,-q['hand_vertical_N']])))
        cases.append(dict(name=key+('_plus100N_hand' if key=='closed' else '_operating'),supports=supports,loads=loads))
    save('lever',regions,cases)
    save('bail',dict(A=cylinder(A,2.35),B=cylinder(B3,2.35)),
         [dict(name='peak_link_compression_half',supports=[dict(region='A',fix='xyz')],
               loads=[dict(region='B',force=(-np.array(peak['link_force_on_hood'])/2).tolist())])])
    def mounts(name):
        regions={};supports=[];depth=v['host_fixed_floor'] if name=='base' else v['host_floor']
        for k,(x,y) in enumerate(mounting_holes(v)[name]):
            x+=v['catch_distance'] if name=='keeper' else 0
            key='mount'+str(k);regions[key]=box([x-3.3,y-3.3,-depth-.1],[x+3.3,y+3.3,-depth+1.5])
            supports.append(dict(region=key,fix='xyz'))
        return regions,supports
    regions,supports=mounts('base');regions['A']=cylinder(A,2.35)
    regions['rear']=box([v['handle_back']-.1,-20,-1.5],[v['handle_back']+3.1,20,.1])
    cases=[]
    for key,q in [('peak_link',peak),('peak_hand',hand),('closed',cl)]:
        loads=[dict(region='A',force=(-np.array(q['link_force_on_hood'])).tolist())]
        if key=='closed':loads.append(dict(region='rear',force=[0,0,q['hand_vertical_N']-v['design_hand_force_N']]))
        cases.append(dict(name=key+('_plus100N_direct_press' if key=='closed' else '_axis'),supports=supports,loads=loads))
    save('base',regions,cases)
    regions,supports=mounts('keeper');wall=Q0-n*(v['epdm_thickness']-v['preload'])
    regions['rubber']=cylinder([wall[0],0,wall[1]],1.5,[-v['epdm_width']/2,v['epdm_width']/2])
    # Retaining roof is at z >= K.z; include one bore-sized neighborhood
    # so the coarse 1.2 mm grid resolves the actual supporting roof too.
    regions['lip']=box([K[0]-.6,-v['epdm_width']/2,K[1]-.05],[K[0]+1.2,v['epdm_width']/2,.05])
    cases=[]
    for key,q in [('closed',cl),('dead',report['dead']),('peak_link',peak),('peak_hand',hand)]:
        cases.append(dict(name=key+'_groove_contact',supports=supports,loads=[
            dict(region='rubber',force=(-np.array(q['rubber_force_on_hook'])).tolist()),
            dict(region='lip',force=(-np.array(q['lip_force_on_hook'])).tolist())]))
    save('keeper',regions,cases)
    (out/'parameters.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    (out/'loads.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(out)

if __name__=='__main__':main()
