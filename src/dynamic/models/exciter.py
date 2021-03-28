import sys
sys.path.append('../..')

import apis
from apis import apis_dynamic

    
def solve_exciter_model_state_variable(generator, par_type):
    '''
    Solve exciter model state variable.
    Args:
        (1) generator, int, generator connected bus number.
        (2) par_type, bool, state variables type. True for actual value and False for estimated value.
    Rets: None
    '''
    EMN = apis.get_generator_related_model_data(generator, 'AVR', 'EMN')
    if EMN == 'SEXS':
        if par_type is True:
            solve_SEXS_model_state_actual_value(generator)
        else:
            solve_SEXS_model_state_estimated_value(generator)
    else:
        pass
    return
    
def solve_SEXS_model_state_estimated_value(generator):
    '''
    Solve state parameter estimation of SEXS excitation model
    Args: 
       generator, int, SEXS model connected bus number
    Rets: None
    '''
    K = apis.get_generator_related_model_data(generator, 'AVR', 'K')
    TE = apis.get_generator_related_model_data(generator, 'AVR', 'TE')
    EMAX = apis.get_generator_related_model_data(generator, 'AVR', 'EMAX')
    EMIN = apis.get_generator_related_model_data(generator, 'AVR', 'EMIN')
    Vref = apis.get_generator_related_model_data(generator, 'AVR', 'Vref')
    
    EC = abs(apis_dynamic.get_bus_state_data(generator, True, 'Vt'))
    Efq = apis_dynamic.get_generator_state_data(generator, True, 'Efq')
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')
    
    dEfq = 1 / TE * ((Vref - EC) * K - Efq)
    Efq0 = Efq + dEfq * time_step

    if Efq == EMAX and dEfq > 0:
        dEfq = 0
        Efq0 = EMAX
    elif Efq == EMIN and dEfq < 0:
        dEfq = 0
        Efq0 = EMIN
    else:
        Efq0 = Efq + dEfq * time_step
    
    apis_dynamic.set_generator_state_data(generator, False, 'Efq', Efq0)
    return 

def solve_SEXS_model_state_actual_value(generator):
    '''
    Solve actual state parameter of SEXS excitation model
    Args: 
       generator, int, SEXS model connected bus number
    Rets: None
    '''
    EC = abs(apis_dynamic.get_bus_state_data(generator, True, 'Vt'))
    EC0 = abs(apis_dynamic.get_bus_state_data(generator, False, 'Vt'))    
    Efq = apis_dynamic.get_generator_state_data(generator, True, 'Efq')
    Efq0 = apis_dynamic.get_generator_state_data(generator, False, 'Efq')

    time_step = apis.get_simulator_parameter('dynamic', 'time_step')
    K = apis.get_generator_related_model_data(generator, 'AVR', 'K')
    TE = apis.get_generator_related_model_data(generator, 'AVR', 'TE')
    EMAX = apis.get_generator_related_model_data(generator, 'AVR', 'EMAX')
    EMIN = apis.get_generator_related_model_data(generator, 'AVR', 'EMIN')
    Vref = apis.get_generator_related_model_data(generator, 'AVR', 'Vref') 

    dEfq = 1 / TE * ((Vref - EC) * K - Efq)
    if (Efq == EMAX and dEfq > 0) or (Efq == EMIN and dEfq < 0):
        dEfq = 0    
    
    dEfq0 = 1 / TE * ((Vref - EC0) * K - Efq0)
    if (Efq0 == EMAX and dEfq0 > 0) or (Efq0 == EMIN and dEfq0 < 0):
        dEfq0 = 0
    Efq = Efq + (dEfq + dEfq0) * 0.5 * time_step
    
    if Efq > EMAX:
        Efq = EMAX
    if Efq < EMIN:
        Efq = EMIN
        
    apis_dynamic.set_generator_state_data(generator, True, 'Efq', Efq)
    return   
