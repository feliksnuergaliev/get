import RPi.GPIO as gp
import time
gp.setmode(gp.BCM)
led=26
gp.setup(led, gp.OUT)
butt=13
gp.setup(butt, gp.IN)
state=0
gp.output(led, state)