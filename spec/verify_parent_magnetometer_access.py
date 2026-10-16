"""Vendor holes, nylon hardware, QT approaches and magnetometer removal."""
from parent_access_common import *
import sys,hashlib
sys.path.insert(0,str(R/'scad/lib'))
import parent_gnss as G

d,c=load();rows=[];proxies={}
holes=G.magnetometer_mounting_xy();board=c['magnetometer'];frame=c['gnss_universal_carrier']
for i,(x,y) in enumerate(holes):
    # Probe the actual imported STEP and final support holes independently.
    for name,sh,probe in [
        ('official PCB hole',board,Part.makeCylinder(1.2,G.MAG_PCB_THICKNESS-.1,v(x,y,G.MAG_ORIGIN[2]+.05))),
        ('printed clearance hole',frame,Part.makeCylinder(1.175,G.MAG_ORIGIN[2]-G.MAG_SHELF_BOTTOM_Z-.1,v(x,y,G.MAG_SHELF_BOTTOM_Z+.05)))]:
        vol=common(sh,probe)
        rows.append(dict(name=f'{name} {i}',collisions=[dict(part=name,mm3=vol)] if vol>.01 else []))
    # Every support must make contact with the board around, not through, its hole.
    pad=frame.common(Part.makeCylinder(G.MAG_BOSS_RADIUS,.25,v(x,y,G.MAG_ORIGIN[2]-.2)))
    assert pad.Volume>.1 and pad.distToShape(board)[0]<.01
    for label in [f'mag_bolt_{i}',f'mag_nut_{i}']:
        rows.append(dict(name=label+' occupied envelope',collisions=collisions(c[label],c,[label])))
    top=c[f'mag_bolt_{i}'].BoundBox.ZMax
    driver=Part.makeCylinder(2.5,120-top,v(x,y,top))
    nutbottom=c[f'mag_nut_{i}'].BoundBox.ZMin
    # Hollow nut-driver approach clears the protruding M2 bolt, like a socket.
    nuttool=Part.makeCylinder(3,5,v(x,y,nutbottom-5)).cut(Part.makeCylinder(1.2,5.2,v(x,y,nutbottom-5.1)))
    rows.append(dict(name=f'top driver {i}',collisions=collisions(driver,c,[f'mag_bolt_{i}'])))
    rows.append(dict(name=f'lower nut tool {i}',collisions=collisions(nuttool,c,[f'mag_nut_{i}'])))
    proxies[f'driver_{i}']=driver;proxies[f'nut_tool_{i}']=nuttool

bb=board.optimalBoundingBox(False,False);length,width,height=G.MAG_QT_PLUG_SIZE
# South socket is used. The unused north socket is next to the case wall.
sh=Part.makeBox(width,length,height,v((bb.XMin+bb.XMax-width)/2,bb.YMin-length,G.MAG_ORIGIN[2]+1))
rows.append(dict(name='south QT plug/straight approach',collisions=collisions(sh,c,['magnetometer'])))
proxies['south_QT_approach']=sh
grip=Part.makeBox(12,26,10,v((bb.XMin+bb.XMax)/2-6,bb.YMin-26,G.MAG_ORIGIN[2]))
grip_installed=collisions(grip,c,['magnetometer'])
rows.append(dict(name='south QT grip after disconnecting/parking SMA',collisions=collisions(grip,c,['magnetometer','gnss_sma_plug','gnss_coax_route'])))
proxies['south_QT_grip']=grip
remove=['magnetometer']+[n for n in c if n.startswith(('mag_bolt_','mag_nut_'))]
sweep=Part.makeBox(bb.XLength,bb.YLength,bb.ZLength+110,v(bb.XMin,bb.YMin,bb.ZMin))
rows.append(dict(name='continuous vertical board removal',collisions=collisions(sweep,c,remove)))
proxies['board_removal']=sweep
# A clearance envelope wider than the actual coax verifies the shelf root.
coax=Part.read(str(G.ANTENNA_DIR/'coax_route_clearance.step'))
rows.append(dict(name='coax OD5 clearance envelope vs modified frame',collisions=collisions(coax,{'gnss_universal_carrier':frame,'magnetometer':board})))
report=dict(status='PASS' if all(not r['collisions'] for r in rows) else 'FAIL',
    vendor_holes_xy_d_mm=G.magnetometer_vendor(),installed_holes_xy_mm=holes,
    model_source='Adafruit official 4479 LIS3MDL STEP, preserved geometry',
    model_sha256=hashlib.sha256((G.MAG_DIR/'ref/4479 LIS3MDL.step').read_bytes()).hexdigest(),
    checks=rows,lid_clearance_mm=c['lid_keepout'].BoundBox.ZMin-bb.ZMax,
    nearest_steel_plate_distance_mm=board.distToShape(c['antenna_ground_plate'])[0],
    nearest_antenna_envelope_distance_mm=board.distToShape(c['gnss_antenna'])[0],
    conditions='Lid open. Disconnect SMA and park coax before gripping the south QT plug. Four nylon M2x8 bolts/nuts. Unplug QT and remove four fasteners before lifting sensor; other boards stay installed. GNSS extraction separately verified with this mount installed.',
    south_QT_grip_with_SMA_connected=grip_installed,
    provisional='Nylon fastener head/nut and south QT mating plug/grip envelopes require actual part measurement. North QT socket unused in case; no header strip fitted in this CAD. Nut driver OD6/ID2.4 hollow approach.',
    magnetic_performance='ANN-MB1 includes magnetic base. Mechanical clearance only. Check sensor range/saturation and measure/calibrate with power/transmission active; calibration does not guarantee removal of magnetic interference. No heading accuracy guarantee.',manufacturing_release=False)
(O/'magnetometer_access_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
Part.makeCompound(list(proxies.values())).exportStep(str(O/'_work/intermediate/magnetometer_access_sweeps.step'))
print(report['status'],[r for r in rows if r['collisions']],flush=True)
assert report['status']=='PASS'
