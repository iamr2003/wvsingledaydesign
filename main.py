#!/usr/bin/env python2

import ev3
import wiiMote
from time import sleep

bMotor = ev3.motor('B')
cMotor = ev3.motor('C')

controller = wiiMote.wiiMote()
controller.setLed(1)
sleep(2)

try:
    controller.setNunchuk()
    while True:
        if (controller.getNunchukButton("C")):
            bMotor.run(-50)
            cMotor.run(50)
        elif (controller.getNunchukButton("Z")):
            bMotor.run(50)
            cMotor.run(-50)
        else:
            speed = controller.getNunchukJoistic()["Y"] * 100
            bMotor.run(speed + controller.getNunchukJoistic()["X"] * 50)
            cMotor.run(speed - controller.getNunchukJoistic()["X"] * 50)
finally:
    bMotor.sendCommand("stop")
    cMotor.sendCommand("stop")

# Classic Controls
# try:
    # controller.setClassic()
#     while True:
#         if (controller.getClassicButton("A")):
#             bMotor.run(50)
#             cMotor.run(-50)
#         else:
#             speed = controller.getClassicJoistics()["leftY"] * 100
#             bMotor.run(speed + controller.getClassicJoistics()["rightX"] * 50)
#             cMotor.run(speed - controller.getClassicJoistics()["rightX"] * 50)
# finally:
#     bMotor.sendCommand("stop")
#     cMotor.sendCommand("stop")