"""Real exterior mesh interference and axial nut retention for Rev.6."""
from pathlib import Path
import json
import numpy as np
import trimesh as tm
from check_td04a_fixture import moved, overlap, box

ROOT = Path(__file__).resolve().parents[1]

def main():
    checks=[]
    def check(name, ok, **e): checks.append(dict(name=name, passed=bool(ok), **e))
    for unit, name in [('parent','parent_exterior'),('child','child_horizontal_plate_frame')]:
        data=json.loads((ROOT/'assemblies'/name/'placement.json').read_text(encoding='utf8'))
        meshes={}; cache={}
        for row in data['items']:
            p=ROOT/row['part']/(row.get('file',Path(row['part']).name)+'.stl')
            if not p.exists():
                check(name+':source_exists:'+row['label'],False,path=str(p)); continue
            if p not in cache: cache[p]=tm.load_mesh(p)
            meshes[row['label']]=moved(cache[p],row['ops'])
        fixture={k:v for k,v in meshes.items() if k.startswith('td04a_r6_')}
        clashes=[]
        for label,mesh in fixture.items():
            for other,solid in meshes.items():
                if other in fixture: continue
                v=overlap(mesh,solid)
                if v>.05: clashes.append(dict(a=label,b=other,volume_mm3=v))
        check(name+':fixture_vs_exterior',not clashes,clashes=clashes)
        if unit=='parent':
            # Nominal region from hole line z=-85 to flange underside z=-25.
            region=box([15,12,60],[35.5,-55,-55])
            reactions=[('carrier_nut_65','td04a_r6_parent_strap',[0,0,1]),('carrier_nut_85','td04a_r6_parent_strap',[0,0,1])]
        else:
            region=box([12,15,60],[154,-91.5,143])
            reactions=[('td04a_r6_child_side_nut_'+str(z),'right_side_frame',[1,0,0]) for z in [12,32]]
        intrusion=[dict(label=k,volume_mm3=v) for k,m in meshes.items() if (v:=overlap(region,m))>.05]
        check(name+':60mm_illustrative_cable_region',not intrusion,intrusions=intrusion,limits='Width/depth illustrative; sensor/cable root absent and unverified')
        for nut_name,face_name,direction in reactions:
            nut=meshes[nut_name];face=meshes[face_name];offset=np.array(direction)*2
            translated=nut.copy();translated.apply_translation(offset)
            sweep=tm.convex.convex_hull(np.vstack([nut.vertices,translated.vertices]))
            seated=overlap(nut,face); swept=overlap(sweep,face); end=overlap(translated,face)
            check(name+':axial_retention:'+nut_name,seated<.05 and swept>.5 and end>.5,
                  direction=direction,travel_mm=2,seated_overlap_mm3=seated,swept_overlap_mm3=swept,end_overlap_mm3=end,
                  reaction=face_name,scope='Continuous convex nut sweep proves geometric stop; no load rating')
        del meshes,cache,fixture
    out=ROOT/'assemblies/td04a_fixture/_work/analysis/cable_clearance_r6/exterior_checks.json'
    result=dict(passed=all(c['passed'] for c in checks),checks=checks,limits=['Sensor ear thickness 3 mm assumed; M4 nut bears on real sensor ear, which is not modeled','Exact hole pitch, body, cable root, bend radius, physical tightening and strength unverified'])
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1

if __name__=='__main__': raise SystemExit(main())
