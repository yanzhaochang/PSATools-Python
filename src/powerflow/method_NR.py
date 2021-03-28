import sys
sys.path.append('..')
import numpy as np

import apis
from apis import apis_system

from .hvdc import correct_hvdc_node_power


def solve_powerflow_with_NR_method(S, Um, Ua):
    '''
    Main function of Newton Raphson method in power flow calculation.
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
            
        power_err = calculate_power_imbalance(S, Um, Ua)  

        if np.max(np.abs(power_err)) < max_err:  
            break
        
        J_mat = build_jacobian_matrix(Um, Ua)  
            
        Um, Ua = correct_node_voltage_and_angle(power_err, Um, Ua, J_mat)  
        S = correct_hvdc_node_power(S, Um)  # Correct HVDC injection power
    
        k = k + 1
    
    print('------------------------------------')
    print('Iteration number of NR method: {}'.format(k))
    
    return S, Um, Ua    
    
def calculate_power_imbalance(S, Um, Ua): 
    '''
    Calculate power unbalance in pu.
    Args:
        (1) S, array, node complex power injection in pu.
        (2) Um, array, initialized node voltage in pu.
        (3) Ua, array, node voltage phase angle in rad.
    Rets:
        power_err, array, power unbalance in pu.
    '''
    PQ_num = apis_system.get_system_bus_number('PQ')
    PV_num = apis_system.get_system_bus_number('PV') 
    p_err, q_err = np.zeros(PQ_num + PV_num), np.zeros(PQ_num)  
    Y_mat = apis_system.get_system_Y_network_matrix('basic')

    for i in range(PQ_num + PV_num):  # Calculate the active power unbalance of PQ node and PV node
        ang_d = Ua[i] - Ua  
        p_err[i] = S[i].real - Um[i] * np.sum(Um * (Y_mat[i, :].real * np.cos(ang_d) + Y_mat[i, :].imag * np.sin(ang_d)))

    for i in range(PQ_num):  # Calculation of reactive power unbalance of PQ node 
        ang_d = Ua[i] - Ua
        q_err[i] = S[i].imag - Um[i] * np.sum(Um * (Y_mat[i, :].real * np.sin(ang_d) - Y_mat[i, :].imag * np.cos(ang_d)))
    
    power_err = np.hstack((p_err, q_err))  
    
    return power_err 
    
def build_jacobian_matrix(Um, Ua): 
    '''
    Build Jacobian matrix for NR solution
    Args:
        (1) Um, array, initialized node voltage in pu.
        (2) Ua, array, node voltage phase angle in rad.
    Rets：
        J_mat, array, Jacobian matrix.
    '''
    PQ_num = apis_system.get_system_bus_number('PQ')
    PV_num = apis_system.get_system_bus_number('PV') 
    Y_mat = apis_system.get_system_Y_network_matrix('basic')
    G, B = Y_mat.real, Y_mat.imag  
    
    H = np.zeros((PQ_num + PV_num, PQ_num + PV_num))  
    N = np.zeros((PQ_num + PV_num, PQ_num))  
    M = np.zeros((PQ_num, PQ_num + PV_num))  
    L = np.zeros((PQ_num, PQ_num))  
    
    for i in range(PQ_num + PV_num):  # H matrix
        for j in range(PQ_num + PV_num):        
            if i != j:  
                ang_d = Ua[i] - Ua[j]
                H[i, j] = - Um[i] * Um[j] * (G[i, j] * np.sin(ang_d) - B[i, j] * np.cos(ang_d))  
            else:  
                ang_d = Ua[i] - Ua
                H[i, i] = Um[i] * np.sum(Um * (G[i, :] * np.sin(ang_d) - B[i, :] * np.cos(ang_d))) + Um[i] ** 2 * B[i, i] 
    
    for i in range(PQ_num + PV_num):  # N matrix 
        for j in range(PQ_num):
            if i != j:  
                ang_d = Ua[i] - Ua[j]
                N[i, j] = - Um[i] * Um[j] * (G[i, j] * np.cos(ang_d) + B[i, j] * np.sin(ang_d)) 
            else:  
                ang_d = Ua[i] - Ua
                N[i, i] = - Um[i] * np.sum(Um * (G[i, :] * np.cos(ang_d) + B[i, :] * np.sin(ang_d))) - Um[i] ** 2 * G[i, i]
    
    for i in range(PQ_num):  # M matrix
        for j in range(PQ_num + PV_num):
            if i != j:  
                ang_d = Ua[i] - Ua[j]
                M[i, j] = Um[i] * Um[j] * (G[i, j] * np.cos(ang_d) + B[i, j] * np.sin(ang_d))
            else:  
                ang_d = Ua[i] - Ua
                M[i, i] = - Um[i] * np.sum(Um * (G[i, :] * np.cos(ang_d) + B[i, :] * np.sin(ang_d))) + Um[i] ** 2 * G[i, i]      
    
    for i in range(PQ_num):  # L matrix
        for j in range(PQ_num):
            if i != j:  
                ang_d = Ua[i] - Ua[j]
                L[i, j] = - Um[i] * Um[j] * (Y_mat[i, j].real * np.sin(ang_d) - Y_mat[i, j].imag * np.cos(ang_d))
            else:  
                ang_d = Ua[i] - Ua
                L[i, i] = - Um[i] * np.sum(Um * (G[i, :] * np.sin(ang_d) - B[i, :] * np.cos(ang_d))) + Um[i] ** 2 * B[i, i]        
     
    J_mat = np.vstack((np.hstack((H, N)), np.hstack((M, L))))  # Combine Jacobian matrix
    
    return J_mat

def correct_node_voltage_and_angle(power_err, Um, Ua, J_mat):
    '''
    Solve the modified equation of NR method and correct the node voltage and phase angle.
    Args:
        (1) power_err, array, power balance in pu.
        (2) Um, array, node voltage in pu.
        (3) Ua, array, node voltage angle in rad.
        (4) J_mat, array, Jacobian matrix.
    输出:
        (1) Um, array, node voltage in pu.
        (2) Ua, array, node voltage angle in rad.
    '''
    PQ_num = apis_system.get_system_bus_number('PQ')
    PV_num = apis_system.get_system_bus_number('PV')  
    
    angle_voltage_correction = np.linalg.solve(- J_mat, power_err)  
    
    angle_correction = angle_voltage_correction[0 : PQ_num + PV_num]  
    voltage_correction = angle_voltage_correction[PQ_num + PV_num : ] 
    
    for i in range(PQ_num): 
        Um[i] = Um[i] + Um[i] * voltage_correction[i]     
    
    for i in range(PQ_num + PV_num): 
        Ua[i] = Ua[i] + angle_correction[i]    
       
    return Um, Ua           