# Solving state variables of generator model.
import sys
sys.path.append('../..')
from math import pi

import apis
from apis import apis_basic
from apis import apis_system
from apis import apis_dynamic


def solve_generator_model_state_variable(generator, par_type):
    '''
    Solve generator model state variables.
    Args:
        (1) generator, int, generator connected bus number.
        (2) par_type, bool, state variables type. True for actual value and False for estimated value.
    Rets: None
    '''
    GMN = apis.get_generator_related_model_data(generator, 'GEN', 'GMN')
    if GMN == 'GENTRA':
        if par_type is True:
            solve_GENTRA_model_state_actual_value(generator)
        else:
            solve_GENTRA_model_state_estimated_value(generator)
            
    elif GMN == 'GENCLS':
        if par_type is True:
            solve_GENCLS_model_state_actual_value(generator)
        else:
            solve_GENCLS_model_state_estimated_value(generator)
            
    else:
        pass
    return
    
def solve_GENTRA_model_state_estimated_value(generator):
    '''
    Solve the estimated value of state variables in GENTRA model
    Args: 
        generator, int, GENTRA model connected bus number
    Rets: None
    '''
    delta = apis_dynamic.get_generator_state_data(generator, True, 'delta')
    omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')
    Pm = apis_dynamic.get_generator_state_data(generator, True, 'Pm')
    Pe = apis_dynamic.get_generator_state_data(generator, True, 'Pe')
    Eqp = apis_dynamic.get_generator_state_data(generator, True, 'Eqp')
    Efq = apis_dynamic.get_generator_state_data(generator, True, 'Efq')
    It = apis_dynamic.get_generator_state_data(generator, True, 'It')
    
    SBASE = apis.get_system_base_data('SBASE')
    MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    BASFRQ = apis.get_system_base_data('BASFRQ')
    omegas = 2 * pi * BASFRQ
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')
    
    H = apis.get_generator_related_model_data(generator, 'GEN', 'H')
    Tj = 2 * H *MBASE / SBASE
    Td0p = apis.get_generator_related_model_data(generator, 'GEN', 'Td0p')
    Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xd')
    Xd = Xd * SBASE / MBASE
    Xdp = apis.get_generator_related_model_data(generator, 'GEN', 'Xdp')
    Xdp = Xdp * SBASE / MBASE
    Id, Iq = apis_basic.convert_xy_to_dq(delta, It.real, It.imag)
    
    ddelta = omegas * (omega - 1)
    domega = 1 / Tj * (Pm - Pe)
    dEqp = 1 / Td0p * (-Eqp - (Xd - Xdp) * Id + Efq)    
    #print('GENTRA model ddelta {} and domega {}'.format(ddelta, domega))
    delta0 = delta + ddelta * time_step
    omega0 = omega + domega * time_step
    Eqp0 = Eqp + dEqp * time_step
    
    apis_dynamic.set_generator_state_data(generator, False, 'Eqp', Eqp0)
    apis_dynamic.set_generator_state_data(generator, False, 'omega', omega0)
    apis_dynamic.set_generator_state_data(generator, False, 'delta', delta0)

    return   
    
