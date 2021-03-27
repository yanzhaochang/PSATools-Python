import sys
sys.path.append('..')

import apis
from apis import apis_system


def init_powerflow_data(file):
    '''
    Initialize the power flow data, parse the data of each component from the file and import it into memory.
    Args: 
        file, str, power flow raw file.
    Rets: None
    '''
    data, index, a = [], [], 0
    with open(file) as f:
        while True:
            text = f.readline().rstrip('\n')
            if not text:
                break
            if text[0] == '0' and text[1] == ' ' and a > 2: 
                index.append(a)
            data.append(text)
            a = a + 1
    
    parse_rate(data[0])
    
    parse_bus(data[3:index[0]])

    parse_load(data[index[0] + 1 : index[1]])

    parse_shunt(data[index[1] + 1 : index[2]])
    
    parse_generator(data[index[2] + 1 : index[3]])

    parse_line(data[index[3] + 1 : index[4]])

    parse_transformer(data[index[4] + 1 : index[5]])
    
    parse_hvdc(data[index[6] + 1 : index[7]])
 
    check_network()
    
    renumber_bus_node()
    return

def check_network():
    '''
    Check the network structure, fan and photovoltaic bus type. If it is PV, change it to PQ node
    Args: None
    Rets: None
    '''
    wt_generators = apis.get_all_devices('WT GENERATOR')
    for wt_generator in wt_generators:
        IDE = apis.get_device_data(wt_generator, 'BUS', 'IDE')
        if IDE == 2:
            apis.set_device_data(wt_generator, 'BUS', 'IDE', 1)
            
    pv_units = apis.get_all_devices('PV UNIT')
    for pv_unit in pv_units:
        IDE = apis.get_device_data(pv_unit, 'BUS', 'IDE')
        if IDE == 2:
            apis.set_device_data(pv_unit, 'BUS', 'IDE', 1)    

    return

def renumber_bus_node():
    '''
    Renumber bus node.
    Args: None
    Rets：None
    '''
    PQ = []
    PV = []
    swing = []
    buses = apis.get_all_devices('BUS')
    for bus in buses:
        IDE = apis.get_device_data(bus, 'BUS', 'IDE')
        if IDE == 1:
            PQ.append(bus)
        elif IDE == 2:
            PV.append(bus)
        elif IDE == 3:
            swing.append(bus)
        else:
            pass
    
    node = PQ + PV + swing
    apis_system.set_system_base_data('BusSqNum', node)
    return 

def parse_rate(data):
    '''
    Parse system base reference capacity and reference frequency
    Args:
        data, list, base data.
    Rets: None
    '''
    temp = data.split(',')
    apis_system.set_system_base_data('SBASE', float(temp[1]))
    apis_system.set_system_base_data('BASFRQ', float(temp[5].split('/')[0]))
    return
    
def parse_bus(data):
    '''
    Parse data of bus steady state model and add to the database.
    Args:
        data, list, bus data.
    Rets: None
    '''
    for item in data:
        temp = item.split(',')  
        device_index = int(temp[0]) 
        apis.add_device(device_index, 'BUS')
        
        apis.set_device_data(device_index, 'BUS', 'BASKV', float(temp[2]))
        apis.set_device_data(device_index, 'BUS', 'IDE', int(temp[3]))
        apis.set_device_data(device_index, 'BUS', 'VM', float(temp[7]))
        apis.set_device_data(device_index, 'BUS', 'VA', float(temp[8]))
    return

def parse_load(data):
    '''
    Parse data of load steady state model and add to the database, only including constant power load.
    Args:
        data, list, load data.
    Rets: None
    '''
    for item in data:
        temp = item.split(',')
        device_index = int(temp[0])
        apis.add_device(device_index, 'LOAD')
        
        apis.set_device_data(device_index, 'LOAD', 'PL', float(temp[5]))
        apis.set_device_data(device_index, 'LOAD', 'QL', float(temp[6]))        
    return    

def parse_shunt(data):
    '''
    Parse data of shunt steady state model and add to the database.
    Args:
        data, list, shunt data.
    Rets: None
    '''
    for item in data:
        temp = item.split(',')
        device_index = int(temp[0])
        apis.add_device(device_index, 'SHUNT') 
        apis.set_device_data(device_index, 'SHUNT', 'BL', float(temp[4]))        
    return

