# 暂态仿真的节点导纳阵并入发电机内导纳
import sys
sys.path.append('..')
import numpy as np

import apis
from apis import apis_basic
from apis import apis_system


def calculate_dynamic_Y_matrix():
    '''
    Calculate the network node admittance matrix needed for dynamic simulation.
    The load is equivalent to a constant admittance and incorporated into the generator impedance
    Args: None
    Rets: None
    '''
    Y_mat = apis_system.get_system_Y_network_matrix('basic')
    SBASE = apis_system.get_system_base_data('SBASE')
    loads = apis.get_all_devices('LOAD')
    for load in loads:
        VM = apis.get_device_data(load, 'BUS', 'VM')
        PL = apis.get_device_data(load, 'LOAD', 'PL')
        QL = apis.get_device_data(load, 'LOAD', 'QL')
        
        i = apis_system.get_bus_num_after_renumber(load)
        Y_mat[i, i] = Y_mat[i, i] + (PL - 1j*QL) / SBASE / VM**2
        
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        YGp = calculate_generator_internal_admittance(generator)
        i = apis_system.get_bus_num_after_renumber(generator)
        Y_mat[i, i] = Y_mat[i, i] + YGp
    
    return Y_mat
    
def calculate_generator_internal_admittance(generator):
    '''
    Calculate the internal admittance YGP of generator connected to grid
    Args:
        generator, generator bus number, int
    Rets:
        YGp, generator internal admittance connected to grid, float, complex
    '''
    GMN = apis.get_generator_related_model_data(generator, 'GEN', 'GMN')
    SBASE = apis_system.get_system_base_data('SBASE')
    MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    if GMN == 'GENCLS':
        # The d-axis reactance of the second order model is stored in the power flow database.
        Xd = apis.get_device_data(generator, 'GENERATOR', 'ZX')
        Xd = Xd * SBASE / MBASE  # Convert reactance from machine base to system base.
        YGp = 1.0 / (1j * Xd)
        
    else:
        if GMN == 'GENROU' or GMN == 'GENSAL':
            Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xdpp')
            Xq = apis.get_generator_related_model_data(generator, 'GEN', 'Xqpp')
            
        elif GMN == 'GENTRA':
            Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xdp')
            Xq = apis.get_generator_related_model_data(generator, 'GEN', 'Xq')
            
        else:
            Xd = 0.0
            Xq = 0.0
        Xd = Xd * SBASE / MBASE  # Convert reactance from machine base to system base.
        Xq = Xq * SBASE / MBASE
        YGp = -0.5j * (Xd + Xq) / (Xd * Xq)
        
    return YGp
