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

Oct 7 2021 update: Using time.sleep() doesn't allow for good control of the frequency. 
Tried adding a while loop to wait until the time deltaT has passed. Seems to work better (?).
Need further testing to check.

Oct 7 2021 update2: Moreover on time.sleep(), setting time.sleep(0) will simply skip the loop.
However, setting time.sleep(1e-52) will not skip it, which limits the sampling rate to around 65 Hz,
even though the sleep time is essentially 0. 

Oct 8 2021 update: Tried delaying using a while loop. Works better than time.sleep(), still not great.
Tried testing the effective frequency vs input frequency, there seems to be a pattern, not sure why. 
Next, try using diff acquisition method. 
'''


def measure(freq, noPoints):
    # Define task and input channel
    device = "Dev3"

    task = ni.Task()
    task.ai_channels.add_ai_voltage_chan(device + "/ai0")
    task.ai_channels.add_ai_voltage_chan(device + "/ai1")
    task.ai_channels.add_ai_voltage_chan(device + "/ai2")

    #measurementTime = 5  # seconds
    numberOfPoints = noPoints
    frequency = freq
    deltaT = 1.0/frequency   #seconds


    # populate lists
    dataLst = [None] * numberOfPoints
    timeLst = [None] * numberOfPoints
    timeIntervalLst = [None] * numberOfPoints
    # Using the task.start() and task.stop() methods highly increases the count rate from ~25 Hz to almost 550 Hz.
    task.start()     # <---- This is very important

    timeInitial = time.time()
    for i in range(numberOfPoints):
        timeLst[i] = time.time()
        dataLst[i] = task.read()

        while time.time() - timeLst[i] < deltaT:
            continue

    task.stop()    # <---- This is very important
    task.close()


    dataArr = np.asarray(dataLst)
    timeArr = np.asarray(timeLst)

    ai0Volts = dataArr[:, 0]
    ai1Volts = dataArr[:, 1]
    ai2Volts = dataArr[:, 2]
    timeArr -= timeInitial


    # plt.plot(timeArr, ai0Volts, label="ai0")
    # plt.plot(timeArr, ai1Volts, label="ai1")
    # plt.plot(timeArr, ai2Volts, label="ai2")
    # plt.legend()
    # plt.show()

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
    print("number of points:", len(timeArr))
    print("total time:", timeArr[-1] - timeArr[0])
    print("frequency:", numberOfPoints / (timeArr[-1] - timeArr[0]))


    timeDiff = timeArr[1:] - timeArr[:-1]
    meanTimeInterval = np.average(timeDiff)
    stdTimeInterval = np.std(timeDiff)
    frequencyTimeInterval = 1/meanTimeInterval
    # plt.plot(timeDiff)
    # plt.show()
    # print()
    # print()
    # print("mean time interval between data points:", meanTimeInterval)
    # print("std of time intervals:", stdTimeInterval)
    #
    # print()
    # print()
    # print("avg frequency from mean time interval:", frequencyTimeInterval)

    return meanTimeInterval, stdTimeInterval, frequencyTimeInterval


def main():
    freqArr = np.linspace(50, 501, 50)
    meanTimeInterval = []
    stdTimeInterval = []
    frequencyInterval = []
    for i in range(len(freqArr)):
        mean, std, f = measure(freqArr[i], int(5*freqArr[i]))

        meanTimeInterval.append(mean)
        stdTimeInterval.append(std)
        frequencyInterval.append(f)

    plt.plot(freqArr, frequencyInterval, "-o")
    plt.plot(freqArr, freqArr)
    plt.show()

main()