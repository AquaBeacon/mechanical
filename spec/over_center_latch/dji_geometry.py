"""B-mounted extended hood, short links and a planar 80-degree groove.

The finished toe's upper bearing point K slides beneath the flat retaining
ledge. EPDM backs the inclined toe face. Once K clears the ledge, the free pose is a clearance
path, not a prediction of a hands-free trajectory. XZ / mm / N.
"""
import math
import numpy as np
from scipy.optimize import brentq

def rotation(deg):
    t=math.radians(deg)
    return np.array([[math.cos(t),-math.sin(t)],[math.sin(t),math.cos(t)]])

def closed_angle(v): return v['closed_angle_deg']
def catch_height(v): return v['catch_height']
def B_at(v,theta):
    return np.array([0.,v['axis_height']])+v['AB_length']*np.array([math.cos(math.radians(theta)),math.sin(math.radians(theta))])

def contact_geometry(v):
    B=B_at(v,closed_angle(v));C=np.array([v['catch_distance'],v['catch_height']])
    left=v['toe_face_x']+v['toe_half_height']/math.tan(math.radians(v['groove_angle_deg']))
    K=C+np.array([left+v['toe_contact_inset'],v['toe_half_height']])
    Q=C+np.array([v['toe_face_x'],0.])
    t=math.radians(v['groove_angle_deg']);n=np.array([math.sin(t),-math.cos(t)]);u=np.array([math.cos(t),math.sin(t)])
    return B,C,K,Q,n,u

def pose(v,theta,lift=0,separate=0):
    B0,C0,K0,Q0,n,u=contact_geometry(v);B=B_at(v,float(theta));D=K0-B0
    ratio=(K0[1]-B[1])/np.linalg.norm(D)
    if abs(ratio)>=1:raise ValueError('Keeper contact branch is unreachable')
    delta=math.degrees(math.asin(ratio)-math.atan2(D[1],D[0]))+float(lift)
    R=rotation(delta);C=B+R@(C0-B0);Q=B+R@(Q0-B0);K=B+R@D
    phi0=math.degrees(math.atan2(C0[1]-B0[1],C0[0]-B0[0]))
    contact_local=rotation(-delta)@(K-B)-(C0-B0)
    left=v['toe_face_x']+v['toe_half_height']/math.tan(math.radians(v['groove_angle_deg']))
    finite=(K[0]<=v['catch_distance']+v['lip_end']-v['contact_chamfer']+1e-8 and not lift)
    return dict(B=[float(B[0]),0,float(B[1])],C=[float(C[0]),0,float(C[1])],
                S=[v['catch_distance']+separate,0,v['catch_height']],Q=[float(Q[0]),0,float(Q[1])],
                K=[float(K[0]),0,float(K[1])],delta_deg=delta,phi=phi0+delta,
                loop_angle=delta,contact_active=bool(finite),contact_edge_coordinate_mm=float(contact_local[0]))

def compression_samples(v,theta):
    B0,C0,K,Q0,n,u=contact_geometry(v);p=pose(v,theta);R=rotation(p['delta_deg']);nh=R@n
    Q=np.array(p['Q'])[[0,2]];wall=Q0-n*(v['epdm_thickness']-v['preload'])
    positions=np.linspace(-v['epdm_height']/2,v['epdm_height']/2,101)+v.get('epdm_tangent_offset',0.)
    surface=wall[None,:]+positions[:,None]*u
    gap=((Q-surface)@nh)/float(n@nh)
    locations=surface+gap[:,None]*n
    along=(locations-Q)@(R@u)
    active=(np.abs(along)<=v['toe_half_height']/math.sin(math.radians(v['groove_angle_deg']))+1e-7)
    if not p['contact_active']:active[:]=False
    delta=np.where(active,np.maximum(0,v['epdm_thickness']-gap),0.)
    return positions,delta,gap,locations

def rubber_force(v,theta,hardness=65):
    from rubber_estimate import modulus
    x,delta,gap,points=compression_samples(v,theta)
    lam=1-delta/v['epdm_thickness']
    if lam.min()<=0:raise ValueError('Rubber crushed against hard wall')
    pressure=modulus(hardness)/3*(lam**-2-lam)
    f=v['epdm_width']*np.trapezoid(pressure,x)
    Q=(v['epdm_width']*np.trapezoid(points*pressure[:,None],x,axis=0)/f) if f>1e-10 else contact_geometry(v)[3]
    return float(f),Q,float(delta.max())

