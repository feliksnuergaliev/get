import RPi.GPIO as gp
import time
gp.setmode(gp.BCM)
led=26
gp.setup(led, gp.OUT)
butt=13
gp.setup(butt, gp.IN)
state=0
while True:
    if gp.input(butt):
        state=not state
        gp.output(led, state)
        time.sleep(0.2)