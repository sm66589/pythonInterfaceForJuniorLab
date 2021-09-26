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
task = ni.Task()
task.ai_channels.add_ai_voltage_chan("Dev3/ai0")
task.ai_channels.add_ai_voltage_chan("Dev3/ai1")
task.ai_channels.add_ai_voltage_chan("Dev3/ai2")

measurementTime = 5  # seconds
numberOfPoints = 1000


########################################################################################################################
# FIRST METHOD:
# create empty array with no fixed length, then use np.append() to append reads to it.
########################################################################################################################

# take readings and append them to their respective list for measurement_time in seconds.
dataArr = np.array([])
timeArr = np.array([])
timeInitial = time.time()
while (time.time() - timeInitial) < measurementTime:
    np.append(dataArr, task.read())
    np.append(timeArr, time.time() - timeInitial)


#divide by columns
ai0Volts = np.asarray([])
ai1Volts = np.asarray([])
ai2Volts = np.asarray([])

for i in range(len(dataArr)):
    ai0Volts = np.append(ai0Volts, dataArr[i][0])
    ai1Volts = np.append(ai1Volts, dataArr[i][1])
    ai2Volts = np.append(ai2Volts, dataArr[i][2])


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
print("number of points:", numberOfPoints)
print("total time:", timeArr[-1])
print("frequency:", numberOfPoints / timeArr[-1])
print()
print()
print("mean time interval between reads:", np.average(timeDiff))
print("std of time intervals:", np.std(timeDiff))


########################################################################################################################
# SECOND METHOD:
# Use predefined arrays and populate them with a given number of items to fix the length.
########################################################################################################################

# populate lists
dataArr = np.asarray([None] * numberOfPoints)   # TODO: try to make a 2D array. Replace [None] with None.
timeArr = np.asarray([None] * numberOfPoints)

timeInitial = time.time()
for i in range(numberOfPoints):
    dataArr[i] = task.read()
    timeArr[i] = time.time() - timeInitial


ai0Volts = np.asarray([])
ai1Volts = np.asarray([])
ai2Volts = np.asarray([])

for i in range(len(dataArr)):
    ai0Volts = np.append(ai0Volts, dataArr[i][0])
    ai1Volts = np.append(ai1Volts, dataArr[i][1])
    ai2Volts = np.append(ai2Volts, dataArr[i][2])


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
print("number of points:", numberOfPoints)
print("total time:", timeArr[-1])
print("frequency:", numberOfPoints / timeArr[-1])
print()
print()
print("mean time interval between reads:", np.average(timeDiff))
print("std of time intervals:", np.std(timeDiff))



task.close()