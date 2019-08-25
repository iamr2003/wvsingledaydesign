#!/usr/bin/env python2

import ev3
import wiiMote
from time import sleep
import thread
import socket
import cwiid

lift = ev3.motor("A")
rightMotor = ev3.motor("B")
leftMotor = ev3.motor("C")
claw = ev3.motor("D")

liftHomePos = lift.getPos()

mote = wiiMote.wiiMote()
mote.setMode(cwiid.RPT_BTN | cwiid.RPT_CLASSIC)
sleep(2)

wasPushed = False
isReversed = False

liftAuto = False


def hatThread():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 8000))
    s.listen(1)
    while True:
        client, addr = s.accept()
        lastCommand = ''
        try:
            while True:
                sleep(0.1)
                if (lastCommand != mote.getMoteButton('')):
                    client.send(str(mote.getMoteButton('')))
                    lastCommand = mote.getMoteButton('')
        except socket.error:
            print("Hat disconnected")


try:
    # thread.start_new_thread(hatThread, ())
    while True:
        # Reversing
        if (mote.getClassicButton("A") and isReversed == False and wasPushed == False):
            isReversed = True
            wasPushed = True
        elif (mote.getClassicButton("A") and isReversed == True and wasPushed == False):
            isReversed = False
            wasPushed = True
        elif (mote.getState()['classic']['buttons'] == 0 and wasPushed == True):
            wasPushed = False

        # Base
        speed = mote.getClassicJoistics()["leftY"] * 100
        rightJoistic = 1.4 * (mote.getClassicJoistics()["rightX"] * mote.getClassicJoistics()["rightX"] * mote.getClassicJoistics()["rightX"])
        if (isReversed == False):
            leftMotor.move(speed + rightJoistic * 100)
            rightMotor.move(speed - rightJoistic * 100)
        else:
            leftMotor.move(-speed + rightJoistic * 100)
            rightMotor.move(-speed - rightJoistic * 100)

        # Claw
        if (mote.getClassicButton("L")):
            claw.move(-100)
        elif (mote.getClassicButton("R")):
            claw.move(100)
        else:
            claw.braking(True)

        # Lift
        if (mote.getClassicButton("ZL")):
            liftAuto = False
            lift.move(50)
        elif (mote.getClassicButton("ZR")):
            liftAuto = True
            lift.moveAbs(liftHomePos, 525)
        elif (liftAuto == False):
            lift.braking(True)

        if (liftHomePos == lift.getPos()):
            liftAuto = False

finally:
    lift.reset()
    leftMotor.reset()
    rightMotor.reset()
    claw.reset()