# Comparison procedure
from stepspy import STEPS

raw_file = '.\data\IEEE9-2阶.raw'
seq_file = '.\data\IEEE9.seq'
dyr_file = '.\data\IEEE9-2阶.dyr'

simulator = STEPS(is_default=False, log_file='log.txt')
simulator.set_allowed_maximum_bus_number(100000)

simulator.load_powerflow_data(raw_file, 'PSS/E')  
simulator.load_dynamic_data(dyr_file, 'PSS/E')

simulator.solve_powerflow('NR')

loads = simulator.get_all_loads()
buses = simulator.get_all_buses()
generators = simulator.get_all_generators()
for load in loads:
    PP0_MW = simulator.get_load_data(load, 'F', 'PP0_MW')
    QP0_MVAR = simulator.get_load_data(load, 'F', 'QP0_MVAR')
    simulator.set_load_data(load, 'F', 'PP0_MW', 0.0)
    simulator.set_load_data(load, 'F', 'QP0_MVAR', 0.0)
    simulator.set_load_data(load, 'F', 'PZ0_MW', PP0_MW)
    simulator.set_load_data(load, 'F', 'QZ0_MVAR', QP0_MVAR)
    
simulator.solve_powerflow('NR')    
    
for generator in generators:
    simulator.prepare_generator_meter(generator, 'ROTOR ANGLE IN DEG')
    simulator.prepare_generator_meter(generator, 'TERMINAL ACTIVE POWER IN MW')
    
simulator.set_dynamic_simulation_time_step(0.001)    
simulator.set_dynamic_simulator_output_file('./test_result/IEEE9_dynamic_result_steps')  
  
simulator.start_dynamic_simulation()
simulator.run_dynamic_simulation_to_time(0.1)
bus = 7
Yf = (0.0, -1e6)
simulator.set_bus_fault(bus, 'THREE PHASE FAULT', Yf)
simulator.run_dynamic_simulation_to_time(0.2)
simulator.clear_bus_fault(bus, 'THREE PHASE FAULT')
simulator.run_dynamic_simulation_to_time(2.0)
simulator.stop_dynamic_simulation()
