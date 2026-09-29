import RPi.GPIO as gp
class PWM_DAC:

    def __init__(self,gpio_pin, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_pin = gpio_pin
        self.pwm_frequency = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose


        gp.setmode(gp.BCM)
        gp.setup(self.gpio_pin, gp.OUT, initial = 0)

        self.pwm = gp.PWM(self.gpio_pin, self.pwm_frequency)
        self.pwm.start(0)

    def deinit(self):
        self.pwm.stop()
        gp.cleanup()

    def set_voltage(self, voltage):
        if not(0.0<=voltage<=self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00-{self.dynamic_range:.2f}В)")
            print("Устанавливаем 0.0 В")
            voltage = 0.0

        duty_cycle = voltage / self.dynamic_range * 100
        self.pwm.ChangeDutyCycle(duty_cycle)
        
        if self.verbose:
            print(f"Коэффицент заполнения : {duty_cycle:.2f} %")

if __name__ == "__main__":
    dac = PWM_DAC(12, 500, 3.290, True)
    try:

        while True:
            try:
                voltage = float(input("enter voltage"))
                dac.set_voltage(voltage)

            except ValueError:
                print('you entered not a number. try again')

    finally:
        dac.deinit()