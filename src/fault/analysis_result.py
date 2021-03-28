# fault analysis result
import csv
import sys
sys.path.append('..')

import apis
from apis import apis_system
from apis import apis_basic


def save_fault_analysis_result(file):
    '''
    Save the results of fault analysis, including node sequence voltage, three-phase voltage, 
        branch sequence current and line three-phase current.
    Args:
    '''    
    bus_data = get_bus_analysis_result()
    
    line_data = get_line_analysis_result()
    
    #transformer_data = get_transformer_analysis_result()  # The calculation results of the transformer are not saved for the time being
    
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(bus_data) 
        writer.writerow([''])
        writer.writerows(line_data) 
    return
    
def get_bus_analysis_result():
    '''
    Get the results of bus fault analysis.
    Args: None
    Rets: 
        bus_data, list, bus analysis result.
    '''
    bus_data = [['BUS', 'VP', 'VN', 'VZ', 'VA', 'VB', 'VC']]
    buses = apis.get_all_devices('BUS')
    for bus in buses:
    
        VP = apis.get_device_sequence_data(bus, 'BUS', 'VP')
        VN = apis.get_device_sequence_data(bus, 'BUS', 'VN')
        VZ = apis.get_device_sequence_data(bus, 'BUS', 'VZ')
        (VA, VB, VC) = apis_basic.composite_three_phase_vector((VP, VN, VZ))
        bus_data.append([bus, VP, VN, VZ, VA, VB, VC])
    return bus_data
    
def get_line_analysis_result():
    '''
    Get the results of line fault analysis.
    Args: None
    Rets: 
        line_data, list, line current analysis result.
    '''
    line_data = [['LINE', 'IPI', 'INI', 'IZI', 'IAI', 'IBI', 'ICI', 'IPJ', 'INJ', 'IZJ', 'IAJ', 'IBJ', 'ICJ']]
    lines = apis.get_all_devices('LINE')
    for line in lines:
        ISI, ISJ = calculate_line_sequence_current(line)
        (IAI, IBI, ICI) = apis_basic.composite_three_phase_vector(ISI)
        (IAJ, IBJ, ICJ) = apis_basic.composite_three_phase_vector(ISJ)
        line_data.append([line, ISI[0], ISI[1], ISI[2], IAI, IBI, ICI, ISJ[0], ISJ[1], ISJ[2], IAJ, IBJ, ICJ])
    return line_data
        
def calculate_line_sequence_current(line):
    '''
    Calculate the sequence current of a line.
    Args:
        line, tuple, (ibus, jbus, ckt).
    Rets:
        (1) ISI, tuple, I-side sequence current, (IPI, INI, IZI).
        (2) ISJ, tuple, J-side sequence current, (IPJ, INJ, IZJ).
    '''
    VPI = apis.get_device_sequence_data(line[0], 'BUS', 'VP')
    VPJ = apis.get_device_sequence_data(line[1], 'BUS', 'VP')
    VNI = apis.get_device_sequence_data(line[0], 'BUS', 'VN')
    VNJ = apis.get_device_sequence_data(line[1], 'BUS', 'VN')
    VZI = apis.get_device_sequence_data(line[0], 'BUS', 'VZ')
    VZJ = apis.get_device_sequence_data(line[0], 'BUS', 'VZ') 

    R = apis.get_device_data(line, 'LINE', 'R')
    X = apis.get_device_data(line, 'LINE', 'X')
    B = apis.get_device_data(line, 'LINE', 'B')  
    BI = apis.get_device_data(line, 'LINE', 'BI')
    BJ = apis.get_device_data(line, 'LINE', 'BJ')

    RLINZ = apis.get_device_sequence_data(line, 'LINE', 'RLINZ')
    XLINZ = apis.get_device_sequence_data(line, 'LINE', 'XLINZ')
    BCHZ = apis.get_device_sequence_data(line, 'LINE', 'BCHZ')
    BI0 = apis.get_device_sequence_data(line, 'LINE', 'BI0')
    BJ0 = apis.get_device_sequence_data(line, 'LINE', 'BJ0')

    IPI = (VPI - VPJ) / (R + 1j*X) + VPI * (0.5j*B + 1j*BI)
    IPJ = (VPJ - VPI) / (R + 1j*X) + VPJ * (0.5j*B + 1j*BJ)
    INI = (VNI - VNJ) / (R + 1j*X) + VNI * (0.5j*B + 1j*BI)
    INJ = (VNJ - VNI) / (R + 1j*X) + VNJ * (0.5j*B + 1j*BJ)
    IZI = (VZI - VZJ) / (RLINZ + 1j*XLINZ) + VZI * (0.5j*BCHZ + 1j*BI0)
    IZJ = (VZJ - VZI) / (RLINZ + 1j*XLINZ) + VZJ * (0.5j*BCHZ + 1j*BJ0)
    
    return (IPI, INI, IZI), (IPJ, INJ, IZJ)