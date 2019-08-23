#!/usr/bin/env python2

import ev3
import wiiMote
from time import sleep
import thread
import socket
import cwiid

turnTable = ev3.motor("A")
claw = ev3.motor("B")
lift = ev3.motor("C")

mote = wiiMote.wiiMote()
mote.setMode(cwiid.RPT_BTN | cwiid.RPT_CLASSIC)
sleep(2)

wasPushed = False
isReversed = False

clawHomePos = claw.getPos()
clawAuto = False

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
        turnTable.run(mote.getClassicJoistics()["rightX"] * 100)
        lift.run(mote.getClassicJoistics()["leftY"] * 500)
        
        #Claw
        if (mote.getClassicButton("L")):
            claw.run(30)
        elif (mote.getClassicButton("R")):
            claw.run(-30)
        else:
            claw.run(0)
finally:
    turnTable.reset()
    claw.reset()
    lift.reset()
