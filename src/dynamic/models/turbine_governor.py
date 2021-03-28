import sys
sys.path.append('../..')
import apis
from apis import apis_dynamic


def solve_turbine_governor_model_state_variable(generator, par_type):
    '''
    Solve turbine governor model state variables.
    Args:
        (1) generator, int, generator connected bus number.
        (2) par_type, bool, state variables type. True for actual value and False for estimated value.
    Rets: None
    '''
    TGMN = apis.get_generator_related_model_data(generator, 'GOV', 'TGMN')
    if TGMN == 'IEEEG1':
        if par_type is True:
            solve_IEEEG1_model_state_actual_value(generator)
        else:
            solve_IEEEG1_model_state_estimated_value(generator)
            
    elif TGMN == 'IEEEG3':
        if par_type is True:
            solve_IEEEG3_model_state_actual_value(generator)
        else:
            solve_IEEEG3_model_state_estimated_value(generator)
    
    else:
        pass
    return

def solve_IEEEG1_model_state_estimated_value(generator):
    '''
    Solving the estimated value of state parameters of IEEEG1 governor model
    Args: 
        generator, IEEEG1 model connected bus number
    Rets: None
    '''
    x1 = apis_dynamic.get_turbine_state_data(generator, True, 'x1')
    x2 = apis_dynamic.get_turbine_state_data(generator, True, 'x2')
    x3 = apis_dynamic.get_turbine_state_data(generator, True, 'x3')
  
    
    omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')
    
    P0 = apis.get_generator_related_model_data(generator, 'GOV', 'P0')
    K = apis.get_generator_related_model_data(generator, 'GOV', 'K') 
    K1 = apis.get_generator_related_model_data(generator, 'GOV', 'K1')
    K3 = apis.get_generator_related_model_data(generator, 'GOV', 'K3')
    T3 = apis.get_generator_related_model_data(generator, 'GOV', 'T3')
    UO = apis.get_generator_related_model_data(generator, 'GOV', 'UO')
    UC = apis.get_generator_related_model_data(generator, 'GOV', 'UC')
    PMAX = apis.get_generator_related_model_data(generator, 'GOV', 'PMAX')
    PMIN = apis.get_generator_related_model_data(generator, 'GOV', 'PMIN')
    T4 = apis.get_generator_related_model_data(generator, 'GOV', 'T4')
    T5 = apis.get_generator_related_model_data(generator, 'GOV', 'T5')

    dx1 = (P0 - abs(omega-1.0) * K - x1) / T3

    if dx1 > UO:
        dx1 = UO
    if dx1 < UC:
        dx1 = UC
        
    if x1 == PMAX and dx1 > 0:
        dx1 = 0
    if x1 == PMIN and dx1 < 0:
        dx1 = 0
    
    dx2 = (x1 - x2) / T4
    dx3 = (x2 - x3) / T5

    x10 = x1 + dx1 * time_step
    x20 = x2 + dx2 * time_step
    x30 = x3 + dx3 * time_step
    
    Pm0 = K1 * x20 + K3 * x30

    apis_dynamic.set_turbine_state_data(generator, False, 'x1', x10)
    apis_dynamic.set_turbine_state_data(generator, False, 'x2', x20)
    apis_dynamic.set_turbine_state_data(generator, False, 'x3', x30)
    
    apis_dynamic.set_generator_state_data(generator, False, 'Pm', Pm0)
    
    return 
    
