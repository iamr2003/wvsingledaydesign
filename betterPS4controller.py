#!/usr/bin/env python2

MAX_SPEED = 100

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

class EV3MotorNotFound(Exception): pass

class EV3Motor:
    def __init__(self, address):
        devices = PYUDEV_CONTEXT.list_devices(subsystem='tacho-motor', LEGO_ADDRESS=address)
        try: self.device = next(d for d in devices)
        except StopIteration: raise EV3MotorNotFound(address)

        self.duty_cycle_sp = open(os.path.join(self.device.sys_path, 'duty_cycle_sp'), 'w', 0)
        self.reset()

    def reset(self):
        self.set_duty_cycle_sp(0)
        self.send_command("run-direct")

    def set_duty_cycle_sp(self, new_duty_cycle_sp):
        return self.duty_cycle_sp.write(str(
            min(max(int(new_duty_cycle_sp), -100), 100)
        ))

    def send_command(self, new_mode):
        with open(os.path.join(self.device.sys_path, 'command'), 'w') as command:
            command.write(str(new_mode))


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

    left = EV3Motor('ev3-ports:outB')
    right = EV3Motor('ev3-ports:outC')

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

            left.set_duty_cycle_sp((speed * 1 - turn * 0.5) * MAX_SPEED)
            right.set_duty_cycle_sp((speed * 1 + turn * 0.5) * MAX_SPEED)
    finally:
        left.send_command('stop')
        right.send_command('stop')
