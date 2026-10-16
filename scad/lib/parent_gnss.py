"""Mechanical GNSS datums in mm; mounting holes are read from vendor EAGLE.

Package heights, mating SMA plug and RG174 diameter are conservative provisional
envelopes. Do not treat them as measured manufacturer dimensions.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import math, re
ROOT = Path(__file__).resolve().parents[2]
BOARD_DIR = ROOT/'parts/parent/interior/cots/sparkfun_neo_f9p'
ANTENNA_DIR = ROOT/'parts/parent/interior/cots/ann_mb1'
EAGLE = BOARD_DIR/'ref/SparkFun NEO-F9P.brd'
BOARD_ORIGIN = [113.5, 205, 64.6]
BOARD_ROTATION = [0, 0, 180]
BOARD_THICKNESS_PROVISIONAL = 1.6
BOARD_COMPONENT_HEIGHT_PROVISIONAL = 10.0
GNSS_HEADER_HEIGHT_PROVISIONAL = 7.0
CABLE_DIAMETER_PROVISIONAL = 2.8
CABLE_BEND_RADIUS_DESIGN = 20.0
GPS_BOSS_TOP = BOARD_ORIGIN[2]
UNIVERSAL_ORIGIN = [69,139,56]
UNIVERSAL_SIZE = [60,80,1.6]
# User measured 2026-10-11: long/short pitch 75/55, all edge offsets 2.5.
UNIVERSAL_HOLE_PITCH = [55.0,75.0]  # assembly X/Y
UNIVERSAL_CLEARANCE_DIAMETER = 3.45
UNIVERSAL_PCB_HOLE_DIAMETER = 3.2  # M3 through-hole envelope; actual drill unmeasured
UNIVERSAL_FRAME_FOOT_XY = [[13,145],[135,145],[22.6,219],[135,219]]
# Wave-retention revision: wider columns and 6 mm deep transverse beams.
# Rear columns stay wholly above PWR's Y215 rear edge and below case Y223.9.
UNIVERSAL_COLUMN_SIZE_FRONT = [9,9]
UNIVERSAL_COLUMN_SIZE_REAR = [8,6]
UNIVERSAL_BEAM_BOTTOM_Z = 50.0
UNIVERSAL_BEAM_TOP_Z = 56.0
CASE_ANCHOR_XY = [[25,25],[185,25],[25,205],[185,205]]
CASE_ANCHOR_SEAT_Z = 16.8
CASE_ANCHOR_HEAD_DH = [7.6,2.2]  # ISO7380 M4x12 button envelope; purchase model pending
UNIVERSAL_CAP_SCREW_XY = [[84,137.5],[133,137.5],[77,220.5],[124,220.5]]
XH_KEEPOUT_PROVISIONAL = [60.7,168,57.6,14.8,24,6.6]  # proposed right-angle connector, pending user/part selection
ANTENNA_SIZE = [60.0, 82.0, 22.5]  # cable points +X, screw pitch along Y
ANTENNA_HOLE_PITCH = 68.0
ANTENNA_HOLE_DIAMETER = 4.5
ANTENNA_CENTRE = [60, 60]
COIL_OUTER_DIAMETER = 100.0  # user specified occupied winding envelope
COIL_INNER_DIAMETER = 75.0
COIL_HEIGHT = 10.0
COIL_BOTTOM_LOCAL = 3.5
RACK_FOOT_OFFSET = 55 / 2**.5
RACK_FOOT_XY = [[12,25],[134,25],[12,95],[134,95]]
LID_TOP_PROVISIONAL = 100.3
CADDY_HEIGHT = 44.8
GROUND_PLATE_THICKNESS = 1.0
GROUND_PLATE_SIZE = [88.0, 60.0]
GROUND_PLATE_Z = 63.6
ANTENNA_Z = GROUND_PLATE_Z + GROUND_PLATE_THICKNESS
ANTENNA_ROTATION = [0,0,90]
RACK_BASE_Z = 18.8
PWR_ORIGIN = [25.8,115,28.3]
MAIN_ORIGIN = [18,112,42]
SONY_ORIGIN = [202.34,208,65.6]
BATTERY_ORIGIN = [197.5,22.1,20]  # avoid south-east case corner; retain vertical service
BATTERY_ROTATION = [0,0,90]
MAIN_ROTATION = [0,0,0]
SONY_ROTATION = [0,0,180]
TX_ORIGIN = [148,140.5,24.8]  # full populated XY plus overhead clears north-east case bay
TX_TOP_EXTRA_MM = 20.0  # Clear above the highest populated TX component, full XY envelope.
MAIN_CARRIER_FOOT_XY = [[21,16.5],[22.5,107.5],[125.5,32],[125.5,107.5]]
SONY_CARRIER_FOOT_XY = [[144,134.5],[201,134.5],[144,211.5],[201,204.5]]
MAIN_SD_MOUTH = [62,26.29,44.5]
SONY_SD_MOUTH = [165.16,134.72,68]
MAIN_USB_MOUTH = [39.11,24.73,46.6]
GROUND_PLATE_HOLES_XY = [[20,38.5],[100,35],[20,85],[100,75]]  # custom steel plate; clear MAIN driver and actual components

# Adafruit 4479 / Switch Science 6266, horizontal, vendor CAD axes preserved.
MAG_DIR = ROOT/'parts/parent/interior/cots/adafruit_lis3mdl'
MAG_ORIGIN = [62.78,195,UNIVERSAL_ORIGIN[2]]
MAG_ROTATION = [0,0,90]
MAG_MAST_XY = [28,219]
MAG_SHELF_BOTTOM_Z = UNIVERSAL_ORIGIN[2] - 4.5
MAG_SHELF_THICKNESS = 4.0
MAG_ARM_WIDTH = 5.8
MAG_MAST_RADIUS = 3.0
MAG_BOSS_RADIUS = 2.4
MAG_CLEARANCE_DIAMETER = 2.45
MAG_EDGE_CHAMFER = .15
MAG_PCB_THICKNESS = 1.57  # imported official STEP substrate
MAG_BOLT_LENGTH = 8.0
MAG_BOLT_HEAD_SIZE = [4.0,1.6]  # provisional nylon M2 head diameter/height
MAG_NUT_AF_HEIGHT = [4.0,1.6]  # provisional nylon M2 nut
MAG_QT_PLUG_SIZE = [15,6,5]  # provisional mated plug + straight approach

def magnetometer_vendor():
    """Four plated holes from official EAGLE, never copied mount coordinates."""
    board=ET.parse(MAG_DIR/'ref/Adafruit LIS3MDL.brd').find('.//board')
    packages={(lib.get('name'),p.get('name')):p for lib in board.findall('./libraries/library') for p in lib.findall('./packages/package')}
    holes=[]
    for e in board.findall('./elements/element'):
        if not e.get('package','').startswith('MOUNTINGHOLE'):continue
        for p in packages[(e.get('library'),e.get('package'))].findall('pad'):
            holes.append([float(e.get('x'))+float(p.get('x')),float(e.get('y'))+float(p.get('y')),float(p.get('drill'))])
    assert len(holes)==4 and all(h[2]==2.5 for h in holes)
    return holes

def magnetometer_mounting_xy():
    return [[MAG_ORIGIN[0]-y,MAG_ORIGIN[1]+x] for x,y,d in magnetometer_vendor()]

def universal_mounting_xy():
    margins=[(size-pitch)/2 for size,pitch in zip(UNIVERSAL_SIZE,UNIVERSAL_HOLE_PITCH)]
    return [[UNIVERSAL_ORIGIN[0]+margins[0]+i*UNIVERSAL_HOLE_PITCH[0],
             UNIVERSAL_ORIGIN[1]+margins[1]+j*UNIVERSAL_HOLE_PITCH[1]]
            for j in [0,1] for i in [0,1]]

def power_switch_centres():
    """Switch lever XY from the authoritative PCB footprint/model offsets."""
    text=(ROOT.parent/'hardware/pcb/PARENT_PWR/PARENT_PWR.kicad_pcb').read_text(encoding='utf-8')
    starts=[m.start() for m in re.finditer(r'\(footprint ',text)];out=[]
    for a,b in zip(starts,starts[1:]+[len(text)]):
        t=text[a:b];ref=re.search(r'\(property "Reference" "(SW_PWR|SW_TX)"',t)
        if not ref:continue
        at=re.search(r'\(at ([\d.-]+) ([\d.-]+) ([\d.-]+)',t)
        off=re.search(r'SW_2MD1_lever.step"\s*\(offset\s*\(xyz ([\d.-]+) ([\d.-]+) ([\d.-]+)',t)
        assert at and off
        x,y,angle=map(float,at.groups());ox,oy,oz=map(float,off.groups());angle=math.radians(angle)
        nx=x+ox*math.cos(angle)-oy*math.sin(angle);ny=-y+ox*math.sin(angle)+oy*math.cos(angle)
        out.append([ref[1],PWR_ORIGIN[0]-ny,PWR_ORIGIN[1]+nx])
    assert len(out)==2
    return out

def battery_xy(x,y):
    return [BATTERY_ORIGIN[0]-y,BATTERY_ORIGIN[1]+x]

def vendor_board():
    board = ET.parse(EAGLE).find('.//board')
    packages = {(lib.get('name'), p.get('name')): p for lib in board.findall('./libraries/library') for p in lib.findall('./packages/package')}
    holes = []
    elements = {e.get('name'): e for e in board.findall('./elements/element')}
    for e in elements.values():
        if e.get('package') != 'STAND-OFF': continue
        for h in packages[(e.get('library'), e.get('package'))].findall('hole'):
            holes.append([float(e.get('x'))+float(h.get('x')), float(e.get('y'))+float(h.get('y')), float(h.get('drill'))])
    outline = [w for w in board.findall('./plain/wire') if w.get('layer') == '20']
    size = [max(float(w.get('x1')) for w in outline), max(float(w.get('y1')) for w in outline)]
    assert len(holes) == 4 and all(h[2] > 3.0 for h in holes)
    return size, holes, elements

def box_xy(x, y):
    """Rotate the EAGLE origin 270 degrees, then translate to case coordinates."""
    return [BOARD_ORIGIN[0]-x, BOARD_ORIGIN[1]-y]

def mounting_xy():
    return [box_xy(x, y) for x, y, d in vendor_board()[1]]
# Print-economy revision: geometry parameters, not alternate assembly datums.
FLOOR_GRID_WIDTH = 7.5
FLOOR_GRID_BOTTOM_Z = 8.84
FLOOR_GRID_TOP_Z = 18.8
GNSS_COLUMN_JOINT_Z = 50.0
GNSS_COLUMN_KEY_HEIGHT = .8
GNSS_COLUMN_KEY_CLEARANCE = .2
RACK_RING_JOINT_LOCAL_Z = 3.0
RACK_KEY_DIAMETER = 5.4
RACK_KEY_CLEARANCE = .2
RACK_KEY_HEIGHT = .8
# Simple upper stack: retain PCB heights and existing M3x45 head seat.
SONY_COLUMN_JOINT_Z = 60.5
SONY_COLUMN_KEY_HEIGHT = .8
SONY_COLUMN_KEY_CLEARANCE = .2
SONY_COLUMN_LENGTH = SONY_COLUMN_JOINT_Z - FLOOR_GRID_TOP_Z
SONY_COLUMN_VARIANTS = {'sony_column_left': [7.0, 5.2], 'sony_column_right': [5.4, 4.6]}
