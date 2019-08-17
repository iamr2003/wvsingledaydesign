#!/usr/bin/env python2

import ev3
import cwiid
from time import sleep
import socket

lift = ev3.motor("A")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
oldCommand = ''

liftHomePos = lift.getPos()
liftAuto = False

try:
    s.connect(('192.168.43.153', 8000))
except:
    print("Incorect Base IP")

try:
    while True:
        command = int(s.recv(1024))
        print(command)
        # Lift
        if (bool(command & cwiid.BTN_A)):
            liftAuto = False
            lift.run(-50)
        elif (bool(command & cwiid.BTN_B)):
            liftAuto = True
            lift.moveAbs(liftHomePos, 100)
        elif (liftAuto == False):
            lift.braking(True)

        if (liftHomePos == lift.getPos()):
            liftAuto = False
finally:
    lift.reset()