def solve_GENTRA_model_state_actual_value(generator):
    '''
    Solve the actual value of state variables in GENTRA model
    Args: 
        generator, int, GENTRA model connected bus number
    Rets: None
    '''
    delta = apis_dynamic.get_generator_state_data(generator, True, 'delta')
    omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')
    Pm = apis_dynamic.get_generator_state_data(generator, True, 'Pm')
    Pe = apis_dynamic.get_generator_state_data(generator, True, 'Pe')
    Eqp = apis_dynamic.get_generator_state_data(generator, True, 'Eqp')
    Efq = apis_dynamic.get_generator_state_data(generator, True, 'Efq')
    It = apis_dynamic.get_generator_state_data(generator, True, 'It')
    
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')    
    SBASE = apis.get_system_base_data('SBASE')
    MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    BASFRQ = apis.get_system_base_data('BASFRQ')
    omegas = 2 * pi * BASFRQ
    
    H = apis.get_generator_related_model_data(generator, 'GEN', 'H')
    Tj = 2 * H *MBASE / SBASE
    Td0p = apis.get_generator_related_model_data(generator, 'GEN', 'Td0p')
    Xd = apis.get_generator_related_model_data(generator, 'GEN', 'Xd')
    Xd = Xd * SBASE / MBASE
    Xdp = apis.get_generator_related_model_data(generator, 'GEN', 'Xdp')
    Xdp = Xdp * SBASE / MBASE
    
    Id, Iq = apis_basic.convert_xy_to_dq(delta, It.real, It.imag)
    
    ddelta = omegas * (omega - 1)  
    domega = 1 / Tj * (Pm - Pe)
    dEqp = 1 / Td0p * (-Eqp - (Xd - Xdp) * Id + Efq) 
    
    delta0 = apis_dynamic.get_generator_state_data(generator, False, 'delta')
    omega0 = apis_dynamic.get_generator_state_data(generator, False, 'omega')
    Pm0 = apis_dynamic.get_generator_state_data(generator, False, 'Pm')
    Pe0 = apis_dynamic.get_generator_state_data(generator, False, 'Pe')
    Eqp0 = apis_dynamic.get_generator_state_data(generator, False, 'Eqp')
    Efq0 = apis_dynamic.get_generator_state_data(generator, False, 'Efq')
    It0 = apis_dynamic.get_generator_state_data(generator, False, 'It')
    
    Id0, Iq0 = apis_basic.convert_xy_to_dq(delta0, It0.real, It0.imag)
    
    ddelta0 = omegas * (omega0 - 1)
    domega0 = 1 / Tj * (Pm0 - Pe0)
    dEqp0 = 1 / Td0p * (-Eqp0 - (Xd - Xdp) * Id0 + Efq0) 
    
    delta = delta + (ddelta + ddelta0) * 0.5 * time_step
    omega = omega + (domega + domega0) * 0.5 * time_step
    Eqp = Eqp + (dEqp + dEqp0) * 0.5 * time_step
    
    apis_dynamic.set_generator_state_data(generator, True, 'Eqp', Eqp)
    apis_dynamic.set_generator_state_data(generator, True, 'omega', omega)
    apis_dynamic.set_generator_state_data(generator, True, 'delta', delta)
    return  
    
def solve_GENCLS_model_state_estimated_value(generator): 
    '''
    Solve the estimated value of state variables in GENCLS model
    Args: 
        generator, int, GENCLS model connected bus number
    Rets: None
    '''
    delta = apis_dynamic.get_generator_state_data(generator, True, 'delta')
    omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')
    Pm = apis_dynamic.get_generator_state_data(generator, True, 'Pm')
    Pe = apis_dynamic.get_generator_state_data(generator, True, 'Pe')
    time_step = apis.get_simulator_parameter('dynamic', 'time_step')    
    
    SBASE = apis_system.get_system_base_data('SBASE')
    BASFRQ = apis_system.get_system_base_data('BASFRQ')
    MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    H = apis.get_generator_related_model_data(generator, 'GEN', 'H')
    Tj = 2 * H * MBASE / SBASE    
    omegas = 2 * pi * BASFRQ    

    ddelta = omegas * (omega - 1)
    domega = 1 / Tj * (Pm - Pe)   
    
    omega0 = omega + domega * time_step
    delta0 = delta + ddelta * time_step

    apis_dynamic.set_generator_state_data(generator, False, 'omega', omega0)
    apis_dynamic.set_generator_state_data(generator, False, 'delta', delta0)
    return 

