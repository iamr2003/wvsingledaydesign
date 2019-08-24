#!/usr/bin/env python

import array
import fcntl
import sys
from time import sleep

# from linux/input.h

KEY_UP = 103
KEY_DOWN = 108
KEY_LEFT = 105
KEY_RIGHT = 106
KEY_ENTER = 28
KEY_BACKSPACE = 14

KEY_MAX = 0x2ff

def EVIOCGKEY(length):
    return 2 << (14+8+8) | length << (8+8) | ord('E') << 8 | 0x18

# end of stuff from linux/input.h

BUF_LEN = (KEY_MAX + 7) / 8

def test_bit(bit, bytes):
    # bit in bytes is 1 when released and 0 when pressed
    return bool(bytes[bit / 8] & (1 << (bit % 8)))

def main(button):
    buf = array.array('B', [0] * BUF_LEN)
    with open('/dev/input/by-path/platform-gpio_keys-event', 'r') as fd:
        ret = fcntl.ioctl(fd, EVIOCGKEY(len(buf)), buf)

    if ret < 0:
        print "ioctl error", ret
        sys.exit(1)

    for key in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'ENTER', 'BACKSPACE']:
        key_code = globals()['KEY_' + key]
        key_state = test_bit(key_code, buf) and "pressed" or "released"
        print '%9s : %s' % (key, key_state)

if __name__ == "__main__":
    while True:
        main('up')
        sleep(1)
