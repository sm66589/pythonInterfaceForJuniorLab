import nidaqmx as ni
import time
import numpy as np
import matplotlib.pyplot as plt


# Define task and input channel
task = ni.Task()
task.ai_channels.add_ai_voltage_chan("Dev3/ai0")
task.ai_channels.add_ai_voltage_chan("Dev3/ai1")
task.ai_channels.add_ai_voltage_chan("Dev3/ai2")


measurement_time = 100    #seconds


data_lst = []
time_lst = []
time_initial = time.time()
while (time.time() - time_initial) < measurement_time:
    data_lst.append(task.read())
    time_lst.append(time.time() - time_initial)


task.close()


dataArr = np.asarray(data_lst)
timeArr = np.asarray(time_lst)
ai0Volts = dataArr[:, 0]
ai1Volts = dataArr[:, 1]
ai2Volts = dataArr[:, 2]


timeDiff = timeArr[1:] - timeArr[:-1]


plt.plot(timeDiff)
plt.show()


# plt.plot(time_lst, ai0Volts)
# plt.plot(time_lst, ai1Volts)
# plt.plot(time_lst, ai2Volts)
# plt.show()


# save_file = open(r"C://Users\sebas\Documents\UT\Fall2021\LA\Python_interface_to_replace_LabView\data\gasLaw_test.txt", "w")
# save_file.write("ai0,    ai1,    ai2,    time")
#
# for i in range(len(time_lst)):
#     str_ai0 = str(ai0Volts[i])
#     str_ai1 = str(ai1Volts[i])
#     str_ai2 = str(ai2Volts[i])
#     str_time = str(time_lst[i])
#     delimiter = ","
#
#     save_file.write(
#         "\n"
#         + str_ai0 + delimiter
#         + str_ai1 + delimiter
#         + str_ai2
#     )
#
# save_file.close()