def solve_GENCLS_model_state_actual_value(generator):
    '''
    Solve the actual value of state variables in GENCLS model.
    Args: 
        generator, int, GENCLS model connected bus number
    Rets: None
    '''
    SBASE = apis_system.get_system_base_data('SBASE')
    BASFRQ = apis_system.get_system_base_data('BASFRQ')
    MBASE = apis.get_device_data(generator, 'GENERATOR', 'MBASE')
    H = apis.get_generator_related_model_data(generator, 'GEN', 'H')
    Tj = 2 * H * MBASE / SBASE    
    omegas = 2 * pi * BASFRQ  
    
    delta = apis_dynamic.get_generator_state_data(generator, True, 'delta')
    omega = apis_dynamic.get_generator_state_data(generator, True, 'omega')
    Pm = apis_dynamic.get_generator_state_data(generator, True, 'Pm')
    Pe = apis_dynamic.get_generator_state_data(generator, True, 'Pe')
    time_step = apis.get_simulator_parameter('dynamic', 'time_step') 
    
    ddelta = omegas * (omega - 1)  
    domega = 1 / Tj * (Pm - Pe) 
    
    delta0 = apis_dynamic.get_generator_state_data(generator, False, 'delta')
    omega0 = apis_dynamic.get_generator_state_data(generator, False, 'omega')
    Pm0 = apis_dynamic.get_generator_state_data(generator, False, 'Pm')
    Pe0 = apis_dynamic.get_generator_state_data(generator, False, 'Pe')
    
    ddelta0 = omegas * (omega0 - 1)
    domega0 = 1 / Tj * (Pm0 - Pe0) 
    
    delta = delta + (ddelta + ddelta0) * 0.5 * time_step
    omega = omega + (domega + domega0) * 0.5 * time_step
    
    apis_dynamic.set_generator_state_data(generator, True, 'omega', omega)
    apis_dynamic.set_generator_state_data(generator, True, 'delta', delta)
    return  
    
  
def solve_GENROU_model_state_parameter_estimated_value(gen_md, par):
    '''
    求解发电机GENROU模型状态变量的估计值
    输入: (1) gen_md, GENROU模型参数
          (2) par, GENTRA模型状态参数
    输出: value, 模型状态估计参数
    '''
    Eqp = par['Eqp']
    Edp = par['Edp']
    Eqpp = par['Eqpp']
    Edpp = par['Edpp']
    Efq = par['Efq']
    delta = par['delta']
    omega = par['omega']
    Pe = par['Pe']
    Pm = par['Pm']
    It = par['It']
    time_step = par['time_step']
    Id, Iq = convert_xy_to_dq(delta, It.real, It.imag)
    
    Xd = gen_md.Xd
    Xq = gen_md.Xq
    Xdp = gen_md.Xdp
    Xqp = gen_md.Xqp
    Xqpp = gen_md.Xqpp
    Xdpp = gen_md.Xdpp
    Td0p = gen_md.Td0p
    Td0pp = gen_md.Td0pp
    Tq0p = gen_md.Tq0p
    Tq0pp = gen_md.Tq0pp
    
    omegas = 2 * pi * Base.BASFRQ
    Tj = 2 * gen_md.H
    
    dEqp = 1/Td0p * (-(Xd-Xdpp)/(Xdp-Xdpp) * Eqp + (Xd-Xdp)/(Xdp-Xdpp) * Eqpp + Efq) 
    dEqpp = 1/Td0pp * (Eqp - Eqpp - (Xdp-Xdpp) * Id)
    dEdp = 1/Tq0p * (-(Xq-Xqpp)/(Xqp-Xqpp) * Edp + (Xq-Xqp)/(Xqp-Xqpp) * Edpp)
    dEdpp = 1/Tq0pp * (Edp - Edpp + (Xqp-Xqpp) * Iq)
    
    ddelta = omegas * (omega - 1)
    domega = 1 / Tj * (Pm - Pe)
    
    Eqp0 = Eqp + dEqp * time_step
    Eqpp0 = Eqpp + dEqpp * time_step
    Edp0 = Edp + dEdp * time_step
    Edpp0 = Edpp + dEdpp * time_step

    delta0 = delta + ddelta * time_step
    omega0 = omega + domega * time_step

    value = {'Eqp0': Eqp0, 'Eqpp0': Eqpp0, 'Edp0': Edp0, 'Edpp0': Edpp0, 'delta0': delta0, 'omega0': omega0}
    return value
    
