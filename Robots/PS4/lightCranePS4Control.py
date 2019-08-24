#!/usr/bin/env python2

MAX_SPEED = 200

# --- Library Includes ---

# evdev for joysticks
import evdev
from evdev import ecodes

# Other libraries
import threading
import ev3


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

    arm = ev3.motor('C')
    turn = ev3.motor('B')
    grabber = ev3.motor('D')
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
