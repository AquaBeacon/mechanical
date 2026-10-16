"""Provisional EPGR-01 estimate, NOT measured rubber/contact properties.

Hardness65 is manufacturer's listing; assuming Shore A for Gent conversion.
Unconfined neo-Hookean strips under a cylindrical nose omit lateral coupling,
bonding, friction and ply adhesive. A useful initial shim setting, not a rating.
"""
import numpy as np

def modulus(shore_a):
    return .0981*(56+7.62336*shore_a)/(.137505*(254-2.54*shore_a))

def force(v,compression,centre_z=None,hardness=65):
    r=v['catch_diameter']/2
    centre_z=v['catch_height'] if centre_z is None else centre_z
    z=np.linspace(v['catch_height']+v['epdm_z_offset']-v['epdm_height']/2,
                  v['catch_height']+v['epdm_z_offset']+v['epdm_height']/2,401)
    offset=z-centre_z
    contact=np.abs(offset)<r
    delta=np.where(contact,np.maximum(0.,compression-r+np.sqrt(np.maximum(0.,r*r-offset*offset))),0.)
    stretch=1-delta/v['epdm_thickness']
    if np.min(stretch)<=0:raise ValueError('Rubber completely crushed')
    stress=modulus(hardness)/3*(stretch**-2-stretch)
    return float(v['epdm_width']*np.trapezoid(stress,z))
