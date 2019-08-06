#!/usr/bin/env python2

import ev3
import wiiMote

bMotor = ev3.motor('B')
cMotor = ev3.motor('C')

controller = wiiMote.wiiMote()
controller.setClassic()
controller.setLed(1)

try:
    while True:
        if (controller.getClassicButton("A")):
            bMotor.run(50)
            cMotor.run(-50)
        else:
            speed = controller.getClassicJoistics()["leftY"] * 100
            bMotor.run(speed + controller.getClassicJoistics()["rightX"] * 50)
            cMotor.run(speed - controller.getClassicJoistics()["rightX"] * 50)
finally:
    bMotor.sendCommand("stop")
    cMotor.sendCommand("stop")