# Get or set device power flow data in database.
# Add a power flow device in database.
import sys
sys.path.append('..')

from database import BusData, LoadData, ShuntData, GenData, LineData, TransData, HvdcData, WtGenData, PvUnitData


def add_device(device_index, device):
    '''
    Add a device in database.
    Args:
        (1) device_index, int or tuple, device index.
        (2) device, str, device name.
    Rets: None
    '''
    if device == 'TRANSFORMER':
        add_transformer(device_index)
        
    elif device == 'LINE':
        add_line(device_index) 
        
    elif device == 'BUS':
        add_bus(device_index)
    
    elif device == 'LOAD':
        add_load(device_index)
    
    elif device == 'SHUNT':
        add_shunt(device_index)
    
    elif device == 'GENERATOR':
        add_generator(device_index)
        
    elif device == 'WT GENERATOR':
        add_wt_generator(device_index)
        
    elif device == 'PV UNIT':
        add_pv_unit(device_index)
    
    elif device == 'HVDC':
        add_hvdc(device_index)
        
    else:
        pass
    return

def get_all_devices(device):
    '''
    Get all kinds of devices.
    Args: 
        device, device type.
    Rets: 
        value, all device index.
    '''
    if device == 'BUS':
        value = get_all_buses()

    elif device == 'LOAD':
        value = get_all_loads()
        
    elif device == 'LINE':
        value = get_all_lines()
        
    elif device == 'GENERATOR':
        value = get_all_generators()
    
    elif device == 'WT GENERATOR':
        value = get_all_wt_generators()
        
    elif device == 'PV UNIT':
        value = get_all_pv_units()
        
    elif device == 'SHUNT':
        value = get_all_shunts()
        
    elif device == 'TRANSFORMER':
        value = get_all_transformers()
        
    elif device == 'HVDC':
        value = get_all_hvdcs()
        
    else:
        value = (  )
    return value
    
def get_device_data(device_index, device, par_name):
    '''
    Get a device power flow data.
    Args:
        (1) device_index, device index.
        (2) device, str, device type.
        (3) par_name, parameter name of device.
    Rets:
        value, device data value.
    '''
    if device == 'BUS':
        value = get_bus_data(device_index, par_name)
        
    elif device == 'LOAD':
        value = get_load_data(device_index, par_name)
    
    elif device == 'SHUNT':
        value = get_shunt_data(device_index, par_name)
        
    elif device == 'GENERATOR':
        value = get_generator_data(device_index, par_name)
        
    elif device == 'WT GENERATOR':
        value = get_wt_generator_data(device_index, par_name)
        
    elif device == 'PV UNIT':
        value = get_pv_unit_data(device_index, par_name)
        
    elif device == 'LINE':
        value = get_line_data(device_index, par_name)
        
    elif device == 'TRANSFORMER':
        value = get_transformer_data(device_index, par_name)
        
    elif device == 'HVDC':
        value = get_hvdc_data(device_index, par_name)
        
    else:
        value = None
    return value   
   
def set_device_data(device_index, device, par_name, value):
    '''
    Set a device power flow data.
    Args:
        (1) device_index, device index.
        (2) device, str, device type.
        (3) par_name, parameter name of device.
        (4) value, device data value.
    Rets: None
    '''
    if device == 'BUS':
        set_bus_data(device_index, par_name, value)
    
    elif device == 'LOAD':
        set_load_data(device_index, par_name, value)
        
    elif device == 'SHUNT':
        set_shunt_data(device_index, par_name, value)
        
    elif device == 'GENERATOR':
        set_generator_data(device_index, par_name, value)
        
    elif device == 'WT GENERATOR':
        set_wt_generator_data(device_index, par_name, value)
        
    elif device == 'PV UNIT':
        set_pv_unit_data(device_index, par_name, value)
        
    elif device == 'LINE':
        set_line_data(device_index, par_name, value)
        
    elif device == 'TRANSFORMER':
        set_transformer_data(device_index, par_name, value)
        
    elif device == 'HVDC':
        set_hvdc_data(device_index, par_name, value)
    else:
        pass
    return    

def add_bus(device_index):
    '''
    Add a bus network model to the database.
    Args:
        device_index, int, bus number
    Rets: None
    '''
    columns_name = list(BusData)
    columns_value = []
    for column in columns_name:
        columns_value.append(None)
    BusData.loc[device_index] = columns_value
    
    set_bus_data(device_index, 'IDE', 0)  # initialize
    set_bus_data(device_index, 'VM', 1.0)
    set_bus_data(device_index, 'VA', 0.0)
    set_bus_data(device_index, 'BASKV', 100.0)
    return

def get_all_buses():
    '''
    Get all bus numbers
    Args: None
    Rets: 
        buses, tuple, all bus number
    '''
    index_values = BusData.index.values.tolist()
    return tuple(index_values)

