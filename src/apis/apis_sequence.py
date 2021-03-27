import sys
sys.path.append('..')

from database import LoadSqData, ShuntSqData, GenSqData, LineSqData, TransSqData, BusSqData


def add_device_sequence_model(device_index, device):
    '''
    Add a device sequence model in database.
    Args:
        (1) device_index, int or tuple, device index.
        (2) device, str, device name.
    Rets: None   
    '''
    if device == 'GENERATOR':
        add_generator_sequence_model(device_index)

    elif device == 'BUS':
        add_bus_sequence_model(device_index)
        
    elif device == 'LINE':
        add_line_sequence_model(device_index)
    
    elif device == 'LOAD':
        add_load_sequence_model(device_index)
        
    elif device == 'TRANSFORMER':
        add_transformer_sequence_model(device_index)
     
    elif device == 'SHUNT':
        add_shunt_sequence_model(device_index)
        
    else:
        print('device {} is not exit'.format(device))
    return

def get_device_sequence_data(device_index, device, par_name):
    '''
    Get a device sequence model data in database.
    Args:
        (1) device_index, int or tuple, device index.
        (2) device, str, device name.
        (3) par_name, str, parameter name.
    Rets: 
        value, parameter value.
    '''
    if device == 'GENERATOR':
        value = get_generator_sequence_data(device_index, par_name)
        
    elif device == 'BUS':
        value = get_bus_sequence_data(device_index, par_name)
        
    elif device == 'LOAD':
        value = get_load_sequence_data(device_index, par_name)
        
    elif device == 'LINE':
        value = get_line_sequence_data(device_index, par_name)
        
    elif device == 'TRANSFORMER':
        value = get_transformer_sequence_data(device_index, par_name)
    
    elif device == 'SHUNT':
        value = get_shunt_sequence_data(device_index, par_name)
        
    else:
        pass
    return value

def set_device_sequence_data(device_index, device, par_name, value):
    '''
    Set a device sequence model data in database.
    Args:
        (1) device_index, int or tuple, device index.
        (2) device, str, device name.
        (3) par_name, str, parameter name.
        (4) value, parameter value.
    Rets: None
    '''
    if device == 'GENERATOR':
        set_generator_sequence_data(device_index, par_name, value)
        
    elif device == 'BUS':
        set_bus_sequence_data(device_index, par_name, value)
        
    elif device == 'LOAD':
        set_load_sequence_data(device_index, par_name, value)
        
    elif device == 'LINE':
        set_line_sequence_data(device_index, par_name, value)
        
    elif device == 'TRANSFORMER':
        set_transformer_sequence_data(device_index, par_name, value)
    
    elif device == 'SHUNT':
        set_shunt_sequence_data(device_index, par_name, value)
    
    else:
        pass
    return 

def add_bus_sequence_model(device_index):   
    '''
    Add a bus sequence network model to the database.
    Args:
        device_index, int, bus number.
    Rets: None
    '''
    columns_name = list(BusSqData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0 + 0.0j)
    BusSqData.loc[device_index] = columns_value
    return

