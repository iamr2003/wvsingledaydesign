#!/usr/bin/env python2

MAX_SPEED = 100

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
        if event.type != ecodes.EV_ABS: continue
        caps = JOYSTICK_CAPS[event.code]
        JOYSTICK_STATE[event.code] = map_range(caps.min, caps.max, -1.0, 1.0, event.value)


# --- Main Code ---

if __name__ == '__main__':

    print('Initializing motors')

    left = ev3.motor('B')
    right = ev3.motor('C')

    print('Discovering joystick')

    # 'Wireless Controller' for DS4
    find_joystick('Wireless Controller')
    joystick_thread = threading.Thread(target=watch_joystick)
    joystick_thread.daemon = True
    joystick_thread.start()

    print('Starting drive loop')

    try:
        while True:
            ls_y = -JOYSTICK_STATE[ecodes.ABS_Y]
            rs_x = -JOYSTICK_STATE[ecodes.ABS_RX]

            speed = -(ls_y ** 2) if ls_y < 0 else (ls_y ** 2)
            turn  = -(rs_x ** 2) if rs_x < 0 else (rs_x ** 2)

            left.run((speed * 1 - turn * 0.5) * MAX_SPEED)
            right.run((speed * 1 + turn * 0.5) * MAX_SPEED)
    finally:
        left.reset()
        right.reset()
