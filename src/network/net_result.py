# network result
import csv
import sys
sys.path.append('..')

from apis import apis_system


def save_network_admittance_matrix(par_type, file):
    '''
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
   
 