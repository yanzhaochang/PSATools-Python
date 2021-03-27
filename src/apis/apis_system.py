# system
import numpy as np
import sys
sys.path.append('..')

from database import Base, YMatrix, PowFlowPar, DynSimPar


def prepare_dynamic_output_meter(device_index, device, par_name):
    '''
    Prepare device output meter in dynamic simulation.
    Args:
        (1) device_index, int, device connected bus number.
        (2) device, str, device name including 'BUS', 'GEN', 'AVR', 'GOV'.
        (3) par_name, str, model state parameter.
    Rets: None
    '''
    meter = DynSimPar['meter']
    meter.append({'index': device_index, 'device': device, 'par_name': par_name})
    return

def get_all_dynamic_output_meters():
    '''
    Get all meter setted before.
    Args: None
    Rets: 
        meter, list, all device meters
    '''
    meter = DynSimPar['meter']
    return meter
    
def get_simulator_parameter(par_type, par_name):
    '''
    Get dynamic simulator configuration parameter.
    Args:
        par_name: String of parameter name.
    Rets:
        value: Value of parameter.
    '''    
    if par_type == 'dynamic':
        simvar = DynSimPar
        
    elif par_type == 'powerflow':
        simvar = PowFlowPar
        
    else:
        print('par_type {} is wrong when getting simulator parameter'.format(par_type))
        
    par_keys = simvar.keys()
    if par_name not in par_keys:
        value = None
        print('par_name {} is not available in par_type {} when getting simulator parameter'.format(par_name, par_type))
    else:
        value = simvar[par_name]
    return value 

def set_simulator_parameter(par_type, par_name, value):
    '''
    Set dynamic simulator configuration parameter.
    Args:
        par_name: String of parameter name.
    Rets: None
    '''    
    if par_type == 'dynamic':
        simvar = DynSimPar
    elif par_type == 'powerflow':
        simvar = PowFlowPar
    else:
        print('par_type {} is wrong when setting simulator parameter'.format(par_type))
        
    par_keys = simvar.keys()
    if par_name not in par_keys:
        print('par_name {} is not available in par_type {} when getting simulator parameter'.format(par_name, par_type))
    else:
        simvar[par_name] = value
    return  
    
def get_bus_num_after_renumber(ibus):
    '''
    Get the bus number after the number
    Args:
        ibus, bus number before renumbering
    Rets:
        ibus, bus number after renumbering
    '''
    BusSqNum = Base['BusSqNum']
    ibus = BusSqNum.index(ibus)
    return ibus

def get_bus_num_before_renumber(ibus):
    '''
    Get the bus number before the number
    Args:
        ibus, bus number after renumbering
    Rets:
        ibus, bus number before renumbering
    '''
    BusSqNum = Base['BusSqNum']
    ibus = BusSqNum[ibus]
    return ibus
  
def get_system_bus_number(par_type):
    '''
    Get the PQ or PV bus number in system.
    Args: None.
    Rets: number, int, 
    '''
    from .apis_device import get_all_devices, get_device_data
    value = 0
    if par_type == 'PQ':
        bus_type = 1
    elif par_type == 'PV':
        bus_type = 2
    else:
        bus_type = 0
        
    buses = get_all_devices('BUS')
    for bus in buses:
        IDE = get_device_data(bus, 'BUS', 'IDE')
        if IDE == bus_type:
            value = value + 1
    return value

def get_system_base_data(par_name):
    '''
    Get system basic data, including based frquency, based power
    Args:
        par_name, str, base parameter name.
    Rets:
        value, value of base parameter
    '''
    par_keys = Base.keys()
    if par_name not in par_keys:
        value = None
        print('The par_name is wrong when getting Y matrix')
    else:
        value = Base[par_name]
    return value  

def set_system_base_data(par_name, value):
    '''
    Set system basic data, including based frquency, based power.
    Args:
        par_name, str, base parameter name.
    Rets:
        value, value of base parameter.
    '''
    Base[par_name] = value
    return value  

def get_system_Y_network_matrix(par_name):
    '''
    Get Y matrix in database
    Args:
        par_name, str, Y matrix name, including 'powerflow', 'dynamic', 'positive', 'negetive', 'zero'
    Rets:
        Y_mat, array, Y matrix
    '''
    from .apis_device import get_all_devices
    
    buses = get_all_devices('BUS')
    par_keys = YMatrix.keys()
    if par_name not in par_keys:
        print('The par_name is wrong when getting Y matrix')
        Y_mat = None
        
    else:
        value = YMatrix[par_name]
        index_values = value.index.values.tolist()
        Y_mat = np.zeros((len(buses), len(buses)), dtype=complex)
        for index in index_values:
            i = int(value.loc[index]['row'])
            j = int(value.loc[index]['column'])
            real = value.loc[index]['real']
            imag = value.loc[index]['imag']
            Y_mat[i, j] = real + 1j * imag
    return Y_mat 

def set_system_Y_network_matrix(par_name, Y_mat):
    '''
    Set Y matrix in database
    Args:
        (1) par_name, str, Y matrix name, including 'basic', 'dynamic', 'positive', 'negetive', 'zero'
        (2) Y_mat, array, Y matrix
    Rets: None
    '''
    YMatrix[par_name].drop(YMatrix[par_name].index, inplace=True)
    n = Y_mat.shape[0]
    a = 0
    value = YMatrix[par_name]
    for i in range(n):
        for j in range(n):
            if Y_mat[i, j] != 0:
                value.loc[a] = [i, j, Y_mat[i, j].real, Y_mat[i, j].imag]
                a = a + 1
    
    value['row'] = value['row'].astype('int')
    value['column'] = value['column'].astype('int')
    return  
    