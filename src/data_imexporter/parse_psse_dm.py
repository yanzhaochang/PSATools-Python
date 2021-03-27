# 解析PSSE的dyr动态模型文件
import sys
sys.path.append('..')
import apis


def init_dynamic_data(file):
    '''
    Initialize the dynamic model data, parse the data of each component from the file and import it into memory.
    Args: 
        file, str, dynamic model data dyr file.
    Rets: None
    '''
    models_data = read_psse_dyr(file)
    
    generator_models_data, exciter_models_data, turbine_governor_models_data = separate_model_data(models_data)
    
    parse_generator_model(generator_models_data)
    
    parse_exciter_model(exciter_models_data)
    
    parse_turbine_governor_model(turbine_governor_models_data)
    
    return

def read_psse_dyr(file):
    '''
    Read the transient model data file and do the preliminary processing.
    Args:
        file, str, dynamic model data dyr file.
    Rets: 
        models_data, list, dyr model data.
    '''
    dyr_lines_data = ''
    with open(file, encoding = 'utf-8') as f:
        while True:
            text = f.readline().rstrip('\n')
            if not text:
                break
            dyr_lines_data = dyr_lines_data + text
            
    model_dyr_data = dyr_lines_data.split('/')[:-1]
    
    models_data = []
    for i in range(len(model_dyr_data)):
        tmp_data = model_dyr_data[i].split(' ')
        data = []
        for item in tmp_data:
            if len(item) != 0:
                data.append(eval(item))
        models_data.append(data)
    return models_data

def separate_model_data(models_data):
    '''
    Separate generator, exciter and governor model data.
    Args: 
        models_data, list, dyr model data.
    Rets:
        (1) generator_models_data, list, generator model data.
        (2) exciter_models_data, list, exciter model data.
        (3) turbine_governor_models_data, list, turbine governor model data.
    '''
    generator_models = ('GENROU', 'GENSAL', 'GENCLS', 'GENTRA')
    exciter_models = ('SEXS', )
    turbine_governor_models = ('IEEEG1', 'IEEEG3')

    generator_models_data = []
    exciter_models_data = []
    turbine_governor_models_data = [] 
    for model_data in models_data:
        if model_data[1] in generator_models:
            generator_models_data.append(model_data)
            
        elif model_data[1] in exciter_models:
            exciter_models_data.append(model_data)
            
        elif model_data[1] in turbine_governor_models:
            turbine_governor_models_data.append(model_data)
            
    return generator_models_data, exciter_models_data, turbine_governor_models_data
    
def parse_generator_model(data):
    '''
    Parse generator model data, including model GENROU, GENSAL, GENTRA, GENCLS.
    Args:
        data, list, generator model data.
    Rets: None
    '''
    for item in data:
        generator = item[0]
        apis.add_generator_related_model(generator, 'GEN')
        apis.set_generator_related_model_data(generator, 'GEN', 'GMN', item[1])
        if item[1] == 'GENROU':
            apis.set_generator_related_model_data(generator, 'GEN', 'Td0p', item[3])
            apis.set_generator_related_model_data(generator, 'GEN', 'Td0pp', item[4])
            apis.set_generator_related_model_data(generator, 'GEN', 'Tq0p', item[5])
            apis.set_generator_related_model_data(generator, 'GEN', 'Tq0pp', item[6])
            apis.set_generator_related_model_data(generator, 'GEN', 'H', item[7])
            apis.set_generator_related_model_data(generator, 'GEN', 'D', item[8])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xd', item[9])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xq', item[10])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xdp', item[11])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xqp', item[12])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xdpp', item[13])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xqpp', item[13])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xl', item[14])

        elif item[1] == 'GENSAL':
            apis.set_generator_related_model_data(generator, 'GEN', 'Td0p', item[3])
            apis.set_generator_related_model_data(generator, 'GEN', 'Td0pp', item[4])
            apis.set_generator_related_model_data(generator, 'GEN', 'Tq0pp', item[5])
            apis.set_generator_related_model_data(generator, 'GEN', 'H', item[6])
            apis.set_generator_related_model_data(generator, 'GEN', 'D', item[7])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xd', item[8])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xq', item[9])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xdp', item[10])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xdpp', item[11])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xqpp', item[11])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xl', item[12])

        elif item[1] == 'GENCLS':
            apis.set_generator_related_model_data(generator, 'GEN', 'H', item[3])
            apis.set_generator_related_model_data(generator, 'GEN', 'D', item[4])
       
        elif item[1] == 'GENTRA':
            apis.set_generator_related_model_data(generator, 'GEN', 'Td0p', item[3])
            apis.set_generator_related_model_data(generator, 'GEN', 'H', item[4])
            apis.set_generator_related_model_data(generator, 'GEN', 'D', item[5])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xd', item[6])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xq', item[7])
            apis.set_generator_related_model_data(generator, 'GEN', 'Xdp', item[8])   
            
        else:
            print('Failed to parse generator model {} data. It is not supported now'.format(item[1]))
            pass
    return

