# 潮流计算结果
import sys
sys.path.append('..')
import csv
import numpy as np
from math import cos, sin, pi, sqrt, acos

import apis
from apis import apis_system
from apis import apis_basic


def get_powerflow_result():
    '''
    Get power flow result in list
    Args: None
    Rets: None
    '''
    bus_data = get_bus_result()
    bus_data.insert(0, ['BUS'])
    
    gen_data = get_generator_result()
    gen_data.insert(0, ['GENERATOR'])
    
    wt_gen_data = get_wt_generator_result()
    wt_gen_data.insert(0, ['WT GENERATOR'])
    
    pv_unit_data = get_pv_unit_result()
    pv_unit_data.insert(0, ['PV UNIT'])
    
    line_data = get_line_result()
    line_data.insert(0, ['LINE'])
        
    trans2_data, trans3_data = get_transformer_result()
    trans2_data.insert(0, ['TWO WINDING TRANSFORMER'])
    trans3_data.insert(0, ['THREE WINDING TRANSFORMER'])
    
    hvdc_data = get_line_result()
    hvdc_data.insert(0, ['HVDC']) 
    
    result_data = bus_data + gen_data + wt_gen_data + pv_unit_data + line_data + trans2_data + trans3_data + hvdc_data    
    return result_data 

def get_bus_result():
    '''
    Get bus volatge result.
    Args: None
    Rets: 
        bus_data, list, bus volatge result.
    '''
    buses = apis.get_all_devices('BUS')
    bus_data = [['NUMBER', 'VOLTAGE/pu', 'ANGLE/deg']]  
    for bus in buses:
        VM = apis.get_device_data(bus, 'BUS', 'VM')
        VA = apis.get_device_data(bus, 'BUS', 'VA')
        bus_data.append([bus, VM, VA])
    return bus_data

def get_generator_result():
    '''
    Get generator power result.
    Args: None
    Rets: 
        gen_data, list, generator power flow result.
    '''
    generators = apis.get_all_devices('GENERATOR')
    gen_data = [['NUMBER', 'PG/MW', 'QG/MVar']]  
    for generator in generators:
        PG = apis.get_device_data(generator, 'GENERATOR', 'PG')
        QG = apis.get_device_data(generator, 'GENERATOR', 'QG')
        gen_data.append([generator, PG, QG])
    return gen_data

def get_wt_generator_result():
    '''
    Get wind tubine power flow result.
    Args: None
    Rets: 
        wt_gen_data, list, wind tubine power flow result.
    '''
    wt_generators = apis.get_all_devices('WT GENERATOR')
    wt_gen_data = [['NUMBER', 'PG/MW', 'QG/MVar']]  
    for wt_gen in wt_generators:
        PG = apis.get_device_data(wt_gen, 'WT GENERATOR', 'PG')
        QG = apis.get_device_data(wt_gen, 'WT GENERATOR', 'QG')
        wt_gen_data.append([wt_gen, PG, QG]) 
    return wt_gen_data

def get_pv_unit_result():
    '''
    Get PV UNIT power flow result.
    Args: None
    Rets: 
        pv_unit_data, list, pv unit power flow result.
    '''
    pv_units = apis.get_all_devices('PV UNIT')
    pv_unit_data = [['NUMBER', 'PG/MW', 'QG/MVar']]  
    for pv_unit in pv_units:
        PG = apis.get_device_data(pv_unit, 'PV UNIT', 'PG')
        QG = apis.get_device_data(pv_unit, 'PV UNIT', 'QG')
        pv_unit_data.append([pv_unit, PG, QG])
    return pv_unit_data

def get_line_result():
    '''
    Get lines power flow result.
    Args: None
    Rets: 
        line_data, list, lines power flow result.
    '''
    lines = apis.get_all_devices('LINE')
    line_data = [['IBUS', 'JBUS', 'CKT', 'PI/MW', 'QI/MVar', 'PJ/MW', 'QJ/MVar', 'LOSS/MW']]  # 线路结果
    for line in lines:
        pi, qi, pj, qj, p_loss = calculate_line_powerflow(line)
        line_data.append([line[0], line[1], line[2], pi, qi, pj, qj, p_loss])
    return line_data
    
