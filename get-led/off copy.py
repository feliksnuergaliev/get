import RPi.GPIO as gp
import time
gp.setmode(gp.BCM)
led=12
leds= [24, 22, 23, 27, 17, 25, 12, 16]
gp.setup(leds, gp.OUT)
gp.output(leds, 0)
light_time = 0.2
while True:
    for led in leds:
        gp.output(led, 1)
        time.sleep(light_time)
        gp.output(led, 0)
    for led in reversed(leds):
        gp.output(led, 1)
        time.sleep(light_time)
        gp.output(led, 0)