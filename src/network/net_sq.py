# sequence network
# There is an error in the calculation of the negative sequence node admittance array, 
# and the calculation result can not correspond to the psse software, which is still under debugging
import numpy as np
import sys
sys.path.append('..')

import apis
from apis import apis_system

from powerflow import powerflow_result


def calculate_sequence_Y_matrix(par_type):
    '''
    Calculate sequence Y matrix, including positive, negative, zero.
    Args:
        par_type, str, Y matrix type, positive, negative, zero.
    Rets:
        Y_mat, array, sequence matrix.
    '''
    if par_type == 'positive':
        Y_mat = calculate_positive_Y_matrix()
        
    elif par_type == 'negative':
        Y_mat = calculate_negative_Y_matrix()
        
    elif par_type == 'zero':
        Y_mat = calculate_zero_Y_matrix()
        
    else:
        Y_mat = None
    return Y_mat
    
def calculate_positive_Y_matrix():
    '''
    Calculate positive nodal admittance matrix.
    Args: None
    Rets:
        Y_mat, array, positive nodal admittance matrix.
    '''
    Y_mat = apis_system.get_system_Y_network_matrix('basic')
    SBASE = apis_system.get_system_base_data('SBASE')
    
    generators = apis.get_all_devices('GENERATOR')  # add generator
    for generator in generators:
        i = apis_system.get_bus_num_after_renumber(generator)
        ZRPOS = apis.get_device_sequence_data(generator, 'GENERATOR', 'ZRPOS')
        ZXPPDV = apis.get_device_sequence_data(generator, 'GENERATOR', 'ZXPPDV')
        MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
        
        gen_z = (ZRPOS + 1j * ZXPPDV) * SBASE / MBASE
        Y_mat[i, i] = Y_mat[i, i] + 1.0 / gen_z 
    
    # The sequence impedance of wind turbine and photovoltaic is not considered for the time being
    '''
    wt_generators = apis.get_all_devices('WT GENERATOR')  # add wt generator
    for wt_generator in wt_generators:
        i = apis_system.get_bus_num_after_renumber(wt_generator)
        ZRPOS = apis.get_device_sequence_data(wt_generator, 'WT GENERATOR', 'ZRPOS')
        ZXPPDV = apis.get_device_sequence_data(wt_generator, 'WT GENERATOR', 'ZXPPDV')
        MBASE = apis.get_device_data(wt_generator, 'WT GENERATOR', 'MBASE')
        
        gen_z = (ZRPOS + 1j * ZXPPDV) * SBASE / MBASE
        Y_mat[i, i] = Y_mat[i, i] + 1.0 / gen_z

    pv_units = apis.get_all_devices('PV UNIT')  # add pv unit
    for pv_unit in pv_units:
        i = apis_system.get_bus_num_after_renumber(pv_unit)
        ZRPOS = apis.get_device_sequence_data(pv_unit, 'PV UNIT', 'ZRPOS')
        ZXPPDV = apis.get_device_sequence_data(pv_unit, 'PV UNIT', 'ZXPPDV')
        MBASE = apis.get_device_data(pv_unit, 'PV UNIT', 'MBASE')
        
        gen_z = (ZRPOS + 1j * ZXPPDV) * SBASE / MBASE
        Y_mat[i, i] = Y_mat[i, i] + 1.0 / gen_z
    '''
    '''
    hvdcs = apis.get_all_devices('HVDC')  # add hvdc
    for hvdc in hvdcs:
        i = apis_system.get_bus_num_after_renumber(hvdc[0])
        j = apis_system.get_bus_num_after_renumber(hvdc[1])
        vi = apis.get_device_data(hvdc[0], 'BUS', 'VM')
        vj = apis.get_device_data(hvdc[1], 'BUS', 'VM')
        Sacr, alpha, Saci, gamma = powerflow_result.calculate_hvdc_steady_parameters(hvdc)
        
        Y_mat[i, i] = Y_mat[i, i] + Sacr.conjugate() / SBASE / vi ** 2
        Y_mat[j, j] = Y_mat[j, j] - Saci / SBASE / vj ** 2  
    '''
    loads = apis.get_all_devices('LOAD')  # add load
    for load in loads:
        i = apis_system.get_bus_num_after_renumber(load)
        VM = apis.get_device_data(load, 'BUS', 'VM')
        PL = apis.get_device_data(load, 'LOAD', 'PL')
        QL = apis.get_device_data(load, 'LOAD', 'QL')
        
        Y_mat[i, i] = Y_mat[i, i] + (PL - 1j * QL) / SBASE / VM**2  # Convert load power into admittance
    
    return Y_mat

