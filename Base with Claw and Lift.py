#!/usr/bin/env python2

import ev3
import wiiMote
from time import sleep

lift = ev3.motor("A")
rightMotor = ev3.motor("B")
leftMotor = ev3.motor("C")
claw = ev3.motor("D")

mote = wiiMote.wiiMote()
mote.setClassic()
sleep(2)
isReversed = False

while True:
    if (mote.getClassicButton("A") and isReversed):
        pass
    speed = mote.getClassicJoistics()["leftY"] * 100
    leftMotor.run(speed + mote.getClassicJoistics()["rightX"] * 100)
    rightMotor.run(speed - mote.getClassicJoistics()["rightX"] * 100)
    if (mote.getClassicButton("L")):
        claw.run(-100)
    elif (mote.getClassicButton("R")):
        claw.run(100)
    else:
        claw.run(0)
    
    if (mote.getClassicButton("ZL")):
        lift.run(-100)
    elif (mote.getClassicButton("ZR")):
        lift.run(100)
    else:
        lift.run(0)