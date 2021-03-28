# Initialize the state variables of each transient model, including generator model, exciter model, governor model, etc
# Parameters with 0 at the end represent estimates value
import sys
sys.path.append('..')

import apis
from apis import apis_basic
from apis import apis_system
from apis import apis_dynamic

from .network_solution import solve_dynamic_bus_voltage


def init_system_state_parameter():
    '''
    Initialize network state variables, including the state variables and estimations of model.
    Args: None
    Rets: None
    '''
    buses = apis.get_all_devices('BUS')
    for bus in buses:
        VM = apis.get_device_data(bus, 'BUS', 'VM')
        VA = apis.get_device_data(bus, 'BUS', 'VA')
        VA = apis_basic.convert_deg_to_rad(VA)
        Vt = apis_basic.build_complex_value(VM, VA)
        
        value = {'Vt': Vt, 'Vt0': Vt}
        apis_dynamic.add_model_state_variable(bus, 'BUS', value) 
    
    init_generators_model_state_parameter()
    
    init_exciters_model_state_parameter()
    
    init_turbine_governor_model_state_parameter()
    return
    
def init_generators_model_state_parameter():
    '''
    Initialize generator model state parameters. 
    Args: None
    Rets: None
    '''
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        GMN = apis.get_generator_related_model_data(generator, 'GEN', 'GMN')
        if GMN == 'GENCLS':
            value = init_generator_GENCLS_model_state_parameter(generator)
            
        elif GMN == 'GENTRA':
            value = init_generator_GENTRA_model_state_parameter(generator)     
            
        else:
            continue
            
        apis_dynamic.add_model_state_variable(generator, 'GENERATOR', value) 
    # network equation solution to reduce the calculation error
    solve_dynamic_bus_voltage(True) 
    for generator in generators:
        Pe = apis_dynamic.get_generator_state_data(generator, True, 'Pe')
        Pe0 = apis_dynamic.get_generator_state_data(generator, False, 'Pe')
        apis_dynamic.set_generator_state_data(generator, True, 'Pm', Pe)
        apis_dynamic.set_generator_state_data(generator, False, 'Pm', Pe0)
        
    return
    
def init_exciters_model_state_parameter():
    '''
    Initialize excitation model state parameters.
    Args: None
    Rets: None
    '''
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        EMN = apis.get_generator_related_model_data(generator, 'AVR', 'EMN')
        if EMN == 'SEXS':
            value = init_exciter_SEXS_model_state_parameter(generator)
        else:
            continue  
        apis_dynamic.add_model_state_variable(generator, 'EXCITATION', value)    

    return
    
def init_turbine_governor_model_state_parameter():
    '''
    Initialize the state variables of the governor model
    Args: None
    Rets: None   
    '''
    generators = apis.get_all_devices('GENERATOR')
    for generator in generators:
        TGMN = apis.get_generator_related_model_data(generator, 'GOV', 'TGMN')
        if TGMN == 'IEEEG1':
            value = init_turbine_IEEEG1_model_state_paremeter(generator)
            
        elif TGMN == 'IEEEG3':  
            value = init_turbine_IEEEG3_model_state_paremeter(generator)
            
        else:
            continue
            
        apis_dynamic.add_model_state_variable(generator, 'TURBINE', value)      
    
    return
    
def init_generator_GENCLS_model_state_parameter(generator):
    '''
    Initialize the second order model state parameters of gencls
    Args: 
        generator, GENCLS model bus, int
    Rets: 
        value, model state parameters, dict
    '''
    VM = apis.get_device_data(generator, 'BUS', 'VM')
    VA = apis.get_device_data(generator, 'BUS', 'VA')
    VA = apis_basic.convert_deg_to_rad(VA)
    Vt = apis_basic.build_complex_value(VM, VA)
    
    PG = apis.get_device_data(generator, 'GENERATOR', 'PG')
    QG = apis.get_device_data(generator, 'GENERATOR', 'QG')
    SBASE = apis_system.get_system_base_data('SBASE')
    It = (PG - 1j * QG) / SBASE / Vt.conjugate()  # injection network current in steady state

    Xq = apis.get_device_data(generator, 'GENERATOR', 'ZX')  # Xq = Xdp
    MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    Xq = Xq * SBASE / MBASE  # Convert reactance from machine base to system base.
    EQ = Vt + 1j * Xq * It  # virtual electromotive force

    delta = apis_basic.get_complex_phase_angle(EQ)

    #print('Generator {} Xq: {}, MBASE: {}, EQ: {}, delta: {}'.format(generator, Xq, MBASE, abs(EQ), delta))
    omega = 1.0  
    Pm = PG / SBASE  
    Pe = PG / SBASE  
    
    value = {'delta': delta, 'omega': omega, 'Pm': Pm, 'Pe': Pe, 'It': It, 'Eqp': abs(EQ), 'Efq': 0.0,
        'delta0': delta, 'omega0': omega, 'Pm0': Pm, 'Pe0': Pe, 'It0': It, 'Eqp0': abs(EQ), 'Efq0': 0.0} 
    return value
    