def calculate_negative_Y_matrix():
    '''
    Calculate negative nodal admittance matrix.
    Args: None
    Rets:
        Y_mat, array, negative nodal admittance matrix.
    '''
    Y_mat = apis_system.get_system_Y_network_matrix('basic')
    SBASE = apis_system.get_system_base_data('SBASE')
    
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        i = apis_system.get_bus_num_after_renumber(generator)
        ZRNEG = apis.get_device_sequence_data(generator, 'GENERATOR', 'ZRNEG')
        ZXNEGDV = apis.get_device_sequence_data(generator, 'GENERATOR', 'ZXNEGDV')
        MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    
        gen_z = (ZRNEG + 1j * ZXNEGDV) * SBASE / MBASE
        Y_mat[i, i] = Y_mat[i, i] + 1.0 / gen_z     
    
    loads = apis.get_all_devices('LOAD')
    for load in loads:
        i = apis_system.get_bus_num_after_renumber(load)
        VM = apis.get_device_data(load, 'BUS', 'VM')
        PNEG = apis.get_device_sequence_data(load, 'LOAD', 'PNEG')
        QNEG = apis.get_device_sequence_data(load, 'LOAD', 'QNEG')
        
        Y_mat[i, i] = Y_mat[i, i] + (PNEG - 1j * QNEG) / SBASE / VM**2  # Convert load power into admittance 
    
    return Y_mat
    