def get_bus_sequence_data(device_index, par_name):
    '''
    Get the model information of a bus sequence data.
    Args:
        (1) device_index, int, generator number at bus.
        (2) par_name, str, model parameter name.
    Rets:
        value, model parameter
    '''
    columns_name = list(BusSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get bus sequence data'.format(par_name))
        return 
        
    index_values = BusSqData.index.values.tolist()
    if device_index not in index_values:
        print('bus {} is not exit when get bus sequence data'.format(device_index))
        return
        
    value = BusSqData.loc[device_index][par_name]
    return value

def set_bus_sequence_data(device_index, par_name, value):
    '''
    Set the model information of a bus sequence data.
    Args:
        (1) device_index, int, bus number.
        (2) par_name, str, model parameter name.
        (3) value, value of the parameter.
    Rets: None
    '''    
    columns_name = list(BusSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set bus sequence data'.format(par_name))
        return 
        
    index_values = BusSqData.index.values.tolist()
    if device_index not in index_values:
        print('bus {} is not exit when set bus sequence data'.format(device_index))
        return
        
    BusSqData.loc[device_index][par_name] = value
    return 

def add_generator_sequence_model(ibus):   
    '''
    Add a generator sequence network model to the database.
    Args:
        ibus, int, generator bus number.
    Rets: None
    '''
    columns_name = list(GenSqData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    GenSqData.loc[ibus] = columns_value
    return

def get_generator_sequence_data(ibus, par_name):
    '''
    Get the model information of a generator sequence data.
    Args:
        (1) ibus, int, generator number at bus
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(GenSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit'.format(par_name))
        return 
        
    index_values = GenSqData.index.values.tolist()
    if ibus not in index_values:
        print('generator {} is not exit'.format(ibus))
        return
        
    value = GenSqData.loc[ibus][par_name]
    return value

def set_generator_sequence_data(ibus, par_name, value):
    '''
    Set the model information of a generator sequence data.
    Args:
        (1) ibus, int, generator number
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(GenSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit'.format(par_name))
        return 
        
    index_values = GenSqData.index.values.tolist()
    if ibus not in index_values:
        print('generator {} is not exit'.format(ibus))
        return
        
    GenSqData.loc[ibus][par_name] = value

    return 

def add_load_sequence_model(ibus):
    '''
    Add a load sequence network model to the database.
    Args:
        ibus, int, load bus number
    Rets: None
    '''
    columns_name = list(LoadSqData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    LoadSqData.loc[ibus] = columns_value
    return

def get_load_sequence_data(ibus, par_name):
    '''
    Get the model information of a load sequence data.
    Args:
        (1) ibus, int, load number at bus
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(LoadSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit'.format(par_name))
        return 
        
    index_values = LoadSqData.index.values.tolist()
    if ibus not in index_values:
        print('generator {} is not exit'.format(ibus))
        return
        
    value = LoadSqData.loc[ibus][par_name]
    return value

def set_load_sequence_data(ibus, par_name, value):
    '''
    Set the model information of a load sequence data.
    Args:
        (1) ibus, int, load number.
        (2) par_name, str, model parameter name.
        (3) value, value of the parameter.
    Rets: None
    '''    
    columns_name = list(LoadSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit'.format(par_name))
        return 
        
    index_values = LoadSqData.index.values.tolist()
    if ibus not in index_values:
        print('load {} is not exit'.format(ibus))
        return
        
    LoadSqData.loc[ibus][par_name] = value
    return 

def add_shunt_sequence_model(device_index):
    '''
    Add a shunt sequence network model to the database.
    Args:
        device_index, tuple, shunt conneted bus number
    Rets: None
    '''
    columns_name = list(ShuntSqData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    ShuntSqData.loc[device_index] = columns_value
    print(ShuntSqData)
    return
    
def get_shunt_sequence_data(device_index, par_name):
    '''
    Get the model information of a shunt sequence data.
    Args:
        (1) ibus, int, shunt number at bus
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(ShuntSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exitwhen get shunt {} data'.format(par_name, device_index))
        return 0.0
        
    index_values = ShuntSqData.index.values.tolist()
    if device_index not in index_values:
        print('shunt {} is not exit when get shunt data parameter {}'.format(device_index, par_name))
        return 0.0
        
    value = ShuntSqData.loc[device_index][par_name]
    
    return value

def set_shunt_sequence_data(device_index, par_name, value):
    '''
    Set the model information of a shunt sequence data.
    Args:
        (1) device_index, int, shunt number.
        (2) par_name, str, model parameter name.
        (3) value, value of the parameter.
    Rets: None
    '''    
    columns_name = list(ShuntSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set shunt sequence data'.format(par_name))
        return 
        
    index_values = ShuntSqData.index.values.tolist()
    if device_index not in index_values:
        print('shunt {} is not exit when set shunt sequence data'.format(device_index))
        return
        
    ShuntSqData.loc[device_index][par_name] = value
    return
    
def add_line_sequence_model(device_index):
    '''
    Add a line sequence network model to the database.
    Args:
        device_index, tuple, (ibus, jbus, ckt)
    Rets: None
    '''
    columns_name = list(LineSqData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    LineSqData.loc[str(device_index)] = columns_value
    return

def get_line_sequence_data(device_index, par_name):
    '''
    Get the model information of a line 
    Args:
        (1) line, tuple, (ibus, jbus, ckt)
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(LineSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get line sequence data'.format(par_name))
        return 
        
    index_values = LineSqData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    if set(device_index) not in index_values:
        print('line {} is not exit'.format(device_index))
        return
        
    value = LineSqData.loc[str(device_index)][par_name]
    return value

def set_line_sequence_data(device_index, par_name, value):
    '''
    Set the model information of a line 
    Args:
        (1) ibus, tuple, (ibus, jbus, ckt)
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(LineSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set line sequence data'.format(par_name))
        return 
        
    index_values = LineSqData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    
    if set(device_index) not in index_values:
        print('line {} is not exit when set line sequence data'.format(device_index))
        return
        
    LineSqData.loc[str(device_index)][par_name] = value
    return
    
def add_transformer_sequence_model(device_index):
    '''
    Add a line sequence network model to the database.
    Args:
        device_index, tuple, (ibus, jbus, ckt)
    Rets: None
    '''
    columns_name = list(TransSqData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0)
    TransSqData.loc[str(device_index)] = columns_value
    return   
    
def get_transformer_sequence_data(device_index, par_name):
    '''
    Get the model information of a two winding transformer or three winding transformer. 
    Args:
        (1) transformer, tuple, (ibus, jbus) or (ibus, jbus, kbus).
        (2) par_name, str, model parameter name.
    Rets:
        value, model parameter.
    '''
    columns_name = list(TransSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get transformer sequence data'.format(par_name))
        return 
        
    index_values = TransSqData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    if set(device_index) not in index_values:
        print('line {} is not exit when get transformer sequence data'.format(device_index))
        return
        
    value = TransSqData.loc[str(device_index)][par_name]
    return value

def set_transformer_sequence_data(device_index, par_name, value): 
    '''
    Get the model information of a two winding transformer or three winding transformer. 
    Args:
        (1) transformer, tuple, (ibus, jbus) or (ibus, jbus, kbus).
        (2) par_name, str, model parameter name.
    Rets:
        value, model parameter.
    '''
    columns_name = list(TransSqData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set transformer sequence data'.format(par_name))
        return 
        
    index_values = TransSqData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    
    if set(device_index) not in index_values:
        print('line {} is not exit when set line transformer data'.format(device_index))
        return
        
    TransSqData.loc[str(device_index)][par_name] = value
    return
