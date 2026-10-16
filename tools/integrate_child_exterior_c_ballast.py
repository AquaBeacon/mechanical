"""Integrate the existing upper ballast supports into the concept C panels."""
import copy
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
PART=ROOT/'parts/child/exterior/printed/child_exterior_open_frame'

def main():
    p=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    c=json.loads((PART/'concept.json').read_text(encoding='utf-8'))
    if p['ballast_mount']['type']=='integrated_c_internal_ballast':
        print('Already integrated');return
    backup=OUT/'_work/intermediate/before_c_ballast_integration'
    backup.mkdir(parents=True,exist_ok=True)
    for source in [OUT/'placement.json',OUT/'README.md',OUT/'child_exterior_concept.blend',PART/'concept.json']:
        if not (backup/source.name).exists():shutil.copy2(source,backup/source.name)
    support=c['variants'].pop('ballast_upper_crossframe')
    boxes=copy.deepcopy(support['boxes'])
    # Close the former 0.5 mm seam by extending only the outside of the back.
    boxes[-1]['center_mm'][1]=161.5
    boxes[-1]['size_mm'][1]=10
    # Connect the lower mounting ears to the existing C side rails.
    boxes += [dict(center_mm=[x,166,64],size_mm=[8,8,28]) for x in [-81.35,81.35]]
    panel=c['variants']['frame_c']
    panel['add_boxes']=boxes
    panel['post_holes']=copy.deepcopy(support['post_holes'])
    for feature in panel['add_boxes']+panel['post_holes']:
        feature['center_mm'][1]-=170
        feature['center_mm'][2]-=166
    panel['note']='C panel, ballast seat, arms, back and A mounting ears form one connected union. Retaining bands remain removable.'
    c['variants']['ballast_retaining_bands']={'kind':'composite','rings':support['rings'],
        'note':'Separate metal band/collar concepts; removable to install the 1 kg weight.'}
    p['items']=[r for r in p['items'] if r['group']!='Ballast support']
    for r in p['items']:
        if r['label']=='C_rear':r['ops']=[{'translate':[0,-170,166]},{'rotate':[0,0,180]}]
    for sign in [-1,1]:
        p['items'].append(dict(label='ballast_bands_rear' if sign<0 else 'ballast_bands_front',
            part=PART.relative_to(ROOT).as_posix(),file='ballast_retaining_bands',geometry='concept',
            group='Ballast retainers',material='steel',print=False,
            ops=[{'rotate':[0,0,180 if sign<0 else 0]}],explode_mm=[0,sign*140,0]))
    p['ballast_mount']['type']='integrated_c_internal_ballast'
    p['ballast_mount']['integrated_support_labels']=['C_front','C_rear']
    p['ballast_mount']['note']='C and the lower weight support are one connected panel per face. A mounting holes and ballast positions retained; metal retaining collars separate. Strength unverified.'
    p['revision']='Purple C incorporates ballast support; A width, ballast positions, cable routing and guard-only movement retained'
    for path,data in [(OUT/'placement.json',p),(PART/'concept.json',c)]:
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
