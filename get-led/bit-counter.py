import RPi.GPIO as gp
import time
gp.setmode(gp.BCM)
led=12
leds= [16, 12, 25, 17, 27, 23, 22, 24]
up=9
down=10
sleep_time=0.2
gp.setup(up, gp.IN)
gp.setup(down, gp.IN)
gp.setup(leds, gp.OUT)
gp.output(leds, 0)
num=0
def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
    sleep_time = 0.2
while True:
    if gp.input(up):
        num +=1
        if num > 256:
            num =0
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    if gp.input(down):
        num -=1
        if num < 0: 
            num=0
        print(num, dec2bin(num))
        time.sleep(sleep_time)
        if gp.input(up) and gp.input(down):
            num=254
            
            print(num, dec2bin(num))
        time.sleep(sleep_time)
    gp.output(leds, dec2bin(num))