def calculate_line_powerflow(line):
    '''
    Calculate a line power flow.
    Args:
        line, tuple, (ibus, jbus, ckt)
    Rets:
        (1) pij, active power at start of line in MW
        (2) qij, reactive power at start of line in MVar
        (3) pji, active power at end of line in MW
        (4) qji, reactive power at end of line in MVar
        (5) p_loss, power loss at line in MW        
    '''
    vmi = apis.get_device_data(line[0], 'BUS', 'VM')
    vai = apis.get_device_data(line[0], 'BUS', 'VA')
    vmj = apis.get_device_data(line[1], 'BUS', 'VM')
    vaj = apis.get_device_data(line[1], 'BUS', 'VA')
    vai = apis_basic.convert_deg_to_rad(vai)
    vaj = apis_basic.convert_deg_to_rad(vaj)
    
    vi = apis_basic.build_complex_value(vmi, vai)
    vj = apis_basic.build_complex_value(vmj, vaj)
    
    R = apis.get_device_data(line, 'LINE', 'R')
    X = apis.get_device_data(line, 'LINE', 'X')
    B = apis.get_device_data(line, 'LINE', 'B')  
    BI = apis.get_device_data(line, 'LINE', 'BI')
    BJ = apis.get_device_data(line, 'LINE', 'BJ')
    
    SBASE = apis_system.get_system_base_data('SBASE')
    z = complex(R, X)  
    y1, y2 = 0.5j * B + 1j * BI, 0.5j * B + 1j * BJ
    
    flow_ij = abs(vi) ** 2 * y1.conjugate() + vi * (vi.conjugate() - vj.conjugate()) * (1 / z).conjugate()
    pij = flow_ij.real * SBASE  
    qij = flow_ij.imag * SBASE  

    flow_ji = abs(vj) ** 2 * y2.conjugate() + vj * (vj.conjugate() - vi.conjugate()) * (1 / z).conjugate()
    pji = flow_ji.real * SBASE  
    qji = flow_ji.imag * SBASE   
    
    p_loss = pij + pji
    
    return pij, qij, pji, qji, p_loss    
    
def get_transformer_result():
    '''
    Get transformers power flow result.
    Args: None
    Rets: 
        (1) trans2_data, list, two winding trans3_data power flow result.
        (2) trans3_data, list, three winding trans3_data power flow result.
    '''
    transformers = apis.get_all_devices('TRANSFORMER')
    trans2_data = [['IBUS', 'JBUS', 'PI/MW', 'QI/MVar', 'PJ/MW', 'QJ/MVar', 'LOSS/MW']]
    trans3_data = [['IBUS', 'JBUS', 'KBUS', 'PI/MW', 'QI/MVar', 'PJ/MW', 'QJ/MVar', 'PK/MW', 'QK/MVar', 'LOSS/MW']] 
    for transformer in transformers:
        if transformer[2] == 0:
            pi, qi, pj, qj, p_loss = calculate_transformer2_powerflow(transformer)
            trans2_data.append([transformer[0], transformer[1], pi, qi, pj, qj, p_loss])
        
        else:
            pi, qi, pj, qj, pk, qk, p_loss = calculate_transformer3_powerflow(transformer)
            trans3_data.append([transformer[0], transformer[1], transformer[2], pi, qi, pj, qj, pk, qk, p_loss])            
    
    return trans2_data, trans3_data

