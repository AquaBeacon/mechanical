"""Inspect stored 3MF settings and plot first/bridge layers from actual G-code."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile
import numpy as np
import trimesh as tm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from review_parent_exterior_slices import paths

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from check_child_horizontal_support_free import bridge_regions
A=ROOT/'assemblies/td04a_fixture'

def main():
    jobs=json.loads((A/'print_jobs/cable_clearance_r6/validation.json').read_text())
    detection={r['file']:r for r in json.loads((A/'_work/analysis/slicing/support_detection/validation.json').read_text())}
    manifest=json.loads((A/'parts/manifest.json').read_text(encoding='utf-8'))
    placements=json.loads((A/'placement.json').read_text(encoding='utf-8'))
    rows=[];panels=[]
    for row in jobs:
        stem=Path(row['file']).stem;p=A/'parts'/row['file'];job=A/'print_jobs/cable_clearance_r6'/stem
        with zipfile.ZipFile(job/(stem+'.3mf')) as z:settings=json.loads(z.read('Metadata/project_settings.config'))
        mesh=tm.load_mesh(p);regions=bridge_regions(mesh)
        records=paths(job/'plate_1.gcode')
        support=sum(1 for zz,f,pp in records if f.startswith('Support'))
        bridges=[float(np.linalg.norm(pp[1,:2]-pp[0,:2])) for zz,f,pp in records if 'bridge' in f.lower()]
        width=max([r['local_width_mm'] for r in regions],default=0)
        rec=dict(file=row['file'],sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                 three_mf_sha256=hashlib.sha256((job/(stem+'.3mf')).read_bytes()).hexdigest(),
                 gcode_sha256=hashlib.sha256((job/'plate_1.gcode').read_bytes()).hexdigest(),
                 layer_mm=float(settings['layer_height']),walls=str(settings['wall_loops']),
                 infill=settings['sparse_infill_density'],support_enabled=str(settings['enable_support']),
                 support_extrusion_moves=support,detector_support_filament_mm=detection[row['file']]['support_filament_mm'],
                 max_projected_downward_region_width_mm=width,
                 max_bridge_extrusion_segment_mm=max(bridges,default=0))
        rec['passed']=(rec['sha256']==row['source_sha256']==detection[row['file']]['source_sha256']
                       and abs(rec['layer_mm']-row['layer_mm'])<1e-6 and rec['walls']=='8'
                       and rec['infill']=='100%' and rec['support_enabled']=='0'
                       and support==0 and width<10 and row['bed_fits'] and not row['warnings'])
        rows.append(rec)
        layers=sorted({z for z,f,p in records if f=='Outer wall'})
        entry=next(e for e in manifest['parts'] if e['file']==row['file'])
        transform=np.array(entry['model_to_print'])
        # Pick sections at the actual sensor/foot axes and near the last roof.
        sensor=placements['confirmed_interface']['hole_center_pitch_mm']/2
        bore_z=next(v for v in placements['fixture_variants'] if v['stem']==stem)['sensor_hole_z_mm']
        axis_z=[(transform@np.array([x,0,bore_z,1]))[2] for x in [-sensor,0,sensor]]
        targets=([layers[0],12.2,65.2,67.8] if 'child_side' in stem else [layers[0],axis_z[0]+.2,axis_z[1]+.2,axis_z[2]+2.8])
        for target in targets:
            z=min(layers,key=lambda zz:abs(zz-target))
            panels.append((stem,z,[(f,p) for zz,f,p in records if zz==z and f!='Custom']))
        rec['reviewed_layers_mm']=[p[1] for p in panels[-4:]]
    fig,axes=plt.subplots(len(jobs)*2,2,figsize=(12,8*len(jobs)))
    for ax,(stem,z,segments) in zip(axes.flat,panels):
        for kind,color in [('part','#247895'),('bridge','#df8500'),('support','#b33d59')]:
            selected=[p[:,:2] for f,p in segments if ('support' if f.startswith('Support') else 'bridge' if 'bridge' in f.lower() else 'part')==kind]
            if selected:ax.add_collection(LineCollection(selected,colors=color,linewidths=.5))
        ax.autoscale();ax.set_aspect('equal');ax.set_title(stem+f' / build Z={z:g} mm')
        ax.set_xlabel('bed X / mm');ax.set_ylabel('bed Y / mm')
    fig.suptitle('Actual G-code: first layer and detail layer\nBlue: part, amber: bridge, red: support')
    fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(A/'_work/images/slice_layers.png',dpi=130);plt.close(fig)
    result=dict(passed=all(r['passed'] for r in rows),parts=rows,
                limits=['Automatic support detection and production toolpaths are inspected separately.',
                        'Small projected regions and reviewed toolpaths do not replace a physical PETG print.',
                        'First print must check teardrop hole roofs, edge chamfers and bed adhesion.',
                        'G2/G3 arcs are endpoint chords in these plots; bridge extrusion strokes are G1.'])
    (A/'_work/analysis/slicing/slice_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1
if __name__=='__main__':sys.exit(main())