def init_generator_GENROU_model_state_parameter(gen_md):
    '''
    初始化GENROU模型的状态参数
    输入: 
        gen_md, GENTRA模型参数, object
    输出: 
        value, 模型状态参数, dict
    '''
    vm = apis.bus.get_bus_data(gen_md.IBUS, 'VM')
    va = apis.bus.get_bus_data(gen_md.IBUS, 'VA')
    va_rad = apis.basic.convert_deg_to_rad(va)
    Vt = apis.basic.build_complex_value(vm, va_rad)
    
    PG = api.gen.get_generator_data(gen_md.IBUS, 'PG')
    QG = api.gen.get_generator_data(gen_md.IBUS, 'QG')
    It = (PG - 1j * QG) / Base.SBASE / Vt.conjugate()  # 计算稳态时发电机注入网络电流

    EQ = Vt + 1j * gen_md.Xq * It  # 发电机虚拟电动势
    delta = apis_basic.get_complex_phase_angle(EQ)

    Vd, Vq = apis.basic.convert_xy_to_dq(delta, Vt.real, Vt.imag)  
    Id, Iq = apis.basic.convert_xy_to_dq(delta, It.real, It.imag)
    
    Eqp = Vq + gen_md.Xdp * Id
    Edp = Vd - gen_md.Xqp * Iq
    Eqpp = Vq + gen_md.Xdpp * Id
    Edpp = Vd - gen_md.Xqpp * Iq   
    Efq = Vq + gen_md.Xd * Id
    omega = 1.0  # 初始同步速   
    Pm = PG / Base.SBASE  # 机械功率
    Pe = PG / Base.SBASE  # 电磁功率

    value = {'IBUS': gen_md.IBUS, 'delta': delta, 'omega': omega, 'Efq': Efq, 'Pm': Pm, 'Pe': Pe, 'It': It,
        'Eqp': Eqp, 'Edp': Edp, 'Eqpp': Eqpp, 'Edpp': Edpp}     
    return value

def init_generator_GENSAL_model_state_parameter(gen_md):
    '''
    初始化GENSAL模型状态参数
    输入: 
        gen_md, GENTRA模型参数, object
    输出: 
        value, 模型状态参数, object
    '''
    vm = apis.bus.get_bus_data(gen_md.IBUS, 'VM')
    va = apis.bus.get_bus_data(gen_md.IBUS, 'VA')
    va_rad = apis.basic.convert_deg_to_rad(va)
    Vt = apis.basic.build_complex_value(vm, va_rad)
    
    PG = api.gen.get_generator_data(gen_md.IBUS, 'PG')
    QG = api.gen.get_generator_data(gen_md.IBUS, 'QG')
    It = (PG - 1j * QG) / Base.SBASE / Vt.conjugate()  # 计算稳态时发电机注入网络电流 
    
    EQ = Vt + 1j * gen_md.Xq * It  # 发电机虚拟电动势
    delta = apis_basic.get_complex_phase_angle(EQ)
    
    Vd, Vq = apis.basic.convert_xy_to_dq(delta, Vt.real, Vt.imag)  
    Id, Iq = apis.basic.convert_xy_to_dq(delta, It.real, It.imag)
    
    Eqp = Vq + gen_md.Xdp * Id
    Eqpp = Vq + gen_md.Xdpp * Id
    Edpp = Vd - gen_md.Xqpp * Iq
    Efq = Vq + gen_md.Xd * Id
    omega = 1.0  # 初始同步速   
    Pm = PG / Base.SBASE  # 机械功率
    Pe = PG / Base.SBASE  # 电磁功率
  
    value = {'IBUS': gen_md.IBUS, 'delta': delta, 'omega': omega, 'Efq': Efq, 'Pm': Pm, 'Pe': Pe, 'It': It,
        'Eqp': Eqp, 'Eqpp': Eqpp, 'Edpp': Edpp, 'delta0': delta, 'omega0': omega, 'Efq0': Efq, 'Pm0': Pm, 
        'Pe0': Pe, 'It0': It, 'Eqp0': Eqp, 'Eqpp0': Eqpp, 'Edpp0': Edpp} 
    return value  

