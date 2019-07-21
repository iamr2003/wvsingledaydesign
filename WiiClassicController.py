#!/usr/bin/env python2

# Drive your robot with a wii remote!
# Left motor on port B, right motor on port C,
# vertical arm on port D.
# Requires the package 'python-cwiid'.
# Make sure bluetooth is enabled in brickman
# before trying to use this. Hold 2 to go forward
# and 1 to go backward.

import os
import time

import cwiid
import pyudev

DEADZONE = 0.2

def clamp(value, lower, upper):
	return min(upper, max(value, lower))

def dead(value):
	return 0 if abs(value) < DEADZONE else value

class EV3Motor:
	def __init__(self, which=0):
		devices = list(pyudev.Context().list_devices(subsystem='tacho-motor') \
				.match_attribute('driver_name', 'lego-ev3-l-motor'))

		if which >= len(devices):
			raise Exception("Motor not found")

		self.device = devices[which]
		self.pos = open(os.path.join(self.device.sys_path, 'position'), 'r+',
				0)
		self.duty_cycle_sp = open(os.path.join(self.device.sys_path,
				'duty_cycle_sp'), 'w', 0)

		self.reset()

	def reset(self):
		self.set_pos(0)
		self.set_duty_cycle_sp(0)
		self.send_command("run-direct")
	def get_pos(self):
		self.pos.seek(0)
		return int(self.pos.read())

	def set_pos(self, new_pos):
		return self.pos.write(str(int(new_pos)))

	def set_duty_cycle_sp(self, new_duty_cycle_sp):
		return self.duty_cycle_sp.write(str(clamp(int(new_duty_cycle_sp), -100, 100)))

	def send_command(self, new_mode):
		with open(os.path.join(self.device.sys_path, 'command'),
				'w') as command:
			command.write(str(new_mode))


print 'Press 1+2 on the wiimote now'
time.sleep(1)
wm = cwiid.Wiimote()
print 'Connected!'
wm.led = 0b0011
wm.rpt_mode = cwiid.RPT_CLASSIC

b = EV3Motor(0)
c = EV3Motor(1)

reverse = 1 # -1 or 1
top_speed = 50
last_btn_state = 0
move = 0

try:
	while True:
		ls_x, ls_y = [dead(v / 32.0 - 1) for v in wm.state['classic']['l_stick']]
		rs_x, rs_y = [dead(v / 16.0 - 1) for v in wm.state['classic']['r_stick']]
		
		speed = ls_y * 100
		
		b.set_duty_cycle_sp(speed + rs_x * 50)
		c.set_duty_cycle_sp(speed - rs_x * 50)
finally:
	b.send_command('stop')
	c.send_command('stop')