def parse_generator(data):
    '''
    Parse data of generator steady state model and add to the database.
    Args:
        data, list, generator data.
    Rets: None
    '''
    for item in data:
        temp = item.split(',')
        device_index = int(temp[0])
        
        if int(temp[26]) == 3:
            apis.add_device(device_index, 'WT GENERATOR')
            apis.set_device_data(device_index, 'WT GENERATOR', 'PG', float(temp[2]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'QG', float(temp[3]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'QT', float(temp[4]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'QB', float(temp[5]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'VS', float(temp[6]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'MBASE', float(temp[8]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'ZR', float(temp[9]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'ZX', float(temp[10]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'PT', float(temp[16]))
            apis.set_device_data(device_index, 'WT GENERATOR', 'PB', float(temp[17]))   
            
        elif int(temp[26]) == 2:    
            apis.add_device(device_index, 'PV UNIT')
            apis.set_device_data(device_index, 'PV UNIT', 'PG', float(temp[2]))
            apis.set_device_data(device_index, 'PV UNIT', 'QG', float(temp[3]))
            apis.set_device_data(device_index, 'PV UNIT', 'QT', float(temp[4]))
            apis.set_device_data(device_index, 'PV UNIT', 'QB', float(temp[5]))
            apis.set_device_data(device_index, 'PV UNIT', 'VS', float(temp[6]))
            apis.set_device_data(device_index, 'PV UNIT', 'MBASE', float(temp[8]))
            apis.set_device_data(device_index, 'PV UNIT', 'ZR', float(temp[9]))
            apis.set_device_data(device_index, 'PV UNIT', 'ZX', float(temp[10]))
            apis.set_device_data(device_index, 'PV UNIT', 'PT', float(temp[16]))
            apis.set_device_data(device_index, 'PV UNIT', 'PB', float(temp[17]))   
            
        elif int(temp[26]) == 0:              
            apis.add_device(device_index, 'GENERATOR')
            apis.set_device_data(device_index, 'GENERATOR', 'PG', float(temp[2]))
            apis.set_device_data(device_index, 'GENERATOR', 'QG', float(temp[3]))
            apis.set_device_data(device_index, 'GENERATOR', 'QT', float(temp[4]))
            apis.set_device_data(device_index, 'GENERATOR', 'QB', float(temp[5]))
            apis.set_device_data(device_index, 'GENERATOR', 'VS', float(temp[6]))
            apis.set_device_data(device_index, 'GENERATOR', 'MBASE', float(temp[8]))
            apis.set_device_data(device_index, 'GENERATOR', 'ZR', float(temp[9]))
            apis.set_device_data(device_index, 'GENERATOR', 'ZX', float(temp[10]))
            apis.set_device_data(device_index, 'GENERATOR', 'PT', float(temp[16]))
            apis.set_device_data(device_index, 'GENERATOR', 'PB', float(temp[17]))   
        else:   
            pass
    return

def parse_line(data):
    '''
    Parse data of line steady state model and add to the database.
    Args:
        data, list, line data.
    Rets: None
    '''
    for item in data:
        temp = item.split(',')
        device_index = (int(temp[0]), int(temp[1]), eval(temp[2]))
        apis.add_device(device_index, 'LINE')
        apis.set_device_data(device_index, 'LINE', 'R', float(temp[3]))
        apis.set_device_data(device_index, 'LINE', 'X', float(temp[4]))
        apis.set_device_data(device_index, 'LINE', 'B', float(temp[5]))
        apis.set_device_data(device_index, 'LINE', 'BI', float(temp[10]))
        apis.set_device_data(device_index, 'LINE', 'BJ', float(temp[12]))
    return

def parse_transformer(data):
    '''
    Parse data of transformer steady state model and add to the database.
    Args:
        data, list, transformer data.
    Rets: None
    '''
    data = iter(data)  
    for item in data:
        rows = [item]
        rows.append(next(data))  
        rows.append(next(data))
        rows.append(next(data))
        if int(item.split(',')[2]) != 0:  
            rows.append(next(data))
        
        if len(rows) == 4:  # Two winding transformer
            temp = rows[0].split(',')
            device_index = (int(temp[0]), int(temp[1]), int(temp[2]))
            apis.add_device(device_index, 'TRANSFORMER')
            
            apis.set_device_data(device_index, 'TRANSFORMER', 'MAG1', float(temp[7]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'MAG2', float(temp[8]))
            
            temp = rows[1].split(',')
            apis.set_device_data(device_index, 'TRANSFORMER', 'R1_2', float(temp[0]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'X1_2', float(temp[1]))            
            apis.set_device_data(device_index, 'TRANSFORMER', 'SBASE1_2', float(temp[2]))
            
            temp = rows[2].split(',')
            apis.set_device_data(device_index, 'TRANSFORMER', 'WINDV1', float(temp[0]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'NOMV1', float(temp[1]))

            temp = rows[3].split(',')
            apis.set_device_data(device_index, 'TRANSFORMER', 'WINDV2', float(temp[0]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'NOMV2', float(temp[1]))

        else:  # Three winding transformer
            temp = rows[0].split(',')
            device_index = (int(temp[0]), int(temp[1]), int(temp[2]))
            apis.add_device(device_index, 'TRANSFORMER')
            
            apis.set_device_data(device_index, 'TRANSFORMER', 'MAG1', float(temp[7]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'MAG2', float(temp[8]))
            
            temp = rows[1].split(',')
            apis.set_device_data(device_index, 'TRANSFORMER', 'R1_2', float(temp[0]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'X1_2', float(temp[1]))            
            apis.set_device_data(device_index, 'TRANSFORMER', 'SBASE1_2', float(temp[2]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'R2_3', float(temp[3])) 
            apis.set_device_data(device_index, 'TRANSFORMER', 'X2_3', float(temp[4]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'SBASE2_3', float(temp[5])) 
            apis.set_device_data(device_index, 'TRANSFORMER', 'R3_1', float(temp[6]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'X3_1', float(temp[7])) 
            apis.set_device_data(device_index, 'TRANSFORMER', 'SBASE3_1', float(temp[8]))
            
            temp = rows[2].split(',')
            apis.set_device_data(device_index, 'TRANSFORMER', 'WINDV1', float(temp[0]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'NOMV1', float(temp[1]))
            
            temp = rows[3].split(',')
            apis.set_device_data(device_index, 'TRANSFORMER', 'WINDV2', float(temp[0]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'NOMV2', float(temp[1])) 

            temp = rows[4].split(',')
            apis.set_device_data(device_index, 'TRANSFORMER', 'WINDV3', float(temp[0]))
            apis.set_device_data(device_index, 'TRANSFORMER', 'NOMV3', float(temp[1])) 
    return

def parse_hvdc(data):
    '''
    Parse data of hvdc steady state model and add to the database.
    Args:
        data, list, hvdc data.
    Rets: None
    '''
    if len(data) == 0:
        return
    k = 0
    while True:

        row1 = data[k].split(',')
        row2 = data[k+1].split(',')
        row3 = data[k+2].split(',')
        
        device_index = (int(row2[0]), int(row3[0]))
        apis.add_device(device_index, 'HVDC')

        apis.set_device_data(device_index, 'HVDC', 'RDC', float(row1[2]))
        apis.set_device_data(device_index, 'HVDC', 'SETVL', float(row1[3]))
        apis.set_device_data(device_index, 'HVDC', 'VSCHD', float(row1[4]))
        
        apis.set_device_data(device_index, 'HVDC', 'NBR', int(row2[1]))
        apis.set_device_data(device_index, 'HVDC', 'ANMXR', float(row2[2]))
        apis.set_device_data(device_index, 'HVDC', 'ANMNR', float(row2[3]))
        apis.set_device_data(device_index, 'HVDC', 'RCR', float(row2[4]))        
        apis.set_device_data(device_index, 'HVDC', 'XCR', float(row2[5]))
        apis.set_device_data(device_index, 'HVDC', 'EBASR', float(row2[6]))
        apis.set_device_data(device_index, 'HVDC', 'TRR', float(row2[7]))
        apis.set_device_data(device_index, 'HVDC', 'TAPR', float(row2[8]))
        apis.set_device_data(device_index, 'HVDC', 'TMXR', float(row2[9]))
        apis.set_device_data(device_index, 'HVDC', 'TMNR', float(row2[10]))        
        apis.set_device_data(device_index, 'HVDC', 'STPR', float(row2[11]))
        apis.set_device_data(device_index, 'HVDC', 'XCAPR', float(row2[16]))
        
        apis.set_device_data(device_index, 'HVDC', 'NBI', int(row3[1]))
        apis.set_device_data(device_index, 'HVDC', 'ANMXI', float(row3[2]))
        apis.set_device_data(device_index, 'HVDC', 'ANMNI', float(row3[3]))
        apis.set_device_data(device_index, 'HVDC', 'RCI', float(row3[4]))        
        apis.set_device_data(device_index, 'HVDC', 'XCI', float(row3[5]))
        apis.set_device_data(device_index, 'HVDC', 'EBASI', float(row3[6]))
        apis.set_device_data(device_index, 'HVDC', 'TRI', float(row3[7]))
        apis.set_device_data(device_index, 'HVDC', 'TAPI', float(row3[8]))
        apis.set_device_data(device_index, 'HVDC', 'TMXI', float(row3[9]))
        apis.set_device_data(device_index, 'HVDC', 'TMNI', float(row3[10]))        
        apis.set_device_data(device_index, 'HVDC', 'STPI', float(row3[11]))
        apis.set_device_data(device_index, 'HVDC', 'XCAPI', float(row3[16]))        
        
        k = k + 3
        if k >= len(data):
            break
    return