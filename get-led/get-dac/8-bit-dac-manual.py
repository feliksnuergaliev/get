import RPi.GPIO as gp
leds=[16, 20, 21, 25, 26, 17, 27, 22]
gp.setmode(gp.BCM)
dac_bits=[2,3]
gp.setup(leds, gp.OUT)
gp.output(leds, 0)
dynamic_range=3.3

def voltage_to_number(voltage):
    if not(0.0<=voltage<=dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00-{dynamic_range:.2f}В)")
        print("")
        return 0

    return int(voltage / dynamic_range * 255)

def number_to_dac(num):
    c=[int(element) for element in bin(num)[2:].zfill(8)]
    gp.output(leds, c)
    return c
try:
    while True:
        try:
            voltage=float(input('Введите напряжение  вольтаx:'))
            number = voltage_to_number(voltage)
            number_to_dac(number)

            print("number:",number,"bits:",number_to_dac(number))

        except ValueError:
            print('Wrong input')
finally:
    gp.output(leds, 0)
    gp.cleanup()
