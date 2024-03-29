#!/usr/bin/env python2

import ev3
import wiiMote
from time import sleep
import thread
import socket
import cwiid

inLeftMotor = ev3.motor("B")
inRightMotor = ev3.motor("C")

mote = wiiMote.wiiMote()
mote.setMode(cwiid.RPT_BTN | cwiid.RPT_CLASSIC)
sleep(2)

wasPushed = False
isReversed = False

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
    thread.start_new_thread(hatThread, ())
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
        rightJoistic = (mote.getClassicJoistics()["rightX"] * mote.getClassicJoistics()["rightX"] * mote.getClassicJoistics()["rightX"])
        if (isReversed == False):
            inLeftMotor.move(-speed + rightJoistic * 100)
            inRightMotor.move(-speed - rightJoistic * 100)
        else:
            inLeftMotor.move(speed + rightJoistic * 100)
            inRightMotor.move(speed - rightJoistic * 100)

finally:
    inLeftMotor.reset()
    inRightMotor.reset()
    