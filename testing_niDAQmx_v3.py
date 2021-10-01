import nidaqmx as ni
import time
import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray

'''
Try to create an array with size numberOfPoints and populate the array with 
numberOfPoints voltage readings. 
 
Contrast this method with creating an empty list and using lst.append() to 
populate the list. Populating an array of pre-defined size is supposedly 
faster than appending to a list with undefined size. 

'''

# Define task and input channel
device = "Dev4"

task = ni.Task()
task.ai_channels.add_ai_voltage_chan(device + "/ai0")
task.ai_channels.add_ai_voltage_chan(device + "/ai1")
task.ai_channels.add_ai_voltage_chan(device + "/ai2")

measurementTime = 5  # seconds
numberOfPoints = 1000

# populate lists
dataLst = [None] * numberOfPoints
timeLst = [None] * numberOfPoints


# Using the task.start() and task.stop() methods highly increases the count rate from ~25 Hz to almost 550 Hz.
task.start()     # <---- This is very important
timeInitial = time.time()
for i in range(numberOfPoints):
    dataLst[i] = task.read()
    timeLst[i] = time.time() - timeInitial

task.stop()    # <----- This is very important
task.close()

dataArr = np.asarray(dataLst)
timeArr = np.asarray(timeLst)

ai0Volts = dataArr[:, 0]
ai1Volts = dataArr[:, 1]
ai2Volts = dataArr[:, 2]


plt.plot(timeArr, ai0Volts, label="ai0")
plt.plot(timeArr, ai1Volts, label="ai1")
plt.plot(timeArr, ai2Volts, label="ai2")
plt.legend()
plt.show()

# save_file = open(r"C://Users\sebas\Documents\UT\Fall2021\LA\Python_interface_to_replace_LabView\data\gasLaw_test_predefinedArray.txt", "w")
# save_file.write("ai0,    ai1,    ai2,    time")
#
# for i in range(len(timeArr)):
#     str_ai0 = str(ai0Volts[i])
#     str_ai1 = str(ai1Volts[i])
#     str_ai2 = str(ai2Volts[i])
#     str_time = str(timeArr[i])
#     delimiter = ","
#
#     save_file.write(
#         "\n"
#         + str_ai0 + delimiter
#         + str_ai1 + delimiter
#         + str_ai2
#     )
# save_file.close()
#
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