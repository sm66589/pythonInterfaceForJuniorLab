import nidaqmx as ni
import time
import numpy as np
import matplotlib.pyplot as plt

# Define task and input channel
device = "Dev4"

task = ni.Task()
task.ci_channels.add_ci_count_edges_chan(device + "/ctr0")
task.start()
time.sleep(1)
task.stop()

print(task.read())

task.close()