def get_bus_data(device_index, par_name):
    '''
    Get the model information of a bus 
    Args:
        (1) device_index, bus number, int
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(BusData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get bus data'.format(par_name))
        return 
        
    index_values = BusData.index.values.tolist()
    if device_index not in index_values:
        print('bus {} is not exit when get bus data'.format(device_index))
        return
        
    value = BusData.loc[device_index][par_name]
    return value

def set_bus_data(ibus, par_name, value):
    '''
    Set the model information of a bus 
    Args:
        (1) ibus, bus number, int
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(BusData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set bus data'.format(par_name))
        return 
        
    index_values = BusData.index.values.tolist()
    if ibus not in index_values:
        print('bus {} is not exit when set bus data'.format(ibus))
        return
        
    BusData.loc[ibus][par_name] = value
    return 

def add_load(device_index):
    '''
    Add a load network model to the database.
    Args:
        device_index, int, load bus number.
    Rets: None
    '''
    columns_name = list(LoadData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    LoadData.loc[device_index] = columns_value
    return
    
def get_all_loads():
    '''
    Get all loads at bus numbers
    Args: None
    Rets: 
        loads, tuple, all loads number
    '''
    index_values = LoadData.index.values.tolist()
    return tuple(index_values)

def get_load_data(device_index, par_name):
    '''
    Get the model information of a load 
    Args:
        (1) device_index, int, load number at bus
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(LoadData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get load data'.format(par_name))
        return 
        
    index_values = LoadData.index.values.tolist()
    if device_index not in index_values:
        print('load {} is not exit when get load data'.format(device_index))
        return
        
    value = LoadData.loc[device_index][par_name]
    
    return value

def set_load_data(device_index, par_name, value):
    '''
    Set the model information of a load 
    Args:
        (1) device_index, int, load number
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(LoadData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set load data'.format(par_name))
        return 
        
    index_values = LoadData.index.values.tolist()
    if device_index not in index_values:
        print('load {} is not exit when set load data'.format(device_index))
        return
        
    LoadData.loc[device_index][par_name] = value
    return 

def add_shunt(device_index):
    '''
    Add a shunt network model to the database.
    Args:
        device_index, int, shunt bus number.
    Rets: None
    '''
    columns_name = list(ShuntData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    ShuntData.loc[device_index] = columns_value
    return

def get_all_shunts():
    '''
    Get all shunts numbers
    Args: None
    Rets: 
        shunts, tuple, all shunts number
    '''
    index_values = ShuntData.index.values.tolist()
    return tuple(index_values)
    
def get_shunt_data(device_index, par_name):
    '''
    Get the model information of a shunt 
    Args:
        (1) device_index, int, shunt number at bus
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(ShuntData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get shunt data'.format(par_name))
        return 
        
    index_values = ShuntData.index.values.tolist()
    if device_index not in index_values:
        print('shunt {} is not exit when get shunt data'.format(device_index))
        return
        
    value = ShuntData.loc[device_index][par_name]
    
    return value

def set_shunt_data(device_index, par_name, value):
    '''
    Set the model information of a shunt 
    Args:
        (1) device_index, int, shunt number
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(ShuntData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set shunt data'.format(par_name))
        return 
        
    index_values = ShuntData.index.values.tolist()
    if device_index not in index_values:
        print('shunt {} is not exit when set shunt data'.format(device_index))
        return
        
    ShuntData.loc[device_index][par_name] = value
    return   

def add_generator(device_index):
    '''
    Add a generator network model to the database.
    Args:
        device_index, int, generator bus number.
    Rets: None
    '''
    columns_name = list(GenData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    GenData.loc[device_index] = columns_value
    return
    
def get_all_generators():
    '''
    Get all generator numbers
    Args: None
    Rets: 
        generators, tuple, all generator number
    '''
    index_values = GenData.index.values.tolist()
    return tuple(index_values)

def get_generator_data(device_index, par_name):
    '''
    Get the model information of a generator 
    Args:
        (1) device_index, int, generator number at bus
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(GenData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get generator data'.format(par_name))
        return 
        
    index_values = GenData.index.values.tolist()
    if device_index not in index_values:
        print('generator {} is not exit when get generator data'.format(device_index))
        return
        
    value = GenData.loc[device_index][par_name]
    
    return value

def set_generator_data(device_index, par_name, value):
    '''
    Set the model information of a generator 
    Args:
        (1) device_index, int, generator number
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(GenData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set generator data'.format(par_name))
        return 
        
    index_values = GenData.index.values.tolist()
    if device_index not in index_values:
        print('generator {} is not exit when set generator data'.format(device_index))
        return
        
    GenData.loc[device_index][par_name] = value
    return

def add_wt_generator(device_index):
    '''
    Add a wind turbine generator network model to the database.
    Args:
        device_index, int, generator bus number.
    Rets: None
    '''
    columns_name = list(WtGenData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    WtGenData.loc[device_index] = columns_value
    return

def get_all_wt_generators():
    '''
    Get all wt generator numbers
    Args: None
    Rets: 
        generators, tuple, all generator number
    '''
    index_values = WtGenData.index.values.tolist()
    return tuple(index_values)

def get_wt_generator_data(device_index, par_name):
    '''
    Get the model information of a generator 
    Args:
        (1) device_index, int, generator number at bus
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(WtGenData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get wt generator data'.format(par_name))
        return 
        
    index_values = WtGenData.index.values.tolist()
    if device_index not in index_values:
        print('wt generator {} is not exit when get wt generator data'.format(device_index))
        return
        
    value = WtGenData.loc[device_index][par_name]
    
    return value

def set_wt_generator_data(device_index, par_name, value):
    '''
    Set the model information of a generator 
    Args:
        (1) device_index, int, generator number
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(WtGenData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set wt generator data'.format(par_name))
        return 
        
    index_values = WtGenData.index.values.tolist()
    if device_index not in index_values:
        print('wt generator {} is not exit when set wt generator data'.format(device_index))
        return
        
    WtGenData.loc[device_index][par_name] = value
    return

def add_pv_unit(device_index):
    '''
    Add a pv unit network model to the database.
    Args:
        device_index, int, generator bus number.
    Rets: None
    '''
    columns_name = list(PvUnitData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0.0)
    PvUnitData.loc[device_index] = columns_value
    return
    
def get_all_pv_units():
    '''
    Get all generator numbers
    Args: None
    Rets: 
        index_values, tuple, all pv unit number
    '''
    index_values = PvUnitData.index.values.tolist()
    return tuple(index_values)

def get_pv_unit_data(device_index, par_name):
    '''
    Get the model information of a pv unit 
    Args:
        (1) device_index, int, pv unit number at bus
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(PvUnitData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get wt generator data'.format(par_name))
        return 
        
    index_values = PvUnitData.index.values.tolist()
    if device_index not in index_values:
        print('wt generator {} is not exit when get wt generator data'.format(device_index))
        return
        
    value = PvUnitData.loc[device_index][par_name]
    
    return value

def set_pv_unit_data(device_index, par_name, value):
    '''
    Set the model information of a pv unit. 
    Args:
        (1) device_index, int, generator number
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(PvUnitData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set pv unit data'.format(par_name))
        return 
        
    index_values = PvUnitData.index.values.tolist()
    if device_index not in index_values:
        print('pv unit {} is not exit when set pv unit data'.format(device_index))
        return
        
    PvUnitData.loc[device_index][par_name] = value
    return    

def add_line(device_index):
    '''
    Add a line model to the database.
    Args:
        device_index, tuple, (ibus, jbus, ckt)
    Rets: None
    '''
    columns_name = list(LineData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0)
    LineData.loc[str(device_index)] = columns_value
    return 
    
def get_all_lines():
    '''
    Get all lines in system
    Args: None
    Rets: 
        lines, tuple, all lines number
    '''
    index_values = LineData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = eval(index_values[i])
    return index_values
    
def get_line_data(device_index, par_name):
    '''
    Get the model information of a line 
    Args:
        (1) device_index, tuple, (ibus, jbus, ckt)
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(LineData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get line data'.format(par_name))
        return 
        
    index_values = LineData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    if set(device_index) not in index_values:
        print('line {} is not exit when get line data'.format(device_index))
        return
        
    value = LineData.loc[str(device_index)][par_name]
    return value

def set_line_data(device_index, par_name, value):
    '''
    Set the model information of a line 
    Args:
        (1) device_index, tuple, (ibus, jbus, ckt)
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(LineData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set line data'.format(par_name))
        return 
        
    index_values = LineData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    
    if set(device_index) not in index_values:
        print('line {} is not exit when set line data'.format(device_index))
        return
        
    LineData.loc[str(device_index)][par_name] = value
    return   


def add_transformer(device_index):
    '''
    Add a transformer model to the database.
    Args:
        device_index, tuple, (ibus, jbus, kbus)
    Rets: None
    '''
    columns_name = list(TransData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0)
    TransData.loc[str(device_index)] = columns_value
    return 
    
def get_all_transformers():
    '''
    Get all two winding transformer
    Args: None
    Rets: 
        transformers, tuple, (ibus, jbus)
    '''
    index_values = TransData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = eval(index_values[i])
    return index_values

def get_transformer_data(device_index, par_name):
    '''
    Get the model information of a two winding transformer or three winding transformer. 
    Args:
        (1) device_index, tuple, (ibus, jbus) or (ibus, jbus, kbus).
        (2) par_name, str, model parameter name.
    Rets:
        value, model parameter.
    '''
    columns_name = list(TransData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get transformer sequence data'.format(par_name))
        return 
        
    index_values = TransData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    if set(device_index) not in index_values:
        print('line {} is not exit when get transformer sequence data'.format(device_index))
        return
        
    value = TransData.loc[str(device_index)][par_name]
    return value

def set_transformer_data(device_index, par_name, value):
    '''
    Get the model information of a two winding transformer or three winding transformer. 
    Args:
        (1) transformer, tuple, (ibus, jbus) or (ibus, jbus, kbus).
        (2) par_name, str, model parameter name.
    Rets:
        value, model parameter.
    '''
    columns_name = list(TransData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set transformer sequence data'.format(par_name))
        return 
        
    index_values = TransData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    
    if set(device_index) not in index_values:
        print('line {} is not exit when set line transformer data'.format(device_index))
        return
        
    TransData.loc[str(device_index)][par_name] = value
    return    

def add_hvdc(device_index):
    '''
    Add a hvdc model to the database.
    Args:
        device_index, tuple, (ibus, jbus)
    Rets: None
    '''
    columns_name = list(HvdcData)
    columns_value = []
    for i in range(len(columns_name)):
        columns_value.append(0)
    HvdcData.loc[str(device_index)] = columns_value
    return 

def get_all_hvdcs():
    '''
    Get all hvdcs in system
    Args: None
    Rets: 
        hvdcs, tuple, all hvdcs number
    '''
    index_values = HvdcData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = eval(index_values[i])
    return index_values

def get_hvdc_data(device_index, par_name):
    '''
    Get the model information of a hvdc 
    Args:
        (1) device_index, tuple, (ibus, jbus)
        (2) par_name, str, model parameter name
    Rets:
        value, model parameter
    '''
    columns_name = list(HvdcData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when get hvdc data'.format(par_name))
        return 
        
    index_values = HvdcData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    if set(device_index) not in index_values:
        print('hvdc {} is not exit when get hvdc data'.format(device_index))
        return
        
    value = HvdcData.loc[str(device_index)][par_name]
    return value

def set_hvdc_data(device_index, par_name, value):
    '''
    Set the model information of a line 
    Args:
        (1) device_index, tuple, (ibus, jbus)
        (2) par_name, str, model parameter name
        (3) value, value of the parameter
    Rets: None
    '''    
    columns_name = list(HvdcData)   
    if par_name not in columns_name:
        print('par_name {} is not exit when set hvdc data'.format(par_name))
        return 
        
    index_values = HvdcData.index.values.tolist()
    for i in range(len(index_values)):
        index_values[i] = set(eval(index_values[i]))
    
    if set(device_index) not in index_values:
        print('hvdc {} is not exit when set hvdc data'.format(device_index))
        return
        
    HvdcData.loc[str(device_index)][par_name] = value
    return   

def get_device_model_data(ibus, model, par_name):
    '''
    Get the model information of a device model on the bus
    Args:
        (1) ibus, bus number, int
        (2) model, model type, str, including GENRATOR, EXCITATION, TURBINE
        (3) par_name, model parameter name, str
    Rets:
        value, model parameter
    '''
    if model == 'GENERATOR':
        tmp = SyncGenMd
    elif model == 'EXCITATION':
        tmp = ExciterMd
    elif model == 'TURBINE':
        tmp = TurGovMd
    else:
        print('model {} is not existential'.format(model))
        return tuple(value)  
        
    item = [item for item in tmp if item.IBUS==ibus]
    if len(item)==0:
        value = None        
    else:
        item = item[0]
        if hasattr(item, par_name):
            value = getattr(item, par_name)
        else:
            value = None
    return value         
    
def set_device_model_data(ibus, model, par_name, value):
    '''
    Set the model information of a device model on the bus
    Args:
        (1) ibus, bus number, int
        (2) model, model type, str, including GENRATOR, EXCITATION, TURBINE
        (3) par_name, model parameter name, str
        (4) value, value of model parameter
    Rets: None
    '''
    if model == 'GENERATOR':
        model_data = SyncGenMd
    elif model == 'EXCITATION':
        model_data = ExciterMd
    elif model == 'TURBINE':
        model_data = TurGovMd
    else:
        print('model {} is not existential'.format(model))
        return tuple(value)
        
    item = [item for item in model_data if item.IBUS==ibus]
    if len(item)==0:
        print('The model {} at bus {} is not exist'.format(model, ibus))

    else:
        item = item[0]
        if hasattr(item, par_name):
            setattr(item, par_name, value)
        else:
            print('parameter {} in model {} at bus {} is not exsit'.format(par_name, model, ibus))
    return 