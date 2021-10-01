import nidaqmx as ni
import time
import numpy as np
import matplotlib.pyplot as plt
'''
Comparing different methods to take a read() measurements and append it to an array.

First method creates an array with predefined length. To append the data to the array, set the value of the item in an
array equal to the read() output.

Second method creates an empty array, then use np.append() to add the value to the array. 

In theory, method 1 should be faster at appending read() to a list, which would increase the max frequency at which
we can take measurements. In practice, there is no measurable difference in the measuring frequency (about 25 Hz)
'''

# Define task and input channel
device = "Dev4"

task = ni.Task()
task.ai_channels.add_ai_voltage_chan(device + "/ai0")
task.ai_channels.add_ai_voltage_chan(device + "/ai1")
task.ai_channels.add_ai_voltage_chan(device + "/ai2")

measurementTime = 5  # seconds
numberOfPoints = 100


########################################################################################################################
# FIRST METHOD:
# create empty array with no fixed length, then use np.append() to append reads to it.
########################################################################################################################

# take readings and append them to their respective list for measurement_time in seconds.
dataLst = []
timeLst = []
timeInitial = time.time()
for i in range(numberOfPoints):
    dataLst.append(task.read())
    timeLst.append(time.time() - timeInitial)


#divide by columns
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


# print time measurements
timeDiff = timeArr[1:] - timeArr[:-1]
plt.plot(timeDiff)
plt.show()

print()
print("METHOD 1: ")
print("number of points:", numberOfPoints)
print("total time:", timeArr[-1])
print("frequency:", numberOfPoints / timeArr[-1])
print()
print("mean time interval between reads:", np.average(timeDiff))
print("std of time intervals:", np.std(timeDiff))
print()


########################################################################################################################
# SECOND METHOD:
# Use predefined arrays and populate them with a given number of items to fix the length.
########################################################################################################################

# populate lists
dataLst = [None] * numberOfPoints
timeLst = [None] * numberOfPoints

timeInitial = time.time()
for i in range(numberOfPoints):
    dataLst[i] = task.read()
    timeLst[i] = time.time() - timeInitial

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


# print time measurements
timeDiff = timeArr[1:] - timeArr[:-1]
plt.plot(timeDiff)
plt.show()

print()
print("SECOND METHOD: ")
print("number of points:", numberOfPoints)
print("total time:", timeArr[-1])
print("frequency:", numberOfPoints / timeArr[-1])
print()
print("mean time interval between reads:", np.average(timeDiff))
print("std of time intervals:", np.std(timeDiff))