def solve_IEEEG1_model_state_actual_value(generator):
    ''' 
    Solving the actual value of state parameters of IEEEG1 governor model
    Args: 
        turbine, IEEEG1 model parameters
    Rets: 
        None
    '''
    x1 = apis_dynamic.get_turbine_state_data(generator, True, 'x1')
    x2 = apis_dynamic.get_turbine_state_data(generator, True, 'x2')
    x3 = apis_dynamic.get_turbine_state_data(generator, True, 'x3')
    
    x10 = apis_dynamic.get_turbine_state_data(generator, False, 'x1')
    x20 = apis_dynamic.get_turbine_state_data(generator, False, 'x2')
    x30 = apis_dynamic.get_turbine_state_data(generator, False, 'x3')   
    
    omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')
    omega0 = apis_dynamic.get_generator_state_data(generator, False, 'omega')
    
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')
    
    P0 = apis.get_generator_related_model_data(generator, 'GOV', 'P0')
    K = apis.get_generator_related_model_data(generator, 'GOV', 'K') 
    K1 = apis.get_generator_related_model_data(generator, 'GOV', 'K1')
    K3 = apis.get_generator_related_model_data(generator, 'GOV', 'K3')
    T3 = apis.get_generator_related_model_data(generator, 'GOV', 'T3')
    UO = apis.get_generator_related_model_data(generator, 'GOV', 'UO')
    UC = apis.get_generator_related_model_data(generator, 'GOV', 'UC')
    PMAX = apis.get_generator_related_model_data(generator, 'GOV', 'PMAX')
    PMIN = apis.get_generator_related_model_data(generator, 'GOV', 'PMIN')
    T4 = apis.get_generator_related_model_data(generator, 'GOV', 'T4')
    T5 = apis.get_generator_related_model_data(generator, 'GOV', 'T5')

    dx1 = (P0 - abs(omega-1) * K - x1) / T3
    if dx1 > UO:
        dx1 = UO
    if dx1 < UC:
        dx1 = UC
        
    if x1 == PMAX and dx1 > 0:
        dx1 = 0
    if x1 == PMIN and dx1 < 0:
        dx1 = 0
    
    dx2 = (x1 - x2) / T4
    dx3 = (x2 - x3) / T5
    
    dx10 = (P0 - abs(omega0-1) * K - x10) / T3
    if dx10 > UO:
        dx10 = UO
    if dx10 < UC:
        dx10 = UC
        
    if x10 == PMAX and dx10 > 0:
        dx10 = 0
    if x10 == PMIN and dx10 < 0:
        dx10 = 0
    
    dx20 = (x10 - x20) / T4
    dx30 = (x20 - x30) / T5
    
    x1 = x1 + (dx1 + dx10) * 0.5 * time_step
    x2 = x2 + (dx2 + dx20) * 0.5 * time_step    
    x3 = x3 + (dx3 + dx30) * 0.5 * time_step

    Pm = K1 * x2 + K3 * x3
    
    apis_dynamic.set_turbine_state_data(generator, True, 'x1', x1)
    apis_dynamic.set_turbine_state_data(generator, True, 'x2', x2)
    apis_dynamic.set_turbine_state_data(generator, True, 'x3', x3)
    
    apis_dynamic.set_generator_state_data(generator, True, 'Pm', Pm)
    
    return     

def solve_IEEEG3_model_state_estimated_value(generator):
    '''
    Solving the estimated value of state parameters of IEEEG3 governor model
    Args: 
        generator, IEEEG3 model parameters
    Rets: 
        None
    '''
    x1 = apis_dynamic.get_turbine_state_data(generator, True, 'x1')
    x2 = apis_dynamic.get_turbine_state_data(generator, True, 'x2')
    x3 = apis_dynamic.get_turbine_state_data(generator, True, 'x3')
    x4 = apis_dynamic.get_turbine_state_data(generator, True, 'x4')       
 
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')
    omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')
    
    P0 = apis.get_generator_related_model_data(generator, 'GOV', 'P0')
    UO = apis.get_generator_related_model_data(generator, 'GOV', 'UO')
    UC = apis.get_generator_related_model_data(generator, 'GOV', 'UC')
    TP = apis.get_generator_related_model_data(generator, 'GOV', 'TP')
    TG = apis.get_generator_related_model_data(generator, 'GOV', 'TG')
    PMAX = apis.get_generator_related_model_data(generator, 'GOV', 'PMAX')
    PMIN = apis.get_generator_related_model_data(generator, 'GOV', 'PMIN')
    delta = apis.get_generator_related_model_data(generator, 'GOV', 'delta')
    sigma = apis.get_generator_related_model_data(generator, 'GOV', 'sigma')
    TR = apis.get_generator_related_model_data(generator, 'GOV', 'TR')
    a11 = apis.get_generator_related_model_data(generator, 'GOV', 'a11')
    a21 = apis.get_generator_related_model_data(generator, 'GOV', 'a21')
    a13 = apis.get_generator_related_model_data(generator, 'GOV', 'a13')
    a23 = apis.get_generator_related_model_data(generator, 'GOV', 'a23')
    TW = apis.get_generator_related_model_data(generator, 'GOV', 'TW')

    x1_input = P0 - abs(omega - 1) - sigma * x2 - TR * x2 - x3
    
    dx1 = (x1_input / TG - x1) / TP
    if x1 == UO and dx1 > 0:
        dx1 = 0
    if x1 == UC and dx1 < 0:
        dx1 = 0
        
    dx2 = x1
    if x2 == PMAX and dx2 > 0:
        dx2 = 0
    if x2 == PMIN and dx2 < 0:
        dx2 = 0
        
    dx3 = (-delta * TR * x2 - TR * x3) / TR**2
    
    dx4 = (-a13*a21*TW * x2 - a11*TW * x4) / (a11*TW)**2
    
    x10 = x1 + dx1 * time_step
    if x10 > UO:
        x10 = UO
    if x10 < UC:
        x10 = UC
    
    x20 = x2 + dx2 * time_step
    if x20 > PMAX:
        x20 = PMAX
    if x20 < PMIN:
        x20 = PMIN
    
    x30 = x3 + dx3 * time_step
    x40 = x4 + dx4 * time_step
    
    Pm0 = a23 * x20 + (a13*a21/a11) * x20 + x40

    apis_dynamic.set_turbine_state_data(generator, False, 'x1', x10)
    apis_dynamic.set_turbine_state_data(generator, False, 'x2', x20)
    apis_dynamic.set_turbine_state_data(generator, False, 'x3', x30)
    apis_dynamic.set_turbine_state_data(generator, False, 'x4', x40)
    
    apis_dynamic.set_generator_state_data(generator, False, 'Pm', Pm0)
    
    return 
    
