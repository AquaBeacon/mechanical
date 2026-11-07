"""Audit stored 3MF settings/hashes and plot actual extrusion layers for review."""
from pathlib import Path
import json,sys,re,zipfile,hashlib
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from check_child_horizontal_support_free import bridge_regions
A=ROOT/'assemblies/parent_exterior'

def paths(path):
    point=np.zeros(3);feature='';rows=[];relative=True;e=0.
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('M83'):relative=True
        if line.startswith('M82'):relative=False
        if line.startswith('; FEATURE:'):feature=line.split(':',1)[1].strip()
        if line.startswith('G92 E'):e=float(re.search(r'E(-?\d*\.?\d+)',line).group(1))
        if not re.match(r'^G[0123] ',line):continue
        args={k:float(v) for k,v in re.findall(r'([XYZE])(-?\d*\.?\d+)',line)}
        old=point.copy()
        for n,k in enumerate('XYZ'):
            if k in args:point[n]=args[k]
        extrusion=args.get('E',0) if relative else args.get('E',e)-e
        if 'E' in args:e=args['E'] if not relative else e+args['E']
        if extrusion>0 and ('X' in args or 'Y' in args) and feature:
            rows.append((round(float(point[2]),3),feature,np.array([old,point])))
    return rows

def main(job_name='qr_standing',analysis_name='qr_standing',image_name='qr_slice_layers'):
    records=json.loads((A/'print_jobs'/job_name/'validation.json').read_text())
    audit=[];panels=[]
    for row in records:
        stem=Path(row['file']).stem;job=A/'print_jobs'/job_name/stem;source=A/'parts'/row['file']
        with zipfile.ZipFile(job/(stem+'.3mf')) as z:settings=json.loads(z.read('Metadata/project_settings.config'))
        mesh=trimesh.load(source,force='mesh');regions=bridge_regions(mesh)
        max_width=max([x['local_width_mm'] for x in regions],default=0)
        rec=dict(file=row['file'],source_hash_matches=hashlib.sha256(source.read_bytes()).hexdigest()==row['source_sha256'],three_mf_sha256=hashlib.sha256((job/(stem+'.3mf')).read_bytes()).hexdigest(),layer_mm=float(settings['layer_height']),wall_loops=settings['wall_loops'],infill=settings['sparse_infill_density'],support_enable=settings['enable_support'],bed_only=settings.get('support_on_build_plate_only'),max_projected_bridge_width_mm=max_width)
        rec['passed']=rec['source_hash_matches'] and abs(rec['layer_mm']-row['layer_mm'])<1e-7 and str(rec['support_enable'])==('0' if row['supports']=='none' else '1') and (row['supports']!='none' or max_width<=10)
        segments=paths(job/'plate_1.gcode')
        extrusion=np.array([p[:,:2] for z,f,p in segments if f!='Custom'])
        lo=extrusion.min(axis=(0,1));hi=extrusion.max(axis=(0,1))
        # Allow 0.25 mm for bead half-width; include support and brim, excluding
        # the printer's own purge/start routine. Test the X1C exclusion too.
        from shapely.geometry import LineString,box
        candidates=extrusion[(extrusion.min(axis=1)[:,0]<18.25)&(extrusion.min(axis=1)[:,1]<28.25)]
        exclusion_hits=sum(LineString(x).intersects(box(0,0,18.25,28.25)) for x in candidates)
        rec.update(extrusion_bounds_xy_mm=[lo.tolist(),hi.tolist()],exclusion_hits=int(exclusion_hits),actual_toolpaths_in_bed=bool(np.all(lo>=0.25) and np.all(hi<=255.75) and exclusion_hits==0))
        rec['passed']=bool(rec['passed'] and rec['actual_toolpaths_in_bed'])
        audit.append(rec)
        if stem not in ['parent_oneplate_bar','parent_oneplate_frame','parent_oneplate_stand','parent_oneplate_camera_qr_female','parent_oneplate_camera_qr_male']:continue
        layers=sorted({x[0] for x in segments if x[1]=='Outer wall'})
        bridge={z:sum(1 for zz,f,p in segments if zz==z and 'bridge' in f.lower()) for z in layers}
        selected=[layers[0],max(layers,key=lambda z:bridge[z]) if max(bridge.values()) else layers[len(layers)//2]]
        for z in selected:panels.append((stem,z,[(f,p) for zz,f,p in segments if zz==z]))
    fig,axes=plt.subplots(len(panels)//2,2,figsize=(12,4.25*len(panels)//2))
    for ax,(stem,z,segments) in zip(axes.flat,panels):
        for kind,color in [('part','#247895'),('bridge','#d88714'),('support','#b33d59')]:
            selected=[p[:,:2] for f,p in segments if ('support' if f.startswith('Support') else 'bridge' if 'bridge' in f.lower() else 'part')==kind]
            if selected:ax.add_collection(LineCollection(selected,colors=color,linewidths=.45))
        ax.autoscale();ax.set_aspect('equal');ax.set_title(stem.replace('parent_oneplate_','')+f' / Z={z:g} mm');ax.set_xlabel('bed X / mm');ax.set_ylabel('bed Y / mm')
    fig.suptitle('Actual G-code: first layer and bridge/detail layer\nBlue: part; amber: bridge; red: support',fontsize=14);fig.tight_layout(rect=[0,0,1,.96])
    fig.savefig(A/'_work/images'/(image_name+'.png'),dpi=150);plt.close(fig)
    result=dict(passed=all(r['passed'] for r in audit),parts=audit,limits=['Projected downward-face width is a screening metric, not a physical bridge qualification.','G2/G3 extrusion is drawn as endpoint chords in the review plot.','Physical adhesion, bridge quality and support removal remain first-print checks.'])
    (A/'_work/analysis'/analysis_name/'slice_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1
if __name__=='__main__':sys.exit(main())
