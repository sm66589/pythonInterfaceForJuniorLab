import nidaqmx as ni
import time
import numpy as np
import matplotlib.pyplot as plt

'''
Simple counter of rising edges. Based on 
https://github.com/ni/nidaqmx-python/blob/master/nidaqmx_examples/ci_count_edges.py

As of 10/01/2021, with input TTL pulses at 200kHz, the counter works using the code below. I don't understand how. 
'''

device = "Dev4"

task = ni.Task()
task.ci_channels.add_ci_count_edges_chan(device + "/ctr0")     # Denotes the channel that will make the counting
task.ci_channels[0].ci_count_edges_term = "/Dev4/PFI2"         # Denotes the source of the edges to count

#                                                              # From the test panel of NI MAX, it can be seen that the
#                                                              counting channel is not the same as the edge source. Not
#                                                              sure why.


countInterval = 10 #seconds

task.start()
initialTime = time.time()
while time.time() - initialTime <= countInterval:
    data = task.read()

print(data)

task.close()
#TODO: Understand how task.read() works for counters. Why does data need to be redefines everytime during the loop?

