#!/usr/bin/env python2

import ev3
import wiiMote
from time import sleep

ArmMotor = ev3.motor("A")
mote = wiiMote.wiiMote()
mote.setClassic()
sleep(2)

wasPushed = False
isReversed = True

try:
    while True:
        if (mote.getClassicButton("A") and isReversed == False and wasPushed == False):
            isReversed = True
            wasPushed = True
        elif (mote.getClassicButton("A") and isReversed == True and wasPushed == False):
            isReversed = False
            wasPushed = True
        elif (mote.getState()['classic']['buttons'] == 0 and wasPushed == True):
            wasPushed = False

        if (isReversed == False):
            ArmMotor.run(mote.getClassicJoistics()["leftY"] * 100)                
        else:
            ArmMotor.run(-mote.getClassicJoistics()["leftY"] * 100)
finally:
    ArmMotor.reset()