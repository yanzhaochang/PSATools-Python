# 发电机相关api
import sys
sys.path.append('..')

from database import GenStateVar, ExcStateVar, TurStateVar, BusStateVar


def add_model_state_variable(generator, model, value):
    '''
    Add a model variable data in database
    Args:
        (1) model, model type, str
        (2) value, model state variables, dict
    Rets: None
    '''
    if model == 'GENERATOR':
        statevar = GenStateVar
    elif model == 'EXCITATION':
        statevar = ExcStateVar
    elif model == 'TURBINE':
        statevar = TurStateVar
    elif model == 'BUS':
        statevar = BusStateVar
    else:
        print('model {} is wrong'.format(model))
        return None
        
    statevar[generator] = value    
    return

# The following APIs are used to obtain and set state variables in transient simulation
def get_generator_state_data(generator, par_type, par_name):
    '''
    Get generator state data.
    Args:
        (1) generator, 
    '''
    value = get_model_state_variable_data(generator, 'GENERATOR', par_type, par_name)
    return value
    
def set_generator_state_data(generator, par_type, par_name, value):
    set_model_state_variable_data(generator, 'GENERATOR', par_type, par_name, value)
    return

def get_exciter_state_data(generator, par_type, par_name):
    value = get_model_state_variable_data(generator, 'EXCITATION', par_type, par_name)
    return value
    
def set_exciter_state_data(generator, par_type, par_name, value):
    set_model_state_variable_data(generator, 'EXCITATION', par_type, par_name, value)
    return

def get_turbine_state_data(generator, par_type, par_name):
    value = get_model_state_variable_data(generator, 'TURBINE', par_type, par_name)
    return value
    
def set_turbine_state_data(generator, par_type, par_name, value):
    set_model_state_variable_data(generator, 'TURBINE', par_type, par_name, value)
    return   

def get_bus_state_data(generator, par_type, par_name):
    value = get_model_state_variable_data(generator, 'BUS', par_type, par_name)
    return value
    
def set_bus_state_data(generator, par_type, par_name, value):
    set_model_state_variable_data(generator, 'BUS', par_type, par_name, value)
    return

def get_model_state_variable_data(generator, model, par_type, par_name):
    '''
    Get the state variables of a certain type of model
    Args:
        (1) generator, the bus number model connected, int
        (2) model, model name including 'GENERATOR', 'EXCITATION', 'TURBINE', 'BUS', str 
        (3) par_type, the type of state variables, bool, True  represent actual value, False represent estimated value
        (4) par_name, the name of state variables
    Rets:
        value, the value of state variables
    '''
    if model == 'GENERATOR':
        statevar = GenStateVar
    elif model == 'EXCITATION':
        statevar = ExcStateVar
    elif model == 'TURBINE':
        statevar = TurStateVar
    elif model == 'BUS':
        statevar = BusStateVar
    else:
        print('model {} is wrong'.format(model))
        return None
    
    if generator not in statevar.keys():
        print('Failed to get model state variable data in generator {}'.format(generator))
        return
    par = statevar[generator]
    
    if par_name not in par.keys():
        print('Failed to get model state variable data in generator {} with parameter {}'.format(generator, par_name))
        value = None
    else:
        if par_type is True:
            value = par[par_name]
        elif par_type is False:
            value = par[par_name + '0']
        else:
            value = None        
    return value
    
def set_model_state_variable_data(generator, model, par_type, par_name, value):
    '''
    Set the state variables of a certain type of model
    Args:
        (1) generator, the bus number model connected, int
        (2) model, model name including 'GENERATOR', 'EXCITATION', 'TURBINE', 'BUS', str 
        (3) par_type, the type of state variables, bool, True  represent actual value, False represent estimated value
        (4) par_name, the name of state variables
        (5) value, the value of state variables
    Rets: None
    '''
    if model == 'GENERATOR':
        statevar = GenStateVar
    elif model == 'EXCITATION':
        statevar = ExcStateVar
    elif model == 'TURBINE':
        statevar = TurStateVar
    elif model == 'BUS':
        statevar = BusStateVar
    else:
        print('model {} is wrong'.format(model))
        return None
        
    if generator not in statevar.keys():
        print('Failed to set model state variable data in generator {}'.format(generator))
        return        
    par = statevar[generator]

    if par_name not in par.keys():
        print('Failed to set model state variable data in generator {} with parameter {}'.format(generator, par_name))
        return
            
    else:
        if par_type is True:
            par[par_name] = value

        elif par_type is False:
            par[par_name + '0'] = value
        else:
            print('The par_type is wrong')
            
    return
    

    
   
