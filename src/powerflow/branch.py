import sys
sys.path.append('..')
import numpy as np

import apis
from apis import apis_system
from apis import apis_basic

from .hvdc import calculate_dc_line_power


def init_powerflow_solution():
    '''
    Initial power flow solution with flat start.
    Args: None
    Rets:
        (1) S, array, node complex power injection in pu.
        (2) Um, array, initialized node voltage in pu.
        (3) Ua, array, node voltage phase angle in rad.
    '''
    buses = apis.get_all_devices('BUS')
    Um, Ua = np.ones(len(buses)), np.zeros(len(buses)) 
    S = np.zeros(len(buses), dtype=complex)  
    
    for bus in buses: 
        IDE = apis.get_device_data(bus, 'BUS', 'IDE')
        if IDE == 1:
            apis.set_device_data(bus, 'BUS', 'VM', 1.0)
            apis.set_device_data(bus, 'BUS', 'VA', 0.0)
            
        if IDE == 2:
            apis.set_device_data(bus, 'BUS', 'VA', 0.0)
            i = apis_system.get_bus_num_after_renumber(bus)
            VM = apis.get_device_data(bus, 'BUS', 'VM')
            Um[i] = VM
            
        if IDE == 3:
            i = apis_system.get_bus_num_after_renumber(bus)
            VM = apis.get_device_data(bus, 'BUS', 'VM')
            VA = apis.get_device_data(bus, 'BUS', 'VA')
            Um[i] = VM
            Ua[i] = apis_basic.convert_deg_to_rad(VA)
    
    loads = apis.get_all_devices('LOAD')
    for load in loads:
        i = apis_system.get_bus_num_after_renumber(load)
        PL = apis.get_device_data(load, 'LOAD', 'PL')
        QL = apis.get_device_data(load, 'LOAD', 'QL')
        S[i] = - PL - 1j * QL + S[i]  
    
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        i = apis_system.get_bus_num_after_renumber(generator)
        PG = apis.get_device_data(generator, 'GENERATOR', 'PG')
        S[i] = PG + S[i]
    
    wt_gens = apis.get_all_devices('WT GENERATOR')
    for wt_gen in wt_gens:
        PG = apis.get_device_data(wt_gen, 'WT GENERATOR', 'PG')
        i = apis_system.get_bus_num_after_renumber(wt_gen)
        S[i] = PG + S[i]  
    
    pv_units = apis.get_all_devices('PV UNIT')
    for pv_unit in pv_units:
        i = apis_system.get_bus_num_after_renumber(pv_unit)
        PG = apis.get_device_data(pv_unit, 'PV UNIT', 'PG')
        S[i] = PG + S[i]  
    
    hvdcs = apis.get_all_devices('HVDC')
    for hvdc in hvdcs:
        VM = apis.get_device_data(hvdc[0], 'BUS', 'VM')
        BASKV = apis.get_device_data(hvdc[0], 'BUS', 'BASKV')
        Vtr = BASKV * VM

        VM = apis.get_device_data(hvdc[1], 'BUS', 'VM')
        BASKV = apis.get_device_data(hvdc[1], 'BUS', 'BASKV')
        Vti = BASKV * VM
        
        Pacr, Qacr, Paci, Qaci = calculate_dc_line_power(hvdc, Vtr, Vti)  # Calculate the initial injection power of HVDC
        
        i = apis_system.get_bus_num_after_renumber(hvdc[0])
        j = apis_system.get_bus_num_after_renumber(hvdc[1])
        S[i] = - Pacr - 1j * Qacr + S[i]
        S[j] = Paci - 1j * Qaci + S[j]
    
    SBASE = apis_system.get_system_base_data('SBASE')
    S = S / SBASE  # Convert power to unit power

    return S, Um, Ua
    