def solve_GENROU_model_state_parameter_actual_value(gen_md, par):
    '''
    求解发电机GENROU模型状态变量的实际值
    输入: (1) gen_md, GENROU模型参数
          (2) par, GENROU模型状态参数
    输出: value, 模型状态实际参数
    '''
    Xd = gen_md.Xd
    Xq = gen_md.Xq
    Xdp = gen_md.Xdp
    Xqp = gen_md.Xqp
    Xqpp = gen_md.Xqpp
    Xdpp = gen_md.Xdpp
    Td0p = gen_md.Td0p
    Td0pp = gen_md.Td0pp
    Tq0p = gen_md.Tq0p
    Tq0pp = gen_md.Tq0pp
    
    omegas = 2 * pi * Base.BASFRQ
    Tj = 2 * gen_md.H

    Eqp = par['Eqp']
    Edp = par['Edp']
    Eqpp = par['Eqpp']
    Edpp = par['Edpp']
    Efq = par['Efq']
    delta = par['delta']
    omega = par['omega']
    Pe = par['Pe']
    Pm = par['Pm']
    It = par['It']
    time_step = par['time_step']
    Id, Iq = convert_xy_to_dq(delta, It.real, It.imag)  

    dEqp = 1/Td0p * (-(Xd-Xdpp)/(Xdp-Xdpp) * Eqp + (Xd-Xdp)/(Xdp-Xdpp) * Eqpp + Efq) 
    dEqpp = 1/Td0pp * (Eqp - Eqpp - (Xdp-Xdpp) * Id)
    dEdp = 1/Tq0p * (-(Xq-Xqpp)/(Xqp-Xqpp) * Edp + (Xq-Xqp)/(Xqp-Xqpp) * Edpp)
    dEdpp = 1/Tq0pp * (Edp - Edpp + (Xqp-Xqpp) * Iq)

    ddelta = omegas * (omega - 1)
    domega = 1 / Tj * (Pm - Pe)

    Eqp0 = par['Eqp0']
    Edp0 = par['Edp0']
    Eqpp0 = par['Eqpp0']
    Edpp0 = par['Edpp0']
    Efq0 = par['Efq0']
    delta0 = par['delta0']
    omega0 = par['omega0']
    Pe0 = par['Pe0']
    Pm0 = par['Pm0']
    It0 = par['It0']
    Id0, Iq0= convert_xy_to_dq(delta0, It0.real, It0.imag)  
    
    dEqp0 = 1/Td0p * (-(Xd-Xdpp)/(Xdp-Xdpp) * Eqp0 + (Xd-Xdp)/(Xdp-Xdpp) * Eqpp0 + Efq0) 
    dEqpp0 = 1/Td0pp * (Eqp0 - Eqpp0 - (Xdp-Xdpp) * Id0)
    dEdp0 = 1/Tq0p * (-(Xq-Xqpp)/(Xqp-Xqpp) * Edp0 + (Xq-Xqp)/(Xqp-Xqpp) * Edpp0)
    dEdpp0 = 1/Tq0pp * (Edp0 - Edpp0 + (Xqp-Xqpp) * Iq0)
    
    ddelta0 = omegas * (omega0 - 1)
    domega0 = 1 / Tj * (Pm0 - Pe0)

    delta = delta + (ddelta + ddelta0) * 0.5 * time_step
    omega = omega + (domega + domega0) * 0.5 * time_step
    Eqp = Eqp + (dEqp + dEqp0) * 0.5 * time_step
    Edp = Edp + (dEdp + dEdp0) * 0.5 * time_step
    Eqpp = Eqpp + (dEqpp + dEqpp0) * 0.5 * time_step
    Edpp = Edpp + (dEdpp + dEdpp0) * 0.5 * time_step

    value = {'delta': delta, 'omega': omega, 'Eqp': Eqp, 'Edp': Edp, 'Eqpp': Eqpp, 'Edpp': Edpp}
    return value

def solve_GENSAL_model_state_parameter_estimated_value(gen_md, par):
    '''
    求解发电机GENSAL模型状态变量的估计值
    输入: (1) gen_md, GENSAL模型参数
          (2) par, GENSAL模型状态参数
    输出: value, 模型状态估计参数
    '''
    Eqp = par['Eqp']
    Eqpp = par['Eqpp']
    Edpp = par['Edpp']
    Efq = par['Efq']
    delta = par['delta']
    omega = par['omega']
    Pe = par['Pe']
    Pm = par['Pm']
    It = par['It']
    time_step = par['time_step']
    Id, Iq = convert_xy_to_dq(delta, It.real, It.imag)
    
    Xd = gen_md.Xd
    Xq = gen_md.Xq
    Xdp = gen_md.Xdp
    Xqpp = gen_md.Xqpp
    Xdpp = gen_md.Xdpp
    Td0p = gen_md.Td0p
    Td0pp = gen_md.Td0pp
    Tq0pp = gen_md.Tq0pp
    Xqp = Xq
    
    omegas = 2 * pi * Base.BASFRQ
    Tj = 2 * gen_md.H
    
    dEqp = 1/Td0p * (-(Xd-Xdpp)/(Xdp-Xdpp) * Eqp + (Xd-Xdp)/(Xdp-Xdpp) * Eqpp + Efq) 
    dEqpp = 1/Td0pp * (Eqp - Eqpp - (Xdp-Xdpp) * Id)
    dEdpp = 1/Tq0pp * (-Edpp + (Xqp-Xqpp) * Iq)
    
    ddelta = omegas * (omega - 1)
    domega = 1 / Tj * (Pm - Pe)
    
    Eqp0 = Eqp + dEqp * time_step
    Eqpp0 = Eqpp + dEqpp * time_step
    Edpp0 = Edpp + dEdpp * time_step

    delta0 = delta + ddelta * time_step
    omega0 = omega + domega * time_step

    value = {'Eqp0': Eqp0, 'Eqpp0': Eqpp0, 'Edpp0': Edpp0, 'delta0': delta0, 'omega0': omega0}
    return value    
  
