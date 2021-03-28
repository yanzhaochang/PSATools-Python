# test
import sys
sys.path.append('.\src')
from PSATool import PAST

raw_file = '.\data\IEEE9-2阶.raw'
seq_file = '.\data\IEEE9.seq'
dyr_file = '.\data\IEEE9-2阶.dyr'

simulator = PAST()
simulator.load_simulation_data(raw_file, 'powerflow')

buses = simulator.get_all_devices('BUS')
print(buses)
   
loads = simulator.get_all_devices('LOAD')
print(loads)

generators = simulator.get_all_devices('GENERATOR')
print(generators)


simulator.build_network_Y_matrix('basic')
simulator.save_network_Y_matrix('./test_result/IEEE9_Y_mat.csv', 'basic')
simulator.solve_powerflow('NR')
simulator.save_powerflow_result('./test_result/IEEE9_powerflow_result.csv')

simulator.load_simulation_data(dyr_file, 'dynamic')

simulator.build_network_Y_matrix('dynamic')
simulator.save_network_Y_matrix('./test_result/IEEE9_Y_dynamic_mat.csv', 'dynamic')

#for bus in buses:
#    simulator.prepare_dynamic_output_meter(bus, 'BUS', 'VM')
#for generator in generators:
#    simulator.prepare_dynamic_output_meter(generator, 'GEN', 'ROTOR ANGLE IN DEG')
simulator.set_simulator_parameter('dynamic', 'output_file', './test_result/IEEE9_dynamic_result.csv')  
  
simulator.start_dynamic_simulation()
simulator.run_dynamic_simulation_to_time(0.1)

bus = 7
Yf = -1j*1e6
simulator.set_bus_fault(bus, Yf)
simulator.run_dynamic_simulation_to_time(0.2)
simulator.clear_bus_fault(bus, Yf)
simulator.run_dynamic_simulation_to_time(2.0)

'''
simulator.load_simulation_data(seq_file, 'sequence')

simulator.build_network_Y_matrix('positive')
simulator.save_network_Y_matrix('./test_result/IEEE9_Y_positive_mat.csv', 'positive')
simulator.build_network_Y_matrix('negative')
simulator.build_network_Y_matrix('zero')

simulator.solve_bus_asymmetry_fault(3, 'single phase grounding', 0.0)
simulator.save_fault_analysis_result('./test_result/IEEE9_fault_analysis.csv')
'''

    
    
    
    
    
    