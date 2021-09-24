import nidaqmx as ni
import timeit
import time
import numpy as np
import matplotlib.pyplot as plt


    # Define task and input channel
def create_Task(task_name='', DevNumber_channel=1):
    task = ni.Task()
    task.ai_channels.add_ai_voltage_chan("Dev2/ai0")
    return task

task = create_Task()
number_of_samples = 50
frequency =20  #Hertz
time_interval = 1/frequency


# Measure time for append a task.read()
# t=time.time()
# T=10.0
# i=0
# lst_test = []
# while time.time()-t<T:
#     lst_test.append(task.read())
#     i+=1
# print(T/i)


lst_volts = []
lst_time = []
initial_time = time.time()
for i in range(number_of_samples):
    lst_time.append(time.time() - initial_time)
    lst_volts.append(task.read())

    time.sleep(time_interval)
final_time = time.time()

plt.plot(lst_time, lst_volts)
plt.show()

print(lst_time)

sum = 0
num = 0
lst_diffTime = []
for i in range(len(lst_time) - 1):
    lst_diffTime.append(np.abs(lst_time[i] - lst_time[i + 1]))

print(lst_diffTime)
print((1 / np.average(lst_diffTime)))

task.close()