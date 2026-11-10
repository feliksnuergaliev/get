import time
from r2r_adc import R2R_ADC
from matplotlib import pyplot as plt

dyn_range = 3.3
experiment_time = 5.0


voltages = []
times = []

try:
    adc = R2R_ADC(dyn_range)
    start = time.time()
    while time.time() - start < experiment_time:
        voltages.append(adc.get_sc_voltage())
        times.append(time.time() - start)
    plt.figure(figsize=(10, 6))
    plt.plot(times, voltages)
    plt.show()

    plttime=[]
    for i in range(1,len(times)):
        plttime.append(times[i] - times[i - 1])
    plt.figure(figsize=(10, 6))
    plt.xlim(0, 0.06)
    plt.hist(plttime, bins=10)

    plt.show()

finally:
    adc.deinit()