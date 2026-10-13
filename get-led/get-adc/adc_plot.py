from matplotlib import pyplot as plt


def plot_voltage_vs_time(time, voltage, max_volatge):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.xname='time'
    plt.yname='voltage'
    plt.show()

