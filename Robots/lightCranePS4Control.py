#!/usr/bin/env python2

MAX_SPEED = 200

# --- Library Includes ---

# evdev for joysticks
import evdev
from evdev import ecodes

# Other libraries
import threading
import pyudev
import os


# --- EV3 Classes ---

PYUDEV_CONTEXT = pyudev.Context()

class sensorNotFound(Exception): pass

class sensor:
    def __init__(self, address):
        colors = PYUDEV_CONTEXT.list_devices(subsystem='lego-sensor', LEGO_ADDRESS='ev3-ports:in' + str(address))
        try: self.isSensor = next(c for c in colors)
        except IndexError: raise sensorNotFound(address)

        self.value_f = open(os.path.join(self.isSensor.sys_path, 'value0'), 'r')
        self.distance_f = open(os.path.join(self.isSensor.sys_path, 'units'), 'r')

    def mode(self, input):
        with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
            mode.write(input)

    def getValue(self):
        self.value_f.seek(0)
        return int(self.value_f.read())

    def colorReflect(self):
        with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
            mode.write('COL-REFLECT')

    def colorColor(self):
        with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
            mode.write('COL-COLOR')

    def touch(self):
        with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
            mode.write('TOUCH')

    def ultraIN(self):
        with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
            mode.write('US-DIST-IN')

    def ultraCM(self):
        with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
            mode.write('US-DIST-CM')

    def ultraDistance(self):
        return (self.getValue() / 10)

class motorNotFound(Exception): pass

class motor:
    def __init__(self, address):
        devices = PYUDEV_CONTEXT.list_devices(subsystem='tacho-motor', LEGO_ADDRESS='ev3-ports:out' + str(address))
        try: self.device = next(d for d in devices)
        except StopIteration: raise motorNotFound(address)

    def reset(self):
        with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
            file.write('reset')

    def sendCommand(self, newMode):
        with open(os.path.join(self.device.sys_path, 'command'),'w') as file:
            file.write(str(newMode))

    def getPos(self):
        with open(os.path.join(self.device.sys_path, 'position'),'r') as file:
            file.seek(0)
            return int(file.read().replace("\n", ""))

    # self.dutySpeed.write(str(int(min(max(newDutySpeed, -100), 100))))
    def move(self, speed):
        with open(os.path.join(self.device.sys_path, 'duty_cycle_sp'), 'w') as file:
            file.write(str(int(min(max(speed, -100), 100))))
        with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
            file.write("move-direct")

    def braking(self, braking):
        if (breaking == True):
            with open(os.path.join(self.device.sys_path, 'stop_action'), 'w') as file:
                file.write('hold')
            with open(os.path.join(self.device.sys_path, 'time_sp'), 'w') as file:
                file.write('0')
            with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
                file.write('move-timed')
        else:
            self.reset()

    def moveRel(self, distance, speed):
        with open(os.path.join(self.device.sys_path, 'speed_sp'), 'w') as file:
            file.write(str(speed))
        with open(os.path.join(self.device.sys_path, 'position_sp'), 'w') as file:
            file.write(str(distance))
        with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
            file.write('move-to-rel-pos')

    def moveAbs(self, distance, speed):
        with open(os.path.join(self.device.sys_path, 'speed_sp'), 'w') as file:
            file.write(str(speed))
        with open(os.path.join(self.device.sys_path, 'position_sp'), 'w') as file:
            file.write(str(distance))
        with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
            file.write('move-to-abs-pos')



# --- Joystick Reading Code ---

JOYSTICK = None
JOYSTICK_CAPS = {}
JOYSTICK_STATE = {}
JOYSTICK_DEFAULT_STATE = 0.0
#304-BTN_A
#305-BTN_B
#306-BTN_C
#307-BTN_NORTH

#545/546/547/544-BTN_DPAD_(DOWN/UP/LEFT/RIGHT)
def map_range(in_min, in_max, out_min, out_max, value):
    return out_min + ((value - in_min) * (out_max - out_min) / (in_max - in_min))

def find_joystick(name):
    global JOYSTICK
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    JOYSTICK = [device for device in devices if device.name == name][0]
    for abs_id, abs_info in JOYSTICK.capabilities()[ecodes.EV_ABS]:
        JOYSTICK_CAPS[abs_id] = abs_info
        JOYSTICK_STATE[abs_id] = JOYSTICK_DEFAULT_STATE

def watch_joystick():
    for event in JOYSTICK.read_loop():
        print(event.code)
        if event.type != ecodes.EV_ABS: continue
        caps = JOYSTICK_CAPS[event.code]
        JOYSTICK_STATE[event.code] = map_range(caps.min, caps.max, -1.0, 1.0, event.value)


# --- Main Code ---

if __name__ == '__main__':

    print('Initializing motors')

    arm = motor('C')
    turn = motor('B')
    grabber = motor('D')
    print('Discovering joystick')

    # 'Wireless Controller' for DS4
    find_joystick('Wireless Controller')
    joystick_thread = threading.Thread(target=watch_joystick)
    joystick_thread.daemon = True
    joystick_thread.start()

    print('Starting drive loop')
    armspeed = 0
    armMode='move'
    armpos =0
    p=1
    try:
        while True:
            ls_y = -JOYSTICK_STATE[ecodes.ABS_Y]
            rs_x = -JOYSTICK_STATE[ecodes.ABS_RX]
            ls_x = -JOYSTICK_STATE[ecodes.ABS_X]

            if abs(ls_y) < 0.05:
                ls_y = 0

            if( ls_y != 0):
                armspeed = -ls_y * MAX_SPEED
                armMode = 'move'
                print('moving')
                print ls_y
            elif (ls_y == 0) and armMode == 'move':
                armpos = arm.getPos()
                armMode = 'hold'
                print ("position set to:" +str(armpos))
            else:
                armspeed = p*(armpos - arm.getPos())
                print ('holding') 
                

            
            arm.move(armspeed)
            turn.move((-rs_x) * MAX_SPEED)
            grabber.move((ls_x*.75) * MAX_SPEED)
    finally:
        arm.sendCommand('stop')
        turn.sendCommand('stop')
        grabber.sendCommand('stop')
