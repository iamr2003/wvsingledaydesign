#!/usr/bin/env python2

import socket
from time import sleep
import EV3

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("0.0.0.0", 8000))
serversocket.listen(1)

b = EV3.Motor('ev3-ports:outB')

while True:
    (clientsocket, address) = serversocket.accept()
    print("connected")
    b.set_duty_cycle_sp(-100)
    sleep(1)
    while True:
        command = clientsocket.recv(128)
        if not command: break
        print(command)
        if (command == 'up'):
            b.send_command('run-forever')
            b.set_duty_cycle_sp(-50)
        elif (command == 'down'):
            b.send_command('run-forever')
            b.set_duty_cycle_sp(50)
        elif (command == 'stop'):
            b.send_command('stop')

    print('disconnected')
    b.send_command('stop')