import sys
sys.path.append('..')
import numpy as np

import apis
from apis import apis_system

from .hvdc import correct_hvdc_node_power


def solve_powerflow_with_PQ_method(S, Um, Ua):
    '''
    Main function of Newton Raphson method in power flow calculation
    Args:
        (1) S, array, node complex power injection in pu before solution.
        (2) Um, array, initialized node voltage in pu before solution.
        (3) Ua, array, node voltage phase angle in rad before solution.
    Rets:
        (1) S, array, node complex power injection in pu after solution.
        (2) Um, array, initialized node voltage in pu after solution.
        (3) Ua, array, node voltage phase angle in rad after solution.
    ''' 
    k = 0  
    k_max = apis_system.get_simulator_parameter('powerflow', 'k_max')
    max_err = apis_system.get_simulator_parameter('powerflow', 'max_err')
    
    while True:
        if k >= k_max:
            break
            
        P, Q = S.real, S.imag  
        
        P_err = calculate_act_power_imbalance(P, Um, Ua)  
        Ua = correct_node_voltage_angle(P_err, Um, Ua)  
        
        Q_err = calculate_ract_power_imbalance(Q, Um, Ua)  
        Um = correct_node_voltage(Q_err, Um, Ua)  
        
        power_err = np.hstack((P_err, Q_err))   
            
        S = correct_hvdc_node_power(S, Um)  
    
        if np.max(np.abs(power_err)) < max_err:  
            break
    
        k = k + 1
    
    print('Iteration number of PQ method: {}'.format(k))
    
    return S, Um, Ua

def calculate_act_power_imbalance(P, Um, Ua): 
    '''
    Calculate node active power unbalance.
    Args: 
        (1) P, array, node active power injection in pu.
        (2) Um, array, node voltage in pu.
        (3) Ua, array, node voltage angle in rad.
    Rets:
        P_err, array, active power unbalance in pu.
    '''
    PQ_num = apis_system.get_system_bus_number('PQ')
    PV_num = apis_system.get_system_bus_number('PV') 
    Y_mat = apis_system.get_system_Y_network_matrix('basic')
    P_err = np.zeros(PQ_num + PV_num)  
    
    for i in range(PQ_num + PV_num):  
        ang_d = Ua[i] - Ua  
        P_err[i] = P[i] - Um[i] * np.sum(Um * (Y_mat[i, :].real * np.cos(ang_d) + Y_mat[i, :].imag * np.sin(ang_d)))
        P_err[i] = P_err[i] / Um[i]
        
    return P_err 

def correct_node_voltage_angle(P_err, Um, Ua):
    '''
    Correct node voltage angle.
    Args:
        (1) P_err, array, active power unbalance in pu.
        (2) Um, array, node voltage in pu.
        (3) Ua, array, node voltage angle in rad.
    Rets:
        Ua, array, node voltage angle in rad.
    '''
    B1 = apis_system.get_system_Y_network_matrix('B1')
    B1 = B1.real
    B1 = B1[0 : np.size(P_err), 0 : np.size(P_err)]  # format B' matrix 
    angle_correction = np.linalg.solve(- B1, P_err)
    for i in range(np.size(P_err)):
        Ua[i] = Ua[i] + angle_correction[i] / Um[i]  
        
    return Ua
    
def calculate_ract_power_imbalance(Q, Um, Ua): 
    '''
    Calculate node reactive power unbalance.
    Args: 
        (1) Q, array, node active power injection in pu.
        (2) Um, array, node voltage in pu.
        (3) Ua, array, node voltage angle in rad.
    Rets:
        Q_err, array, node reactive power unbalance in pu.
    ''' 
    PQ_num = apis_system.get_system_bus_number('PQ')
    Y_mat = apis_system.get_system_Y_network_matrix('basic')
    Q_err = np.zeros(PQ_num)
    
    for i in range(PQ_num):
        ang_d = Ua[i] - Ua
        Q_err[i] = Q[i] - Um[i] * np.sum(Um * (Y_mat[i, :].real * np.sin(ang_d) - Y_mat[i, :].imag * np.cos(ang_d)))
        Q_err[i] = Q_err[i] / Um[i]
        
    return Q_err  
    
def correct_node_voltage(Q_err, Um, Ua):
    '''
    Correct node voltage.
    Args: 
        (1) Q_err, array, reactive power unbalance in pu.
        (2) Um, array, node voltage in pu.
        (3) Ua, array, node voltage angle in rad.
    Rets:
        Um, array, node voltage in pu.
    '''
    B2 = apis_system.get_system_Y_network_matrix('B2')
    B2 = B2.real
    B2 = B2[0 : np.size(Q_err), 0 : np.size(Q_err)]  # format B" matrix 
    voltage_correction = np.linalg.solve(- B2, Q_err) 
    for i in range(np.size(Q_err)):
        Um[i] = Um[i] + voltage_correction[i] 
        
    return Um
