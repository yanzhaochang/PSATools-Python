import sys
import numpy as np
sys.path.append('..')

import apis
from apis import apis_system


def calculate_network_Y_matrix(c=True, r=True):
    '''
    Calculate system Y matrix for power flow solution.
    Args:
        (1) c, bool, considering the charging capacitance and the nonstandard transformer ratio.
        (2) r, bool, considering branch resistance.
    Rest:
        Y_mat: nodal admittance matrix, array.
    '''
    buses = apis.get_all_devices('BUS')
    Y_mat = np.zeros((len(buses), len(buses)), dtype = complex)  
    lines = apis.get_all_devices('LINE')
    transformers = apis.get_all_devices('TRANSFORMER')
    
    for line in lines:  
        i = apis_system.get_bus_num_after_renumber(line[0])
        j = apis_system.get_bus_num_after_renumber(line[1])
 
        Yij, Yi, Yj = build_line_equivalent_circuit(line, c, r)
        
        Y_mat[i, j] = Y_mat[i, j] - Yij 
        Y_mat[j, i] = Y_mat[j, i] - Yij
        Y_mat[i, i] = Y_mat[i, i] + Yij + Yi 
        Y_mat[j, j] = Y_mat[j, j] + Yij + Yj 
    
    for transformer in transformers:
        if transformer[2] == 0:
            i = apis_system.get_bus_num_after_renumber(transformer[0])
            j = apis_system.get_bus_num_after_renumber(transformer[1])
            
            Yij, Yi, Yj = build_transformer2_equivalent_circuit(transformer, c, r)
        
            Y_mat[i, j] = Y_mat[i, j] - Yij
            Y_mat[j, i] = Y_mat[j, i] - Yij
            Y_mat[i, i] = Y_mat[i, i] + Yij + Yi   
            Y_mat[j, j] = Y_mat[j, j] + Yij + Yj 
            
        else:
            i = apis_system.get_bus_num_after_renumber(transformer[0])
            j = apis_system.get_bus_num_after_renumber(transformer[1])   
            k = apis_system.get_bus_num_after_renumber(transformer[2])
            
            trans3_Y_mat = build_transformer3_equivalent_circuit(transformer, c, r)
        
            Y_mat[i, i] = Y_mat[i, i] + trans3_Y_mat[0, 0]
            Y_mat[i, j] = Y_mat[i, j] + trans3_Y_mat[0, 1]
            Y_mat[i, k] = Y_mat[i, k] + trans3_Y_mat[0, 2]
            Y_mat[j, i] = Y_mat[j, i] + trans3_Y_mat[1, 0]
            Y_mat[j, j] = Y_mat[j, j] + trans3_Y_mat[1, 1]
            Y_mat[j, k] = Y_mat[j, k] + trans3_Y_mat[1, 2]
            Y_mat[k, i] = Y_mat[k, i] + trans3_Y_mat[2, 0]
            Y_mat[k, j] = Y_mat[k, j] + trans3_Y_mat[2, 1]
            Y_mat[k, k] = Y_mat[k, k] + trans3_Y_mat[2, 2]

    if c is True:
        shunts = apis.get_all_devices('SHUNT')
        for shunt in shunts:  
            i = apis_system.get_bus_num_after_renumber(shunt)
            BL = apis.get_device_data(shunt, 'SHUNT', 'BL')
            SBASE = apis_system.get_system_base_data('SBASE')
            Y_mat[i, i] = Y_mat[i, i] + 1j * BL / SBASE

    return Y_mat
    
def build_line_equivalent_circuit(line, c, r):
    '''
    Build equivalent circuit of transmission line.
    Args:
        (1) line, tuple, (IBUS, JBUS, CKT).
        (2) c, bool, considering the charging capacitance and the nonstandard transformer ratio.
        (3) r, bool, considering branch resistance.
    Rets:
        (1) Yij, mutual admittance.
        (2) Yi, I-side self admittance.
        (3) Yj, J-side self admittance.
    '''
    R = apis.get_device_data(line, 'LINE', 'R')
    X = apis.get_device_data(line, 'LINE', 'X')
    Yij = 1.0 / complex(R, X)
    if r is False:
        Yij = 1.0 / (1j * X)
        
    B = apis.get_device_data(line, 'LINE', 'B') 
    BI = apis.get_device_data(line, 'LINE', 'BI')
    BJ = apis.get_device_data(line, 'LINE', 'BJ')
    
    Yi = 0.5j * B + 1j * BI
    Yj = 0.5j * B + 1j * BJ
    if c is False:
        Yi, Yj = 0.0, 0.0
        
    return Yij, Yi, Yj 
    
