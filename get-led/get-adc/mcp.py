from matplotlib import pyplot as plt
import mcp3021_driver

import time

ex_time =5.0

voltages=[]
times = []

try:
    adc=mcp3021_driver.MCP3021(5)
    start= time.time()
    while time.time() - start < ex_time:
        voltages.append(adc.get_voltage())
        times.append(time.time() - start)
    plt.figure(figsize=(10, 6))
    plt. plot(times, voltages)
    plt.title('Зависимость напряжени я от времени')
    plt.grid(True)
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