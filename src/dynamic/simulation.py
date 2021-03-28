# Simulation
import csv
import sys
sys.path.append('..')

import apis
from apis import apis_system
from apis import apis_basic
from apis import apis_dynamic

import network

from .models import solve_model_state_variables
from .network_solution import solve_dynamic_bus_voltage
from .init_simulation import init_system_state_parameter


def start_dynamic_simulation():
    '''
    Initialize the dynamic simulation and initialize the relevant parameters of transient calculation
    Args: None
    Rets: None
    '''
    print('------ Start dynamic simulation -------')
    init_dynamic_output_file()
    
    network.build_network_Y_matrix('dynamic')  # calculation of nodal admittance matrix after load equivalence
    
    init_system_state_parameter()  
    
    generators = apis.get_all_devices('GENERATOR')
    data = 'Time  |'
    for generator in generators:
        data = data + '  delta-{} '.format(generator)
    print(data)
    return 

def run_dynamic_simulation_to_time(stop_time):
    '''
    Run the simulation to a certain time
    Args: 
        stop_time, specific time
    Rets: None
    '''
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')
    while True:
        current_time = apis.get_simulator_parameter('dynamic', 'current_time')
        if current_time > stop_time:
            break
        else:
            show_transient_process_data()  # Show computing information
            add_transient_process_data_to_file()
            run_dynamic_simulation_to_a_step()  # Run one step simulation
            current_time = current_time + time_step
            apis.set_simulator_parameter('dynamic', 'current_time', round(current_time, 4))
    return
    
def run_dynamic_simulation_to_a_step():
    '''
    Run one step simulation
    Args: None
    Rets: None
    '''
    generators = apis.get_all_devices('GENERATOR')
    
    solve_dynamic_bus_voltage(True)  # Solving the actual transient voltage of system bus
    for generator in generators:
        solve_model_state_variables(generator, 'GEN', False)
        solve_model_state_variables(generator, 'AVR', False)
        solve_model_state_variables(generator, 'GOV', False)
    
    solve_dynamic_bus_voltage(False)  # Solving the estimated transient voltage of system bus
    for generator in generators:
        solve_model_state_variables(generator, 'GEN', True)
        solve_model_state_variables(generator, 'AVR', True)
        solve_model_state_variables(generator, 'GOV', True) 
    
    return
    
def show_transient_process_data():
    '''
    Show the information change process of each step of transient process
    Args: None
    Rets: None
    '''
    generators = apis.get_all_devices('GENERATOR')
    current_time = apis.get_simulator_parameter('dynamic', 'current_time')
    data = '{:.3f}  '.format(current_time)
    for generator in generators:
        delta = apis_dynamic.get_generator_state_data(generator, True, 'delta')
        delta = apis_basic.convert_rad_to_deg(delta)
        
        data = data + '{:.6f}  '.format(delta)
    print(data)  
    return

def init_dynamic_output_file():
    '''
    Initialize dynamic simulation output file header.
    Args: None
    Rets: None
    '''
    output_file = apis.get_simulator_parameter('dynamic', 'output_file')
    if len(output_file) == 0:
        return
    meters = apis_system.get_all_dynamic_output_meters()
    csv_head = ['TIME']
    buses = apis.get_all_devices('BUS')
    for meter in meters:
        if meter['device'] == 'BUS':
            csv_head.append('{} AT BUS {}'.format(meter['par_name'], meter['index']))
            
        elif meter['device'] == 'GEN':
            csv_head.append('{} @ GENERATOR {} AT BUS {}'.format(meter['par_name'], meter['index'], meter['index']))
            
        else:
            continue

    with open(output_file, 'w', newline='') as f: 
        csv_write = csv.writer(f)
        csv_write.writerow(csv_head)
    return
    
def add_transient_process_data_to_file():
    '''
    Add transient process data to dynamic output file.
    Args: None
    Rets: None
    '''
    output_file = apis.get_simulator_parameter('dynamic', 'output_file')
    if len(output_file) == 0:
        return
    current_time = current_time = apis.get_simulator_parameter('dynamic', 'current_time')
    data_row = [round(current_time, 4)]
    meters = apis_system.get_all_dynamic_output_meters()
    for meter in meters:
        if meter['device'] == 'BUS':
            Vt = apis_dynamic.get_bus_state_data(meter['index'], True, 'Vt')
            if meter['par_name'] == 'VOLTAGE in PU':
                data_row.append(abs(Vt))
                
            elif meter['par_name'] == 'ANGLE IN DEG':
                value = apis_basic.get_complex_phase_angle(Vt)
                value = apis_basic.convert_rad_to_deg(value)
                data_row.append(value)
                
            elif meter['par_name'] == 'ANGLE IN RAD':
                value = apis_basic.get_complex_phase_angle(Vt)
                data_row.append(value)            
            else:
                data_row.append(None)
                
        elif meter['device'] == 'GEN':
            if meter['par_name'] == 'ROTOR ANGLE IN DEG':
                delta = apis_dynamic.get_generator_state_data(meter['index'], True, 'delta')
                delta = apis_basic.convert_rad_to_deg(delta)
                data_row.append(delta)
            
            elif meter['par_name'] == 'ROTOR ANGLE IN RAD':
                delta = apis_dynamic.get_generator_state_data(meter['index'], True, 'delta')
                data_row.append(delta)  
                
            elif meter['par_name'] == 'TERMINAL ACTIVE POWER IN MW':
                Pe = apis_dynamic.get_generator_state_data(meter['index'], True, 'Pe')
                SBASE = apis_system.get_system_base_data('SBASE')
                data_row.append(Pe*SBASE)
            
            elif meter['par_name'] == 'ROTOR SPEED IN PU':
                omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')
                data_row.append(omega)
                
            elif meter['par_name'] == 'MECHANICAL POWER IN MW':
                Pm = apis_dynamic.get_generator_state_data(generator, True, 'Pm')
                SBASE = apis_system.get_system_base_data('SBASE')
                data_row.append(Pm*SBASE)
            
            elif meter['par_name'] == 'EXCITATION VOLTAGE IN PU':
                Efq = apis_dynamic.get_generator_state_data(generator, True, 'Efq')
                data_row.append(Efq)
                
            else:
                data_row.append(None)
        else:
            continue

        
    with open(output_file, 'a+', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)    
    return
    