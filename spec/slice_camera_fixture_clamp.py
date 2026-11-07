"""Slice the four changed fixture shapes through the existing X1C pipeline."""
from pathlib import Path
from slice_camera_twist import main
ROOT=Path(__file__).resolve().parents[1]

def review_nut_roofs():
    from review_parent_exterior_slices import paths
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    for name,stem,roof in [('parent_exterior','parent_oneplate_camera_qr_female',14.8),('child_horizontal_plate_frame','child_horizontal_twist_mount_camera_receiver',4.8)]:
        a=ROOT/'assemblies'/name
        lines=paths(a/'print_jobs/camera_fixture_clamp_20261029'/stem/'plate_1.gcode')
        layers=sorted({z for z,f,p in lines})
        zs=[min(layers,key=lambda z:abs(z-t)) for t in [roof-.1,roof,roof+.1,roof+.2]]
        fig,axes=plt.subplots(1,4,figsize=(16,4))
        for ax,z in zip(axes,zs):
            for cat,color in [('wall','#247895'),('bridge','#d88714'),('support','#8a659f')]:
                seg=[p[:,:2] for zz,f,p in lines if zz==z and cat in f.lower()]
                if seg:ax.add_collection(LineCollection(seg,colors=color,linewidths=.6))
            ax.autoscale();ax.set_aspect('equal');ax.set_title('Z='+str(z)+' mm')
        fig.suptitle('Nut pocket roof: walls blue / bridges orange / supports violet')
        fig.tight_layout();fig.savefig(a/'_work/images/camera_fixture_nut_roofs.png',dpi=130);plt.close(fig)

if __name__=='__main__':
    jobs=[
        ('parent_exterior','camera_mount_twist','parts/child/exterior/printed/dji_osmo_action6_mount_m3'),
        ('parent_exterior','parent_oneplate_camera_qr_female','parts/parent/exterior/printed/parent_oneplate_camera_qr'),
        ('child_horizontal_plate_frame','child_horizontal_twist_mount_camera_receiver','parts/child/exterior/printed/child_horizontal_twist_mount'),
        ('parent_exterior','camera_rotary_spacer','parts/child/exterior/printed/dji_osmo_action6_mount_m3')]
    main('camera_fixture_clamp_20261029',extra_jobs=[(a,s,ROOT/p/(s+'.stl'),True) for a,s,p in jobs])
    review_nut_roofs()
