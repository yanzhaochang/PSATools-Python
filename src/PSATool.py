'''
@ Copyright: School of electrical engineering, Shandong University.

@ File name: PSATool.py

@ Function: A programming example for power system analysis course teaching.
    This module is the top encapsulation module of the program, which can be called by external reference 

@ Creation date: 2020-03-15

@ Founder: Yanzhao Chang, Master of Electrical Engineering.

@ 修改标识：2017年10月2日

@ 修改描述：

@ 修改日期：

'''
import data_imexporter
import apis
import network
import powerflow
import fault
import dynamic

class PSATE():
    def __init__(self):
        return
    
    def load_simulation_data(self, file, par_type):
        '''
        Load basic raw, seq, dyr data for simulation.
        Args:
            (1) file, str, file path.
            (2) par_type, file type, 'powerflow' for .raw data, 'sequence' for .seq data, 'dynamic' for .dyr data.
        Rets: None    
        '''    
        data_imexporter.load_simulation_data(file, par_type)
        return

    def get_simulator_parameter(self, par_type, par_name):
        value = apis.get_simulator_parameter(par_type, par_name)
        return value
        
    def set_simulator_parameter(self, par_type, par_name, value):
        apis.set_simulator_parameter(par_type, par_name, value)
        return
        
    def get_all_devices(self, device):
        devices = apis.get_all_devices(device)
        return devices
    
    def get_device_data(self, device_index, device, par_name):
        value = apis.get_device_data(device_index, device, par_name)
        return value
    
    def get_device_sequence_data(self, device_index, device, par_name):
        value = apis.get_device_sequence_data(device_index, device, par_name)
        return value
        
    def set_device_data(self, device_index, device, par_name, value):
        apis.set_device_data(device_index, device, par_name, value)
        return
    
    def set_device_sequence_data(self, device_index, device, par_name, value):
        apis.set_device_sequence_data(device_index, device, par_name, value)
        return
        
    def build_network_Y_matrix(self, par_type):      
        network.build_network_Y_matrix(par_type)
        return
        
    def save_network_Y_matrix(self, file, par_type):
        network.save_network_Y_matrix(file, par_type)
        return
        
    def solve_powerflow(self, method):
        powerflow.solve_powerflow(method)
        return
        
    def save_powerflow_result(self, file):
        powerflow.save_powerflow_result(file)
        return
    
    def solve_bus_asymmetry_fault(self, bus, par_type, Zf):
        fault.solve_bus_asymmetry_fault(bus, par_type, Zf)
        return
    
    def save_fault_analysis_result(self, file):
        fault.save_fault_analysis_result(file)
        return
    
    def get_generator_related_model_data(self, generator, model_type, par_name):
        value = apis.get_generator_related_model_data(generator, model_type, par_name)
        return value

    def set_generator_related_model_data(self, generator, model_type, par_name, value):
        apis.set_generator_related_model_data(generator, model_type, par_name, value)
        return 
    
    def prepare_dynamic_output_meter(self, device_index, device, meter_type):
        apis.prepare_dynamic_output_meter(device_index, device, meter_type)
        return
        
    def start_dynamic_simulation(self):
        dynamic.start_dynamic_simulation()
        return
        
    def run_dynamic_simulation_to_time(self, stop_time):
        dynamic.run_dynamic_simulation_to_time(stop_time)
        return
        
    def set_bus_fault(self, bus, Yf):
        dynamic.set_bus_fault(bus, Yf)
        return
        
    def clear_bus_fault(self, bus, Yf):
        dynamic.clear_bus_fault(bus, Yf)
        return
    
    def trip_line(self, line):
        dynamic.trip_line(line)
        return