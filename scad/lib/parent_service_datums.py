"""Shared service dimensions and hardware specification; mm, importable without CAD."""
import parent_gnss as D

MAIN_LIFT=3.0
ANT_SOUTH=12.0
ANT_LIFT=8.8
PWR_LIFT=5.5
PWR_SOUTH=11.0
SENSOR_LEG_LENGTH=50.0
SENSOR_BASE_Z=D.FLOOR_GRID_TOP_Z
SENSOR_JOINT_Z=SENSOR_BASE_Z+SENSOR_LEG_LENGTH
SONY_SERVICE_LIFT=SENSOR_JOINT_Z-D.SONY_COLUMN_JOINT_Z
GNSS_SERVICE_LIFT=SENSOR_JOINT_Z-D.GNSS_COLUMN_JOINT_Z
FLOOR_WASHER_T=.5
FLOOR_HEAD_Z=D.FLOOR_GRID_BOTTOM_Z-FLOOR_WASHER_T
FLOOR_NUT_DEPTH=2.6
FLOOR_NUT_HEIGHT=2.4
FLOOR_NUT_TOP_Z=D.FLOOR_GRID_BOTTOM_Z+FLOOR_NUT_DEPTH
FLOOR_NUT_BOTTOM_Z=FLOOR_NUT_TOP_Z-FLOOR_NUT_HEIGHT

def retrofit_fasteners(G,main_holes,pwr_holes):
    """Nominal hardware datums for validation and assembly publication."""
    rows=[]
    def add(label,x,y,head,length,nut=None,direction=-1,diameter=3,washer=False):
        rows.append(dict(label=label,xy=[x,y],head_z=head,length=length,nut_z=nut,
                         direction=direction,diameter=diameter,washer=washer))
    for i,(x,y) in enumerate(G.RACK_FOOT_XY):
        add('cradle_service_'+str(i),x,y,35.6,30,nut=FLOOR_NUT_BOTTOM_Z)
    for i,(x,y) in enumerate(G.UNIVERSAL_FRAME_FOOT_XY):
        add('gnss_floor_'+str(i),x,y,SENSOR_JOINT_Z+2.5,65,nut=FLOOR_NUT_BOTTOM_Z)
    for i,(x,y) in enumerate(G.SONY_CARRIER_FOOT_XY):
        if i!=2:
            add('sony_floor_'+str(i),x,y,SENSOR_JOINT_Z+G.SONY_PLATE_THICKNESS,65,nut=FLOOR_NUT_BOTTOM_Z)
        else:
            add('sony_plate_'+str(i),x,y,SENSOR_JOINT_Z+G.SONY_PLATE_THICKNESS,10)
    for i,(x,y) in enumerate(main_holes):add('main_pcb_'+str(i),x,y,43.6+MAIN_LIFT,8)
    for i,(x,y) in enumerate(pwr_holes):
        add('pwr_adapter_'+str(i),x,y,30.25,8)
        add('pwr_pcb_'+str(i),135.6-x,330-PWR_SOUTH-y,29.9+PWR_LIFT,6)
    for i,(x,y) in enumerate([(12,35),(12,75),(137.5,35),(137.5,75)]):add('shelf_joint_'+str(i),x,y,63.6+ANT_LIFT,30)
    for i,(x,y) in enumerate(G.GROUND_PLATE_HOLES_XY):add('steel_'+str(i),x,y-12,64.6+ANT_LIFT,10,55.7+ANT_LIFT,washer=True)
    for i,x in enumerate([26,94]):add('antenna_'+str(i),x,48,70.6+ANT_LIFT,18,54.6+ANT_LIFT,diameter=4,washer=True)
    return rows