def solve_IEEEG3_model_state_actual_value(generator):
    '''
    Solving the estimated value of state parameters of IEEEG3 governor model
    Args: 
        generator, IEEEG3 model parameters
    Rets: 
        None
    '''
    x1 = apis_dynamic.get_turbine_state_data(generator, True, 'x1')
    x2 = apis_dynamic.get_turbine_state_data(generator, True, 'x2')
    x3 = apis_dynamic.get_turbine_state_data(generator, True, 'x3')
    x4 = apis_dynamic.get_turbine_state_data(generator, True, 'x4')    
 
    x10 = apis_dynamic.get_turbine_state_data(generator, False, 'x1')
    x20 = apis_dynamic.get_turbine_state_data(generator, False, 'x2')
    x30 = apis_dynamic.get_turbine_state_data(generator, False, 'x3')
    x40 = apis_dynamic.get_turbine_state_data(generator, False, 'x4')
    
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')
    omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')   
    omega0 = apis_dynamic.get_generator_state_data(generator, False, 'omega') 
    
    P0 = apis.get_generator_related_model_data(generator, 'GOV', 'P0')
    UO = apis.get_generator_related_model_data(generator, 'GOV', 'UO')
    UC = apis.get_generator_related_model_data(generator, 'GOV', 'UC')
    TP = apis.get_generator_related_model_data(generator, 'GOV', 'TP')
    TG = apis.get_generator_related_model_data(generator, 'GOV', 'TG')
    PMAX = apis.get_generator_related_model_data(generator, 'GOV', 'PMAX')
    PMIN = apis.get_generator_related_model_data(generator, 'GOV', 'PMIN')
    delta = apis.get_generator_related_model_data(generator, 'GOV', 'delta')
    sigma = apis.get_generator_related_model_data(generator, 'GOV', 'sigma')
    TR = apis.get_generator_related_model_data(generator, 'GOV', 'TR')
    a11 = apis.get_generator_related_model_data(generator, 'GOV', 'a11')
    a21 = apis.get_generator_related_model_data(generator, 'GOV', 'a21')
    a13 = apis.get_generator_related_model_data(generator, 'GOV', 'a13')
    a23 = apis.get_generator_related_model_data(generator, 'GOV', 'a23')
    TW = apis.get_generator_related_model_data(generator, 'GOV', 'TW')
    
    x1_input = P0 - abs(omega - 1) - sigma * x2 - TR * x2 - x3
    
    dx1 = (x1_input / TG - x1) / TP
    if x1 == UO and dx1 > 0:
        dx1 = 0
    if x1 == UC and dx1 < 0:
        dx1 = 0
        
    dx2 = x1
    if x2 == PMAX and dx2 > 0:
        dx2 = 0
    if x2 == PMIN and dx2 < 0:
        dx2 = 0
        
    dx3 = (-delta * TR * x2 - TR * x3) / TR**2
    
    dx4 = (-a13*a21*TW * x2 - a11*TW * x4) / (a11*TW)**2

    x1_input0 = P0 - abs(omega0 - 1) - sigma * x20 - TR * x20 - x30
    
    dx10 = (x1_input0 / TG - x10) / TP
    if x10 == UO and dx10 > 0:
        dx10 = 0
    if x10 == UC and dx10 < 0:
        dx10 = 0
        
    dx20 = x10
    if x20 == PMAX and dx20 > 0:
        dx20 = 0
    if x20 == PMIN and dx20 < 0:
        dx20 = 0
        
    dx30 = (-delta * TR * x20 - TR * x30) / TR**2
    
    dx40 = (-a13*a21*TW * x20 - a11*TW * x40) / (a11*TW)**2 
    
    x1 = x1 + (dx1 + dx10) * 0.5 * time_step
    x2 = x2 + (dx2 + dx20) * 0.5 * time_step
    x3 = x3 + (dx3 + dx30) * 0.5 * time_step
    x4 = x4 + (dx4 + dx40) * 0.5 * time_step   

    Pm = a23 * x2 + (a13*a21/a11) * x2 + x4
    
    apis_dynamic.set_turbine_state_data(generator, True, 'x1', x1)
    apis_dynamic.set_turbine_state_data(generator, True, 'x2', x2)
    apis_dynamic.set_turbine_state_data(generator, True, 'x3', x3)
    apis_dynamic.set_turbine_state_data(generator, True, 'x4', x4)
    
    apis_dynamic.set_generator_state_data(generator, True, 'Pm', Pm)
    
    return 