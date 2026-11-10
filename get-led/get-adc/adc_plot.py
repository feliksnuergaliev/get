from matplotlib import pyplot as plt

def plot_sampling_hist(time):
    plttime=[]
    for i in range(1,len(time)):
        plttime.append(time[i] - time[i - 1])
    plt.figure(figsize=(10, 6))
    plt.xlim(0, 0.06)
    plt.hist(plttime, bins=10)

    plt.show()

def plot_voltage_vs_time(time, voltage, max_volatge):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.xname='time'
    plt.yname='voltage'
    plt.show()