def load_at(v,theta):
    B0,C0,K0,Q0,n,u=contact_geometry(v);p=pose(v,theta);K=np.array(p['K'])[[0,2]];B=np.array(p['B'])[[0,2]];R=rotation(p['delta_deg'])
    force,Q,comp=rubber_force(v,theta)
    # Work-conjugate contact force for normal gap strain: the rotating claw
    # normal is divided by its projection on the fixed sheet normal.
    nh=R@n;contact_normal=nh/float(n@nh)
    H=B+R@(np.array([v.get('hand_load_x',v['handle_back']+3),v['hood_top']])-B0)
    link=(B-np.array([0.,v['axis_height']]))/v['AB_length'];roof=np.array([0.,-1.])
    def cross(a,b):return a[0]*b[1]-a[1]*b[0]
    matrix=np.array([[link[0],roof[0],0],[link[1],roof[1],-1],
                     [0,cross(K-B,roof),cross(H-B,[0,-1])]])
    T,N,F=np.linalg.solve(matrix,-force*np.array([contact_normal[0],contact_normal[1],cross(Q-B,contact_normal)]))
    contact=force*contact_normal+N*roof
    return dict(angle_deg=float(theta),compression_mm=comp,normal_rubber_N=force,
        clamp_horizontal_N=float(contact[0]),gasket_N=float(contact[0]),link_N=float(T),lip_N=float(N),
        hand_vertical_N=float(F),link_force_on_hood=[float(T*link[0]),0,float(T*link[1])],
        rubber_force_on_hook=[float(force*contact_normal[0]),0,float(force*contact_normal[1])],
        lip_force_on_hook=[float(N*roof[0]),0,float(N*roof[1])],
        rubber_point=[float(Q[0]),0,float(Q[1])],hand_point=[float(H[0]),0,float(H[1])],**p)

def dead_angle(v):
    def f(th):return load_at(v,th)['hand_vertical_N']
    xs=np.linspace(v['open_angle'],closed_angle(v),121)
    brackets=[(a,b) for a,b in zip(xs[:-1],xs[1:]) if f(a)>0 and f(b)<0]
    if not brackets:raise ValueError('No restoring-moment reversal before closure')
    return float(brentq(f,*brackets[-1]))

def over_center(v,theta):
    q=load_at(v,theta)
    return -q['hand_vertical_N']*abs(q['hand_point'][0]-q['B'][0])/max(q['normal_rubber_N'],1e-10)

def tip_moment_arm(v,theta):
    q=load_at(v,theta);return abs(q['hand_point'][0]-q['B'][0])

def dimensions(v):
    return dict(closed_angle=closed_angle(v),lever_half=v['base_bearing_width']/2,
        base_inner=0,base_outer=v['base_bearing_width']/2,
        link_inner=v['base_bearing_width']/2+v['print_clearance'],
        link_outer=v['base_bearing_width']/2+v['print_clearance']+v['link_thickness'],
        hood_inner=v['base_bearing_width']/2+2*v['print_clearance']+v['link_thickness'],
        hood_outer=v['base_bearing_width']/2+2*v['print_clearance']+v['link_thickness']+v['hood_cheek_thickness'])

def mounting_holes(v):
    return {'base':[(x,y) for x in [v['platform_base_x1'],v['platform_base_x2']] for y in [-v['platform_mount_y'],v['platform_mount_y']]],
            'keeper':[(v['platform_keeper_x'],y) for y in [-v['platform_mount_y'],v['platform_mount_y']]]}

def layout(v,theta=None,lift=0,separate=0,hardware=True,guide=True):
    theta=closed_angle(v) if theta is None else theta;p=pose(v,theta,lift,separate);d=dimensions(v)
    entries=[('base','base',[0,0,0],0,'SlateGray'),
             ('bail','link_left',[0,-d['link_outer'],v['axis_height']],-theta,'Orange'),
             ('bail','link_right',[0,d['link_inner'],v['axis_height']],-theta,'Orange'),
             ('lever','lever',p['B'],-p['delta_deg'],'SteelBlue'),
             ('keeper','keeper',[v['catch_distance']+separate,0,0],0,'SeaGreen')]
    if hardware:entries += [('axis_a','axis_a',[0,0,v['axis_height']],0,'Silver'),('axis_b','axis_b',p['B'],0,'Silver')]
    entries += [('epdm','epdm',[v['catch_distance']+separate,0,0],0,'Black')]
    return [dict(part='parts/common/jigs/over_center_latch',file='over_center_latch_'+stem,label=label,color=color,
                 ops=[{'translate':pos},{'rotate':[0,rot,0]}]) for stem,label,pos,rot,color in entries]

def calibrate_preload(v):
    def f(preload):
        return load_at(dict(v,preload=preload),closed_angle(v))['clamp_horizontal_N']-v['design_clamp_force_N']
    return float(brentq(f,.001,v['epdm_thickness']*.45))
