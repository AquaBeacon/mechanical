"""Publish the verified Sony plate and update its existing print delivery."""
from pathlib import Path
import json,shutil,sys
import trimesh
ROOT=Path(__file__).resolve().parents[1]
ASM=ROOT/'assemblies/parent_hand_service'
WORK=ASM/'_work/analysis/sony_plate_thickening_20261024'
PART=ROOT/'parts/parent/interior/printed/parent_hand_service'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    run=Path(sys.argv[1]);receipt=read(run/'report.json');assert receipt['status']=='passed'
    report=json.loads(next(x.removeprefix('SONY_REPORT=') for x in (run/'logs/freecad.log').read_text(encoding='utf-8').splitlines() if x.startswith('SONY_REPORT=')))
    assert report['passed'] and report['thickness_mm']==3.2
    for key,snapshot in read(run/'job.json')['snapshots'].items():
        import hashlib
        assert hashlib.sha256((ROOT/key).read_bytes()).hexdigest()==snapshot['sha256'],key
    mesh=trimesh.load_mesh(run/'sony_mount_plate.stl');assert mesh.is_watertight and mesh.is_winding_consistent
    text='// Generated from parent_corner_mounts.sony_shapes; rebuild with spec/build_parent_sony_plate.py through CadService.\n'
    text+='polyhedron(points='+json.dumps(mesh.vertices.tolist())+',faces='+json.dumps(mesh.faces[:,::-1].tolist())+',convexity=10);\n'
    (PART/'sony_mount_plate.scad').write_text(text,encoding='utf-8')
    for suffix in ['step','stl']:shutil.copyfile(run/('sony_mount_plate.'+suffix),PART/('sony_mount_plate.'+suffix))
    write(WORK/'geometry_checks.json',report)
    for file in ['placement.json','service_placement.json']:
        d=read(ASM/file)
        for row in d['items']:
            n=row['label']
            if n=='sony_mount_plate':row.update(print=True,note='3.2 mm reinforced plate; reprint one. Column joint Z60.5 unchanged; PCB lifted1.6 mm.')
            elif n=='spresense':row['ops'][0]['translate'][2]=67.2
            elif n.startswith('sony_mount_'):row['ops'][0]['translate'][2]=68.8
            elif n.startswith('retrofit_sony_top_') and n.endswith('_bolt'):row['ops'][0]['translate'][2]=63.7
        d['sony_plate_revision']=dict(date='2026-10-24',thickness_mm=3.2,pcb_lift_mm=1.6,column_joint_z_mm=60.5)
        write(ASM/file,d)
    config=read(ASM/'print_config.json')
    config.setdefault('notes',[]).append('assemblies/parent_hand_service/sony_plate_thickening_report.md') if 'assemblies/parent_hand_service/sony_plate_thickening_report.md' not in config.setdefault('notes',[]) else None
    config['note']='Sony固定板は厚3.2 mm版を1個再印刷。基板と基板ねじ座は1.6 mm上昇、支柱接合面は維持。'+config.get('note','')
    write(ASM/'print_config.json',config)
    metadata=read(PART/'manufacturing.json')
    dep='../../../../../spec/build_parent_sony_plate.py'
    if dep not in metadata['source_dependencies']:metadata['source_dependencies'].append(dep)
    write(PART/'manufacturing.json',metadata)
    print('Published verified Sony plate; render and sync next.')
if __name__=='__main__':main()
