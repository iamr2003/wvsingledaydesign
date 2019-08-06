#!/usr/bin/env python2

import ev3
from time import sleep
import socket

ArmMotor = ev3.motor("A")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
oldCommand = ''

try:
    s.connect(('192.168.1.106', 8000))
except:
    print("Incorect Base IP")

try:
    while True:
        command = s.recv(1024)
        print(command)
        if (command == 'up\n'):
            ArmMotor.run(-50)
        elif (command == 'down\n'):
            ArmMotor.run(50)
        elif (command == 'brake\n'):
            ArmMotor.run(0)
            ArmMotor.braking(True)
finally:
    ArmMotor.reset()