def calculate_transformer2_powerflow(transformer):
    '''
    Calculate power flow of double winding transformer
    Args:
        transformer, tuple, (ibus, jbus) 
    Rets:
        (1) pij, active power at first winding in MW.
        (2) qij, reactive power at first winding in MVar.
        (3) pji, active power at second winding in MW.
        (4) qji, reactive power at second winding in MVar.
        (5) p_loss, power loss at transformer in MW            
    '''
    vmi = apis.get_device_data(transformer[0], 'BUS', 'VM')
    vai = apis.get_device_data(transformer[0], 'BUS', 'VA')
    vmj = apis.get_device_data(transformer[1], 'BUS', 'VM')
    vaj = apis.get_device_data(transformer[1], 'BUS', 'VA')
    vai = apis_basic.convert_deg_to_rad(vai)
    vaj = apis_basic.convert_deg_to_rad(vaj)
    
    vi = apis_basic.build_complex_value(vmi, vai)
    vj = apis_basic.build_complex_value(vmj, vaj)   
    
    R1_2 = apis.get_device_data(transformer, 'TRANSFORMER', 'R1_2')
    X1_2 = apis.get_device_data(transformer, 'TRANSFORMER', 'X1_2')
    WINDV1 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV1')
    WINDV2 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV2')
    
    Zps = complex(R1_2, X1_2) 
    k = WINDV1 / WINDV2
    Zij = k * Zps  
    Yj = (k - 1) / (k * Zps)
    Yi = (1 - k) / (k ** 2 * Zps)
    
    SBASE = apis_system.get_system_base_data('SBASE')
    flow_ij = abs(vi) ** 2 * Yi.conjugate() + vi * (vi.conjugate() - vj.conjugate()) * (1 / Zij).conjugate()
    pij = flow_ij.real * SBASE  
    qij = flow_ij.imag * SBASE  

    flow_ji = abs(vj) ** 2 * Yj.conjugate() + vj * (vj.conjugate() - vi.conjugate()) * (1 / Zij).conjugate()
    pji = flow_ji.real * SBASE  
    qji = flow_ji.imag * SBASE   
    
    p_loss = pij + pji
    
    return pij, qij, pji, qji, p_loss 
    
def calculate_transformer3_powerflow(transformer):
    '''
    Calculate power flow of three winding transformer.
    Args:
        transformer, tuple, (ibus, jbus, kbus).
    Rets:
        (1) pi, primary active power in MW.
        (2) qi, primary reactive power in MVar.
        (3) pj, secondary active power in MW.
        (4) qj, secondary reactive power in MVar.
        (5) pk, third side active power in MW.
        (6) qk, third side reactive power in MVar.
        (7) p_loss, power loss in MW.      
    '''
    vmi = apis.get_device_data(transformer[0], 'BUS', 'VM')
    vai = apis.get_device_data(transformer[0], 'BUS', 'VA')
    vmj = apis.get_device_data(transformer[1], 'BUS', 'VM')
    vaj = apis.get_device_data(transformer[1], 'BUS', 'VA')
    vmk = apis.get_device_data(transformer[2], 'BUS', 'VM')
    vak = apis.get_device_data(transformer[2], 'BUS', 'VA')
    vai = apis_basic.convert_deg_to_rad(vai)
    vaj = apis_basic.convert_deg_to_rad(vaj)
    vak = apis_basic.convert_deg_to_rad(vak)
    
    vi = apis_basic.build_complex_value(vmi, vai)
    vj = apis_basic.build_complex_value(vmj, vaj) 
    vk = apis_basic.build_complex_value(vmk, vak)
    
    v_matrix = np.array([[vi], [vj], [vk]], dtype=complex)
    SBASE = apis_system.get_system_base_data('SBASE')
    
    y_matrix = calculate_transformer3_matrix(transformer)  
    i_matrix = np.dot(y_matrix, v_matrix)  
    s_matrix = v_matrix * i_matrix.conjugate() * SBASE  
    s_matrix = s_matrix.reshape(-1)
    
    pi, qi = s_matrix[0].real, s_matrix[0].imag
    pj, qj = s_matrix[1].real, s_matrix[1].imag
    pk, qk = s_matrix[2].real, s_matrix[2].imag
    p_loss = pi + pj + pk
    
    return pi, qi, pj, qj, pk, qk, p_loss

