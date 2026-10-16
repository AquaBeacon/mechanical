"""Check the actual top-frame openings and full clamp-driver approach."""
from pathlib import Path
import hashlib, json
import numpy as np
import trimesh
from shapely.geometry import Point, Polygon
from prepare_child_horizontal_plate_frame import ROOT, OUT, PART, load_world, overlap, save, printed_baseline


def main():
    p=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    world=load_world(p);by_name={r['label']:(r,m) for r,m in world}
    top_row,top=by_name['removable_upper_frame'];settings=p['top_clamp_access']
    joints=[j for j in p['fastener_joints'] if j['label'].startswith('clamp_join_')]
    failures=[];holes=[];tools=[]
    if len(joints)!=6 or not top.is_volume or len(top.split())!=1 or np.count_nonzero(top.area_faces<1e-12):
        failures.append(dict(kind='top_mesh_or_screw_count',count=len(joints)))
    centres=[j['seat_mm'][:2] for j in joints]
    if centres!=settings['hole_centres_xy_mm']:
        failures.append(dict(kind='placement_hole_centres'))
    # Inspect the real mid-plane bore, plus the two chamfered entrances. The
    # nearest other contour includes the frame edge and all neighbouring holes.
    bottom=top.bounds[0,2];thickness=p['dimensions_mm']['top_thickness']
    sections={}
    for z in (bottom+.001,bottom+thickness/2,bottom+thickness-.001):
        section=top.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
        loops=[] if section is None else [Polygon(loop[:,:2]).simplify(1e-4) for loop in section.discrete]
        sections[z]=loops
        for j in joints:
            centre=Point(j['seat_mm'][:2]);candidates=[poly for poly in loops if poly.covers(centre)]
            bore=min(candidates,key=lambda poly:poly.area) if candidates else None
            if bore is None:
                failures.append(dict(kind='missing_service_bore',screw=j['label'],z_mm=z));continue
            width=2*bore.exterior.distance(centre)
            ligament=min(bore.exterior.distance(poly.exterior) for poly in loops if poly is not bore)
            row=dict(screw=j['label'],centre_xy_mm=j['seat_mm'][:2],z_mm=z,
                inscribed_diameter_mm=width,sides=len(bore.exterior.coords)-1,
                nearest_contour_ligament_mm=ligament)
            holes.append(row)
            if ligament<3:
                failures.append(dict(kind='service_bore_ligament',**row))
            if abs(z-bottom-thickness/2)<1e-4:
                if abs(width-settings['bore_inscribed_diameter_mm'])>.001 or row['sides']!=settings['bore_sides']:
                    failures.append(dict(kind='service_bore_throat',**row))
            elif width<settings['bore_inscribed_diameter_mm']+.5:
                failures.append(dict(kind='missing_entrance_chamfer',**row))
    for j in joints:
        seat=np.array(j['seat_mm']);screw=by_name[j['label']+'_screw'][1]
        head_top=float(screw.bounds[1,2]);length=settings['driver_length_mm']
        tool=trimesh.creation.cylinder(radius=settings['driver_diameter_mm']/2,height=length,sections=64)
        tool.apply_translation([seat[0],seat[1],head_top+.2+length/2])
        blocked=[dict(part=r['label'],volume_mm3=overlap(tool,m)) for r,m in world
                 if r['label']!=j['label']+'_screw']
        blocked=[row for row in blocked if row['volume_mm3']>.1]
        # The shaft must clear the entire top, with handle space above the plate.
        free_above=tool.bounds[1,2]-(bottom+thickness)
        row=dict(screw=j['label'],driver_diameter_mm=settings['driver_diameter_mm'],
            driver_length_mm=length,bounds_mm=tool.bounds.tolist(),above_plate_mm=free_above,blocked=blocked)
        tools.append(row)
        if blocked or free_above<10:
            failures.append(dict(kind='driver_approach',**row))
    # The old top is kept as a historical geometry reference. The new cuts
    # must not alter any of the eight clamp mounting axes or their bearing area.
    old_path=OUT/'_work/intermediate/history/before_top_clamp_access'/PART.relative_to(ROOT)/'child_horizontal_plate_frame_top.stl'
    old=trimesh.load(old_path,force='mesh')
    old.apply_translation([0,0,bottom])
    bearing=[]
    for j in p['fastener_joints']:
        if not j['label'].startswith('mount_upper_'):continue
        x,y=j['seat_mm'][:2]
        probe=trimesh.creation.cylinder(radius=3.5,height=thickness,sections=64)
        probe.apply_translation([x,y,bottom+thickness/2])
        a=overlap(old,probe);b=overlap(top,probe)
        bearing.append(dict(screw=j['label'],previous_material_mm3=a,current_material_mm3=b))
        if abs(a-b)>.001:
            failures.append(dict(kind='existing_mount_bearing_changed',**bearing[-1]))
    result=dict(result='FAIL' if failures else 'PASS',service_screws=len(joints),
        bore_sections=holes,driver_approaches=tools,mount_bearing=bearing,
        minimum_ligament_mm=min(row['nearest_contour_ligament_mm'] for row in holes),
        top_bounds_mm=top.bounds.tolist(),top_volume_mm3=float(top.volume),
        watertight=bool(top.is_volume),zero_area_faces=int(np.count_nonzero(top.area_faces<1e-12)),
        printed_stock_sha256=printed_baseline(),failures=failures,
        input_sha256={f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in
            [OUT/'placement.json',Path(__file__).resolve(),PART/'child_horizontal_plate_frame.scad',old_path,
             PART/'child_horizontal_plate_frame_top.stl']},
        limitations=['8 mm x 70 mm driver envelope is a provisional existing tool assumption; confirm the actual tool',
                    'Rigid CAD and section measurements only; no PETG load qualification'])
    save(OUT/'_work/analysis/top_clamp_access/validation.json',result)
    # Actual mid-plane mesh contours and actual screw axes, not a drawn CAD substitute.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.family']='Yu Gothic'
    fig,ax=plt.subplots(figsize=(9,9),facecolor='#f4f3ef')
    for poly in sections[bottom+thickness/2]:
        coords=np.array(poly.exterior.coords);ax.plot(coords[:,0],coords[:,1],color='#407a91',lw=1)
    for index,j in enumerate(joints,1):
        x,y=j['seat_mm'][:2]
        ax.add_patch(plt.Circle((x,y),settings['driver_diameter_mm']/2,color='#df9844',alpha=.65))
        ax.text(x+8,y,f'{index}',va='center',color='#805826')
    ax.set_aspect('equal');ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.grid(alpha=.15)
    ax.set_title('トップフレーム：クランプ締付ねじ6本の真上にφ10工具穴\n橙：φ8工具軸、穴の縁は0.4 mm面取り',fontsize=13)
    fig.tight_layout();dest=OUT/'_work/images/top_clamp_access.png'
    dest.parent.mkdir(parents=True,exist_ok=True);fig.savefig(dest,dpi=150);plt.close(fig)
    print(json.dumps(dict(result=result['result'],holes=len(joints),minimum_ligament_mm=result['minimum_ligament_mm'],failures=failures),ensure_ascii=False))
    if failures:raise RuntimeError('Top clamp access failed')


if __name__=='__main__':main()
