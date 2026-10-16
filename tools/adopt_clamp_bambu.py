"""Adopt the dimension-checked Bambu smoothed trial as an exploration part.

No mesh editing: copy the rendered and independently read-back CAD outputs,
record their hashes and synchronize the one canonical manufacturing source.
"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=PART/'_work/analysis/bambu_petg_basic_v3'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    geometry=read(CASE/'geometry_checks.json')
    step=read(CASE/'step_checks.json')
    provenance=read(CASE/'final_provenance.json')
    assert geometry['pass'] and step['pass_check']
    assert sha(CASE/'finished_candidate.stl')==provenance['final_part_sha256']
    assert (PART/'_work/analysis/stress_smooth_r85_v065/adoption_snapshot/manifest.json').exists()
    records=[]
    for src,dst in [(CASE/'smoothed_density_surface.stl',PART/'spec/smoothed_density_surface.stl'),
                    (CASE/'finished_candidate.stl',PART/'child_wte4_suspension_clamp_smooth.stl'),
                    (CASE/'finished_candidate.step',PART/'child_wte4_suspension_clamp_smooth.step')]:
        shutil.copy2(src,dst)
        assert sha(src)==sha(dst)
        records.append(dict(source=str(src),canonical=str(dst),sha256=sha(dst)))
    save(CASE/'canonical_adoption.json',dict(status='exploration_only',reason='Direct native density smoothing and dimension-checked CAD interfaces; independent strength not qualified',files=records))
    m=read(PART/'manufacturing.json')
    m['material']='Bambu Lab PETG Basic (upgraded, TDS V3.0)'
    m['note']='Bambu PETG Basic TDS V3.0 anchored provisional orthotropic card. 100% infill, 8 walls, 0.20 mm layers, 0.4 mm nozzle, build Z. Direct native density smoothing with exact M3/rubber CAD interfaces. Six identical halves, about 1.014 kg at 1.25 g/cm3. Exploration only: independent strength, internal bridging, wet slip and creep not qualified. Rubber and hardware are non-print COTS.'
    m['source_dependencies']=['spec/smoothed_density_surface.stl','spec/bambu_petg_basic_material.json']
    save(PART/'manufacturing.json',m)
    config=read(ROOT/'assemblies/child_clamp_suspension/print_config.json')
    config['note']='**吊り下げ用の強度は未合格。形状・造形の検討用。** Bambu Lab PETG Basic（アップグレード版TDS V3.0）、100%インフィル、外周8、上下8層、0.20 mm、0.4 mmノズル、積層Zで平置き。直接平滑化した半リング6個、約1.014 kg（ゴム・金属・サポート別）。固定M3は各組4本全て使用。最適化格子の8ケースは合格だが、完成形状の独立解析は未合格。支持なし造形は不合格（過張出し16.8%）。吊り荷重は積層方向と一致し、実物の層間強度・濡れたゴムの滑り・クリープを要確認。内部密閉空洞に除去不能なサポートを生成しない。TDS試験条件は255°C、ベッド70°C、150 mm/s、100%インフィル。詳細はDESIGN_NOTES.md。'
    config['notes']=['parts/child/exterior/printed/child_wte4_suspension_clamp/BAMBU_PETG_BASIC.md',
                     'parts/child/exterior/printed/child_wte4_suspension_clamp/SMOOTH_TOPOLOGY.md']
    save(ROOT/'assemblies/child_clamp_suspension/print_config.json',config)
    placement=read(ROOT/'assemblies/child_clamp_suspension/placement.json')
    placement['note']='Exploration only: directly smoothed Bambu PETG Basic TDS V3.0 topology with dimension-checked M3/rubber interfaces. Eight topology cases pass; independent suspension strength not qualified. Six identical finished halves. Provisional WTE4 200 mm z centres 40/100/160 and frame pitch 36 x 16 mm.'
    save(ROOT/'assemblies/child_clamp_suspension/placement.json',placement)
    print(json.dumps(dict(copied=records,status='exploration_only')))


if __name__=='__main__':
    main()
