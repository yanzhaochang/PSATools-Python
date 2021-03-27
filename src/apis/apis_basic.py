# basic method
from math import pi, cos, sin, sqrt, atan
import numpy as np


def build_complex_value(VM, VA):
    '''
    Build complex number  by amplitude and phase angle, and the phase angle is rad radian.
    Args:
        (1) VM, amplitude.
        (2) VA, phase angle in rad.
    Rets: 
        value, complex number with the format a+jb.
    '''
    value = VM * (cos(VA) + 1j * sin(VA))
    return value
    
def convert_deg_to_rad(angle):
    '''
    Convert angle from deg to rad.
    Args:
        angle, angle in deg.
    Rets:
        angle, angle in rad.
    '''
    angle = angle * pi / 180.0
    return angle

def convert_rad_to_deg(angle):
    '''
    Convert angle from rad to deg.
    Args:
        angle, angle in rad.
    Rets:
        angle, angle in deg.
    '''
    angle = angle * 180.0 / pi
    return angle

def get_complex_phase_angle(value):
    '''
    Get complex phase angle in rad.
    Args:
        value, complex.
    Rets:
        angle, phase angle in rad. 
    '''
    angle = atan(value.imag / value.real)
    return angle
    
def convert_xy_to_dq(derta, Ax, Ay):
    '''
    Convert the value of the xy frame to the value of the dq frame.
    Args:
        (1) derta, angle in rad.
        (2)(3) Ax, Ay,  x-component and y-component.
    Rets:
        (1)(2) Ad, Aq, d-component and q-component.
    '''
    convert_mat = np.array([[sin(derta), -cos(derta)], [cos(derta), sin(derta)]])
    Axy_mat = np.array([[Ax], [Ay]])
    Adq_mat = np.dot(convert_mat, Axy_mat)
    Ad, Aq = Adq_mat[0, 0], Adq_mat[1, 0]
    return Ad, Aq
    
def composite_three_phase_vector(Fa):
    '''
    Calculate three phase asymmetry vector from sequence component.
    Args:
        Fa, tuple, sequence component, (Fa1, Fa2, Fa0), (positive, negative, zero).
    Rets:
        F, A. B, C three phase components, (Fa, Fb, Fc).
    '''
    (Fa1, Fa2, Fa0) = Fa
    a = -0.5 + sqrt(3) * 0.5j  
    
    Fa = Fa1 + Fa2 + Fa0
    Fb = a ** 2 * Fa1 + a * Fa2 + Fa0
    Fc = a * Fa1 + a ** 2 * Fa2 + Fa0
    
    return (Fa, Fb, Fc)