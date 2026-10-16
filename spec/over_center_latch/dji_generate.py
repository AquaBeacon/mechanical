"""Generate canonical source and placement for the authorized 40 N design."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from geometry import *

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'parts/common/jigs/over_center_latch';ASM=ROOT/'assemblies/over_center_latch'

def main():
    v=json.loads((P/'parameters.json').read_text(encoding='utf-8'))
    v['preload']=calibrate_preload(v)
    B,C,K,Q,n,u=contact_geometry(v);d=dimensions(v)
    v['BC_length']=float(np.linalg.norm(C-B))
    (P/'parameters.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
    left=v['toe_face_x'];hh=v['toe_half_height'];slope=1/math.tan(math.radians(v['groove_angle_deg']))
    top=C+[left+hh*slope,hh];bottom=C+[left-hh*slope,-hh]
    right=C[0]+v['toe_right'];outer=C[0]+v['claw_neck_width'];roof=v['hood_top']-v['hood_roof_thickness']
    # Carry the claw neck through the roof thickness. A 0.1 mm overlap at
    # its underside leaves the chamfered joint too sensitive to voxel size.
    neck_front=C[0]+v['lip_end']+.7
    # Raise the outer heel underside so its opening sweep clears the pocket
    # floor. Preserve the 80-degree loaded face and its full toe height.
    toe=[bottom.tolist(),[right,bottom[1]],[outer,bottom[1]+v.get('claw_outer_underside_relief',0)], [outer,v['hood_top']-.5],
         [neck_front,v['hood_top']-.5],[neck_front,2.],[right,top[1]],top.tolist()]
    # Continuous side ribs carry the claw moment to B rather than bending
    # only the thin top panel. Their bottom stays above the host surface.
    side=[[v['handle_back'],v['hood_top']],[outer,v['hood_top']],[outer,1],
          [B[0]+3,1],[B[0]+3,B[1]-1],[B[0]-3,B[1]-2],
          [v['handle_front'],4],[v['handle_back'],0]]
    handle=[[v['handle_back'],0],[v['handle_back']+3,0],[v['handle_back']+3,roof],
            [v['handle_front'],roof],[v['handle_front'],v['hood_top']],[v['handle_back'],v['hood_top']]]
    wall=Q-n*(v['epdm_thickness']-v['preload'])
    def wallx(z):return float(wall[0]-C[0]+slope*(z-wall[1]))
    z=v['pocket_floor'];cl=v['contact_chamfer'];r=v['keeper_recess_front']
    cavity=[[wallx(z+.2),z+.2],[wallx(z)+.2,z],[r-.2,z],[r,z+.2],[r,5],
            [v['lip_end'],5],[v['lip_end'],K[1]+cl],[v['lip_end']-cl,K[1]],
            [wallx(K[1]),K[1]]]
    # Compressed EPDM face; nominal free 3 mm thickness is recorded separately.
    epdm=[]
    for a,b in [(-1,0),(1,0),(1,1),(-1,1)]:
        point=wall+u*(a*v['epdm_height']/2+v.get('epdm_tangent_offset',0.))+n*b*(v['epdm_thickness']-v['preload'])
        epdm.append([float(point[0]-C[0]),float(point[1])])
    sweep=[]
    # 2 degree samples are much finer than the 0.4 mm motion allowance;
    # the independent actual-STL sweep still checks 273 moving poses.
    sweep_poses=[(th,0) for th in np.linspace(v['open_angle'],closed_angle(v),31)]
    sweep_poses += [(v['open_angle'],lift) for lift in np.linspace(0,v['release_angle'],19)]
    for th,lift in sweep_poses:
        q=pose(v,th,lift);cc=B+rotation(-q['delta_deg'])@(np.array([0.,v['axis_height']])-np.array(q['B'])[[0,2]])
        sweep.append(cc.tolist())
    derived=dict(B_closed=B.tolist(),toe_neck_points=toe,hood_side_points=side,handle_points=handle,
                 keeper_void_points=cavity,epdm_points=epdm,A_hardware_sweep=sweep,axis_access_radius=4.2,**d)
    text='// GENERATED: edit parameters.json, spec/over_center_latch/latch_body.scad and generate.py.\n'
    text+='use <../../../../scad/lib/util.scad>\npart="assembly";\n'
    text+='\n'.join(f'{k}={json.dumps(x)};' for k,x in {**v,**derived}.items() if isinstance(x,(int,float,list,bool)))+'\n'
    text+=(Path(__file__).with_name('latch_body.scad')).read_text(encoding='utf-8')
    (P/'over_center_latch.scad').write_text(text,encoding='utf-8')
    parts=['base','bail','lever','keeper','epdm','axis_a','axis_b']
    (P/'variants.txt').write_text(''.join(f'{s} part="{s}"\n' for s in parts),encoding='utf-8')
    deps=['geometry.py','dji_geometry.py','latch_body.scad','generate.py','dji_generate.py','dji_verify.py','build_verify.py','rubber_estimate.py','clamp_loads.py','clamp_studies.py','dji_studies.py','petg_basic_fea.py']
    manuf=dict(source_dependencies=['../../../../spec/over_center_latch/'+s for s in deps]+['parameters.json'],
               non_print_files=['over_center_latch_'+s for s in ['epdm','axis_a','axis_b']],
               print_rotations_deg={'over_center_latch_'+s:[90,0,0] for s in ['base','bail','lever','keeper']},
               stl_export_format='asciistl',portable_stl_export_format='stl_ascii',step_coplanar_merge=True,
               degenerate_edge_flip_files=['over_center_latch_lever'])
    (P/'manufacturing.json').write_text(json.dumps(manuf,indent=2)+'\n',encoding='utf-8')
    (ASM/'placement.json').write_text(json.dumps(dict(name='over_center_latch',units='mm',
       note='DJI-type short links, extended B-mounted hood, 80deg recessed keeper. Nominal 40 N horizontal clamp; rubber properties provisional.',items=layout(v)),indent=2)+'\n',encoding='utf-8')
    config=dict(status='prototype_strength_unverified',note='強度検証未完了の試作版。40 Nは実測校正が必要。構造解析の収束と固定部の局所応力は未解決で、100 N手押し耐力を認定しない。X1C PETG Basic / 0.4 nozzle / 0.2 layer / 6 walls / 100% infill. Four types, five printed pieces. M3x20 countersunk A, M3x35 cap B. No dedicated stop; hood seats on platform.',notes=['parts/common/jigs/over_center_latch/README.md'])
    (ASM/'print_config.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
    interfaces=dict(units='mm',base_holes=mounting_holes(v)['base'],keeper_local_holes=mounting_holes(v)['keeper'],
        keeper_closed_origin=[v['catch_distance'],0,0],fixed_plate_mm=v['host_fixed_floor'],receiver_plate_mm=v['host_floor'],
        groove_deg=v['groove_angle_deg'],epdm_cut_mm=[v['epdm_width'],v['epdm_height'],1],epdm_sheets=3,
        closed_preload_normal_mm=v['preload'],claw_height_mm=2*hh,additional_stopper=False)
    (P/'interfaces.json').write_text(json.dumps(interfaces,indent=2)+'\n',encoding='utf-8')
    dead=dead_angle(v);rows=[load_at(v,th) for th in np.linspace(v['open_angle'],closed_angle(v),601)]
    active=[q for q in rows if q['normal_rubber_N']>1e-6]
    assert all(q['lip_N']>=-1e-7 for q in active),'Unilateral lip contact would lift off'
    report=dict(target_closed_clamp_N=40,closed=load_at(v,closed_angle(v)),dead=load_at(v,dead),
        dead_angle_deg=dead,snap_travel_deg=closed_angle(v)-dead,
        peak_link=max(rows,key=lambda q:q['link_N']),peak_hand=max(rows,key=lambda q:abs(q['hand_vertical_N'])),
        peak_clamp=max(rows,key=lambda q:q['clamp_horizontal_N']),max_compression_mm=max(q['compression_mm'] for q in rows),
        restoring_moment_lever_margin_mm=over_center(v,closed_angle(v)),
        hardness_sensitivity_closed_N={str(h):rubber_force(v,closed_angle(v),h)[0]*n[0] for h in [60,65,70]},
        limitations=['Nominal estimate assuming Shore A65 and freely bulging neo-Hookean solid EPDM',
                    'No measured force; adhesive, three sheet interfaces, friction, contact width and PETG compliance omitted',
                    'Finite contact model explicitly ends before toe disengagement; free trajectory is hand-guided'])
    out=ASM/'_work/analysis/kinematics';out.mkdir(parents=True,exist_ok=True)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    step_poses=[dict(angle_deg=th,lift_deg=lift,items=layout(v,th,lift)) for th,lift in
                [(v['open_angle'],0),(dead,0),(closed_angle(v),0),(v['open_angle'],v['release_angle'])]]
    (out/'step_poses.json').write_text(json.dumps(step_poses,indent=2)+'\n',encoding='utf-8')
    img=ASM/'_work/images';img.mkdir(parents=True,exist_ok=True)
    fig,axes=plt.subplots(1,3,figsize=(14,4.6))
    for ax,th,label in zip(axes,[v['open_angle'],dead,closed_angle(v)],['Released','Actual dead point','Closed']):
        p=pose(v,th);b=np.array(p['B'])[[0,2]];c=np.array(p['C'])[[0,2]]
        ax.plot([0,b[0]],[v['axis_height'],b[1]],'-o',color='#df9a32',lw=5)
        ax.plot([b[0],c[0]],[b[1],c[1]],'-o',color='#3579a0',lw=4)
        ax.plot([v['host_seam_x'],45],[0,0],color='#46836b',lw=2)
        ax.scatter(*K,color='black',marker='x');ax.set_title(f'{label}: {th:.2f} deg')
        for name,point in [('A',[0,v['axis_height']]),('B',b),('C',c)]:ax.annotate(name,point,xytext=(4,6),textcoords='offset points')
        ax.set_aspect('equal');ax.set_xlim(-20,45);ax.set_ylim(-9,20);ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(img/'three_poses.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(8,7),sharex=True)
    axes[0].plot([q['angle_deg'] for q in rows],[q['clamp_horizontal_N'] for q in rows],label='Horizontal clamp N')
    axes[0].plot([q['angle_deg'] for q in rows],[q['link_N'] for q in rows],label='Total short-link compression N')
    axes[1].plot([q['angle_deg'] for q in rows],[q['hand_vertical_N'] for q in rows],label='Downward hand force N (+ close / - restoring)')
    for ax in axes:ax.axvline(dead,color='gray',ls='--');ax.grid(alpha=.3);ax.legend(fontsize=8)
    axes[1].set_xlabel('Short-link angle / deg');fig.tight_layout();fig.savefig(img/'holding_force.png',dpi=160);plt.close(fig)
    print(json.dumps({k:report[k] for k in ['target_closed_clamp_N','dead_angle_deg','snap_travel_deg','max_compression_mm','restoring_moment_lever_margin_mm']},indent=2))

if __name__=='__main__':main()
