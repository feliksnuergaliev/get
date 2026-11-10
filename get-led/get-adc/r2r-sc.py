import r2r_adc
import time
import adc_plot

if __name__ == "__main__": 
    adc= r2r_adc.R2R_ADC(3.3, 0.0001)
    voltage_list =[]
    time_list = []
    duration = 5.0
    try:
        start = time.time()
        while(time.time()-start<duration):
            voltage_list.append(adc.get_sc_voltage())
            time_list.append(time.time()-start)
        adc_plot.plot_voltage_vs_time(time_list, voltage_list, 3.3)
        adc_plot.plot_sampling_hist(time_list)
    finally:
        adc.deinit()