def solve_GENSAL_model_state_parameter_actual_value(gen_md, par):
    '''
    求解发电机GENSAL模型状态变量的实际值
    输入: (1) gen_md, GENROU模型参数
          (2) par, GENROU模型状态参数
    输出: value, 模型状态实际参数
    '''
    Xd = gen_md.Xd
    Xq = gen_md.Xq
    Xdp = gen_md.Xdp
    Xqpp = gen_md.Xqpp
    Xdpp = gen_md.Xdpp
    Td0p = gen_md.Td0p
    Td0pp = gen_md.Td0pp
    Tq0pp = gen_md.Tq0pp
    Xqp = Xq
    
    omegas = 2 * pi * Base.BASFRQ
    Tj = 2 * gen_md.H

    Eqp = par['Eqp']
    Eqpp = par['Eqpp']
    Edpp = par['Edpp']
    Efq = par['Efq']
    delta = par['delta']
    omega = par['omega']
    Pe = par['Pe']
    Pm = par['Pm']
    It = par['It']
    time_step = par['time_step']
    Id, Iq = convert_xy_to_dq(delta, It.real, It.imag)  

    dEqp = 1/Td0p * (-(Xd-Xdpp)/(Xdp-Xdpp) * Eqp + (Xd-Xdp)/(Xdp-Xdpp) * Eqpp + Efq) 
    dEqpp = 1/Td0pp * (Eqp - Eqpp - (Xdp-Xdpp) * Id)
    dEdpp = 1/Tq0pp * (-Edpp + (Xqp-Xqpp) * Iq)

    ddelta = omegas * (omega - 1)
    domega = 1 / Tj * (Pm - Pe)

    Eqp0 = par['Eqp0']
    Eqpp0 = par['Eqpp0']
    Edpp0 = par['Edpp0']
    Efq0 = par['Efq0']
    delta0 = par['delta0']
    omega0 = par['omega0']
    Pe0 = par['Pe0']
    Pm0 = par['Pm0']
    It0 = par['It0']
    Id0, Iq0= convert_xy_to_dq(delta0, It0.real, It0.imag)  
    
    dEqp0 = 1/Td0p * (-(Xd-Xdpp)/(Xdp-Xdpp) * Eqp0 + (Xd-Xdp)/(Xdp-Xdpp) * Eqpp0 + Efq0) 
    dEqpp0 = 1/Td0pp * (Eqp0 - Eqpp0 - (Xdp-Xdpp) * Id0)
    dEdpp0 = 1/Tq0pp * (-Edpp0 + (Xqp-Xqpp) * Iq0)
    
    ddelta0 = omegas * (omega0 - 1)
    domega0 = 1 / Tj * (Pm0 - Pe0)

    delta = delta + (ddelta + ddelta0) * 0.5 * time_step
    omega = omega + (domega + domega0) * 0.5 * time_step
    Eqp = Eqp + (dEqp + dEqp0) * 0.5 * time_step
    Eqpp = Eqpp + (dEqpp + dEqpp0) * 0.5 * time_step
    Edpp = Edpp + (dEdpp + dEdpp0) * 0.5 * time_step

    value = {'delta': delta, 'omega': omega, 'Eqp': Eqp, 'Eqpp': Eqpp, 'Edpp': Edpp}
    return value
    