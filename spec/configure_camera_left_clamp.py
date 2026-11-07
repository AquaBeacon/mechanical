"""Place the shared front-view-left 25 mm clamp; retain the existing C pose."""
from pathlib import Path
from copy import deepcopy
import json

ROOT=Path(__file__).resolve().parents[1]
PART='parts/child/exterior/printed/dji_osmo_action6_mount_m3'
SCREWS='parts/common/interior/cots/screw'

def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    for name,prefix,group in [('parent_exterior','camera_','camera'),
                              ('child_horizontal_plate_frame','side_camera_','child_camera')]:
        folder=ROOT/'assemblies'/name
        p=json.loads((folder/'placement.json').read_text(encoding='utf-8'))
        mount=next(r for r in p['items'] if r['label']==prefix+'mount')
        pose=deepcopy(mount['ops'])
        p['items']=[r for r in p['items'] if r.get('revision_owner')!='left_clamp_20261025']
        case=next(r for r in p['items'] if r['label']==prefix+'case_reference')
        case.update(part=PART,file='camera_case_41mm',ops=deepcopy(pose),print=False,
                    note='Depth 41 mm measured; case rear is aligned to original backplate -23.45. Actual M5-axis offset remains unmeasured.')
        mount['note']='25 mm clamp shifted 17 mm right from front-view left edge; rear lower 20 mm keepout; 41 mm measured case thickness. Physical fit pending.'
        def row(suffix,part,file,ops,printed,color):
            p['items'].append(dict(label=prefix+suffix,part=part,file=file,ops=ops,
                group='accessories' if printed else 'fasteners',print=printed,color=color,
                owner='camera_twist_accessory',revision_owner='left_clamp_20261025',removal_group=group))
        row('front_clamp',PART,'camera_front_clamp',deepcopy(pose),True,'Orange')
        for i,x in enumerate([11.5,24.5]):
            for kind,stem,z in [('screw','screw_m4x16_socket',4),
                                 ('washer','screw_washer_m4_08',4),('nut','screw_nut_m4',10.6)]:
                ops=deepcopy(pose)+[{'translate':[x,11.5,z]}]
                if kind=='screw':ops.append({'rotate':[180,0,0]})
                if kind=='nut':ops.append({'rotate':[0,0,30]})
                row(f'clamp_{i}_{kind}',SCREWS,stem,ops,False,'Silver')
        p['camera_twist_mount'].update(front_rotation_stop_removed=False,
            left_clamp_revision='clamp_right5_20261029',rear_projecting_pad_removed=True,case_rear_datum_mm=-23.45,measured_case_depth_mm=41,
            former_bottom_supports_removed=True,clamp_foot_direction='inward',clamp_screws_insert_from='below',
            front_view_left_width_mm=25,front_view_right_shift_mm=17,clamp_x_range_mm=[5.5,30.5],M5_finger_gap_mm=None,front_jaw_adjustment_mm=[0,3],
            physical_rotation_hold_status='new_clamp_not_yet_physically_tested',
            previous_revision_test='rear_clearance_20261024: user reported insufficient rotation hold',
            interface_limits='Case depth confirmed; width/height and M5-axis offset remain provisional.')
        p['camera_twist_mount'].pop('pending_revision',None)
        save(folder/'placement.json',p)
    meta_path=ROOT/PART/'manufacturing.json'
    meta=json.loads(meta_path.read_text(encoding='utf-8'))
    meta['print_rotations_deg']['camera_front_clamp']=[0,0,0]
    meta['layer_heights_mm']['camera_front_clamp']=.1
    meta['support_modes']['camera_front_clamp']='auto'
    if 'camera_case_41mm' not in meta['non_print_files']:meta['non_print_files'].append('camera_case_41mm')
    save(meta_path,meta)

if __name__=='__main__':main()