def calculate_transformer3_matrix(transformer):
    '''
    Calculate admittance matrix of three winding transformer.
    Args:
        transformer, tuple, (ibus, jbus, kbus).
    Rets:
        y_matrix, array, admittance matrix of three winding transformer.
    '''
    R1_2 = apis.get_device_data(transformer, 'TRANSFORMER', 'R1_2')
    X1_2 = apis.get_device_data(transformer, 'TRANSFORMER', 'X1_2')
    R3_1 = apis.get_device_data(transformer, 'TRANSFORMER', 'R3_1')
    X3_1 = apis.get_device_data(transformer, 'TRANSFORMER', 'X3_1')
    R2_3 = apis.get_device_data(transformer, 'TRANSFORMER', 'R2_3')
    X2_3 = apis.get_device_data(transformer, 'TRANSFORMER', 'X2_3')
    WINDV1 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV1')
    WINDV2 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV2')
    WINDV3 = apis.get_device_data(transformer, 'TRANSFORMER', 'WINDV3')
    
    Zp = 0.5 * (complex(R1_2, X1_2) + complex(R3_1, X3_1) - complex(R2_3, X2_3))  
    Zs = 0.5 * (complex(R1_2, X1_2) + complex(R2_3, X2_3) - complex(R3_1, X3_1))
    Zt = 0.5 * (complex(R3_1, X3_1) + complex(R2_3, X2_3) - complex(R1_2, X1_2))

    kp, ks, kt = WINDV1, WINDV2, WINDV3
    Yeq1, Yeq2, Yeq3 = 1 / (kp * Zp), 1 / (ks * Zs), 1 / (kt * Zt)
    Yeq22 = (1 - ks) / (ks ** 2 * Zs)
    Yeq21 = (ks - 1) / (ks * Zs)
    Yeq32 = (1 - kt) / (kt ** 2 * Zt)
    Yeq31 = (kt - 1) / (kt * Zt)
    
    temp = Yeq1 + Yeq2 + Yeq3 + Yeq21 + Yeq31
    Y11 = Yeq1 - Yeq1 ** 2 / temp
    Y12 = - Yeq1 * Yeq2 / temp
    Y13 = - Yeq1 * Yeq3 / temp
    Y21 = - Yeq1 * Yeq2 / temp
    Y22 = Yeq2 + Yeq22 - Yeq2 ** 2 / temp
    Y23 = - Yeq2 * Yeq3 / temp
    Y31 = - Yeq3 * Yeq1 / temp
    Y32 = - Yeq3 * Yeq2 / temp
    Y33 = Yeq3 + Yeq32 - Yeq3 ** 2 / temp
    
    y_matrix = np.array([[Y11, Y12, Y13], [Y21, Y22, Y23], [Y31, Y32, Y33]], dtype = complex)
    return y_matrix  
    
def get_hvdc_result():
    '''
    Get hvdc power flow result.
    Args: None
    Rets: 
        hvdc_data, list, hvdc power flow result.
    '''
    hvdcs = apis.get_all_hvdcs()
    hvdc_data = [['IBUS', 'JBUS', 'PLR/MW', 'QLR/MVar', 'ANR/deg', 'TAPR', 'PLI/MW', 'QLI/MVar', 'ANI', 'TAPI']]
    for hvdc in hvdcs:
        Sacr, alpha, Saci, gamma = calculate_hvdc_steady_parameters(hvdc)
        alpha = apis_basic.convert_rad_to_deg(alpha)
        gamma = apis_basic.convert_rad_to_deg(gamma)
        TAPR = apis.get_device_data(hvdc, 'HVDC', 'TAPR')
        TAPI = apis.get_device_data(hvdc, 'HVDC', 'TAPI')
        hvdc_data.append([hvdc[0], hvdc[1], Sacr.real, Sacr.imag, alpha, TAPR, Saci.real, Saci.imag, gamma, TAPI])
    
    return hvdc_data
    
