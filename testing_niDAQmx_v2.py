import nidaqmx as ni
import time
import numpy as np
import matplotlib.pyplot as plt

'''
So far, all attempts to control the frequency have not been successful.

Try to not use time.sleep(), instead, let the loop take readings as fast
as it can, just set the total measurement_time. 

Take three voltage readings from three analog channels per time coordinate.
This is designed with the ideal gas law experiment in mind. 

'''

# Define task and input channel
task = ni.Task()
task.ai_channels.add_ai_voltage_chan("Dev3/ai0")
task.ai_channels.add_ai_voltage_chan("Dev3/ai1")
task.ai_channels.add_ai_voltage_chan("Dev3/ai2")


measurement_time = 5    #seconds


# take readings and append them to their respective list for measurement_time in seconds.
data_lst = []
time_lst = []
time_initial = time.time()
while (time.time() - time_initial) < measurement_time:
    data_lst.append(task.read())
    time_lst.append(time.time() - time_initial)


task.close()


#divide by columns
dataArr = np.asarray(data_lst)
timeArr = np.asarray(time_lst)
ai0Volts = dataArr[:, 0]
ai1Volts = dataArr[:, 1]
ai2Volts = dataArr[:, 2]


plt.plot(timeArr, ai0Volts)
plt.plot(timeArr, ai1Volts)
plt.plot(timeArr, ai2Volts)
plt.show()


#write to file in CSV format
save_file = open(r"C://Users\sebas\Documents\UT\Fall2021\LA\Python_interface_to_replace_LabView\data\gasLaw_test.txt", "w")
save_file.write("ai0,    ai1,    ai2,    time")    #header


for i in range(len(timeArr)):
    str_ai0 = str(ai0Volts[i])
    str_ai1 = str(ai1Volts[i])
    str_ai2 = str(ai2Volts[i])
    str_time = str(timeArr[i])
    delimiter = ","

    save_file.write(
        "\n"
        + str_ai0 + delimiter
        + str_ai1 + delimiter
        + str_ai2
    )

save_file.close()

numberOfPoints = len(ai0Volts)
print()
print("number of points:", numberOfPoints)
print("total time:", timeArr[-1])
print("frequency:", numberOfPoints / timeArr[-1])


timeDiff = timeArr[1:] - timeArr[:-1]
plt.plot(timeDiff)
plt.show()
print()
print()
print("mean time interval between data points:", np.average(timeDiff))
print("std of time intervals:", np.std(timeDiff))