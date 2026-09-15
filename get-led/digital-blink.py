import RPi.GPIO as gp
import time 
gp.setmode(gp.BCM)
led=26
gp.setup(led, gp.OUT)
state=0
period=1.0
while True:
    gp.output(led,state)
    state = not state
    time.sleep(period)

