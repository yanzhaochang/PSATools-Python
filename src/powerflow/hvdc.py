import sys
sys.path.append('..')
import numpy as np
from math import sin, cos, atan, acos, sqrt, pi

import apis
from apis import apis_system
from apis import apis_basic


def correct_hvdc_node_power(S, Um):
    '''
    Correct power injection at HVDC nodes
    Args:
        (1) S, array, node injection power in pu.
        (2) Um, array, node voltage in pu.
    Rets:
        S: array, node injection power in pu.
    '''
    hvdcs = apis.get_all_devices('HVDC')
    loads = apis.get_all_devices('LOAD')
    for hvdc in hvdcs:
        VM = apis.get_device_data(hvdc[0], 'BUS', 'VM')
        BASKV = apis.get_device_data(hvdc[0], 'BUS', 'BASKV')
        Vtr = BASKV * VM

        VM = apis.get_device_data(hvdc[1], 'BUS', 'VM')
        BASKV = apis.get_device_data(hvdc[1], 'BUS', 'BASKV')
        Vti = BASKV * VM
        
        Si, Sr = 0.0, 0.0  # Obtain the load on the HVDC bus 
        if hvdc[0] in loads:
            PL = apis.get_device_data(hvdc[0], 'LOAD', 'PL')
            QL = apis.get_device_data(hvdc[0], 'LOAD', 'QL')
            Sr = Sr + PL + 1j * QL
        if hvdc[1] in loads:
            PL = apis.get_device_data(hvdc[1], 'LOAD', 'PL')
            QL = apis.get_device_data(hvdc[1], 'LOAD', 'QL')
            Si = Si + PL + 1j * QL
                
        Pacr, Qacr, Paci, Qaci = calculate_dc_line_power(hvdc, Vtr, Vti)
        
        i = apis_system.get_bus_num_after_renumber(hvdc[0])
        j = apis_system.get_bus_num_after_renumber(hvdc[1])
        SBASE = apis_system.get_system_base_data('SBASE')
        S[i] = (- Pacr - 1j * Qacr - Sr) / SBASE
        S[j] = (Paci - 1j * Qaci - Si) / SBASE
        
    return S

def calculate_dc_line_power(hvdc, Vtr, Vti):
    '''
    Calculate the system injection power at both ends of hcdc.
    In steady state, the control mode of HVDC is to fix DC power on rectifier side and DC voltage on inverter side.
    Args:
        (1) hvdc, tuple, hvdc in format (ibus, jbus).
        (2) Vtr, AC bus voltage in kV at rectifier side.
        (3) Vti, AC bus voltage in kV at inverter side.
    Rets:
        (1) Pacr, Active power in MW absorbed by rectifier side.
        (2) Qacr, Reactive power in MVar absorbed by rectifier side.
        (3) Paci, Active power in MW output from inverter side.
        (4) Qaci, Reactive power in MVar output by rectifier side.
    '''
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

    return Pacr, Qacr, Paci, Qaci 