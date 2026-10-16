"""Documentation for the canonical top-mounted wave retention revision."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
paths=['assemblies/parent_hand_service/README.md','parts/parent/interior/printed/parent_hand_service/README.md','parts/parent/interior/printed/gnss_universal_carrier/README.md','parts/parent/interior/printed/ann_mb1_internal_rack/README.md']
for path in paths:
 p=R/path;t=p.read_text(encoding='utf-8')
 for a,b in [('X61.78','X62.78'),('X44–61.78','X45–62.78'),('X46.54／59.24','X47.54／60.24'),('左後支柱X20/Y219から','後梁X28/Y219から'),('Ø7.8支柱','左Ø7.8／右Ø6.8支柱'),('Ø8.4×0.7','Ø8.4貫通'),('Ø8.4×深さ0.7の局所逃げ','Ø8.4貫通工具穴'),('ラック最終全稜面取り0.1 mm','ラック主要形状を結合前0.2 mm面取り'),('閉姿勢102項目・箱外姿勢100項目','閉姿勢115項目・箱外姿勢113項目')]:t=t.replace(a,b)
 if path.startswith('assemblies/'):
  t=re.sub(r'1\. キャリア・ラック・GNSS台の16本.*?\n2\..*?\n', '''1. 裸の床をケースへM4×8ボタンねじ4本で固定する。座面Z16.8、頭上端19.0、公称ねじ込み5.04 mm。ボス高さ10 mm・ねじ深さは実物確認事項。床上からM3ナット16個（AF5.5×厚2.4）を六角穴へ入れる。ナット下面Z16.2、平面をX方向へ向けるZ回転30°。東側の穴は一部開放のため仮保持して台で押さえる。
2. 空のアンテナラックをM3×50の4本で固定。鋼板・アンテナ・巻き束はまだ載せない。空のMAIN台を最終位置から北92 mm／上14.2 mmでケース内へ入れ、南92 mmに滑らせて14.2 mm下げる。MAIN基板は北92 mm／上4.8 mmから南84 mmへ滑らせ、4.8 mm下げ、最後に南8 mmへ滑らせる。MAIN台前左M3×25を1本、基板と台を共締めするM3×30を3本、残りの基板穴へM3×8を1本。実部品包絡を逃がす連続経路はwave_assembly_checks.json。
3. PWR・TX、Sony台／基板、GNSS台／基板の順に取り付ける。Sony台はM3×45を4本、頭座面Z59.3。GNSS台はM3×40を4本、頭座面Z52.5。いずれも上から締め、床の金属ナットへ通す。GNSS後押さえのねじ軸はX77/124・Y220.5。最後に鋼板・アンテナと巻き束、配線を取り付ける。鋼板穴はX20/Y35、X100/Y35、X20/Y85、X100/Y75。整備時は逆順。ケース外USBのため床を外すときは各上部モジュールを先に外す。
''',t,flags=re.S)
  t=t.replace('3. MAIN/PWR/TX','4. MAIN/PWR/TX')
  t+='\n組立経路の追加検証は[wave_assembly_checks.json](wave_assembly_checks.json)。床の裏へ工具を入れる必要はない。長ねじ／ナットは購入金属部品で印刷しない。組立前の基板・ケーブルがあるため、床一式を無分解で抜く手順ではない。\n'
 else:
  t+='\n上締め改訂：床側16個のM3六角ナットへ長ねじで締結。MAINは台前左M3×25＋基板共締めM3×30×3、SonyはM3×45×4、GNSSはM3×40×4、アンテナはM3×50×4。床下面から締める旧M3×8×16は現行に使用しない。組立は現行assemblyのREADMEの順序を守る。\n'
 p.write_text(t,encoding='utf-8')
p=R/'docs/配線・ケーブル計画.md';t=p.read_text(encoding='utf-8');t+='\n2026-10-09上締め改訂：MAINの段階的スライド組立を先に行い、その後GNSS・アンテナの同軸と電源ハーネスを取り付ける。床をケースから外す際はコネクタを外してモジュールを逆順で撤去する。電池／両SDの通常サービス経路は維持。\n';p.write_text(t,encoding='utf-8')
