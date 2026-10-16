"""Copy only successful native frame A slices into its assembly print_jobs."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE = PART/'_work/analysis/frame_a_rim_thickness'
OUT = ROOT/'assemblies/child_exterior_structure/print_jobs'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    inputs = json.loads((CASE/'slice/manufacturing_inputs.json').read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, qty in [('lower_minus',2),('lower_plus',2),('upper_minus',2),('upper_plus',2),('splice',12)]:
        folder = CASE/'slice'/name
        result = json.loads((folder/'slice.json').read_text())
        source = PART/f'child_exterior_structural_frame_{name}.stl'
        assert result['pass'] and result['bed_fits'] and result['exit_code_slicer'] == 0
        assert inputs[name]['exit_code'] == 0 and sha(source) == inputs[name]['source_sha256']
        project = Path(result['project_3mf'])
        with zipfile.ZipFile(project) as z:
            assert z.testzip() is None
            model = ET.fromstring(z.read('3D/3dmodel.model'))
            transforms = [item.attrib.get('transform','') for item in model.iter()
                          if item.tag.split('}')[-1]=='item']
            assert transforms and all(list(map(float,t.split()[:9])) == [1,0,0,0,1,0,0,0,1] for t in transforms)
        dest = OUT/project.name
        shutil.copy2(project,dest)
        row = dict(file=dest.name,quantity=qty,source=source.relative_to(ROOT).as_posix(),
                   source_sha256=sha(source),project_sha256=sha(dest),
                   printer=result['printer_name'],material='Bambu PETG Basic',layer_mm=.2,
                   process_overrides=inputs[name]['process_overrides'],
                   supports='normal(auto)',orientation='flat Z; XY orientation preserved; translated to plate',
                   preset_sha256={kind:sha(folder/f'preset_{kind}.json') for kind in ['machine','process','filament']},
                   slicer_result=(folder/'slice.json').relative_to(ROOT).as_posix(),
                   filament_g=result['filament_g'],print_time_s=result['print_time_s'],
                   support_filament_g=result['support_filament_g'])
        rows.append(row)
    total_g=sum(r['quantity']*r['filament_g'] for r in rows)
    total_s=sum(r['quantity']*r['print_time_s'] for r in rows)
    data=dict(status='prototype_unqualified_joints',note='Actual native slices; strength and support removability are not qualified.',
              jobs=rows,total_filament_g=total_g,total_print_hours=total_s/3600)
    (OUT/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# フレームAのX1 Carbon用スライス','',
           '各3MFは1部品をスライス済み。表の回数だけ印刷する。左右一式は5種類20個。印刷部品の入口は [../parts/PRINT.md](../parts/PRINT.md)。','',
           'X1 Carbon・0.4 mmノズル、Bambu PETG Basic、Textured PEI Plate、層高0.20 mm、外周8、100%インフィル、aligned rectilinear・角度0°、外側ブリム5 mm、通常自動サポート45°。平置きZとXY方向を維持した。メーカー標準プロファイルを作業用JSONへ展開し、上記設定だけを変更した。','',
           '| 3MF | 印刷回数 | 1回の推定材料 g | 1回の推定時間 h |','|---|---:|---:|---:|']
    for r in rows:
        lines.append(f"| [{r['file']}]({r['file']}) | {r['quantity']} | {r['filament_g']:.2f} | {r['print_time_s']/3600:.2f} |")
    lines+=['',f'全20個のスライサ推定は約 {total_g/1000:.2f} kg、約 {total_s/3600:.1f} 時間。ブリム・支持材を含む。実測値ではない。',
            '', 'A分割片には支持材が発生する。接合板には支持材押出しが発生しない。支持材の除去可能性・接合面の仕上がりは未検証。印刷前にBambu Studioで支持材の位置を確認し、造形後に下部通路・ねじ穴・ナット座・工具通路を清掃する。',
            '', 'FEAのラスタX材料カードは、このツールパスを実測して校正したものではない。積層内の表面・ソリッド充填方向も含む強度評価は未認定。3MFの変更・再スライス後はこのスライス確認の対象外となる。',
            '', 'STLと3MFのSHA-256、元スライス結果、設定は [manifest.json](manifest.json) に記録する。購入ねじ・ナット・ワッシャは3MFに含まない。']
    (OUT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Packaged five jobs: {total_g:.2f} g, {total_s/3600:.2f} hours for 20 parts')


if __name__=='__main__':
    main()