def init_generator_GENTRA_model_state_parameter(generator):
    '''
    Initialize the GENTRA model state parameters.
    Args: 
        generator, int, GENTRA model bus.
    Rets: 
        value, dict, model state parameters.
    '''
    VM = apis.get_device_data(generator, 'BUS', 'VM')
    VA = apis.get_device_data(generator, 'BUS', 'VA')
    VA = apis_basic.convert_deg_to_rad(VA)
    Vt = apis_basic.build_complex_value(VM, VA)
    
    MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    PG = apis.get_device_data(generator, 'GENERATOR', 'PG')
    QG = apis.get_device_data(generator, 'GENERATOR', 'QG')
    SBASE = apis_system.get_system_base_data('SBASE')
    
    It = (PG - 1j * QG) / SBASE / Vt.conjugate()  
    
    Xq = apis.get_generator_related_model_data(generator, 'GEN', 'Xq')
    Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xd')
    Xdp = apis.get_generator_related_model_data(generator, 'GEN', 'Xdp')
    
    Xq = Xq * SBASE / MBASE
    Xd = Xd * SBASE / MBASE
    Xdp = Xdp * SBASE / MBASE
    
    EQ = Vt + 1j * Xq * It  
    delta = apis_basic.get_complex_phase_angle(EQ)
    
    Vd, Vq = apis_basic.convert_xy_to_dq(delta, Vt.real, Vt.imag)  
    Id, Iq = apis_basic.convert_xy_to_dq(delta, It.real, It.imag)
    
    Efq = Vq + Xd * Id
    Eqp = Vq + Xdp * Id
    omega = 1.0    
    Pm = PG / SBASE  
    Pe = PG / SBASE  
  
    value = {'delta': delta, 'omega': omega, 'Efq': Efq, 'Pm': Pm, 'Pe': Pe, 'It': It, 'Eqp': Eqp, 
        'delta0': delta, 'omega0': omega, 'Efq0': Efq, 'Pm0': Pm, 'Pe0': Pe, 'It0': It, 'Eqp0': Eqp} 
    return value 

def init_exciter_SEXS_model_state_parameter(generator):
    '''
    Initialize state parameters of SEXS excitation system model.
    Args: 
        generator, int, SEXS model connected bus number.
    Rets: 
        value, dict, model state variables.
    '''
    Efq = apis_dynamic.get_generator_state_data(generator, True, 'Efq')
    EC = abs(apis_dynamic.get_bus_state_data(generator, True, 'Vt'))
    
    K = apis.get_generator_related_model_data(generator, 'AVR', 'K')
    Vref = Efq / K + EC
    
    apis.set_generator_related_model_data(generator, 'AVR', 'Vref', Vref)
    value = {}
    return value

def init_turbine_IEEEG1_model_state_paremeter(generator):
    '''
    Initialize of IEEEG1 speed regulation model state parameters.
    Args: 
        generator, int, the bus turbine governor connected.
    Rets: 
        value, dict, model state variables.
    '''
    K1 = apis.get_generator_related_model_data(generator, 'GOV', 'K1')
    K3 = apis.get_generator_related_model_data(generator, 'GOV', 'K3')
    Pm = apis_dynamic.get_generator_state_data(generator, True, 'Pm')

    x1 = Pm / (K1 + K3)
    x2 = Pm / (K1 + K3)
    x3 = Pm / (K1 + K3)
    P0 = x1
    apis.set_generator_related_model_data(generator, 'GOV', 'P0', P0)
    
    value = {'x1': x1, 'x2': x2, 'x3': x3, 'x10': x1, 'x20': x2, 'x30': x3}
    return value

def init_turbine_IEEEG3_model_state_paremeter(generator):
    '''
    Initialize of IEEEG3 speed regulation model state parameters.
    Args: 
        generator, int, the bus turbine governor connected.
    Rets: 
        value, dict, model state variables.
    '''
    Pm = apis_dynamic.get_generator_state_data(generator, True, 'Pm')
    sigma = apis.get_generator_related_model_data(generator, 'GOV', 'sigma')
    delta = apis.get_generator_related_model_data(generator, 'GOV', 'delta')
    TR = apis.get_generator_related_model_data(generator, 'GOV', 'TR')
    a11 = apis.get_generator_related_model_data(generator, 'GOV', 'a11')
    a21 = apis.get_generator_related_model_data(generator, 'GOV', 'a21')
    a13 = apis.get_generator_related_model_data(generator, 'GOV', 'a13')
    a23 = apis.get_generator_related_model_data(generator, 'GOV', 'a23')    

    x2 = Pm / a23    
    x3 = - delta * x2
    x1 = 0.0
    P0 = sigma * x2 + TR * x2 + x3
    x4 = -a13 * a21 / a11 * x2
    
    apis.set_generator_related_model_data(generator, 'GOV', 'P0', P0)
    value = {'x1': x1, 'x2': x2, 'x3': x3, 'x4': x4, 'x10': x1, 'x20': x2, 'x30': x3, 'x40': x4}
    return value    