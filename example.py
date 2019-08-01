#!/usr/bin/env python2

import cwiid
import ev3
from time import sleep

def dead(value):
	return 0 if abs(value) < 0.2 else value

b = ev3.motor('B')
c = ev3.motor('C')

print('Press 1+2 on the wiimote now')
sleep(1)
wm = cwiid.Wiimote()
print('Connected!')
wm.led = 0b0011
wm.rpt_mode = cwiid.RPT_CLASSIC

while True:
	try:
		ls_x, ls_y = [dead(v / 32.0 - 1) for v in wm.state['classic']['l_stick']]
		rs_x, rs_y = [dead(v / 16.0 - 1) for v in wm.state['classic']['r_stick']]

		speed = ls_y * 100

		if (bool(wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_A) == True):
			pass
			b.setSpeed(-99)
			c.setSpeed(99)
		else:
			b.setSpeed(int(speed + rs_x * 50))
			c.setSpeed(int(speed - rs_x * 50))
	except:
		pass