"""Generate the photo-metal-replacement views from authoritative placement.json."""
from pathlib import Path
import json, os, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/td04a_fixture'
OPENSCAD=Path(os.environ.get('OPENSCAD',r'C:\Program Files\OpenSCAD\openscad.exe'))

def main():
    import trimesh as tm
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from check_td04a_fixture import moved, matrix
    data=json.loads((A/'placement.json').read_text(encoding='utf-8'))
    view=A/'td04a_fixture_view.scad'
    subprocess.run([sys.executable,str(ROOT/'scad/lib/asm_gen.py'),str(A/'placement.json'),str(view)],check=True)
    lines=['\n// View-only sensor/exterior SCHEMATICS, not measured fit models or print parts.']
    for v in data['fixture_variants']:
        s=v['broad_face_normal'][2];cx=v['origin_mm'][0];r=v['reference_body'];hz=v['sensor_hole_z_mm'];bz=r['broad_face_z_mm'];near=r['near_body_z_mm']
        ear0=min(hz+r['ear_z_relative_mm'][0]*s,hz+r['ear_z_relative_mm'][1]*s)
        earh=r['ear_z_relative_mm'][1]-r['ear_z_relative_mm'][0]
        sensor_x=v.get('sensor_center_x_mm',0)
        extz=0 if s<0 else -6
        if v['unit']=='child':
            target=v['side_attachment'];case=json.loads((ROOT/target['target_assembly']).read_text(encoding='utf-8'))
            frame=next(row for row in case['items'] if row['label']==target['frame_label'])
            transform=matrix(frame['ops']);transform[:3,3]-=target['target_origin_mm']
            fm=tm.load_mesh(ROOT/frame['part']/(frame['file']+'.stl'));fm.apply_transform(transform)
            crop=tm.creation.box([12,26,55]);crop.apply_translation([-6,13,27.5])
            cropped=tm.boolean.intersection([fm,crop],engine='manifold')
            cropped.export(A/'_work/intermediate/child_side_reference.stl')
            exterior='color([.65,.72,.78,.55]) import("_work/intermediate/child_side_reference.stl");'
        else:
            exterior=f'color([.65,.72,.78,.35]) translate([-13,8,{extz}]) cube([26,34,6]);'
        lines.append(f"""
if(show_{v['unit']}) translate([{cx},0,0]) {{
    // Symbolic acoustic direction only: no TD04A body or ear geometry.
    color("DodgerBlue") translate([{sensor_x},-30,{hz}]) rotate([{180 if s<0 else 0},0,0]) {{ cylinder(d=1.5,h=14,$fn=20); translate([0,0,14]) cylinder(d1=5,d2=0,h=6,$fn=32); }}
    color([0.1,0.8,0.6,0.25]) translate([{sensor_x-6},-25,{min(5*s,hz)}]) cube([12,15,60]);
    {exterior}
}}
""")
    with view.open('a',encoding='utf-8') as f:f.write('\n'.join(lines))
    meshes=[moved(tm.load_mesh(ROOT/r['part']/(r['file']+'.stl')),r['ops']) for r in data['items']]
    tm.util.concatenate(meshes).export(A/'td04a_fixture.stl')
    for v in data['fixture_variants']:
        unit=v['unit'];s=v['broad_face_normal'][2];cx=v['origin_mm'][0]
        dest=A/'_work/images'/(v['variant']+'_assembled.png')
        # View from the broad-face side so both the flange and requested face are visible.
        args=[str(OPENSCAD),'-o',str(dest),'--imgsize=1000,950','--projection=o','--viewall',
              '--camera='+','.join(str(n) for n in [cx+100,-150,s*90,cx,-4,s*30]),
              '-D','show_parent='+('true' if unit=='parent' else 'false'),
              '-D','show_child='+('true' if unit=='child' else 'false'),str(view)]
        subprocess.run(args,check=True,cwd=ROOT,timeout=120)
    plt.rcParams['font.family']='Meiryo'
    fig,axes=plt.subplots(1,2,figsize=(12,7),facecolor='white')
    for ax,v in zip(axes,data['fixture_variants']):
        ax.imshow(plt.imread(A/'_work/images'/(v['variant']+'_assembled.png')));ax.axis('off')
        title='親機用：広い面が下向き ↓' if v['unit']=='parent' else '子機用：側面へ固定・広い面は上 ↑'
        ax.set_title(title,fontsize=16,pad=8)
        ax.text(.03,-.02,'オレンジ：写真の金属部を置き換える治具\n緑：高さ60 mmの予約域（幅・奥行は仮）　青矢印：送受信方向',transform=ax.transAxes,fontsize=10)
    fig.suptitle('TD04A用 曲げ金具 2種類　／　M4・12 mmピッチ／穴列基準の逃げ60 mm',fontsize=18,y=.98)
    fig.text(.5,.025,'旧TD04A本体モデルは不使用。親機M5/20、子機側面M3/20。実物適合・強度は未確認。',ha='center',fontsize=11)
    fig.subplots_adjust(left=.01,right=.99,bottom=.14,top=.88,wspace=.05)
    fig.savefig(A/'_work/images/fixture_assembled.png',dpi=140);plt.close(fig)
    print(view)
if __name__=='__main__':main()
