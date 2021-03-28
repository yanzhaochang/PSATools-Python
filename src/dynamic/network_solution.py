# network solution in dynamic simulation
import numpy as np
import sys
sys.path.append('..')
from math import sin, cos, pi

import apis
from apis import apis_system
from apis import apis_dynamic


def solve_dynamic_bus_voltage(par_type):
    '''
    Solve the bus dynamic voltage
    Arg: 
        par_type, bool, bool, type of state variables, True represent actual voltage, False repersent estimated voltage
    Rets: None
    '''
    Y_mat = apis_system.get_system_Y_network_matrix('dynamic')  
    max_net_iter = 15
    
    I1 = calculate_generators_injection_current_I1(par_type)  
    buses = apis.get_all_devices('BUS')
    U0 = np.zeros(len(buses), dtype=complex)  # Bus voltage estimated value

    for bus in buses:
        i = apis_system.get_bus_num_after_renumber(bus)
        U0[i] = apis_dynamic.get_bus_state_data(bus, par_type, 'Vt')
    
    for i in range(max_net_iter):
        I2 = calculate_generators_injection_current_I2(U0, par_type)  
        I = I1 + I2

        U1 = np.linalg.solve(Y_mat, I)  
        if np.max(np.abs(U1-U0)) < 1e-12:  # Convergence error of network equation
            break
        else:
            U0 = U1.copy()  
    
    # Update network bus voltage
    for bus in buses:
        i = apis_system.get_bus_num_after_renumber(bus)
        apis_dynamic.set_bus_state_data(bus, par_type, 'Vt', U1[i])  

    update_generators_electromagnetic_power(par_type)
    return 

def update_generators_electromagnetic_power(par_type):
    '''
    Update the electromagnetic power of generators
    Args: 
        par_type, bool, type of state variables, True represent actual value, False repersent estimated value.
    Rets: None
    '''      
    buses = apis.get_all_devices('BUS')
    U0 = np.zeros(len(buses), dtype=complex)  
    for bus in buses:
        i = apis_system.get_bus_num_after_renumber(bus)
        U0[i] = apis_dynamic.get_bus_state_data(bus, par_type, 'Vt')   
 
    I1 = calculate_generators_injection_current_I1(par_type)  # Generator injection current I1 vector
    I2 = calculate_generators_injection_current_I2(U0, par_type) # Generator injection current I2 vector

    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        Vt = apis_dynamic.get_bus_state_data(generator, par_type, 'Vt')
        YGp = calculate_generator_internal_admittance(generator)
        
        i = apis_system.get_bus_num_after_renumber(generator)
        It = I1[i] + I2[i] - YGp * Vt 
        Pe = (Vt * It.conjugate()).real
        
        apis_dynamic.set_generator_state_data(generator, par_type, 'Pe', Pe)
        apis_dynamic.set_generator_state_data(generator, par_type, 'It', It)

    return
    
def calculate_generators_injection_current_I1(par_type):
    '''
    Calculate generators injection current I1 vector.
    Args: 
        par_type, bool, True represent actual value, False repersent estimated value.
    Rets: 
        gens_I1, array, generators injection current I1 vector.
    '''    
    buses = apis.get_all_devices('BUS')
    gens_I1 = np.zeros(len(buses), dtype=complex)
    
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        Ed, Eq = get_generator_internal_ralated_potential(generator, par_type) 
        delta = apis_dynamic.get_generator_state_data(generator, par_type, 'delta')

        Ex = Ed * sin(delta) + Eq * cos(delta)
        Ey = -Ed * cos(delta) + Eq * sin(delta)
        E = Ex + 1j * Ey 
        
        i = apis_system.get_bus_num_after_renumber(generator)
        YGp = calculate_generator_internal_admittance(generator)
        gens_I1[i] = YGp * E
        
    return gens_I1
    
