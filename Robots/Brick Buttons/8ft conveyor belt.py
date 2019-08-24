#!/usr/bin/env python2

import ev3
from time import sleep
import thread

sorterMotor = ev3.motor("A")
shortConveyorMotor = ev3.motor("B")
conveyorMotor = ev3.motor("C")

colorSensor = ev3.sensor(2)
colorSensor.colorColor()
ev3Button = ev3.buttons()

upPushed = False
downPushed = False
conveyor = 0
shortConveyor = 0

def sort():
    sortColor = 6
    print(colorSensor.getValue())
    if (colorSensor.getValue() == sortColor):
            sleep(0.1)
            sorterMotor.moveRel(500, 1500)
            sleep(0.5)
            sorterMotor.moveRel(-500, 1500)
            sleep(0.2)

        # print(ultrasonicSensor.getValue())
        # if (colorSensor.getValue() == sortColor):
        #     print('found')
        #     while (ultrasonicSensor.getValue() >= 50):
        #         sleep(0.1)
        #     # sleep(0.3)
        #     sorterMotor.moveRel(500, 1500)
        #     sleep(0.5)
        #     sorterMotor.moveRel(-500, 1500)
        # sleep(0.1)

try:
    # thread.start_new_thread(sort, ())
    while True:
        sortColor = 6
        print(colorSensor.getValue())
        if (colorSensor.getValue() == sortColor):
                sleep(0.1)
                sorterMotor.moveRel(500, 1500)
                sleep(0.5)
                sorterMotor.moveRel(-500, 1500)
                sleep(0.2)
        if (ev3Button.getButton('up') == True and upPushed == False):
            if (conveyor == 2):
                conveyor = 0
            else:
                conveyor += 1
            upPushed = True
        elif (ev3Button.getButton('up') == False and upPushed == True):
            upPushed = False

        if (conveyor == 1):
            conveyorMotor.move(-100)
        elif (conveyor == 2):
            conveyorMotor.move(100)
        else:
            conveyorMotor.move(0)

        if (ev3Button.getButton('down') == True and downPushed == False):
            if (shortConveyor != 2):
                shortConveyor += 1
            else:
                shortConveyor = 0
            downPushed = True
        elif (ev3Button.getButton('down') == False and downPushed == True):
            downPushed = False

        if (shortConveyor == 1):
            shortConveyorMotor.move(-50)
        elif (shortConveyor == 2):
            shortConveyorMotor.move(50)
        else:
            shortConveyorMotor.move(0)

finally:
    sorterMotor.reset()
    shortConveyorMotor.reset()
    conveyorMotor.reset()