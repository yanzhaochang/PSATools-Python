# disturbance in dynamic simulation
import sys
sys.path.append('..')

import apis
from apis import apis_system

from .network_solution import solve_dynamic_bus_voltage


def set_bus_fault(bus, Yf):
    '''
    Set bus three phase short circuit fault.
    Args: 
        (1) bus, int, bus number.
        (2) Yf, ground admittance, y+jb
    Rets: None
    '''    
    i = apis_system.get_bus_num_after_renumber(bus)
    Y_mat = apis_system.get_system_Y_network_matrix('dynamic')
    Y_mat[i, i] = Y_mat[i, i] + Yf
    apis_system.set_system_Y_network_matrix('dynamic', Y_mat)
    current_time = apis.get_simulator_parameter('dynamic', 'current_time')
    print('--------set bus {} three phase short circuit at time {:.4f}--------'.format(bus, current_time))
    #solve_dynamic_bus_voltage(True)
    return   

def clear_bus_fault(bus, Yf):
    '''
    Clear bus three phase short circuit fault.
    Args:
        (1) bus, int, bus number.
        (2) Yf, ground admittance, y+jb
    Rets: None
    '''
    i = apis_system.get_bus_num_after_renumber(bus)
    Y_mat = apis_system.get_system_Y_network_matrix('dynamic')
    Y_mat[i, i] = Y_mat[i, i] - Yf
    apis_system.set_system_Y_network_matrix('dynamic', Y_mat)
    current_time = apis.get_simulator_parameter('dynamic', 'current_time')
    print('--------Clear bus {} three phase short circuit at time {:.4f}--------'.format(bus, current_time))
    return 
    
def trip_line(line):
    '''
    Trip line.
    Args:
        line, (ibus, jbus, ckt).
    Rets: None
    '''
    Y_mat = apis_system.get_system_Y_network_matrix('dynamic')
    R = apis.get_device_data(line, 'LINE', 'R')
    X = apis.get_device_data(line, 'LINE', 'X')
    B = apis.get_device_data(line, 'LINE', 'B')
    BI = apis.get_device_data(line, 'LINE', 'BI')
    BJ = apis.get_device_data(line, 'LINE', 'BJ')
    
    i = apis_system.get_bus_num_after_renumber(line[0])
    j = apis_system.get_bus_num_after_renumber(line[1])
    
    Yij = 1.0 / complex(R, X)
    Yi = 0.5j * B + 1j * BI
    Yj = 0.5j * B + 1j * BJ    
    
    Y_mat[i, i] = Y_mat[i, i] - Yi
    Y_mat[j, j] = Y_mat[j, j] - Yj
    Y_mat[i, i] = Y_mat[i, i] - Yij - Yi 
    Y_mat[j, j] = Y_mat[j, j] - Yij - Yj
    apis_system.set_system_Y_network_matrix('dynamic', Y_mat)
    current_time = apis.get_simulator_parameter('dynamic', 'current_time')
    print('--------Trip line {} at time {:.4f}--------'.format(line, current_time))    
    return