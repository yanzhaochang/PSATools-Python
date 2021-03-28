# The solution of differential equation of the model

from .sync_generator import solve_generator_model_state_variable
from .exciter import solve_exciter_model_state_variable
from .turbine_governor import solve_turbine_governor_model_state_variable


def solve_model_state_variables(generator, model, par_type):
    '''
    Solve model state variables at generator.
    Args:
        (1) generator, int, generator connected bus number.
        (2) model, str, model name, including GEN, AVR, GOV.
        (3) par_type, bool, state variables type. True for actual value and False for estimated value.
    Rets: None
    '''
    if model == 'GEN':
        solve_generator_model_state_variable(generator, par_type)
        
    elif model == 'AVR':
        solve_exciter_model_state_variable(generator, par_type)
    
    elif model == 'GOV':
        solve_turbine_governor_model_state_variable(generator, par_type)
        
    else:
        pass
        
    return