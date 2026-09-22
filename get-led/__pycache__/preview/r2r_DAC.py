import RPi.GPIO as gp
class R2R_DAC:
    def __init__(self,gpio_bits,dynamic_range,verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        gp.setmode(gp.BCM)
        gp.setup(self.gpio_bits, gp.OUT)

    def deinit(self):
        gp.output(self.gpio_bits, 0)
        gp.cleanup()

    def set_number(self, number):
        c=[int(element) for element in bin(number)[2:].zfill(8)]
        gp.output(self.gpio_bits, c)
        return c

    def set_voltage(self, voltage):
        if not(0.0<=voltage<=self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00-{self.dynamic_range:.2f}В)")
            print("")
            return 0
        b= int(voltage / self.dynamic_range * 255)
        self.set_number(b)
        return b

if __name__ == "__main__":
    dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)

    try:
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах:"))
                dac.set_voltage(voltage)

            except ValueError:
                print(f"Вы ввели не число. Попробуйте еще раз/n")

    finally:
        dac.deinit()