def calculate_generators_injection_current_I2(bus_v, par_type):
    '''
    Calculate generators injection current I1 vector.
    Args: 
        (1) bus_v, array, bus voltage.
        (2) par_type: bool, True represent actual value, False repersent estimated value.
    输出: 
        gens_I2, array, generators injection current I2 vector.
    ''' 
    buses = apis.get_all_devices('BUS')
    gens_I2 = np.zeros(len(buses), dtype=complex)  
    
    SBASE = apis_system.get_system_base_data('SBASE')
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        i = apis_system.get_bus_num_after_renumber(generator)
        GMN = apis.get_generator_related_model_data(generator, 'GEN', 'GMN')
        MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
        
        if GMN == 'GENCLS':
            gens_I2[i] = 0.0 + 0.0j
        
        else:        
            if GMN == 'GENROU' or GMN == 'GENSAL':
                Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xdpp')
                Xq = apis.get_generator_related_model_data(generator, 'GEN', 'Xqpp')
            
            elif GMN == 'GENTRA':
                Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xdp')
                Xq = apis.get_generator_related_model_data(generator, 'GEN', 'Xq')        
            else:
                Xd = 0.0
                Xq = 0.0        

            Xd = Xd * SBASE / MBASE
            Xq = Xq * SBASE / MBASE
            Ed, Eq = get_generator_internal_ralated_potential(generator, par_type)
            delta = apis_dynamic.get_generator_state_data(generator, par_type, 'delta')
        
            Ex = Ed * sin(delta) + Eq * cos(delta)
            Ey = -Ed * cos(delta) + Eq * sin(delta)
            E = Ex + 1j * Ey
 
            gens_I2[i] = 0.5j * (Xd - Xq) / (Xd * Xq) * (E.conjugate() - bus_v[i].conjugate()) * (cos(2*delta) + 1j*sin(2*delta))
    
    return gens_I2  
    
def get_generator_internal_ralated_potential(generator, par_type):
    '''
    Get the internal potential of the generator.
    Args: 
        (1) generator, model bus number.
        (2) par_type, par_type, bool, True is for actual value, False is for estimated value.
    Rets: 
        (1) Ed, d-axis potential. 
        (2) Eq, q-axis potential.   
    '''
    GMN = apis.get_generator_related_model_data(generator, 'GEN', 'GMN')
    if GMN == 'GENTRA' or GMN == 'GENCLS':
        Ed = 0.0
        Eq = apis_dynamic.get_generator_state_data(generator, par_type, 'Eqp')

    elif GMN == 'GENROU' or GMN == 'GENSAL':
        Ed = apis_dynamic.get_generator_state_data(generator, par_type, 'Edpp')
        Eq = apis_dynamic.get_generator_state_data(generator, par_type, 'Eqpp')
    
    else:
        Ed = 0.0
        Eq = 0.0      
        
    return Ed, Eq 

def calculate_generator_internal_admittance(generator):
    '''
    Calculate the internal admittance YGP of generator connected to grid
    Args:
        generator, int, generator bus number.
    Rets:
        YGp, float, complex, generator internal admittance connected to grid.
    '''
    GMN = apis.get_generator_related_model_data(generator, 'GEN', 'GMN')
    SBASE = apis_system.get_system_base_data('SBASE')
    MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    if GMN == 'GENCLS':
        ZX = apis.get_device_data(generator, 'GENERATOR', 'ZX')
        Xd = ZX * SBASE / MBASE
        YGp = 1.0 / (1j * Xd)
        
    else:
        if GMN == 'GENROU' or GMN == 'GENSAL':
            Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xdpp')
            Xq = apis.get_generator_related_model_data(generator, 'GEN', 'Xqpp')
            
        elif GMN == 'GENTRA':
            Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xdp')
            Xq = apis.get_generator_related_model_data(generator, 'GEN', 'Xq')        
        else:
            Xd = 0.0
            Xq = 0.0
        Xd = Xd * SBASE / MBASE
        Xq = Xq * SBASE / MBASE
        YGp = -0.5j * (Xd + Xq) / (Xd * Xq)
        
    return YGp