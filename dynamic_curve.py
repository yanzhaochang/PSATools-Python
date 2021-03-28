# Plot the rotor angle curve
import pandas as pd

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题


data_psa = pd.read_csv('.\\test_result\IEEE9_dynamic_result.csv', header=0)
data_steps = pd.read_csv('.\\test_result\IEEE9_dynamic_result_steps.csv', header=0)
print(data_psa)
'''
fig = plt.figure(num=1, figsize=(15, 8),dpi=80)     #开启一个窗口，同时设置大小，分辨率
ax1 = fig.add_subplot(1, 1, 1)  #通过fig添加子图，参数：行数，列数，第几个。
ax1.set_title('python-drawing')            #设置图体，plt.title
ax1.set_xlabel('x-name')                    #设置x轴名称,plt.xlabel
ax1.set_ylabel('y-name')                    #设置y轴名称,plt.ylabel
'''
time_psa = data_psa['TIME']
angle1_psa = data_psa['ROTOR ANGLE IN DEG @ GENERATOR 1 AT BUS 1'].values
angle2_psa = data_psa['ROTOR ANGLE IN DEG @ GENERATOR 2 AT BUS 2'].values
angle3_psa = data_psa['ROTOR ANGLE IN DEG @ GENERATOR 3 AT BUS 3'].values

time_steps = data_steps['TIME']
angle1_steps = data_steps['ROTOR ANGLE IN DEG @ GENERATOR 1 AT BUS 1'].values
angle2_steps = data_steps['ROTOR ANGLE IN DEG @ GENERATOR 1 AT BUS 2'].values
angle3_steps = data_steps['ROTOR ANGLE IN DEG @ GENERATOR 1 AT BUS 3'].values


angle2_1_psa = angle2_psa - angle1_psa
angle3_1_psa = angle3_psa - angle1_psa

angle2_1_steps = angle2_steps - angle1_steps
angle3_1_steps = angle3_steps - angle1_steps
'''
plt.figure(1)
plt.plot(time_psa, angle2_1_psa, color='y', label='发电机2-1')
plt.plot(time_psa, angle2_1_psa, 'b', label='发电机3-1')#'b'指：color='blue'

plt.plot(time_steps, angle2_1_steps, linestyle='-', color='y', label='发电机2-1')
plt.plot(time_steps, angle3_1_steps, linestyle='-', color='b', label='发电机3-1')#'b'指：color='blue'

plt.ylim(-50,90)  # 仅设置y轴坐标范围
plt.xlim(0.0, 2.0)
plt.xlabel('时间/s')
plt.ylabel('功角差/deg')
plt.legend()  #显示上面的labe
plt.title('程序仿真功角曲线')  #标题
'''

plt.figure(1)
plt.plot(time_psa, angle1_psa, color='b', label='教学程序')
plt.plot(time_steps, angle1_steps, color='y', linestyle='-', label='PSS/E')
plt.xlim(0.0, 2.0)
plt.xlabel('时间/s')
plt.ylabel('转子角/deg')
plt.legend()  #显示上面的labe
#plt.title('发电机1功角曲线')  #标题

plt.figure(2)
plt.plot(time_psa, angle2_psa, color='b', label='教学程序')
plt.plot(time_steps, angle2_steps, color='y', linestyle='-', label='PSS/E')
plt.xlim(0.0, 2.0)
plt.xlabel('时间/s')
plt.ylabel('转子角/deg')
plt.legend()  #显示上面的labe
#plt.title('发电机2功角曲线')  #标题

plt.figure(3)
plt.plot(time_psa, angle3_psa, color='b', label='教学程序')
plt.plot(time_steps, angle3_steps, color='y', linestyle='-', label='PSS/E')
plt.xlim(0.0, 2.0)
plt.xlabel('时间/s')
plt.ylabel('转子角/deg')
plt.legend()  #显示上面的labe
#plt.title('发电机3功角曲线')  #标题

'''
plt.figure(1)
plt.plot(time_psa, angle2_1_psa, color='b', label='教学程序')
plt.plot(time_steps, angle2_1_steps, color='y', linestyle='-', label='PSS/E')
plt.xlim(0.0, 2.0)
plt.xlabel('时间/s')
plt.ylabel('功角差/deg')
plt.legend()  #显示上面的labe
#plt.title('发电机2和发电机1功角差曲线')  #标题
'''
plt.show()