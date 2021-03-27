# parse sequence data
import sys
sys.path.append('..')

import apis
from apis import apis_basic


def init_sequence_data(file):
    '''
    Initialize sequence net model data.
    Args:
        file, str, data file.
    Rets: None
    '''
    data, index = [], []
    a = 0  

    with open(file, encoding = 'utf-8') as f:
        while True:
            text = f.readline().rstrip('\n')
            if not text:
                break

            if text[0] == '0' and text[1] == ' ' and a > 0: 
                index.append(a)

            data.append(text)
            a = a + 1

    parse_generator_seq(data[1 : index[0]])
    
    parse_load_seq(data[index[0]+1 : index[1]])
    
    parse_line_seq(data[index[1]+1 : index[2]])
    
    #parse_mline_seq(data[index[2]+1 : index[3]])
    
    parse_transformer_seq(data[index[3]+1 : index[4]])
    
    parse_shunt_seq(data[index[5]+1 : index[6]])     

    init_bus_sequence_voltage()    
    return 

def init_bus_sequence_voltage():
    '''
    Initialize node sequence voltage.
    Args: None
    Rets: None
    '''
    buses = apis.get_all_devices('BUS')
    for bus in buses:
        VM = apis.get_device_data(bus, 'BUS', 'VM')
        VA = apis.get_device_data(bus, 'BUS', 'VA')
        VA = apis_basic.convert_deg_to_rad(VA)
        bus_v = apis_basic.build_complex_value(VM, VA)
        
        apis.add_device_sequence_model(bus, 'BUS')
        apis.set_device_sequence_data(bus, 'BUS', 'VP', bus_v)
        apis.set_device_sequence_data(bus, 'BUS', 'VN', 0.0)
        apis.set_device_sequence_data(bus, 'BUS', 'VZ', 0.0)
    return
        
def parse_generator_seq(data):
    '''
    Parse data of generator sequence network model and add to the database.
    Args:
        data, list, generator sequence data.
    Rets: None
    '''
    for i in range(len(data)):
        temp = data[i].split(',')
        
        apis.add_device_sequence_model(int(temp[0]), 'GENERATOR')
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZRPOS', float(temp[2]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZXPPDV', float(temp[3]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZXPDV', float(temp[4]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZXSDV', float(temp[5]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZRNEG', float(temp[6]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZXNEGDV', float(temp[7]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZR0', float(temp[8]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZX0DV', float(temp[9]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZRG', float(temp[11]))
        apis.set_device_sequence_data(int(temp[0]), 'GENERATOR', 'ZXG', float(temp[12]))        
    
    return

def parse_load_seq(data):
    '''
    Parse data of load sequence network model and add to the database.
    Args:
        data, list, load sequence data.
    Rets: None
    '''
    for i in range(len(data)):
        temp = data[i].split(',')
        apis.add_device_sequence_model(int(temp[0]), 'LOAD')
        apis.set_device_sequence_data(int(temp[0]), 'LOAD', 'PNEG', float(temp[2]))
        apis.set_device_sequence_data(int(temp[0]), 'LOAD', 'QNEG', float(temp[3]))
        apis.set_device_sequence_data(int(temp[0]), 'LOAD', 'PZERO', float(temp[5]))
        apis.set_device_sequence_data(int(temp[0]), 'LOAD', 'QZERO', float(temp[6]))
    
    return
    
def parse_line_seq(data):
    '''
    Parse data of line sequence network model and add to the database.
    Args:
        data, list, line sequence data.
    Rets: None
    '''
    for i in range(len(data)):
        temp = data[i].split(',')
        device_index = (int(temp[0]), int(temp[1]), eval(temp[2]))
        apis.add_device_sequence_model(device_index, 'LINE')
        apis.set_device_sequence_data(device_index, 'LINE', 'RLINZ', float(temp[3]))
        apis.set_device_sequence_data(device_index, 'LINE', 'XLINZ', float(temp[4]))
        apis.set_device_sequence_data(device_index, 'LINE', 'BCHZ', float(temp[5]))
        apis.set_device_sequence_data(device_index, 'LINE', 'BI0', float(temp[7]))
        apis.set_device_sequence_data(device_index, 'LINE', 'BJ0', float(temp[9]))
        
    return
    
def parse_transformer_seq(data):
    '''
    Parse data of tranformer sequence network model and add to the database.
    Args:
        data, list, tranformer sequence data.
    Rets: None
    '''
    for i in range(len(data)):
        temp = data[i].split(',')
        device_index = (int(temp[0]), int(temp[1]), int(temp[2]))
        
        apis.add_device_sequence_model(device_index, 'TRANSFORMER')
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'CC', int(temp[6]))
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'RG1', float(temp[7]))
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'XG1', float(temp[8]))
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'R01', float(temp[9]))
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'X01', float(temp[10]))        
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'RG2', float(temp[11]))
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'XG2', float(temp[12]))
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'R02', float(temp[13]))
        apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'X02', float(temp[14]))            
        if len(temp) > 18:
            apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'RG3', float(temp[15]))
            apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'XG3', float(temp[16]))
            apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'R03', float(temp[17]))
            apis.set_device_sequence_data(device_index, 'TRANSFORMER', 'X03', float(temp[18]))         
        
    return
    
def parse_shunt_seq(data):
    '''
    Parse data of shunt sequence network model and add to the database.
    Args:
        data, list, shunt sequence data.
    Rets: None
    '''
    for i in range(len(data)):
        print('s')
        temp = data[i].split(',')
        device_index = int(temp[0])
        apis.add_device_sequence_model(device_index, 'SHUNT')
        apis.set_device_sequence_data(device_index, 'SHUNT', 'BSZERO', float(temp[3]))
    return   
