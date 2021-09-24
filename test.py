import timeit
import time

initial_time = time.time()

number_of_samples = 100
frequency = 10
time_interval = 1/frequency

for i in range(number_of_samples):
    time.sleep(1)
    print(time.time() - initial_time)