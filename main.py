#!/usr/bin/env python2

import ev3
import wiiMote
from time import sleep

bMotor = ev3.motor('B')
cMotor = ev3.motor('C')

controller = wiiMote.wiiMote()
controller.setClassic()
controller.setLed(1)
sleep(2)

try:
    while True:
        if (controller.getClassicButtons("A")):
            bMotor.setSpeed(50)
            cMotor.setSpeed(-50)
        else:
            speed = controller.getClassicJoistics()["leftY"] * 100
            bMotor.setSpeed(int(speed + controller.getClassicJoistics()["rightX"] * 50))
            cMotor.setSpeed(int(speed - controller.getClassicJoistics()["rightX"] * 50))
finally:
    bMotor.sendCommand("stop")
    cMotor.sendCommand("stop")
    