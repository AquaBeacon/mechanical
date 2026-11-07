"""Slice and review the single replacement Sony plate with existing X1C profiles."""
from pathlib import Path
import json,sys,subprocess,datetime,hashlib,zipfile
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from slice_parent_spacers import paths
R=Path(__file__).resolve().parents[1];A=R/'assemblies/parent_hand_service'
W=A/'_work/analysis/sony_plate_thickening_20261024/slicing'
J=A/'print_jobs/sony_plate_thickening_20261024'
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    W.mkdir(parents=True,exist_ok=True);J.mkdir(parents=True,exist_ok=True)
    old=A/'_work/analysis/spacer_delivery_20261022'
    for name in ['machine','process','filament']:
        d=json.loads((old/(name+'.json')).read_text(encoding='utf-8'))
        if name=='process':d.update(print_settings_id='Sony 3.2mm plate PETG wall4 solid',brim_width='3')
        write(W/(name+'.json'),d)
    source=A/'parts/sony_mount_plate.stl';mesh=trimesh.load_mesh(source)
    mesh.apply_translation([128-mesh.bounds[:,0].mean(),128-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
    staged=W/'sony_plate_placed.stl';mesh.export(staged)
    cmd=['C:/Program Files/Bambu Studio/bambu-studio.exe','--debug','2','--datadir',str(W/'studio_data'),
         '--load-settings',str(W/'machine.json')+';'+str(W/'process.json'),'--load-filaments',str(W/'filament.json'),
         '--arrange','0','--orient','0','--slice','0','--export-3mf','sony_mount_plate.3mf','--outputdir',str(J),str(staged)]
    p=subprocess.Popen(cmd,cwd=J,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',creationflags=0x08000000)
    rec=dict(pid=p.pid,start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),owner='sony_plate_thickening',purpose='single plate slicing',command=cmd)
    write(W/'process_record.json',rec)
    try:out,_=p.communicate(timeout=120)
    except subprocess.TimeoutExpired:p.terminate();p.communicate(timeout=10);raise
    rec['exit_code']=p.returncode;write(W/'process_record.json',rec);(W/'slice.log').write_text(out,encoding='utf-8');assert p.returncode==0,out[-1500:]
    result=json.loads((J/'result.json').read_text(encoding='utf-8'));assert result['return_code']==0
    project=J/'sony_mount_plate.3mf'
    with zipfile.ZipFile(project) as z:
        assert z.testzip() is None
        (W/'plate_1.gcode').write_bytes(z.read('Metadata/plate_1.gcode'))
    segments=paths(W/'plate_1.gcode');walls=sorted({z for z,f,p in segments if f=='Outer wall'})
    supports=[(z,f,p) for z,f,p in segments if f.lower().startswith('support')]
    assert min(walls)==.2 and max(walls)>=6.4
    fig,axes=plt.subplots(2,2,figsize=(10,9))
    for ax,target in zip(axes.flat,[.2,.8,3.2,6.6]):
        layer=min(walls,key=lambda x:abs(x-target))
        for support,color in [(False,'#246d85'),(True,'#e07a32')]:
            lines=[p[:,:2] for z,f,p in segments if abs(z-layer)<.001 and f.lower().startswith('support')==support and f!='Custom']
            if lines:ax.add_collection(LineCollection(lines,colors=color,linewidths=.6))
        ax.set(xlim=(90,166),ylim=(80,176),aspect='equal',title='Z '+str(layer)+' mm')
    fig.tight_layout();fig.savefig(A/'_work/images/sony_plate_thickened_toolpaths.png',dpi=140);plt.close(fig)
    plate=result['sliced_plates'][0]
    record=dict(passed=True,source_stl_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),three_mf_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),
                material='Generic PETG',printer='X1 Carbon 0.4mm',layer_mm=.2,walls=4,infill_percent=100,support_detection='normal(auto),45deg,all surfaces,bridge exemption disabled',
                support_extrusion_moves=len(supports),filament_g=sum(f['total_used_g'] for f in plate['filaments']),prediction_seconds=plate['total_predication'],
                model_top_layer_mm=max(walls),warnings=plate.get('warning_message',''))
    write(J/'manifest.json',record);print(json.dumps(record))
if __name__=='__main__':main()
