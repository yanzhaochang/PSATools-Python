# DC method to solve power flow
import sys
sys.path.append('..')
import numpy as np

import apis
from apis import apis_system
from apis import apis_basic


def solve_powerflow_with_DC_method(S, Um, Ua):
    '''
    Solve power flow with DC power flow method
    Args:
        (1) S, array, node complex power injection in pu before solution.
        (2) Um, array, initialized node voltage in pu before solution.
        (3) Ua, array, node voltage phase angle in rad before solution.
    Rets: None 
    '''
    print('Solve power flow with DC method')
    P = S.real
    buses = apis.get_all_devices('BUS')
    PQ_num = apis_system.get_system_bus_number('PQ')
    PV_num = apis_system.get_system_bus_number('PV') 
    B1 = apis_system.get_system_Y_network_matrix('B1')
    
    B1_ = B1[0 : PQ_num + PV_num, 0: PQ_num + PV_num]  
    Ua = np.linalg.solve(- B1_, P[0 : PQ_num + PV_num]) # Voltage angle
    
    Ua = np.hstack((Ua, np.zeros(len(buses) - PQ_num - PV_num)))   
        
    for i in range(PQ_num + PV_num, len(buses)):  # Balance node
        ang_d = Ua[i] - Ua
        P[i] = Um[i] * np.sum(Um * (B1[i, :] * np.sin(ang_d)))       
    
    for bus in buses:
        i = apis_system.get_bus_num_after_renumber(bus)
        angle = apis_basic.convert_rad_to_deg(Ua[i])
        apis.set_device_data(bus, 'BUS', 'VA', angle)
    
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        IDE = apis.get_device_data(generator, 'BUS', 'IDE')
        if IDE == 3:
            i = apis_system.get_bus_num_after_renumber(generator)
            SBASE = apis_system.get_system_base_data('SBASE')
            apis.set_device_data(generator, 'GENERATOR', 'PG', P[i] * SBASE)
    return