def build_transformer2_equivalent_circuit(transformer, c, r):
    '''
    Build equivalent circuit of two winding transformer.
    Args:
        (1) transformer, tuple, (IBUS, JBUS, KBUS).
        (2) c, bool, considering the charging capacitance and the nonstandard transformer ratio.
        (3) r, bool, considering branch resistance.      
    Rets:
        (1) Yij, mutual admittance.
        (2) Yi, I-side self admittance.
        (3) Yj, J-side self admittance.
    '''
    MAG1 = apis.get_device_data(transformer, 'TRANSFORMER', 'MAG1')
    MAG2 = apis.get_device_data(transformer, 'TRANSFORMER', 'MAG2')
    exci_admit = complex(MAG1, MAG2) 
    
    R1_2 = apis.get_device_data(transformer, 'TRANSFORMER', 'R1_2')
    X1_2 = apis.get_device_data(transformer, 'TRANSFORMER', 'X1_2')    
    Zps = complex(R1_2, X1_2)  
    if r is False:
        Zps = 1j * X1_2

    WINDV1 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV1')
    WINDV2 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV2')        
    k = WINDV1 / WINDV2  
    if c is False:
        k = 1.0
        exci_admit = 0.0
    Yij = 1 / (k * Zps)  
    Yj = (k - 1) / (k * Zps) 
    Yi = (1 - k) / (k ** 2 * Zps) + exci_admit  
    
    return Yij, Yi, Yj
    
def build_transformer3_equivalent_circuit(transformer, c, r):
    '''
    Build the equivalent circuit of three winding transformer.
    Args:
        (1) transformer, tuple, (IBUS, JBUS, KBUS).
        (2) c, bool, True is to include non-standard transformation ratio.
        (3) r, bool, True is represent branch resistance.        
    Rets:
        trans3_Y_mat, array, Admittance matrix of three winding transformer. 
    '''
    R1_2 = apis.get_device_data(transformer, 'TRANSFORMER', 'R1_2')
    X1_2 = apis.get_device_data(transformer, 'TRANSFORMER', 'X1_2')        
    R3_1 = apis.get_device_data(transformer, 'TRANSFORMER', 'R3_1')
    X3_1 = apis.get_device_data(transformer, 'TRANSFORMER', 'X3_1')
    R2_3 = apis.get_device_data(transformer, 'TRANSFORMER', 'R2_3')        
    X2_3 = apis.get_device_data(transformer, 'TRANSFORMER', 'X2_3')
    
    Zp = 0.5 * (complex(R1_2, X1_2) + complex(R3_1, X3_1) - complex(R2_3, X2_3))  
    Zs = 0.5 * (complex(R1_2, X1_2) + complex(R2_3, X2_3) - complex(R3_1, X3_1))
    Zt = 0.5 * (complex(R3_1, X3_1) + complex(R2_3, X2_3) - complex(R1_2, X1_2))
    if r is False:  
        Zp = 0.5 * (1j * X1_2 + 1j * X3_1 - 1j * X2_3)  
        Zs = 0.5 * (1j * X1_2 + 1j * X2_3 - 1j * X3_1)
        Zt = 0.5 * (1j * X3_1 + 1j * X2_3 - 1j * X1_2) 
        
    WINDV1 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV1')
    WINDV2 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV2')        
    WINDV3 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV3') 
    kp, ks, kt = WINDV1, WINDV2, WINDV3
    if c is False:  
        kp, ks, kt = 1.0, 1.0, 1.0
        
    Yeq1, Yeq2, Yeq3 = 1 / (kp * Zp), 1 / (ks * Zs), 1 / (kt * Zt)
    Yeq22 = (1 - ks) / (ks ** 2 * Zs)
    Yeq21 = (ks - 1) / (ks * Zs)
    Yeq32 = (1 - kt) / (kt ** 2 * Zt)
    Yeq31 = (kt - 1) / (kt * Zt)
    
    temp = Yeq1 + Yeq2 + Yeq3 + Yeq21 + Yeq31  #Eliminating star node of three winding transformer
    Y11 = Yeq1 - Yeq1 ** 2 / temp  
    Y12 = - Yeq1 * Yeq2 / temp  
    Y13 = - Yeq1 * Yeq3 / temp  
    Y21 = - Yeq1 * Yeq2 / temp  
    Y22 = Yeq2 + Yeq22 - Yeq2 ** 2 / temp  
    Y23 = - Yeq2 * Yeq3 / temp  
    Y31 = - Yeq3 * Yeq1 / temp  
    Y32 = - Yeq3 * Yeq2 / temp  
    Y33 = Yeq3 + Yeq32 - Yeq3 ** 2 / temp  
    
    trans3_Y_mat = np.array([[Y11, Y12, Y13], [Y21, Y22, Y23], [Y31, Y32, Y33]], dtype = complex)  
    
    return trans3_Y_mat
  