def parse_exciter_model(data):
    '''
    Parse exciter model data, including model SEXS
    Args:
        data, list, exciter model data.
    Rets: None
    '''
    for item in data:
        generator = item[0]
        apis.add_generator_related_model(generator, 'AVR')   
        apis.set_generator_related_model_data(generator, 'AVR', 'EMN', item[1])        
        if item[1] == 'SEXS':  
            apis.set_generator_related_model_data(generator, 'AVR', 'TA', item[3] * item[4])
            apis.set_generator_related_model_data(generator, 'AVR', 'TB', item[4])
            apis.set_generator_related_model_data(generator, 'AVR', 'K', item[5])
            apis.set_generator_related_model_data(generator, 'AVR', 'TE', item[6])
            apis.set_generator_related_model_data(generator, 'AVR', 'EMIN', item[7])
            apis.set_generator_related_model_data(generator, 'AVR', 'EMAX', item[8])

        else:
            print('Failed to parse exciter model {} data. It is not supported now'.format(item[1]))
            pass
    return

def parse_turbine_governor_model(data):
    '''
    Parse turbine governor model data, including model IEEEG1 and IEEEG3.
    Args:
        data, list, turbine governor model data.
    Rets: None
    '''
    for item in data:
        generator = item[0]
        apis.add_generator_related_model(generator, 'GOV')
        apis.set_generator_related_model_data(generator, 'GOV', 'TGMN', item[1])
        if item[1] == 'IEEEG1':
            apis.set_generator_related_model_data(generator, 'GOV', 'M', item[4])
            apis.set_generator_related_model_data(generator, 'GOV', 'K', item[5])
            apis.set_generator_related_model_data(generator, 'GOV', 'T1', item[6])
            apis.set_generator_related_model_data(generator, 'GOV', 'T2', item[7])
            apis.set_generator_related_model_data(generator, 'GOV', 'T3', item[8])
            apis.set_generator_related_model_data(generator, 'GOV', 'UO', item[9])
            apis.set_generator_related_model_data(generator, 'GOV', 'UC', item[10])
            apis.set_generator_related_model_data(generator, 'GOV', 'PMAX', item[11])
            apis.set_generator_related_model_data(generator, 'GOV', 'PMIN', item[12])
            apis.set_generator_related_model_data(generator, 'GOV', 'T4', item[13])
            apis.set_generator_related_model_data(generator, 'GOV', 'K1', item[14])
            apis.set_generator_related_model_data(generator, 'GOV', 'K2', item[15])
            apis.set_generator_related_model_data(generator, 'GOV', 'T5', item[16])
            apis.set_generator_related_model_data(generator, 'GOV', 'K3', item[17])
            apis.set_generator_related_model_data(generator, 'GOV', 'K4', item[18])
            apis.set_generator_related_model_data(generator, 'GOV', 'T6', item[19])
            apis.set_generator_related_model_data(generator, 'GOV', 'K5', item[20])
            apis.set_generator_related_model_data(generator, 'GOV', 'K6', item[21])
            apis.set_generator_related_model_data(generator, 'GOV', 'T7', item[22])
            apis.set_generator_related_model_data(generator, 'GOV', 'K7', item[23])
            apis.set_generator_related_model_data(generator, 'GOV', 'K8', item[24])

        elif item[1] == 'IEEEG3':
            apis.set_generator_related_model_data(generator, 'GOV', 'TG', item[3])
            apis.set_generator_related_model_data(generator, 'GOV', 'TP', item[4])
            apis.set_generator_related_model_data(generator, 'GOV', 'UO', item[5])
            apis.set_generator_related_model_data(generator, 'GOV', 'UC', item[6])
            apis.set_generator_related_model_data(generator, 'GOV', 'PMAX', item[7])
            apis.set_generator_related_model_data(generator, 'GOV', 'PMIN', item[8])
            apis.set_generator_related_model_data(generator, 'GOV', 'sigma', item[9])
            apis.set_generator_related_model_data(generator, 'GOV', 'delta', item[10])
            apis.set_generator_related_model_data(generator, 'GOV', 'TR', item[11])
            apis.set_generator_related_model_data(generator, 'GOV', 'TW', item[12])
            apis.set_generator_related_model_data(generator, 'GOV', 'a11', item[13])
            apis.set_generator_related_model_data(generator, 'GOV', 'a13', item[14])
            apis.set_generator_related_model_data(generator, 'GOV', 'a21', item[15])
            apis.set_generator_related_model_data(generator, 'GOV', 'a23', item[16])
            
        else:
            print('Failed to parse turbine governor model {} data. It is not supported now'.format(item[1]))
            pass
    return
    
