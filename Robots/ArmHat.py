#!/usr/bin/env python2

import ev3
import cwiid
from time import sleep
import socket

ArmMotor = ev3.motor("A")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
oldCommand = ''

try:
    s.connect(('192.168.43.153', 8000))
except:
    print("Incorect Base IP")

try:
    while True:
        command = int(s.recv(1024))
        print(command)
        if (bool(command & cwiid.BTN_A)):
            ArmMotor.move(-50)
        elif (bool(command & cwiid.BTN_B)):
            ArmMotor.move(20)
        elif (command == 0):
            ArmMotor.move(0)
            ArmMotor.braking(True)
finally:
    ArmMotor.reset()