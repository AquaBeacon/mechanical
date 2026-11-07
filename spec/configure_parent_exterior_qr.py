"""Idempotent Rev.2 migration from the recorded placement, preserving old history."""
from pathlib import Path
import json, subprocess, hashlib

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
H=A/'_work/analysis/qr_standing/history'
def write(p,d):
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    current=json.loads((A/'placement.json').read_text(encoding='utf-8'))
    if current.get('revision')=='qr_standing_r2':
        print('Rev.2 is already configured; retain canonical placement and print settings.')
        return
    p=json.loads((H/'assemblies/parent_exterior/placement.json').read_text(encoding='utf-8'))
    # The old reference folder was already deleted before this work. Migrate only
    # the required purchased proxies; never restore the retired assembly.
    refs=ROOT/'parts/common/exterior/cots/parent_clamp_hardware'
    refs.mkdir(parents=True,exist_ok=True)
    sources=[]
    for stem in sorted({i['file'] for i in p['items'] if i['part']=='assemblies/parent_clamped/reference'}):
        old=f'assemblies/parent_clamped/reference/{stem}.stl'
        dst=refs/(stem+'.stl')
        # Subsequent runs use the migrated reference; a future commit may no
        # longer contain the retired path at HEAD.
        data=dst.read_bytes() if dst.exists() else subprocess.check_output(['git','show',f'HEAD:{old}'],cwd=ROOT)
        if data.startswith(b'version https://git-lfs.github.com/spec/v1'):
            data=subprocess.check_output(['git','lfs','smudge'],input=data,cwd=ROOT)
            if data.startswith(b'version https://git-lfs.github.com/spec/v1'):
                raise RuntimeError('LFS reference is unavailable: '+old)
        if not dst.exists() or dst.read_bytes().startswith(b'version https://git-lfs.github.com/spec/v1'):dst.write_bytes(data)
        sources.append({'from':old,'to':str(dst.relative_to(ROOT)),'sha256':hashlib.sha256(data).hexdigest()})
    write(refs/'migration.json',sources)
    (refs/'README.md').write_text('# 親機クランプ購入品・参考形状\n\n旧parent_clamped/referenceの削除済み参照を元のバイト列で移管。移動元とSHAはmigration.json。印刷対象ではない。蓋・パッドは既存の仮モデル。全ねじはRev.2でM5×180へ変更し、共有screw生成元を参照する。\n',encoding='utf-8')
    out=[]
    for i in p['items']:
        label=i['label']
        if label in ['locating_side_left','locating_side_right','locating_end_fixed','locating_end_push']:continue
        if label.startswith(('locating_side_bolt','locating_side_nut','locating_end_bolt','locating_end_nut')):continue
        if i['part']=='assemblies/parent_clamped/reference':i['part']=str(refs.relative_to(ROOT)).replace('\\','/')
        if label.startswith('rod_'):
            i['part']='parts/common/interior/cots/screw';i['file']='screw_rod_m5x180'
            i['ops'][0]['translate'][2]=142
        if label.startswith('washer_'):
            z=i['ops'][0]['translate'][2];i['ops'][0]['translate'][2]=-31 if z<0 else 122.3
        if label.startswith('nut_'):
            z=i['ops'][0]['translate'][2];i['ops'][0]['translate'][2]=-36 if z<0 else 123.3
        if label in ['camera_mount','camera_case_reference','locating_camera_stop'] or label.startswith('locating_camera_'):
            i['ops'][0]['translate'][2]-=36.5
            i['removal_group']='camera'
            if label.startswith('locating_camera_adjust_'):
                i['ops'][2]['translate'][1]=18
        if label=='camera_mount':i['note']='Existing camera contact geometry; attached to integrated C male adapter at its 40 mm rear holes.'
        if label in ['td04a_actual_shape_reference','td_bracket_jaw'] or label.startswith('td_screw_'):i['removal_group']='td04a'
        out.append(i)
    def item(label,part,file,ops,group='exterior',**extra):
        out.append(dict(label=label,part=part,file=file,ops=ops,group=group,color='Orange' if group=='exterior' else 'Silver',**extra))
    base='parts/parent/exterior/printed/'
    for s in (-1,1):
        item(f'stand_{s}',base+'parent_oneplate_stand','parent_oneplate_stand',[{'translate':[s*116,0,0]},{'rotate':[0,0,0 if s==1 else 180]}])
    female_ops=[{'translate':[-40,0,-30]},{'rotate':[180,0,90]}]
    item('camera_qr_female',base+'parent_oneplate_camera_qr','parent_oneplate_camera_qr_female',female_ops)
    item('camera_qr_male',base+'parent_oneplate_camera_qr','parent_oneplate_camera_qr_male',[{'translate':[-40,0,-54.5]},{'rotate':[0,0,90]}],removal_group='camera')
    item('camera_qr_knob','parts/common/jigs/quick_release_prototypes','quick_release_prototypes_twist_knob',female_ops+[{'translate':[20.5,0,14]},{'rotate':[0,90,0]}])
    for v in ['lock_bolt','lock_nut','lock_washer','rubber_pads']:
        item('camera_qr_'+v,'parts/common/interior/cots/quick_release_hardware','quick_release_hardware_'+v,female_ops,'hardware',**({'removal_group':'camera'} if v=='rubber_pads' else {}))
    screws='parts/common/interior/cots/screw'
    for x in (-60,-20):
        for y in (-20,20):
            for kind,z,length in [('female',-27.5,25),('male',-64.9,14)]:
                extra={'removal_group':'camera'} if kind=='male' else {}
                item(f'qr_{kind}_bolt_{x}_{y}',screws,f'screw_m3x{length}_socket',[{'translate':[x,y,z]},{'rotate':[180,0,0]}],'hardware',**extra)
                nut_ops=[{'translate':[x,y,-4.8 if kind=='female' else -57.1]}]
                if kind=='male':nut_ops.append({'rotate':[0,0,90]})
                item(f'qr_{kind}_nut_{x}_{y}',screws,'screw_nut_m3',nut_ops,'hardware',**extra)
    p.update(items=out,note='Rev.2: integrated vessel datums, solid 20 mm clamp bars, C-twist camera release and two ground skids. Ground Z=-72; remove camera and TD04A for standing.',revision='qr_standing_r2',coordinate_system='Box bottom and three datums Z=0; deck top -0.8, reinforced underside -20, TD seat -12; ground -72; QR lock withdraws along +Y.')
    write(A/'placement.json',p)
    write(A/'print_config.json',{'status':'prototype_qr_standing','note':'Rev.2: PETG、0.4 mmノズル。QRは0.1 mm層、他0.2 mm層。8壁・100%充填を初期条件とする。旧repeatable_mountの3MFは旧形状の履歴で再使用不可。新形状の実スライスと実締結・自立試験は検証記録を確認。'})
    variants=ROOT/screws/'variants.txt';s=variants.read_text(encoding='utf-8-sig')
    for line in ['rod_m5x180 kind="rod" d=5 l=180','m3x25_socket d=3 l=25 head_d=5.5 head_h=3','m3x14_socket d=3 l=14 head_d=5.5 head_h=3']:
        if not any(x.startswith(line.split()[0]+' ') for x in s.splitlines()):s+='\n'+line+'\n'
    variants.write_text(s,encoding='utf-8')
    print('Configured Rev.2; 180 mm rods replace the previous 150 mm rods.')

if __name__=='__main__':main()
