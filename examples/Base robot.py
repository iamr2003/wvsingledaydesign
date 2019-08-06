#!/usr/bin/env python2

import ev3
import wiiMote
from time import sleep
import thread
import socket
import cwiid

#Motors
# motor = ev3.motor("A")

mote = wiiMote.wiiMote()
mote.setMode(cwiid.RPT_BTN | cwiid.RPT_CLASSIC)
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
                if (mote.getMoteButton("A") and lastCommand != 'up\n'):
                    client.send("up\n")
                    lastCommand = "up\n"
                elif (mote.getMoteButton("B") and lastCommand != 'down\n'):
                    client.send("down\n")
                    lastCommand = "down\n"
                elif(mote.getState()['buttons'] == 0 and lastCommand != 'brake\n'):
                    client.send("brake\n")
                    lastCommand = "brake\n"
        except socket.error:
            print("Hat disconnected")



def liftThread():
    while True:
        sleep(0.1)
        if (mote.getClassicButton("ZL")):
            lift.run(-50)
        elif (mote.getClassicButton("ZR")):
            lift.moveAbs(liftHomePos, 100)
            while liftHomePos != lift.getPos():
                sleep(0.01)
        else:
            lift.braking(True)


def clawThread():
    while True:
        sleep(0.1)
        if (mote.getClassicButton("L")):
            claw.run(-100)
        elif (mote.getClassicButton("R")):
            claw.run(100)
        else:
            claw.braking(True)

try:
    thread.start_new_thread(liftThread, ())
    thread.start_new_thread(clawThread, ())
    thread.start_new_thread(hatThread, ())
    while True:
        speed = mote.getClassicJoistics()["leftY"] * 100
        if (mote.getClassicButton("A") and isReversed):
            speed = (speed * speed * speed)
            rightJoistic = (mote.getClassicJoistics()["rightX"] * mote.getClassicJoistics()["rightX"] * mote.getClassicJoistics()["rightX"])
            leftMotor.run(speed + rightJoistic * 100)
            rightMotor.run(speed - rightJoistic * 100)
        else:
            leftMotor.run(speed + mote.getClassicJoistics()["rightX"] * 100)
            rightMotor.run(speed - mote.getClassicJoistics()["rightX"] * 100)
finally:
    lift.reset()
    leftMotor.reset()
    rightMotor.reset()
    claw.reset()
