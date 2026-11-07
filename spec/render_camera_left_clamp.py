"""Actual-mesh side section and front-view contact-band drawing."""
from pathlib import Path
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
P=Path(__file__).resolve().parents[1]/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
fig,(side,front)=plt.subplots(1,2,figsize=(12,7))
for stem,color,label in [('camera_mount_twist','#237da0','Body / rear stop'),('camera_front_clamp','#df8d25','Front clamp')]:
    m=trimesh.load(P/(stem+'.stl'),force='mesh')
    section=m.section(plane_origin=[25,0,0],plane_normal=[1,0,0])
    for i,path in enumerate(section.discrete):side.plot(path[:,1],path[:,2],color=color,lw=2,label=label if i==0 else None)
side.add_patch(Rectangle((-23.45,36.5),41,75,color='#939da5',alpha=.2))
side.add_patch(Rectangle((-23.45,8),20,28.5,color='#dc5555',alpha=.18))
side.annotate('',xy=(-23.45,90),xytext=(17.55,90),arrowprops=dict(arrowstyle='<->'))
side.text(0,93,'41 mm measured',ha='center')
side.text(-10.5,20,'20 mm\nrear clearance',ha='center',fontsize=9)
side.set(xlim=(-58,52),ylim=(-6,120),xlabel='Y / toward camera front (mm)',ylabel='Z (mm)',title='Side section through left clamp',aspect='equal')
side.legend(loc='lower left',fontsize=8);side.grid(alpha=.15)
front.add_patch(Rectangle((-47.5,36.5),95,75,facecolor='#d8dee3',edgecolor='#495057'))
front.add_patch(Rectangle((-47.5,36.5),25,31.5,fill=False,edgecolor='#df8d25',linestyle='--',linewidth=1.5))
front.add_patch(Rectangle((-35.5,36.5),25,31.5,color='#df8d25',alpha=.8))
front.annotate('',xy=(-23,91),xytext=(-35,91),arrowprops=dict(arrowstyle='->',color='#a96a12',lw=2))
front.text(-25,94,'12 mm right',ha='center',fontsize=9)
front.annotate('',xy=(-35.5,117),xytext=(-10.5,117),arrowprops=dict(arrowstyle='<->'))
front.text(-23,120,'25 mm',ha='center')
front.text(-23,76,'Front clamp band',ha='center',fontsize=9)
front.text(0,30,'M5 axis below case',ha='center',fontsize=9)
front.plot(0,24,'o',color='#495057')
# Actual Y=4 section shows the separate M5 fingers and unnotched clamp foot.
for stem,color in [('camera_mount_twist','#237da0'),('camera_front_clamp','#df8d25')]:
    m=trimesh.load(P/(stem+'.stl'),force='mesh')
    section=m.section(plane_origin=[0,4,0],plane_normal=[0,1,0])
    for path in section.discrete:front.plot(-path[:,0],path[:,2],color=color,lw=1.5)
front.annotate('2.85 mm gap',xy=(-9.075,11),xytext=(-31,-1),fontsize=9,arrowprops=dict(arrowstyle='->'))

front.set(xlim=(-58,58),ylim=(-6,128),xlabel='Front-view horizontal (mm)',title='Looking at the camera front',aspect='equal')
front.grid(alpha=.15)
fig.suptitle('41 mm case | 25 mm clamp shifted right 12 mm | R1 edges / R3 foot root',fontsize=14)
fig.text(.5,.02,'Case width / height and M5-axis offsets remain provisional. Drawing is not a strength certification.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.04,1,.95]);fig.savefig(P/'_work/images/clamp_clearance_20261026_section.png',dpi=160);plt.close(fig)