def calculate_zero_Y_matrix():
    '''
    Calculate zero nodal admittance matrix.
    Args: None
    Rets:
        Y_mat, array, zero nodal admittance matrix.
    '''
    buses = apis.get_all_devices('BUS')
    Y_mat = np.zeros((len(buses), len(buses)), dtype = complex)
    
    SBASE = apis_system.get_system_base_data('SBASE')    
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        i = apis_system.get_bus_num_after_renumber(generator)
        MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
        ZR0 = apis.get_device_sequence_data(generator, 'GENERATOR', 'ZR0')
        ZX0DV = apis.get_device_sequence_data(generator, 'GENERATOR', 'ZX0DV')   
        ZRG = apis.get_device_sequence_data(generator, 'GENERATOR', 'ZRG')
        ZXG = apis.get_device_sequence_data(generator, 'GENERATOR', 'ZXG') 
        
        #By default, all generators are star grounded and have grounding impedance
        gen_z = (ZR0 + 1j * ZX0DV + 3 * (ZRG + 1j * ZXG)) * SBASE / MBASE 
        Y_mat[i, i] = Y_mat[i, i] + 1.0 / gen_z
    
    lines = apis.get_all_devices('LINE')
    for line in lines:
        i = apis_system.get_bus_num_after_renumber(line[0])
        j = apis_system.get_bus_num_after_renumber(line[1])
        
        RLINZ = apis.get_device_sequence_data(line, 'LINE', 'RLINZ')
        XLINZ = apis.get_device_sequence_data(line, 'LINE', 'XLINZ')
        BCHZ = apis.get_device_sequence_data(line, 'LINE', 'BCHZ')
        BI0 = apis.get_device_sequence_data(line, 'LINE', 'BI0')
        BJ0 = apis.get_device_sequence_data(line, 'LINE', 'BJ0')  
        
        Yij = 1.0 / complex(RLINZ, XLINZ) 
        Yi = 0.5j * BCHZ + 1j * BI0
        Yj = 0.5j * BCHZ + 1j * BJ0        

        Y_mat[i, j] = Y_mat[i, j] - Yij 
        Y_mat[j, i] = Y_mat[j, i] - Yij
        Y_mat[i, i] = Y_mat[i, i] + Yij + Yi 
        Y_mat[j, j] = Y_mat[j, j] + Yij + Yj 

    transformers = apis.get_all_devices('TRANSFORMER')
    for transformer in transformers:
        if transformer[2] == 0:
            i = apis_system.get_bus_num_after_renumber(transformer[0])
            j = apis_system.get_bus_num_after_renumber(transformer[1]) 
            Yij, Yi, Yj = build_transformer2_zero_equivalent_circuit(transformer)
            
            Y_mat[i, j] = Y_mat[i, j] - Yij
            Y_mat[j, i] = Y_mat[j, i] - Yij
            Y_mat[i, i] = Y_mat[i, i] + Yij + Yi 
            Y_mat[j, j] = Y_mat[j, j] + Yij + Yj   
        
        else:
            i = apis_system.get_bus_num_after_renumber(transformer[0])
            j = apis_system.get_bus_num_after_renumber(transformer[1]) 
            k = apis_system.get_bus_num_after_renumber(transformer[2])
            trans3_Y_mat = build_transformer3_zero_equivalent_circuit(transformer)
            
            Y_mat[i, i] = Y_mat[i, i] + trans3_Y_mat[0, 0]
            Y_mat[i, j] = Y_mat[i, j] + trans3_Y_mat[0, 1]
            Y_mat[i, k] = Y_mat[i, k] + trans3_Y_mat[0, 2]
            Y_mat[j, i] = Y_mat[j, i] + trans3_Y_mat[1, 0]
            Y_mat[j, j] = Y_mat[j, j] + trans3_Y_mat[1, 1]
            Y_mat[j, k] = Y_mat[j, k] + trans3_Y_mat[1, 2]
            Y_mat[k, i] = Y_mat[k, i] + trans3_Y_mat[2, 0]
            Y_mat[k, j] = Y_mat[k, j] + trans3_Y_mat[2, 1]
            Y_mat[k, k] = Y_mat[k, k] + trans3_Y_mat[2, 2]    
    shunts = apis.get_all_devices('SHUNT')
    for shunt in shunts:
        i = apis_system.get_bus_num_after_renumber(shunt)
        BSZERO = apis.get_device_sequence_data(shunt, 'SHUNT', 'BSZERO')
        Y_mat[i, i] = Y_mat[i, i] + 1j * BSZERO / SBASE
    
    loads = apis.get_all_devices('LOAD')
    for load in loads:  
        i = apis_system.get_bus_num_after_renumber(load)
        load_vm = apis.get_device_data(load, 'BUS', 'VM')
        PZERO = apis.get_device_sequence_data(load, 'LOAD', 'PZERO')
        QZERO = apis.get_device_sequence_data(load, 'LOAD', 'QZERO')
        Y_mat[i, i] = Y_mat[i, i] + (PZERO + 1j * QZERO) / SBASE / load_vm ** 2    
        
    return Y_mat  
    
def build_transformer2_zero_equivalent_circuit(transformer):
    '''
    Build the zero sequence equivalent circuit of double winding transformer, and the branch to ground is ignored.
    Args:
        transformer, tuple, (IBUS, JBUS, 0).
    Rets:
        (1) Yij, Admittance of double winding from i to j.
        (2) Yi, i-side self admittance.
        (3) Yj, i-side self admittance.
    '''
    CC = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'CC')
    WINDV2 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV2')
    WINDV1 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV1')
    R01 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'R01')
    X01 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'X01')
    RG1 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'RG1')
    XG1 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'XG1')    
    RG2 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'RG2')
    XG2 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'XG2')
    
    if CC == 1:  # YNyn 
        Zt = WINDV2 ** 2 * (R01 + 1j * X01)
        k = WINDV1 / WINDV2  
        Yij = 1 / (k * Zt)  
        Yj = (k - 1) / (k * Zt)  
        Yi = (1 - k) / (k ** 2 * Zt)  
        
    elif CC == 2:  # YNd
        Zt = R01 + 1j * X01 + 3 * (RG1 + 1j * XG1) 
        k = WINDV1
        Yi = 1 / (k * Zt)  
        Yij = 0.0
        Yj = 0.0
        
    elif CC == 3:  # Dyn
        Zeq = R01 + 1j * X01 + 3 * (RG2 + 1j * XG2)  
        k = WINDV2  
        Yj = 1 / (k * Zeq)  
        Yi = 0.0
        Yij = 0.0
        
    else:  # Without zero sequence path, including Yy, Yd, Dy, Dd, Yyn, YNy 
        Yij, Yi, Yj = 0.0, 0.0, 0.0  
        
    return Yij, Yi, Yj
 
