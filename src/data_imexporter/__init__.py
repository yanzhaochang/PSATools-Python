import sys
sys.path.append('..')

from .parse_psse_pf import init_powerflow_data
from .parse_psse_sq import init_sequence_data
from .parse_psse_dm import init_dynamic_data

def load_simulation_data(file, par_type):
    if par_type == 'powerflow':
        init_powerflow_data(file)

    elif par_type == 'sequence':
        init_sequence_data(file)
        
    elif par_type == 'dynamic':
        init_dynamic_data(file)
        
    else:
        pass
    return
    
