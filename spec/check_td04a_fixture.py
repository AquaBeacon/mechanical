"""Check the actual L bracket mesh, holes, hardware and corrected orientation.

No physical fit or load rating is inferred from hypothetical bracket gauges.
Run from any directory after rebuilding the bracket and print pack.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sys

import numpy as np
import trimesh as tm

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/td04a_fixture'
OUT=A/'_work/analysis'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def matrix(ops):
    result=np.eye(4)
    for op in ops:
        for kind,v in op.items():
            if kind=='translate': m=tm.transformations.translation_matrix(v)
            elif kind=='rotate': m=tm.transformations.euler_matrix(*np.radians(v))
            elif kind=='scale': m=np.diag([*v,1])
            elif kind=='mirror':
                n=np.array(v,dtype=float);n/=np.linalg.norm(n);m=np.eye(4);m[:3,:3]-=2*np.outer(n,n)
            else: raise ValueError(kind)
            result=result@m
    return result
def box(size,center):
    m=tm.creation.box(size);m.apply_translation(center);return m
def overlap(a,b):
    if np.any(np.minimum(a.bounds[1],b.bounds[1])-np.maximum(a.bounds[0],b.bounds[0])<=1e-6):return 0.
    result=tm.boolean.intersection([a,b],engine='manifold')
    return abs(float(result.volume)) if len(result.faces) else 0.
def moved(m,ops):
    m=m.copy();m.apply_transform(matrix(ops));return m

def main():
    import re
    OUT.mkdir(parents=True,exist_ok=True)
    data=json.loads((A/'placement.json').read_text(encoding='utf-8'))
    part=ROOT/'parts/common/exterior/printed/td04a_bracket_mount'
    source=(part/'td04a_bracket_mount.scad').read_text(encoding='utf-8')
    def dim(key):return float(re.search(r'^'+key+r'=([0-9.]+);',source,re.M).group(1))
    checks=[];sources={};meshes={}
    def check(name,ok,**e):checks.append(dict(name=name,passed=bool(ok),**e))
    for row in data['items']:
        path=ROOT/row['part']/(row['file']+'.stl');m=moved(tm.load_mesh(path),row['ops']);meshes[row['label']]=m
        sources[path.relative_to(ROOT).as_posix()]=digest(path)
        check('closed_mesh:'+row['label'],m.is_volume and m.is_watertight and len(m.split())==1)
    t=dim('wall');pitch=data['confirmed_interface']['hole_center_pitch_mm'];variant_results=[]
    def cylinder(axis,c,r,h):
        m=tm.creation.cylinder(radius=r,height=h,sections=48)
        if axis=='Y':m.apply_transform(tm.transformations.euler_matrix(np.pi/2,0,0))
        elif axis=='X':m.apply_transform(tm.transformations.euler_matrix(0,np.pi/2,0))
        m.apply_translation(c);return m
    for v in data['fixture_variants']:
        unit=v['unit'];sgn=v['broad_face_normal'][2];origin=np.array(v['origin_mm'])
        local={}
        for name,m in meshes.items():
            if name.startswith(unit+'_'):
                local[name]=m.copy();local[name].apply_translation(-origin)
        bracket=local[unit+'_strap'];z=sgn*dim('sensor_offset');child=unit=='child';cx=dim('child_sensor_x') if child else 0
        check(unit+':outer_dimensions',np.allclose(bracket.extents,[dim('child_reach'),dim('child_side_depth'),dim('strap_length')] if child else [dim('bracket_width'),dim('foot_depth'),dim('strap_length')],atol=.01),bounds_mm=bracket.bounds.tolist(),volume_mm3=float(bracket.volume))
        def hole_centers(origin,normal,cols,d=4.5,roof=0):
            section=bracket.section(plane_origin=origin,plane_normal=normal);out=[]
            for loop in section.discrete:
                pts=loop[:,cols]
                if max(np.ptp(pts,axis=0))<7:
                    center=(pts.min(axis=0)+pts.max(axis=0))/2;center[roof]=pts[:,roof].min()+d/2;out.append(center.tolist())
            return sorted(out)
        sensor=hole_centers([0,t/2,0],[0,1,0],[0,2],roof=1 if child else 0)
        foot=hole_centers([t/2,0,0],[1,0,0],[1,2],d=3.5,roof=1) if child else hole_centers([0,0,sgn*t/2],[0,0,1],[0,1],d=dim('exterior_hole_d'))
        check(unit+':sensor_holes',np.shape(sensor)==(2,2) and np.allclose(sensor,[[cx-pitch/2,z],[cx+pitch/2,z]],atol=.01),centers_xz_mm=sensor)
        foot_xy=[[dim('child_hole_y'),dim('child_first_z')],[dim('child_hole_y'),dim('child_first_z')+v['side_attachment']['pitch_mm']]] if child else [[0,dim('exterior_first_y')],[0,dim('exterior_first_y')+dim('exterior_hole_pitch')]]
        check(unit+':exterior_holes',np.shape(foot)==(2,2) and np.allclose(foot,foot_xy,atol=.01),centers_xy_mm=foot,status='provisional exterior interface')
        front=(np.abs(bracket.triangles_center[:,1])<.001)&(bracket.face_normals[:,1]<-.999)
        contact=((np.abs(bracket.triangles_center[:,0])<.001)&(bracket.face_normals[:,0]<-.999)) if child else ((np.abs(bracket.triangles_center[:,2])<.001)&(bracket.face_normals[:,2]*sgn<-.999))
        check(unit+':actual_orthogonal_planes',bracket.area_faces[front].sum()>600 and bracket.area_faces[contact].sum()>500)
        broad=np.array(v['broad_face_normal']);baseline=np.array(data['confirmed_interface']['hole_baseline']);fix=np.array(data['confirmed_interface']['fixing_plane_normal'])
        ref=v['reference_body'];bz=ref['broad_face_z_mm']
        check(unit+':sensor_faces_requested_direction',sgn==(-1 if unit=='parent' else 1) and abs(broad@baseline)<1e-8 and abs(broad@fix)<1e-8 and (bz-z)*sgn>0 and (0-z)*sgn<0 and abs(z-v['sensor_hole_z_mm'])<.001,broad_face_normal=broad.tolist(),hole_z_mm=z,broad_face_reference_z_mm=bz,exterior_contact_z_mm=0)
        clashes=[]
        for (la,ma),(lb,mb) in itertools.combinations(local.items(),2):
            vol=overlap(ma,mb)
            if vol>.05:clashes.append(dict(a=la,b=lb,volume_mm3=vol))
        check(unit+':hardware_interferences',not clashes,clashes=clashes)
        for x in [cx-pitch/2,cx+pitch/2]:
            check(unit+':M4_clearance:'+str(x),overlap(bracket,cylinder('Y',[x,t/2,z],2.24,t+.02))<.001)
            socket=cylinder('Y',[x,-33.85,z],5.5,60)
            socket=tm.boolean.difference([socket,cylinder('Y',[x,-33.85,z],4.2,60.2)],engine='manifold')
            for tag,tool in [('rear_driver_d8',cylinder('Y',[x,39.9,z],4,60)),('front_socket_od11',socket)]:
                vol=sum(overlap(tool,m) for m in local.values())
                check(unit+':'+tag+':'+str(x),vol<.001,intersection_mm3=vol)
        if child:
            target=v['side_attachment'];case=json.loads((ROOT/target['target_assembly']).read_text(encoding='utf-8'))
            sources[target['target_assembly']]=digest(ROOT/target['target_assembly'])
            row=next(r for r in case['items'] if r['label']==target['frame_label'])
            frame=moved(tm.load_mesh(ROOT/row['part']/(row['file']+'.stl')),row['ops']);frame.apply_translation(-np.array(target['target_origin_mm']))
            check('child:side_face_contact',abs(frame.bounds[1,0])<.001 and abs(bracket.bounds[0,0])<.001)
            check('child:frame_fit',sum(overlap(frame,m) for m in local.values())<.05)
            for y,zz in foot_xy:
                bore=cylinder('X',[-3.5,y,zz],1.74,17.1)
                check('child:existing_M3_hole:'+str(zz),overlap(frame,bore)+overlap(bracket,bore)<.001)
                tool=cylinder('X',[39.1,y,zz],4,60)
                check('child:side_driver:'+str(zz),sum(overlap(tool,m) for m in [frame,*local.values()])<.001)
                nut=local[f'child_side_nut_{int(zz)}'];worst=0.
                for travel in [0,2,4,8]:
                    n=nut.copy();n.apply_translation([-travel,0,0]);worst=max(worst,overlap(frame,n))
                check('child:existing_nut_pocket:'+str(zz),worst<.001,max_intersection_mm3=worst)
            # Review the bracket and its six side fasteners against available case meshes.
            clashes=[];missing=[];cache={};new=[m for key,m in local.items() if key=='child_strap' or key.startswith('child_side_')]
            for row in case['items']:
                # The current exterior now includes this very fixture. Compare
                # against the other components, not a second copy of itself.
                if row['label'].startswith('td04a_r6_'):
                    continue
                path=ROOT/row['part']/(row.get('file',Path(row['part']).name)+'.stl')
                if not path.exists():missing.append(str(path.relative_to(ROOT)));continue
                if path not in cache:
                    cache[path]=tm.load_mesh(path);sources[path.relative_to(ROOT).as_posix()]=digest(path)
                m=moved(cache[path],row['ops']);m.apply_translation(-np.array(target['target_origin_mm']))
                vol=sum(overlap(m,n) for n in new)
                if vol>.05:clashes.append(dict(label=row['label'],intersection_mm3=vol))
            check('child:case_installation_review',not clashes and not missing,clashes=clashes,missing=missing,target_origin_mm=target['target_origin_mm'])
        else:
            for _,y in foot_xy:
                check(unit+':foot_M4_clearance:'+str(y),overlap(bracket,cylinder('Z',[0,y,sgn*t/2],2.74,t+.02))<.001)
                check(unit+':foot_driver_d8:'+str(y),overlap(bracket,cylinder('Z',[0,y,sgn*39.1],4,60))<.001)
        meta=json.loads((part/'manufacturing.json').read_text(encoding='utf-8'));rot=meta['print_rotations_deg'][v['stem']]
        check(unit+':roof_direction',np.allclose(matrix([dict(rotate=rot)])[:3,:3]@([0,0,1] if child else [1,0,0]),[0,0,1],atol=1e-8))
        reservation=v['cable_reservation']; lo,hi=reservation['z_range_mm']; y0,y1=reservation['y_range_mm']
        space=box([reservation['width_mm'],y1-y0,hi-lo],[reservation['x_center_mm'],(y0+y1)/2,(lo+hi)/2])
        check(unit+':60mm_cable_reservation',abs(hi-lo-60)<1e-9 and sum(overlap(space,m) for m in local.values())<.001,scope='illustrative width/depth; actual cable and body unmeasured')
        variant_results.append(dict(unit=unit,stem=v['stem'],sensor_hole_centers_xz_mm=sensor,exterior_hole_centers_mm=foot,exterior_hole_plane='YZ' if child else 'XY',broad_face_normal=broad.tolist()))
    accepted=json.loads((OUT/'parent_accepted_hashes.json').read_text(encoding='utf-8'))
    check('legacy_parent_bytes_preserved_only_when_requested',not data.get('preserve_parent_accepted_bytes', False) or all(digest(part/('td04a_bracket_mount_parent_down.'+ext))==sha for ext,sha in accepted.items()))
    check('different_variant_files',len({v['stem'] for v in data['fixture_variants']})==2)
    result=dict(passed=all(c['passed'] for c in checks),revision=data['revision'],sources_sha256=sources,checks=checks,variants=variant_results,limits=['Sensor body is an orientation reference only; its dimensions and cable boot are unmeasured','Exterior attachment pattern and placements remain provisional','No physical print, strength or creep validation'])
    (OUT/'geometry_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[c for c in checks if not c['passed']]),indent=2))
    return 0 if result['passed'] else 1
if __name__=='__main__':sys.exit(main())
