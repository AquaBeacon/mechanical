"""Plot the numeric retrofit study, explicitly as a non-manufacturing layout."""
from pathlib import Path
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_hand_service/_work/images'
ANALYSIS=ROOT/'assemblies/parent_hand_service/_work/analysis/retrofit_20261024'

def main():
    run=Path(sys.argv[1])
    log=(run/'logs/freecad.log').read_text(encoding='utf-8',errors='replace')
    raw=next(line[len('LAYOUT_SURVEY='):] for line in log.splitlines() if line.startswith('LAYOUT_SURVEY='))
    data=json.loads(raw)
    ANALYSIS.mkdir(parents=True,exist_ok=True)
    (ANALYSIS/'layout_survey.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    plt.rcParams['font.family']='Yu Gothic'
    plt.rcParams['font.size']=10
    fig,axs=plt.subplots(1,2,figsize=(14,8),gridspec_kw={'width_ratios':[1,1.2]})
    fig.patch.set_facecolor('#f4f6f8')
    colors={'p_main':'#3182bd','p_pwr':'#31a678','antenna_ground_plate':'#f3b547',
            'gnss_antenna':'#d99028','gnss_universal_carrier':'#9572bb','gnss_receiver':'#9572bb',
            'lipo':'#dd7f73','spresense':'#80939a','rtc_service_reserve':'#d43d50',
            'xt_bat_20mm':'#11aab0','xt_tx_20mm':'#11aab0','coax_ring':'#8c8c8c'}
    names={'p_main':'MAIN','p_pwr':'PWR','antenna_ground_plate':'アンテナ鋼板',
           'gnss_antenna':'アンテナ','gnss_universal_carrier':'GNSS・磁気センサ台',
           'gnss_receiver':'GNSS','lipo':'LiPo（維持）','spresense':'Sony（位置維持）',
           'rtc_service_reserve':'RTC +10 mm 予約','xt_bat_20mm':'XT 20 mm',
           'xt_tx_20mm':'XT 20 mm','coax_ring':'コード巻（位置維持）'}
    b=data['bounds']
    for i,ax in enumerate(axs):
        ax.set_facecolor('white')
        for name in ['p_main','p_pwr','coax_ring','spresense','lipo','gnss_universal_carrier',
                     'gnss_receiver','antenna_ground_plate','gnss_antenna','rtc_service_reserve','xt_bat_20mm','xt_tx_20mm']:
            q=b[name];a,c=(0,1) if i==0 else (1,2)
            x,y=q[a],q[c];w,h=q[a+3]-x,q[c+3]-y
            ax.add_patch(Rectangle((x,y),w,h,facecolor=colors[name],alpha=.18,
                                   edgecolor=colors[name],linewidth=1.7,
                                   hatch='///' if name=='rtc_service_reserve' else None))
            if i==0 and name in ['p_main','p_pwr','lipo','spresense']:
                ax.text(x+w/2,y+h/2,names[name],ha='center',va='center',weight='bold',fontsize=10)
        if i==0:
            ax.set_xlim(0,210);ax.set_ylim(0,230);ax.set_aspect('equal')
            ax.set_xlabel('X [mm]');ax.set_ylabel('Y [mm]　↑ 北 / ↓ 南')
            ax.set_title('上面配置：外形包絡の重なりを表示')
            ax.annotate('鋼板を南へ12 mm',xy=(60,18),xytext=(7,4),arrowprops={'arrowstyle':'->'},fontsize=9)
            ax.annotate('RTC上方 +10 mm を予約',xy=(78,94),xytext=(5,70),arrowprops={'arrowstyle':'->'},fontsize=9)
            ax.annotate('XT 接続20 mm',xy=(80,211),xytext=(115,226),arrowprops={'arrowstyle':'->'},fontsize=9)
        else:
            ax.set_xlim(0,230);ax.set_ylim(0,105);ax.set_aspect('equal')
            ax.axhline(97.1,color='#333333',linestyle='--');ax.text(2,98.5,'ふた屋根下面 Z97.1',fontsize=9)
            ax.axhline(18.8,color='#999999',linestyle=':');ax.text(3,11,'床板は無加工・再印刷なし',fontsize=9)
            ax.set_xlabel('Y [mm]');ax.set_ylabel('Z [mm]')
            ax.set_title('側面投影：X方向に離れた部品も重なって見える')
            for name in ['gnss_receiver','gnss_antenna','p_main','p_pwr']:
                q=b[name];ax.text((q[1]+q[4])/2,q[5]+2,names[name],ha='center',fontsize=9)
        ax.grid(alpha=.12)
    fig.suptitle('親機内装の改良候補 — 配置検討用・印刷不可',fontsize=18,weight='bold',y=.97)
    fig.text(.52,.25,'支持部・裏ナット・工具経路・取り外し動作は別途設計／検証が必要。\n色付き矩形は部品の外形包絡で、完成部品の形状ではありません。',fontsize=10)
    fig.subplots_adjust(top=.9,bottom=.08,wspace=.18)
    OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/'retrofit_layout_candidate.png'
    fig.savefig(target,dpi=160,facecolor=fig.get_facecolor())
    plt.close(fig)
    print(target)

if __name__=='__main__': main()
