"""Inspect the new nut pocket in actual sliced paths, including local supports."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from slice_parent_frame_spacers import model_paths
R=Path(__file__).resolve().parents[1];A=R/'assemblies/parent_hand_service';W=A/'_work/analysis/frame_spacers_20261024'
def main():
    publication=json.loads((W/'publication.json').read_text(encoding='utf-8'))
    review=json.loads((W/'slicing/plate_2/review.json').read_text(encoding='utf-8'))
    member=next(e for e in review['members'] if e['name']=='gnss_sony_shared_column')
    shift=np.array(member['bounds'][0])-np.array(publication['exports']['gnss_sony_shared_column']['bounds_mm'][0])
    row=next(r for r in publication['hardware'] if r['label']=='sony_top_2')
    x,y=row['xy'];lo=np.array([x-4,y-4,row['nut_z']-.3])+shift;hi=lo+[8,12,3.3]
    segments=model_paths(W/'slicing/plate_2/plate_1.gcode');bad=[]
    for z,t,p in segments:
        if not t.lower().startswith('support'):continue
        mid=(p[:-1]+p[1:])/2
        if np.any(np.all(mid>lo+.05,axis=1)&np.all(mid<hi-.05,axis=1)):bad.append(dict(z=z,feature=t))
    assert not bad,bad
    center=np.array([x,y,0])+shift
    fig,axs=plt.subplots(2,2,figsize=(10,9))
    for ax,z in zip(axs.flat,[36.8,39.2,39.4,39.6]):
        for t,color in [('Outer wall','#245d78'),('Inner wall','#62a4bb'),('Overhang wall','#a65496'),('Bridge','#a65496'),('Internal solid infill','#4e9950'),('Gap infill','#4e9950'),('Support','#df8a35'),('Support interface','#df8a35')]:
            lines=[p[:,:2] for zz,tt,p in segments if abs(zz-z)<.001 and tt==t]
            if lines:ax.add_collection(LineCollection(lines,colors=color,linewidths=1))
        ax.add_patch(Rectangle((center[0]-2.9,center[1]),5.8,4.5,fill=False,color='#bd4137',linestyle='--'))
        ax.set(xlim=(center[0]-6,center[0]+6),ylim=(center[1]-7,center[1]+8),aspect='equal',title=f'Z {z} mm');ax.grid(alpha=.2)
    fig.suptitle('Shared-column nut entry and roof: actual extrusion paths\nDashed box = side entry; purple = overhang/bridge; orange = support')
    fig.tight_layout();fig.savefig(A/'_work/images/frame_spacers_nut_roof_toolpaths.png',dpi=150);plt.close(fig)
    record=dict(passed=True,support_extrusion_inside_nut_pocket=0,checked_print_box_mm=[lo.tolist(),hi.tolist()],note='Pocket roof toolpaths need visual review and a physical print; zero local supports is not proof of bridge quality.')
    (W/'nut_roof_path_checks.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps(record))
if __name__=='__main__':main()
