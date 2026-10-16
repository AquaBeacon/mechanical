"""Compose the horizontal layout design board from verified CAD renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_concept/_work/images'
FONT=Path('C:/Windows/Fonts/YuGothM.ttc');BOLD=Path('C:/Windows/Fonts/YuGothB.ttc')
def font(size,bold=False):return ImageFont.truetype(str(BOLD if bold else FONT),size)
canvas=Image.new('RGB',(2400,3000),'#F2F4F3');d=ImageDraw.Draw(canvas)
d.text((72,46),'子機外装 / 横置き耐圧容器',font=font(58,True),fill='#14323E')
d.text((75,131),'HORIZONTAL OPEN FRAME   /   2026.10.07   /   exploration_only',font=font(26),fill='#5A747C')
hero=Image.open(OUT/'child_exterior_hero.png').convert('RGB')
canvas.paste(ImageOps.pad(hero,(1610,1230),color='#F2F4F3'),(64,212))
x=1740;d.text((x,245),'今回の設計条件',font=font(38,True),fill='#14323E')
notes=[('01  耐圧容器','4インチ・200 mmを横置き','容器の軸 = 前後方向'),
       ('02  上向き機器','振動子・水中ライトは上向き','直上の中心軸を開放'),
       ('03  カメラ','前面で水平方向を見る','既存の防水ケースを再利用'),
       ('04  下側のおもり','C 1,000 g×2 + B 60 g×4','合計 2,240 g を低い位置へ'),
       ('05  黄橙色のブロック','浮力材の予約スペース','材質・必要量はこれから決定')]
for j,(title,line1,line2) in enumerate(notes):
 y=335+j*196;d.text((x,y),title,font=font(30,True),fill='#174F68')
 d.text((x,y+55),line1,font=font(26),fill='#344E57');d.text((x,y+96),line2,font=font(25),fill='#6B7E84')
panels=[(72,1490,'側面 / 容器は水平・機器は上向き','side'),
        (1240,1490,'上面 / 機器と予約浮力材の分離','plan'),
        (72,2210,'後面 / キャップと配線経路','rear'),
        (1240,2210,'分解 / 仮の部品構成','exploded')]
for x,y,title,stem in panels:
 d.text((x,y),title,font=font(32,True),fill='#14323E')
 img=Image.open(OUT/('child_exterior_'+stem+'.png')).convert('RGB')
 canvas.paste(ImageOps.pad(img,(1090,605),color='#E8EDEE'),(x,y+65))
d.line((72,2913,2325,2913),fill='#C7D2D5',width=2)
d.text((75,2930),'BlueROV2の配置思想を参考にした外観検討。取付・強度・浮力バランス・内装の横置き固定は未検証。',font=font(25),fill='#62747A')
canvas.save(OUT/'child_exterior_design_board.png')
# Compact annotated hero for sharing without opening the full board.
img=Image.new('RGB',(1700,1480),'#F2F4F3');h=ImageDraw.Draw(img)
h.text((52,32),'横置き容器 + 上向き振動子・ライト + 前向きカメラ',font=font(38,True),fill='#14323E')
img.paste(hero,(0,104))
h.text((52,1418),'設計イメージ / 黄橙色は浮力材の仮予約体積 / 製作寸法・強度・浮力は未確定',font=font(25),fill='#62747A')
img.save(OUT/'child_exterior_horizontal_overview.png')
print(OUT/'child_exterior_design_board.png')
