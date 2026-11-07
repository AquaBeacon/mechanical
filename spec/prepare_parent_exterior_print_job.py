"""Prepare six quantity-complete X1C plates from the current portable parts.

No CAD is regenerated and no printer is contacted. Existing validated single-part
projects are retained; grouped plates use the same installed Bambu CLI/presets.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,shutil,zipfile
import xml.etree.ElementTree as ET
import numpy as np
import trimesh
from shapely.geometry import LineString,box
from topopt import slicer
from topopt.cli import slice as native
from review_parent_exterior_slices import paths
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
JOB='x1c_petg_rev6'
OUT=A/'print_jobs'/JOB
WORK=A/'_work/analysis'/JOB
INTERMEDIATE=A/'_work/intermediate'/JOB
PREVIOUS=A/'print_jobs/support_reduction'
NS={'c':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02',
    'p':'http://schemas.microsoft.com/3dmanufacturing/production/2015/06'}

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def save(path,data):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def stem(name):return 'parent_oneplate_'+name

PLATES=[
    dict(name='01_fixtures',title='小物・TD04A治具',template=stem('td_support'),brim=6,parts=[
        (stem('td_support'),45,75,'TD04A'),(stem('camera_stop'),95,75,'Stop'),
        ('parent_light_jaw',95,112,'Jaw'),('quick_release_prototypes_twist_knob',165,75,'Knob'),
        (stem('box_locator_pressure_pad'),95,145,'Pad 1'),
        (stem('box_locator_pressure_pad'),125,145,'Pad 2'),
        (stem('box_locator_pressure_pad'),155,145,'Pad 3')]),
    dict(name='02_camera_qr_pair',title='カメラQR オス・メス',template=stem('camera_qr_female'),brim=3,parts=[
        (stem('camera_qr_female'),55,90,'QR F'),(stem('camera_qr_male'),133,90,'QR M')]),
    dict(name='03_camera_mount',title='カメラマウント',single='camera_mount'),
    dict(name='04_stands_pair',title='脚2個',template=stem('stand'),brim=3,parts=[
        (stem('stand'),65,35,'Stand 1'),(stem('stand'),131,35,'Stand 2')]),
    dict(name='05_main_plate',title='主プレート',single=stem('frame')),
    dict(name='06_upper_clamp',title='上側押さえ',single=stem('bar')),
]

def xml_transform(value):
    if not value:return np.eye(4)
    values=np.array([float(v) for v in value.split()]).reshape(4,3)
    result=np.eye(4);result[:3,:3]=values[:3,:].T;result[:3,3]=values[3,:]
    return result

def saved_mesh(project):
    """Resolve saved 3MF production components and all build transforms."""
    with zipfile.ZipFile(project) as archive:
        assert archive.testzip() is None
        trees={}
        def tree(path):
            if path not in trees:trees[path]=ET.fromstring(archive.read(path))
            return trees[path]
        def obj_mesh(path,object_id,transform):
            obj=tree(path).find(f'c:resources/c:object[@id="{object_id}"]',NS)
            assert obj is not None,(path,object_id)
            mesh=obj.find('c:mesh',NS)
            if mesh is not None:
                vertices=[[float(v.attrib[a]) for a in ('x','y','z')] for v in mesh.find('c:vertices',NS)]
                faces=[[int(v.attrib[a]) for a in ('v1','v2','v3')] for v in mesh.find('c:triangles',NS)]
                result=trimesh.Trimesh(vertices=vertices,faces=faces)
                result.apply_transform(transform);return [result]
            results=[]
            for component in obj.findall('c:components/c:component',NS):
                target=component.attrib.get('{'+NS['p']+'}path',path).lstrip('/')
                results+=obj_mesh(target,component.attrib['objectid'],transform@xml_transform(component.attrib.get('transform')))
            return results
        meshes=[]
        for item in tree('3D/3dmodel.model').findall('c:build/c:item',NS):
            meshes+=obj_mesh('3D/3dmodel.model',item.attrib['objectid'],xml_transform(item.attrib.get('transform')))
        settings=read_settings(archive)
    return trimesh.util.concatenate(meshes),settings

def read_settings(archive):return json.loads(archive.read('Metadata/project_settings.config'))

def verify_existing():
    """Verify that the ready projects still match the current printable sources."""
    report=read(OUT/'manifest.json')
    portable=read(A/'parts/manifest.json')
    required=Counter({e['stem']:e['quantity'] for e in portable['parts']})
    actual=Counter()
    assert report['passed'] and report['placement_sha256']==sha(A/'placement.json')
    assert report['portable_sources']=={e['file']:e['sha256'] for e in portable['parts']}
    for e in portable['parts']:
        assert sha(A/'parts'/e['file'])==e['sha256'],e['file']
    for r in report['plates']:
        project=OUT/r['file'];gcode=project.parent/'plate_1.gcode'
        assert r==read(project.parent/'validation.json')
        assert r['passed'] and sha(project)==r['sha256'] and sha(gcode)==r['gcode_sha256']
        with zipfile.ZipFile(project) as archive:
            assert archive.testzip() is None
            assert hashlib.sha256(archive.read('Metadata/plate_1.gcode')).hexdigest()==sha(gcode),r['name']
        assert r['support_filament_mm']==r['actual_support_extrusion_moves']==r['exclusion_hits']==0
        assert r['part_count']==len(r['parts'])==r['saved_3mf_components']
        for part in r['parts']:
            assert part['source_sha256']==sha(A/'parts'/part['file'])
            actual[part['stem']]+=1
    assert actual==required and sum(actual.values())==report['part_count']==14
    assert len(report['plates'])==6
    assert abs(sum(r['grams'] for r in report['plates'])-report['grams'])<.001
    assert sum(r['seconds'] for r in report['plates'])==report['seconds']
    print('PASS: 6 ready projects, 14 parts, source / 3MF / embedded G-code hashes match',flush=True)

def write_instructions(report):
    """Keep the operational instructions beside the six native projects."""
    def duration(seconds):
        minutes=round(seconds/60)
        return f'{minutes//60}時間{minutes%60:02d}分'
    rows=[
        '# parent_exterior Rev.6 印刷用3MF',
        '',
        '2026-10-20。印刷一式の入口は[parts/PRINT.md](../../parts/PRINT.md)。',
        '**下の6ファイルを各1回ずつ印刷すると、11種類・14個が揃います。3MFには必要数を配置済みなので、追加の複製は不要です。**',
        '',
        f'X1 Carbon・0.4 mmノズル・PETG・Textured PEI Plate用。合計見積りは **{report["grams"]:.1f} g・{duration(report["seconds"])}**。ブリムを含むスライサー見積りで、実測ではありません。',
        'PETGは合計1.8 kg以上を目安に準備してください。新品1 kgスプールなら2本分です。主プレートには単独で約756 g必要なので、残量800 g以上のスプールを使ってください。',
        '',
        '| 順番・3MFを開く | 内容 | 個数 | 見積り材料 | 見積り時間 |',
        '|---|---|---:|---:|---|',
    ]
    contents={
        '01_fixtures':'TD04A支持1、カメラ角度ストップ1、押さえ板1、ノブ1、圧力パッド3',
        '02_camera_qr_pair':'QRメス1・オス1',
        '03_camera_mount':'カメラマウント1',
        '04_stands_pair':'脚2',
        '05_main_plate':'主プレート1（一体位置決め部・予備M4穴付き）',
        '06_upper_clamp':'上側押さえ1',
    }
    for r in report['plates']:
        rows.append(f'| [{r["name"]}：{r["title"]}]({r["file"]}) | {contents[r["name"]]} | {r["part_count"]} | {r["grams"]:.1f} g | {duration(r["seconds"])} |')
    rows += [
        '',
        'まず01〜03を印刷し、QRの回転・抜去、TD04Aとカメラの取付を実物で確認してから、大きい主プレートと上側押さえへ進めてください。組立寸法・ねじの指定は[assembly README](../../README.md#既存機器の固定組立)を参照してください。',
        '',
        '## Bambu Studioでの操作',
        '',
        '1. 各3MFを「プロジェクト」として開き、プリンタがX1 Carbon・0.4 mm、プレートがTextured PEI Plateになっていることを確認します。',
        '2. 装填したPETGとフィラメントの割当を合わせます。03はGeneric PETG、他はBambu PETG Basicの既存条件です。別の材料・機種へ変更する場合は、その条件で再スライスしてください。',
        '3. 保存済みの姿勢・配置・倍率を使います。特に05はベッド端に近いため、自動配置やブリム拡大をせず、2 mmブリムを維持してください。',
        '4. プレビューで対象プレートと数量を確認して印刷します。複数部品のプレートは全体を一層ずつ印刷する設定です。冷却後に外し、ブリムを除去してください。',
        '',
        'STLから配置し直す場合は[parts/PRINT.md](../../parts/PRINT.md)の表が必要総数です。STLも印刷姿勢を反映済みなので、組立時の回転を重ねないでください。',
        '',
        '## 保存条件と確認結果',
        '',
        '- 01・04〜06：0.20 mm層、8壁、100%充填。02（QR）：0.10 mm層、8壁、100%充填。03：0.20 mm層、6壁、Gyroid 15%。',
        '- ブリム：01は小物を含め6 mm、05は2 mm、他は3 mm。',
        '- 全6プレートで実G-codeのサポート材押出0。01・05・06は自動支持を有効のまま0。02・03・04は既存の短い橋渡しを使うサポートなし設定です。',
        '- 保存3MF内の閉メッシュ、14個の数量、元STLとの外形・体積、全層の押出経路とX1Cの使用禁止領域を照合済み。実印刷・嵌合・強度は未確認です。',
        '',
        '![6プレートの配置と最初の層](../../_work/images/x1c_petg_rev6_plates.png)',
        '',
        '[検査・元STLと3MFのSHA-256](manifest.json)。G-codeとプリセットは各プレートのフォルダに保存しています。通常は表の3MFを使用してください。',
        '再生成：リポジトリ直下で `python spec/prepare_parent_exterior_print_job.py`。現行の印刷用STLと検証済み単品プロジェクトから配置・スライス・照合を行い、CAD形状は変更しません。',
        '',
    ]
    (OUT/'README.md').write_text('\n'.join(rows),encoding='utf-8')

def main():
    manifest=read(A/'parts/manifest.json');entries={e['stem']:e for e in manifest['parts']}
    previous={Path(r['file']).stem:r for r in read(PREVIOUS/'validation.json')}
    previous_audit=read(A/'_work/analysis/support_reduction/slice_audit.json')
    assert previous_audit['passed'] and previous_audit['all_production_support_free']
    for name,e in entries.items():
        assert sha(A/'parts'/e['file'])==e['sha256']==previous[name]['source_sha256'],name
    for folder in (OUT,WORK,INTERMEDIATE):folder.mkdir(parents=True,exist_ok=True)
    records=[];actual_counts=Counter();panels=[]
    for plate in PLATES:
        name=plate['name'];dest=OUT/name;dest.mkdir(exist_ok=True)
        project=dest/(name+'.3mf');parts=[];expected=[]
        if 'single' in plate:
            s=plate['single'];e=entries[s]
            old=PREVIOUS/s/(s+'.3mf')
            previous_row=next(r for r in previous_audit['parts'] if r['file']==s+'.stl')
            assert sha(old)==previous_row['three_mf_sha256']
            shutil.copy2(old,project);shutil.copy2(PREVIOUS/s/'plate_1.gcode',dest/'plate_1.gcode')
            for filename in ('preset_machine.json','preset_process.json','preset_filament.json'):
                shutil.copy2(PREVIOUS/s/filename,dest/filename)
            expected=[trimesh.load(A/'parts'/e['file'],force='mesh')]
            parts=[dict(stem=s,file=e['file'],source_sha256=e['sha256'],label=plate['title'])]
            info=previous[s]
            grams=info['grams'];seconds=info['seconds'];support_mm=info['support_filament_mm']
        else:
            for s,x,y,label in plate['parts']:
                e=entries[s];mesh=trimesh.load(A/'parts'/e['file'],force='mesh')
                translation=np.array([x,y,0])-mesh.bounds[0]
                mesh.apply_translation(translation);expected.append(mesh)
                parts.append(dict(stem=s,file=e['file'],source_sha256=e['sha256'],translation_mm=translation.tolist(),label=label))
            # Conservative brim envelopes must remain separate before slicing.
            envelopes=[box(m.bounds[0,0]-plate['brim']-.4,m.bounds[0,1]-plate['brim']-.4,
                           m.bounds[1,0]+plate['brim']+.4,m.bounds[1,1]+plate['brim']+.4) for m in expected]
            assert all(not envelopes[i].intersects(envelopes[j]) for i in range(len(envelopes)) for j in range(i))
            combined=trimesh.util.concatenate(expected)
            input_stl=INTERMEDIATE/(name+'.stl');combined.export(input_stl,file_type='stl_ascii')
            assert trimesh.load(input_stl,force='mesh').is_watertight
            files={}
            for kind in ('machine','process','filament'):
                source=PREVIOUS/plate['template']/('preset_'+kind+'.json')
                data=read(source)
                if kind=='process':data.update(brim_width=str(plate['brim']),print_sequence='by layer')
                output=dest/('preset_'+kind+'.json');save(output,data);files[kind]=str(output)
            code,output,_=native._run(r'C:\Program Files\Bambu Studio\bambu-studio.exe',files,str(input_stl),str(dest),project.name,'keep',240,bed_type='Textured PEI Plate')
            (A/'_work/logs'/(JOB+'_'+name+'.log')).write_text(output,encoding='utf-8')
            assert code==0,(name,code,output[-1500:])
            info,_,features=native._read_3mf(project)
            grams=info['filament_g'];seconds=info['print_time_s'];support_mm=slicer.support_mm(features)
            save(dest/'slice.json',info)
        actual,settings=saved_mesh(project);planned=trimesh.util.concatenate(expected)
        assert actual.is_watertight and actual.is_winding_consistent,name
        shells=actual.split(only_watertight=False);assert len(shells)==len(parts),(name,len(shells),len(parts))
        delta=actual.bounds[0]-planned.bounds[0]
        assert abs(delta[2])<.001,(name,delta)
        planned.apply_translation(delta)
        assert np.max(abs(actual.bounds-planned.bounds))<.001
        assert abs(actual.volume-planned.volume)/planned.volume<1e-5
        remaining=list(shells)
        for part,mesh in zip(parts,expected):
            mesh=mesh.copy();mesh.apply_translation(delta)
            index=min(range(len(remaining)),key=lambda i:float(np.max(abs(remaining[i].bounds-mesh.bounds))))
            saved=remaining.pop(index);error=float(np.max(abs(saved.bounds-mesh.bounds)))
            assert error<.001 and abs(saved.volume-mesh.volume)/mesh.volume<1e-5,(name,part['stem'],error)
            part['saved_bounds_mm']=saved.bounds.tolist();actual_counts[part['stem']]+=1
        segments=paths(dest/'plate_1.gcode')
        with zipfile.ZipFile(project) as archive:
            assert hashlib.sha256(archive.read('Metadata/plate_1.gcode')).hexdigest()==sha(dest/'plate_1.gcode'),name
        extrusion=np.array([p[:,:2] for z,f,p in segments if f!='Custom'])
        lo=extrusion.min(axis=(0,1));hi=extrusion.max(axis=(0,1))
        candidates=extrusion[(extrusion.min(axis=1)[:,0]<18.25)&(extrusion.min(axis=1)[:,1]<28.25)]
        exclusion_hits=sum(LineString(p).intersects(box(0,0,18.25,28.25)) for p in candidates)
        support_moves=sum(f.startswith('Support') for z,f,p in segments)
        assert np.all(lo>=.25) and np.all(hi<=255.75) and not exclusion_hits,(name,lo,hi,exclusion_hits)
        assert support_mm==0 and support_moves==0,(name,support_mm,support_moves)
        if 'single' not in plate:
            assert str(settings['brim_width'])==str(plate['brim'])
        layer=float(settings['layer_height'])
        assert layer==(.1 if 'qr_pair' in name else .2)
        camera='camera_mount' in name
        assert str(settings['wall_loops'])==('6' if camera else '8')
        assert settings['sparse_infill_density']==('15%' if camera else '100%')
        first=min(z for z,f,p in segments if f=='Outer wall')
        panels.append((name,grams,seconds,[(f,p) for z,f,p in segments if z==first and f!='Custom'],parts))
        record=dict(name=name,title=plate['title'],file=str(project.relative_to(OUT)).replace('\\','/'),
                    sha256=sha(project),parts=parts,part_count=len(parts),grams=grams,seconds=seconds,
                    layer_mm=layer,wall_loops=settings['wall_loops'],infill=settings['sparse_infill_density'],
                    brim_mm=float(settings['brim_width']),support_enable=settings['enable_support'],
                    material_profile=settings.get('filament_settings_id'),machine=settings.get('printer_model'),
                    gcode_sha256=sha(dest/'plate_1.gcode'),support_filament_mm=support_mm,
                    actual_support_extrusion_moves=support_moves,extrusion_bounds_xy_mm=[lo.tolist(),hi.tolist()],
                    exclusion_hits=int(exclusion_hits),saved_3mf_components=len(shells),passed=True)
        records.append(record);save(dest/'validation.json',record)
        print(name,len(parts),'parts',grams,'g',seconds,'s; support=0 / bed PASS',flush=True)
    required=Counter({s:e['quantity'] for s,e in entries.items()})
    assert actual_counts==required,(actual_counts,required)
    report=dict(passed=True,assembly='parent_exterior',revision=6,plates=records,
                quantities=dict(actual_counts),part_count=sum(actual_counts.values()),
                grams=sum(r['grams'] for r in records),seconds=sum(r['seconds'] for r in records),
                portable_sources={e['file']:e['sha256'] for e in entries.values()},
                placement_sha256=sha(A/'placement.json'),physical_print_verified=False)
    save(OUT/'manifest.json',report);save(WORK/'print_job_checks.json',report)
    write_instructions(report)
    fig,axes=plt.subplots(2,3,figsize=(15,11))
    for ax,(name,grams,seconds,lines,parts) in zip(axes.flat,panels):
        ax.add_patch(Rectangle((0,0),256,256,fill=False,edgecolor='#777'))
        ax.add_patch(Rectangle((0,0),18.25,28.25,color='#dddddd'))
        ax.add_collection(LineCollection([p[:,:2] for f,p in lines],colors='#247895',linewidths=.4))
        for part in parts:
            b=np.array(part['saved_bounds_mm']);xy=b[:,:2].mean(axis=0)
            if len(parts)>1:ax.text(*xy,part['label'],ha='center',va='center',fontsize=8,color='#a23d1c')
        ax.set(xlim=(-2,258),ylim=(-2,258),xticks=[0,128,256],yticks=[0,128,256])
        ax.set_aspect('equal');ax.set_title(f'{name}\n{len(parts)} parts / {grams:.1f} g / {seconds/3600:.1f} h')
    fig.suptitle('X1C PETG Rev.6: quantity-complete plates / actual first-layer extrusion',fontsize=14)
    fig.tight_layout(rect=[0,0,1,.95]);fig.savefig(A/'_work/images'/(JOB+'_plates.png'),dpi=140);plt.close(fig)
    print('READY:',len(records),'plates,',sum(actual_counts.values()),'parts,',round(report['grams'],1),'g',flush=True)

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only',action='store_true',help='verify the existing projects without slicing')
    args=parser.parse_args()
    if not args.verify_only:main()
    verify_existing()
