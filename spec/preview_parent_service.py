from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
p=Path('mechanical/assemblies/parent_service_review')
fig,ax=plt.subplots(figsize=(8,9))
ax.add_patch(Rectangle((0,0),210,230,fill=False,lw=2))
ax.add_patch(Rectangle((13.5,13.5),183,203,fill=False,ls='--',ec='gray'))
for label,x,y,w,h,c in [('P-MAIN',15.5,40.5,112,88,'#91bcce'),('P-PWR',19.5,133.5,100,84,'#acd9b1'),('TX',134.5,140.5,50,74,'#edd28c'),('Sony EXT',134.5,41,53.34,68.58,'#f1ba8c'),('Sony MAIN + IMU',145.79,41,20.6,50,'#e27c55'),('LiPo 6-face retainer',16,49.5,111,53,'#c086ae')]:
 ax.add_patch(Rectangle((x,y),w,h,fc=c,ec='#333',alpha=.7));ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=9)
ports=[('MAIN USB',36.61,41.23,-1,14,30),('MAIN SD',59.5,42.8,-1,20,25),('Sony USB1',154.79,39.4,-1,14,30),('Sony USB2',179.1,41.94,-1,14,30),('Sony SD',171.68,114.28,1,22,25)]
for n,x,y,d,w,l in ports:
 ax.add_patch(Rectangle((x-w/2,y if d>0 else y-l),w,l,fc='#78dcca',ec='#008d7a',alpha=.65))
 ax.annotate('',(x,y+d*l),(x,y),arrowprops={'arrowstyle':'->','color':'#006251'})
 ax.text(x,y+d*l/2,n,rotation=90,fontsize=8,ha='center',va='center')
ax.set(xlim=(-5,215),ylim=(-5,235),xlabel='Box X [mm]',ylabel='Box Y [mm]',title='Lid-open service revision / green = reserved USB & SD paths')
ax.set_aspect('equal');ax.grid(alpha=.15);fig.tight_layout();fig.savefig(p/'layout.png',dpi=160)
print('layout.png')

