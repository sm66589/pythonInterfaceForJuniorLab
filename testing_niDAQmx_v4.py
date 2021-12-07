import nidaqmx as ni
import time
import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray

'''



'''

# Define task and input channels. Task is an object from the NI library.
device = "Dev4"

task = ni.Task()
task.ai_channels.add_ai_voltage_chan(device + "/ai0")
task.ai_channels.add_ai_voltage_chan(device + "/ai1")
task.ai_channels.add_ai_voltage_chan(device + "/ai2")

# Set total acquisition time in seconds. Acquisition frequency is fixed to ~450 Hz.
acqTime = 10  # seconds



# Using the task.start() and task.stop() methods highly increases the count rate from ~25 Hz to almost 550 Hz.
dataLst = []
timeLst = []

task.start()   # <---- This is very important
timeInitial = time.time()

while time.time() - timeInitial <= acqTime:
    dataLst.append(task.read())
    timeLst.append(time.time() - timeInitial)

task.stop()    # <----- This is very important

task.close()   # Once data collection is finished, the task needs to be closed.



# convert lists into numpy arrays for easier data analysis.
dataArr = np.asarray(dataLst)
timeArr = np.asarray(timeLst)

# separate dataArr into columns for their respective channels.
ai0Volts = dataArr[:, 0]
ai1Volts = dataArr[:, 1]
ai2Volts = dataArr[:, 2]



# save data to a file. Make sure the save path is correct.
save_file = open(r"C://Users\sebas\Documents\UT\Fall2021\LA\Python_interface_to_replace_LabView\data\gasLaw_test_predefinedArray.txt", "w")
save_file.write("ai0,    ai1,    ai2,    time")

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
        + str_ai2 + delimiter
        + str_time
    )
save_file.close()



# plotting data.
plt.plot(timeArr, ai0Volts, '-.', label="ai0")
plt.plot(timeArr, ai1Volts, '-.', label="ai1")
plt.plot(timeArr, ai2Volts, '-.', label="ai2")
plt.legend()
plt.show()



# # the section below is characterizing the acquisiton frequency.
# print()
# print("number of points:", numberOfPoints)
# print("total time:", timeArr[-1])
# print("frequency:", numberOfPoints / timeArr[-1])
#
#
# timeDiff = timeArr[1:] - timeArr[:-1]
# plt.plot(timeDiff, '.')
# plt.show()
# print()
# print()
# print("mean time interval between data points:", np.average(timeDiff))
# print("std of time intervals:", np.std(timeDiff))