def build_transformer3_zero_equivalent_circuit(transformer):
    '''
    Build the zero sequence equivalent circuit of three winding transformer, and the branch to ground is ignored.
    Args:
        transformer, tuple, (ibus, jbus, kbus).
    Rets:
        trans3_Y_mat, array, nodal matrix of transformer.
    '''
    WINDV2 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV2')
    WINDV1 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV1')
    WINDV3 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV3')
    CC = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'CC')
    R01 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'R01')
    X01 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'X01')
    R02 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'R02')
    X02 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'X02')
    R03 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'R03')
    X03 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'X03')
    RG1 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'RG1')
    XG1 = apis.get_device_sequence_data(transformer, 'TRANSFORMER', 'XG1')    
    if CC == 1:  # YNynyn
        Z10 = R01 + 1j * X01
        Z20 = R02 + 1j * X02
        Z30 = R03 + 1j * X03
        Zg0 = 3 * (RG1 + 1j * XG1)
        Yeq1, Yeq2, Yeq3 = 1 / (WINDV1 * Z10), 1 / (WINDV2 * Z20), 1 / (WINDV3 * Z30)
        
        temp = Yeq1 + Yeq2 + Yeq3 + 1 / Zg0  
        Y11 = Yeq1 - Yeq1 ** 2 / temp  
        Y12 = - Yeq1 * Yeq2 / temp  
        Y13 = - Yeq1 * Yeq3 / temp  
        Y21 = - Yeq1 * Yeq2 / temp  
        Y22 = Yeq2 - Yeq2 ** 2 / temp  
        Y23 = - Yeq2 * Yeq3 / temp  
        Y31 = - Yeq3 * Yeq1 / temp  
        Y32 = - Yeq3 * Yeq2 / temp  
        Y33 = Yeq3 - Yeq3 ** 2 / temp   
      
    elif CC == 2:  # YNynd
        Z10 = R01 + 1j * X01
        Z20 = R02 + 1j * X02
        Z30 = R03 + 1j * X03
        Zg0 = Z30
        
        Yeq1, Yeq2 = 1 / (WINDV1 * Z10), 1 / (WINDV2 * Z20)

        temp = Yeq1 + Yeq2 + 1 / Zg0
        Y11 = Yeq1 - Yeq1 ** 2 / temp  
        Y12 = - Yeq1 * Yeq2 / temp  
        Y13 = 0.0  
        Y21 = - Yeq1 * Yeq2 / temp  
        Y22 = Yeq2 - Yeq2 ** 2 / temp  
        Y23 = 0.0  
        Y31, Y32, Y33 = 0.0, 0.0, 0.0
        
    elif CC == 3:  # Dynd
        Z10 = R01 + 1j * X01
        Z20 = R02 + 1j * X02
        Z30 = R03 + 1j * X03  
        Zg0 = 1 / (1 / Z20 + 1 / Z30)
        
        Y11, Y12, Y13 = 0.0, 0.0, 0.0
        Y21 = 0.0
        Y22 = 1 / (WINDV2 * (Zg0 + Z20))  
        Y23 = 0.0
        Y31, Y32, Y33 = 0.0, 0.0, 0.0
        
    else:  # Ddd, Ddy, Dyd, Dyy, Ydd, Ydy, Yyd or Yyy
        Y11, Y12, Y13 = 0.0, 0.0, 0.0
        Y21, Y22, Y23 = 0.0, 0.0, 0.0
        Y31, Y32, Y33 = 0.0, 0.0, 0.0
        
    trans3_Y_mat = np.array([[Y11, Y12, Y13], [Y21, Y22, Y23], [Y31, Y32, Y33]], dtype = complex)   
        
    return trans3_Y_mat