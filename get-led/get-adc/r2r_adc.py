import RPi.GPIO as gp
import time
class R2R_ADC:
    def __init__ (self,dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range=dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        gp.setmode(gp.BCM)
        gp.setup(self.bits_gpio, gp.OUT, initial = 0)
        gp.setup(self.comp_gpio, gp.IN)
        

    def deinit(self):
        gp.output(self.bits_gpio, 0)
        gp.cleanup()


    def set_number(self, number):
        c=[int(element) for element in bin(number)[2:].zfill(8)]
        gp.output(self.bits_gpio, c)
        return c

    def sequential_counting_adc(self):
        for i in range (256) :
            self.set_number(i)
            time.sleep(self.compare_time)
            if gp.input(self.comp_gpio) == 1:
                return i
        return 255

    def get_sc_voltage(self):
        return self.sequential_counting_adc() / (2 ** len(self.bits_gpio) - 1) * self.dynamic_range

    def sucsessive_approximation_adc(self):
        for bit in reversed(range(self.bits_gpio)):
            trial = code | (1 << bit)
            self.set_dac(trial)
            time.sleep(self.compare_time)
            if self.comparator():
                code = trial

        return code


if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.3)
        while True:
            voltage = adc.get_sc_voltage()
            print(f"Напряжение {voltage:.3f}")

    finally:
        adc.deinit()

