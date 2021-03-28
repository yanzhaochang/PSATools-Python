import sys
sys.path.append('..')
import csv

import network 

from .method_NR import solve_powerflow_with_NR_method
from .method_PQ import solve_powerflow_with_PQ_method
from .method_DC import solve_powerflow_with_DC_method
from .branch import init_powerflow_solution, update_powerflow, show_powerflow_result
from .powerflow_result import get_powerflow_result


def solve_powerflow(method):
    '''
    Power flow solving function.
    Args:
        method, str, 'PQ' or 'NR', 'DC'.
    Rets: None
    '''
    network.build_network_Y_matrix('basic')
    S, Um, Ua = init_powerflow_solution()  # flat start
    
    if method == 'NR':
        S, Um, Ua = solve_powerflow_with_NR_method(S, Um, Ua)
        update_powerflow(S, Um, Ua)   
        
    elif method == 'PQ':
        network.build_network_Y_matrix('B1')
        network.build_network_Y_matrix('B2')
        S, Um, Ua = solve_powerflow_with_PQ_method(S, Um, Ua)  
        update_powerflow(S, Um, Ua) 
        
    elif method == 'DC':
        network.build_network_Y_matrix('B1')
        network.build_network_Y_matrix('B2')
        solve_powerflow_with_DC_method(S, Um, Ua)  
        
    else:
        pass
   
    show_powerflow_result()
    
    return

def save_powerflow_result(file):
    '''
    Save power flow result in file.
    Args:
        file, str, file name.
    Rets: None
    '''
    result_data = get_powerflow_result()
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result_data) 
    return
    