def change_generator_model_parameter_in_system_base():
    '''
    将发电机的阻抗转换为系统基准下
    '''
    for gen_md in SyncGenMd:
        gen = [gen for gen in GenData if gen.NUMBER==gen_md.IBUS][0]  # 初始化基准功率, 电抗
        gen_md.H = gen_md.H * gen.MBASE / Base.SBASE
        
        if gen_md.GMN == 'GENROU':
            gen_md.Xq = gen_md.Xq * Base.SBASE / gen.MBASE  # 电抗转为系统基准
            gen_md.Xd = gen_md.Xd * Base.SBASE / gen.MBASE
            gen_md.Xdp = gen_md.Xdp * Base.SBASE / gen.MBASE
            gen_md.Xqp = gen_md.Xqp * Base.SBASE / gen.MBASE
            gen_md.Xdpp = gen_md.Xdpp * Base.SBASE / gen.MBASE
            gen_md.Xqpp = gen_md.Xqpp * Base.SBASE / gen.MBASE  
            
        elif gen_md.GMN == 'GENSAL':
            gen_md.Xq = gen_md.Xq * Base.SBASE / gen.MBASE  # 电抗转为系统基准
            gen_md.Xd = gen_md.Xd * Base.SBASE / gen.MBASE
            gen_md.Xdp = gen_md.Xdp * Base.SBASE / gen.MBASE
            gen_md.Xdpp = gen_md.Xdpp * Base.SBASE / gen.MBASE
            gen_md.Xqpp = gen_md.Xqpp * Base.SBASE / gen.MBASE 
            
        elif gen_md.GMN == 'GENTRA':
            gen_md.Xq = gen_md.Xq * Base.SBASE / gen.MBASE  # 电抗转为系统基准
            gen_md.Xd = gen_md.Xd * Base.SBASE / gen.MBASE
            gen_md.Xdp = gen_md.Xdp * Base.SBASE / gen.MBASE
        
        elif gen_md.GMN == 'GENCLS': 
            gen_md.Xq = gen.ZX * Base.SBASE / gen.MBASE  # 电抗转为系统基准
            gen_md.Xdp = gen_md.Xq
            
        else:
            print('发电机{}的模型{}暂不支持'.format(gen_md.IBUS, gen_md.GMN))
            continue
    return 