def calculate_hvdc_steady_parameters(hvdc):
    '''
    Calculate the system injection power at both ends of hcdc.
    In steady state, the control mode of HVDC is to fix DC power on rectifier side and DC voltage on inverter side.
    Args:
        hvdc, tuple, hvdc in format (ibus, jbus).
    Rets:
        (1) Sacr, power absorbed by rectifier side.
        (2) alpha, trigger angle in deg
        (3) Saci, power output from inverter side.
        (4) gamma, extinction angle in deg
    '''
    VM = apis.get_device_data(hvdc[0], 'BUS', 'VM')
    BASKV = apis.get_device_data(hvdc[0], 'BUS', 'BASKV')
    Vtr = BASKV * VM

    VM = apis.get_device_data(hvdc[1], 'BUS', 'VM')
    BASKV = apis.get_device_data(hvdc[1], 'BUS', 'BASKV')
    Vti = BASKV * VM    
    
    Vdci = apis.get_device_data(hvdc, 'HVDC', 'VSCHD')  # Fixed DC voltage at inverter side
    Pacr = apis.get_device_data(hvdc, 'HVDC', 'SETVL')  # Fixed DC power at rectifier side
    RDC = apis.get_device_data(hvdc, 'HVDC', 'RDC')  # DC circuit resistance
    
    Idc = (- Vdci + sqrt(Vdci ** 2 + 4 * RDC * Pacr)) / (2 * RDC)  # Calculate the DC current in A
    
    # Inverse side solution
    Paci = Vdci * Idc  # DC power of inverter side in MW
    
    ANMNI = apis.get_device_data(hvdc, 'HVDC', 'ANMNI') # Inverter side minimum gamma in deg
    NBI = apis.get_device_data(hvdc, 'HVDC', 'NBI')
    XCI = apis.get_device_data(hvdc, 'HVDC', 'XCI')
    TRI = apis.get_device_data(hvdc, 'HVDC', 'TRI')
    TMNI = apis.get_device_data(hvdc, 'HVDC', 'TMNI')
    STPI = apis.get_device_data(hvdc, 'HVDC', 'STPI')
    gamma = apis_basic.convert_deg_to_rad(ANMNI)  

    Eaci = (Vdci / NBI + 3*XCI*Idc / pi) * pi / (3*sqrt(2) * cos(gamma))  # Open circuit AC line voltage of inverter side converter DC side 
    x = int((Vti * TRI / Eaci  - TMNI) / STPI)  # Suitable tap position
    TAPI = TMNI + x * STPI  # Find the tap
    apis.set_device_data(hvdc, 'HVDC', 'TAPI', TAPI)
    
    Eaci = Vti * TRI / TAPI  # The open circuit voltage in kV under this tap
    cos_gamma = (Vdci / NBI + 3 * XCI * Idc / pi) * pi / (3 * sqrt(2) * Eaci)
    gamma = acos(cos_gamma)
    
    miu_i = acos(cos_gamma - sqrt(2) * Idc * XCI / Eaci) - gamma  # Overlap angle of inverter side in rad
    tan_faii = (2*miu_i + sin(2*gamma) - sin(2*miu_i + 2*gamma)) / (cos(2*gamma) - cos(2*miu_i + 2*gamma))
    Qaci = Paci * tan_faii  # Reactive power of inverter side in MVar
    
    # Rectifier side solution
    Vdcr = Pacr / Idc 
    
    ANMNR = apis.get_device_data(hvdc, 'HVDC', 'ANMNR') # Rectifier minimum alpha in deg    
    alpha = apis_basic.convert_deg_to_rad(ANMNR) 
    NBR = apis.get_device_data(hvdc, 'HVDC', 'NBR')
    XCR = apis.get_device_data(hvdc, 'HVDC', 'XCR')
    TRR = apis.get_device_data(hvdc, 'HVDC', 'TRR')
    TMNR = apis.get_device_data(hvdc, 'HVDC', 'TMNR')
    STPR = apis.get_device_data(hvdc, 'HVDC', 'STPR')    
    Eacr = (Vdcr / NBR + 3 * XCR * Idc / pi) * pi / (3 * sqrt(2) * cos(alpha))  # DC side open circuit AC line voltage 
    x = int((Vtr * TRR / Eacr - TMNR) / STPR)  
    TAPR = TMNR + x * STPR
    apis.set_device_data(hvdc, 'HVDC', 'TAPR', TAPR)
    Eacr = Vtr * TRR / TAPR  
    cos_alpha = (Vdcr / NBR + 3 * XCR * Idc / pi) * pi / (3 * sqrt(2) * Eacr)  
    alpha = acos(cos_alpha)
 
    miu_r = acos(cos_alpha - sqrt(2) * Idc * XCR / Eacr) - alpha  
    tan_fair = (2*miu_r + sin(2*alpha) - sin(2*miu_r + 2*alpha)) / (cos(2*alpha) - cos(2* miu_r + 2*alpha))
    Qacr = Pacr * tan_fair  

    return Pacr+1j*Qacr, alpha, Paci+1j*Qaci, gamma 