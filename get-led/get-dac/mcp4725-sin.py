import mcp4725_driver as mc
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

if __name__ == "__main__":
    try:
        dac=mc.MCP4725(5.0, 0x61, True)
        start = time.time()
        while True:
            t = time.time() - start
            voltage = amplitude * sg.get_sin_wave_amplitude(signal_frequency, t)
            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)


    finally:
        dac.deinit()