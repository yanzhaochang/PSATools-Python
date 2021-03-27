import sys
sys.path.append('..')

from database import SyncGenMd, ExciterMd, TurGovMd


def get_generator_related_model_data(generator, model_type, par_name):
    '''
    Get generator related model data.
    Args:
        (1) generator, generator device id in format of bus.
        (2) model_type, str of model type.
        (3) par_name, str of parameter name.
    Rets:
        value, value of parameter. If model type or parameter name is not supported, None is returned.
    '''
    if model_type == 'GEN':
        model_data = SyncGenMd
        
    elif model_type == 'AVR':
        model_data = ExciterMd

    elif model_type == 'GOV':
        model_data = TurGovMd

    else:
        print('Failed to get generator ralated model in model_type {} at generator {}'.format(model_type, generator))
        return
        
    if not model_data:
        return
    if par_name not in model_data[generator].keys():
        print('Failed to get generator ralated model in par_name {} at generator {} with model_type {}'.format(par_name, generator, model_type))
        value = None
    else:
        value = model_data[generator][par_name]
    return value
    
def set_generator_related_model_data(generator, model_type, par_name, value):
    '''
    Set generator related model data.
    If model type or parameter name is not supported, nothing will be changed.
    If value is not a number, function may malfunction and package may exit with error.
    Args:
        (1) generator, int, generator device connected bus.
        (2) model_type, str of model type.
        (3) par_name, str of parameter name.
        (4) value, value of parameter.
    Rets: None
    '''
    if model_type == 'GEN':
        model_data = SyncGenMd
        
    elif model_type == 'AVR':
        model_data = ExciterMd
        
    elif model_type == 'GOV':
        model_data = TurGovMd
        
    else:
        print('Failed to set generator ralated model in model_type {}'.format(model_type))
        return
    model_data[generator][par_name] = value
    return
    
def add_generator_related_model(generator, model_type):
    '''
    Add generator ralated model in database.
    Args:
        (1) generator, int, generator connected bus.
        (2) model_type, str of model type, including GEN, AVR, GOV.
    Rets: None
    '''
    if model_type == 'GEN':
        model_data = SyncGenMd
        
    elif model_type == 'AVR':
        model_data = ExciterMd
        
    elif model_type == 'GOV':
        model_data = TurGovMd
        
    else:
        print('Failed to add generator ralated model in model type {}'.format(model_type))
        return
        
    model_data[generator] = {}
    return
    