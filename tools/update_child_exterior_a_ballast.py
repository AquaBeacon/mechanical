"""A-mounted symmetric ballast and hinge-side transducer concept migration."""
import json
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept'
PART=ROOT/'parts/child/exterior/printed/child_exterior_open_frame'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    hist=OUT/'_work/intermediate/before_a_ballast'
    hist.mkdir(parents=True,exist_ok=True)
    for src in [OUT/'placement.json',OUT/'child_exterior_concept.blend',OUT/'README.md',PART/'concept.json']:
        if not (hist/src.name).exists(): shutil.copy2(src,hist/src.name)
    p,c=read(hist/'placement.json'),read(hist/'concept.json')
    p['items']=[r for r in p['items'] if r['group']!='Frame B']
    c['variants'].pop('frame_b_bottom',None)
    # One right-hand source, left instance rotated 180 degrees: paired mass and geometry.
    c['variants']['ballast_c_a_cradle']={
        'kind':'composite','boxes':[
            {'size_mm':[8,100,152],'center_mm':[4,0,-36]},
            {'size_mm':[66.5,60,8],'center_mm':[33.25,0,-109]}],
        'rings':[{'center_mm':[33.25,0,z],'outer_radius_mm':28.5,'inner_radius_mm':24.75,'height_mm':10} for z in [-94,-63]],
        'note':'Visual cup and two retaining bands. Fastening, liners and strength not fabrication-approved.'}
    c['variants']['ballast_b_a_backing']={'kind':'bar','size_mm':[6,24,184],'bevel_mm':1}
    for r in p['items']:
        if r['group']=='Ballast C':
            sign=-1 if r['label'].endswith('left') else 1
            r['ops']=[{'translate':[sign*130.6,0,-105]}]
            r['mass_g']=1000
        if r['group']=='Ballast B':
            index=int(r['label'].split('_')[-1])-1
            sign=-1 if index<2 else 1
            y=-76 if index%2==0 else 76
            r['ops']=[{'translate':[sign*103.35,y,-10]},{'rotate':[0,sign*90,0]}]
            r['mass_g']=60
        if r['label']=='transducer_inside_c':
            r['ops']=[{'translate':[40,-118,220]},{'rotate':[180,0,180]}]
        if r['label']=='transducer_inner_mount':
            r['ops']=[{'translate':[54,-123,149]}]
    for sign in [-1,1]:
        p['items'].append(dict(label=f'ballast_C_A_cradle_{sign}',part='parts/child/exterior/printed/child_exterior_open_frame',
            file='ballast_c_a_cradle',group='Ballast support',geometry='concept',material='frame_a',print=False,
            ops=[{'translate':[sign*97.35,0,0]},{'rotate':[0,0,0 if sign>0 else 180]}],explode_mm=[sign*120,0,0]))
        for y in [-76,76]:
            p['items'].append(dict(label=f'ballast_B_backing_{sign}_{y}',part='parts/child/exterior/printed/child_exterior_open_frame',
                file='ballast_b_a_backing',group='Ballast support',geometry='concept',material='frame_a',print=False,
                ops=[{'translate':[sign*100.35,y,-10]}],explode_mm=[sign*120,0,0]))
    p['ballast_mount']={'type':'paired_outboard_A_cradles','c_centers_xy_mm':[[-130.6,0],[130.6,0]],
        'c_bottom_z_mm':-105,'declared_total_mass_g':2240,'frame_mount_holes_yz_mm':[[y,z] for y in [-42,42,-76,76] for z in [-100,40]],
        'note':'Equal 1000 g per side, equal height. Each side also carries 2 x 60 g plates. Whole-vehicle CG/CB not yet known.'}
    p['revision']='No bottom B; equal low A-mounted ballast; transducer on fixed hinge side'
    p['notes']=[n for n in p['notes'] if 'ballast' not in n.lower() and 'bottom plate' not in n.lower()]
    p['notes'].append('Frame B removed. Ballast attached symmetrically to A; only guard moves. Transducer moved to fixed -Y hinge side.')
    write(OUT/'placement.json',p);write(PART/'concept.json',c)
if __name__=='__main__': main()