def update_powerflow(S, Um, Ua):
    '''
    Update component data after solving power flow.
    Args:
        (1) S, array, node complex power injection in pu.
        (2) Um, array, initialized node voltage in pu.
        (3) Ua, array, node voltage phase angle in rad.
    Rets: None
    '''
    PQ_num = apis_system.get_system_bus_number('PQ')
    PV_num = apis_system.get_system_bus_number('PV')
    Y_mat = apis_system.get_system_Y_network_matrix('basic')
    buses = apis.get_all_devices('BUS')

    for i in range(PQ_num, len(buses)):  # Calculate reactive power injection of PV node and balance node
        ang_d = Ua[i] - Ua
        S[i] = S[i].real + 1j * Um[i] * np.sum(Um * (Y_mat[i, :].real * np.sin(ang_d) - Y_mat[i, :].imag * np.cos(ang_d)))
    
    for i in range(PQ_num+PV_num, len(buses)):  # Calculate of active power injection of balance node
        ang_d = Ua[i] - Ua
        S[i] = 1j * S[i].imag + Um[i] * np.sum(Um * (Y_mat[i, :].real * np.cos(ang_d) + Y_mat[i, :].imag * np.sin(ang_d)))
    
    Ua = apis_basic.convert_rad_to_deg(Ua)
    for bus in buses:  # Update bus voltage and phase angle
        i = apis_system.get_bus_num_after_renumber(bus)
        apis.set_device_data(bus, 'BUS', 'VM', Um[i])
        apis.set_device_data(bus, 'BUS', 'VA', Ua[i]) 
    
    generators = apis.get_all_devices('GENERATOR')
    SBASE = apis_system.get_system_base_data('SBASE')
    for generator in generators:  # Update the output of generator
        i = apis_system.get_bus_num_after_renumber(generator)
        apis.set_device_data(generator, 'GENERATOR', 'QG', S[i].imag * SBASE)
        IDE = apis.get_device_data(generator, 'BUS', 'IDE')
        if IDE == 3:
            apis.set_device_data(generator, 'GENERATOR', 'PG', S[i].real * SBASE) 
    return
    
def show_powerflow_result():
    '''
    Show powerflow result
    Args: None
    Rets: None
    ''' 
    print('-------------------------------------')
    print('Power flow solution reports:')
    print('BUS, VOLTAGE/pu, ANGLE/deg,  LOAD/pu,  GENERATE/pu')
    buses = apis.get_all_devices('BUS')
    loads = apis.get_all_devices('LOAD')
    generators = apis.get_all_devices('GENERATOR')
    wt_generators = apis.get_all_devices('WT GENERATOR')
    pv_units = apis.get_all_devices('PV UNIT')
    SBASE = apis_system.get_system_base_data('SBASE')
    
    for bus in buses:
        VM = apis.get_device_data(bus, 'BUS', 'VM')
        VA = apis.get_device_data(bus, 'BUS', 'VA')
        
        load_power = 0 + 1j * 0 
        if bus in loads:
           PL = apis.get_device_data(bus, 'LOAD', 'PL')
           QL = apis.get_device_data(bus, 'LOAD', 'QL')
           load_power =  (PL + 1j * QL) / SBASE
            
        gen_power = 0 + 1j * 0
        if bus in generators:
           PG = apis.get_device_data(bus, 'GENERATOR', 'PG')
           QG = apis.get_device_data(bus, 'GENERATOR', 'QG')
           gen_power =  (PG + 1j * QG) / SBASE        
        
        if bus in wt_generators:
           PG = apis.get_device_data(bus, 'WT GENERATOR', 'PG')
           QG = apis.get_device_data(bus, 'WT GENERATOR', 'QG')
           gen_power =  (PG + 1j * QG) / SBASE         
        
        if bus in pv_units:
           PG = apis.get_device_data(bus, 'PV UNIT', 'PG')
           QG = apis.get_device_data(bus, 'PV UNIT', 'QG')
           gen_power =  (PG + 1j * QG) / SBASE             
      
        print('#{},  {:.4f},  {:.3f},  {:.3f},  {:.3f}'.format(bus, VM, VA, load_power, gen_power)) 
        
    return