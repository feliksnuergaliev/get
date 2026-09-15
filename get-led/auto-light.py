import RPi.GPIO as gp
import time 
gp.setmode(gp.BCM)
led=26
gp.setup(led, gp.OUT)
ph=6
gp.setup(ph, gp.IN)
state =0
while True:
    if gp.input(ph):
        state= not state
        gp.output(led, state)
        time.sleep = 0.2

