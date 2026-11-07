"""Add dated retrofit documentation without deleting prior design history."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def prepend(rel,text):
    p=ROOT/rel;s=p.read_text(encoding='utf-8-sig')
    if text not in s:p.write_text(text+'\n\n'+s,encoding='utf-8')
def main():
    prepend('assemblies/parent_hand_service/README.md','''# 2026-10-24 親機内装改良・嵌合確認用試作

現行配置は `placement.json`。印刷入口は [parts/PRINT.md](parts/PRINT.md)、組立と締結の詳細は [改良報告](retrofit_report.md)。以下の旧柱・旧MAIN固定板の印刷案内は履歴であり、今回の改良部品と混ぜない。

最下段床板とLiPo固定具を無加工で再使用する。MAIN＋アンテナは4本の整備ねじと配線を外して一緒に持ち上げる。新規締結は最長30 mm。RTCの追加10 mm包絡、XT前方20 mm、電源スイッチ操作路を検査した配置を採用する。アンテナ上面と蓋の公称すきまは1.2 mmで、実物嵌合・ケーブルの取り回し・締付け強度は未確認。

追加印刷は16種類19個。床裏からの組み直しが必要。旧全長貫通ねじと上面開放ナット座を改良構成に使わない。''')
    prepend('assemblies/parent_hand_service/_work/analysis/retrofit_20261024/README.md','2026-10-24 最終候補の入口は [改良報告](../../../retrofit_report.md) と `release_record.json`。以下は初期探索の履歴。数値は最終配置と異なる場合がある。')
    for folder in ['parent_hand_service','ann_mb1_internal_rack','gnss_universal_carrier']:
        prepend('parts/parent/interior/printed/'+folder+'/README.md','''## 2026-10-24 内装改良バリアント

設計元は `scad/lib/parent_service_retrofit.py`、生成入口は `spec/build_parent_hand_service.py --service-retrofit`。旧部品は保持し、現行内装の選択は `assemblies/parent_hand_service/placement.json` に従う。新規バリアントの手順・再使用範囲・金具は [改良報告](../../../../../assemblies/parent_hand_service/retrofit_report.md)。STLの姿勢は manufacturing.json を使い、支持材禁止モディファイアは部品として印刷しない。実物検証前の試作。''')
    prepend('docs/配線・ケーブル計画.md','''## 2026-10-24 親機内装改良

電源基板は元の向きのまま南へ11 mm、上へ5.5 mm。XT差込口前方20 mmを空ける。MAINは上へ3 mm、GNSS／磁気センサ一式は上へ16 mm、アンテナは南へ12 mm・上へ8.8 mm。現行配置は parent_hand_service/placement.json。

同軸はR20 mmの引出しとアンテナ側約235 mmの自由な整備ループを確保する。新リングの上面開放入口を使い、工具路を塞がない。整備時は電源・MAIN配線・受信機側SMAを外し、ループを解放してMAIN＋アンテナを持ち上げる。ケーブルの実変形と巻き量は未検証。詳細は [改良報告](../assemblies/parent_hand_service/retrofit_report.md)。''')
    prepend('docs/部品一覧.md','2026-10-24 親機内装の改良バリアントは [改良報告](../assemblies/parent_hand_service/retrofit_report.md) と [印刷一式](../assemblies/parent_hand_service/parts/PRINT.md) を参照。床板・LiPo固定具・既存GNSS枠・Sony固定板を再使用し、16種類19個を交換印刷する。')
    p=ROOT/'assemblies/README.md';s=p.read_text(encoding='utf-8');s=s.replace('| 13 / 20 |','| 16 / 19 |');p.write_text(s,encoding='utf-8')
if __name__=='__main__':main()
