# network function
import csv
import sys
sys.path.append('..')
from apis import apis_system

from .net_dm import calculate_dynamic_Y_matrix
from .net_pf import calculate_network_Y_matrix
from .net_sq import calculate_sequence_Y_matrix


def build_network_Y_matrix(par_type):
    '''
    Build the network node admittance matrix and store it in database.
    Args: 
        par_type, str, Y matrix type, including basic, B1, B2, positive, negative, zero, dynamic.
    Rets: None
    '''
    if par_type == 'basic':
        Y_mat = calculate_network_Y_matrix()
        apis_system.set_system_Y_network_matrix('basic', Y_mat)
    
    elif par_type == 'B1':
        Y_mat = calculate_network_Y_matrix(c=False)  
        B1_mat = Y_mat.imag 
        apis_system.set_system_Y_network_matrix('B1', B1_mat)
        
    elif par_type == 'B2':
        Y_mat = calculate_network_Y_matrix(r=False)  
        B2_mat = Y_mat.imag     
        apis_system.set_system_Y_network_matrix('B2', B2_mat)
    
    elif par_type == 'positive':
        Y_mat = calculate_sequence_Y_matrix('positive')
        apis_system.set_system_Y_network_matrix('positive', Y_mat)
    
    elif par_type == 'negative':
        Y_mat = calculate_sequence_Y_matrix('negative')
        apis_system.set_system_Y_network_matrix('negative', Y_mat)
     
    elif par_type == 'zero':
        Y_mat = calculate_sequence_Y_matrix('zero')
        apis_system.set_system_Y_network_matrix('zero', Y_mat)
    
    elif par_type == 'dynamic':
        Y_mat = calculate_dynamic_Y_matrix()
        apis_system.set_system_Y_network_matrix('dynamic', Y_mat)    
    else:
        pass
    return

def save_network_Y_matrix(file, par_type):
    '''
    Save the network node admittance matrix.
    Args: 
        file, str, saving file name.
    Rets: None
    '''
    Y_mat = apis_system.get_system_Y_network_matrix(par_type)
    
    data = []
    for i in range(Y_mat.shape[0]):
        for j in range(Y_mat.shape[1]):
            if Y_mat[i, j] != 0:
                m = apis_system.get_bus_num_before_renumber(i)
                n = apis_system.get_bus_num_before_renumber(j)
                g = round(Y_mat[i, j].real, 6)
                b = round(Y_mat[i, j].imag, 6)
                data.append([i, m, j, n, g, b])
                
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['row', 'row bus', 'column', 'column bus', 'real', 'imag'])
        writer.writerows(data)    
    return

