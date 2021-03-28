# fault analysis
import numpy as np
import sys
sys.path.append('..')

import apis
from apis import apis_system
from apis import apis_basic

import network


def solve_bus_asymmetry_fault(node, fault_type, Zf):
    '''
    Solve the bus asymmetric short circuit fault after the situation.
    Args:
        (1) node, int, fault bus number.
        (2) fault_type, fault type.
        (3) Zf, grounding impedance.
    Rets: None
    '''
    VM = apis.get_device_data(node, 'BUS', 'VM')
    VA = apis.get_device_data(node, 'BUS', 'VA')
    U0 = apis_basic.build_complex_value(VM, VA)
    
    network.build_network_Y_matrix('positive')
    network.build_network_Y_matrix('negative')
    network.build_network_Y_matrix('zero')
    
    ibus = apis_system.get_bus_num_after_renumber(node)
    Z1 = get_network_Z_matrix_element(ibus, ibus, 'positive')
    Z2 = get_network_Z_matrix_element(ibus, ibus, 'negative')
    Z0 = get_network_Z_matrix_element(ibus, ibus, 'zero')
    
    print('------------------------------------')
    print('equivalent impedance from bus {}'.format(node))
    print('positive: {:.5f}, negative: {:.5f}, zero: {:.5f}'.format(Z1, Z2, Z0))
    
    if fault_type == 'single phase grounding':
        If1 = U0 / (Z1 + Z2 + Z0 + 3 * Zf) 
        If2 = If1
        If0 = If1
        
    elif fault_type == 'two phase short circuit':
        If1 = U0 / (Z1 + Z2 + Zf)
        If2 = - If1
        If0 = 0.0
        
    elif fault_type == 'two phase short circuit grounding':
        If1 = U0 / (Z1 + (Z2 * (Z0 + 3 * Zf) / (Z2 + Z0 + 3 *Zf)))
        If2 = - If1 * (Z0 + 3 * Zf) / (Z2 + 3 * Zf)
        If0 = - If1 * Z2 / (Z2 + 3 * Zf)    
        
    elif fault_type == 'three phase grounding':
        If1 = U0 / (Z1 + Zf)
        If2, If0 = 0.0, 0.0 
        
    else:
        print('parameter {} is wrong'.format(fault_type))
        return
    
    If = (If1, If2, If0)
    print('------------------------------------')
    print('short circuit current at bus {}'.format(node))
    print('positive: {:.3f},  negative: {:.3f},  zero: {:.3f}'.format(If1, If2, If0))  
    (Ia, Ib, Ic) = apis_basic.composite_three_phase_vector(If)
    print('phase A: {:.3f},  phase B: {:.3f},  phase C: {:.3f}'.format(Ia, Ib, Ic))
    update_bus_sequence_voltage(node, If)
    show_analysis_result()
    return
    
def get_network_Z_matrix_element(row, column, par_type):
    '''
    Get a value of node impedance matrix in a row and a column.
    Because the admittance matrix is symmetric, the impedance matrix is also symmetric, meeting condition Zij=Zji.
    Args:
        (1) row, int, row number.
        (2) column, int, column number.
        (3) par_type, str, Z matrix type, 'positive', 'negative' and 'zero'.
    Rets:
        value, Z matrix value located at (row, column).
    '''
    Y_mat = apis_system.get_system_Y_network_matrix(par_type)
    buses = apis.get_all_devices('BUS')
    I = np.zeros(len(buses))
    I[row] = 1.0
    U = np.linalg.solve(Y_mat, I)
    value = U[column]   
    return value
    
def update_bus_sequence_voltage(node, If):
    '''
    Update the bus sequence voltage in the database.
    Args:
        (1) node, int, fault bus number.
        (2) If, tuple, sequence current of short circuit node, (If1, If2, If3).
    Rets: None
    '''
    ibus = apis_system.get_bus_num_after_renumber(node)
    (If1, If2, If0) = If
    
    buses = apis.get_all_devices('BUS')
    for bus in buses:
        VM = apis.get_device_data(bus, 'BUS', 'VM')
        VA = apis.get_device_data(bus, 'BUS', 'VA')
        U0 = apis_basic.build_complex_value(VM, VA)
        
        i = apis_system.get_bus_num_after_renumber(bus)
        
        Z1 = get_network_Z_matrix_element(i, ibus, 'positive')
        Z2 = get_network_Z_matrix_element(i, ibus, 'negative')
        Z0 = get_network_Z_matrix_element(i, ibus, 'zero')  
        
        VP = U0 - Z1 * If1
        VN = - Z2 * If2
        VZ = - Z0 * If0
        apis.set_device_sequence_data(bus, 'BUS', 'VP', VP)
        apis.set_device_sequence_data(bus, 'BUS', 'VN', VN)
        apis.set_device_sequence_data(bus, 'BUS', 'VZ', VZ)
    return    
    
def show_analysis_result():
    '''
    Show the node sequence voltage results of short circuit analysis.
    Args: None
    Rets: None
    '''
    print('------------------------------------')
    print('bus sequence voltage result')
    print('BUS   ----   VP   ----   VN   ----   VZ')
    buses = apis.get_all_devices('BUS')
    for bus in buses:
        VP = apis.get_device_sequence_data(bus, 'BUS', 'VP')
        VN = apis.get_device_sequence_data(bus, 'BUS', 'VN')
        VZ = apis.get_device_sequence_data(bus, 'BUS', 'VZ')
        print('#{}  {:.3f}  {:.3f}  {:.3f} '.format(bus, VP, VN, VZ))
    return    
    
    