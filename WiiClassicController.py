#!/usr/bin/env python2

# Drive your robot with a wii remote!
# Left motor on port B, right motor on port C,
# vertical arm on port D.
# Requires the package 'python-cwiid'.
# Make sure bluetooth is enabled in brickman
# Its archade drive with the two joistics on the classic

import os
import time

import cwiid
import pyudev

DEADZONE = 0.2

def clamp(value, lower, upper):
	return min(upper, max(value, lower))

def dead(value):
	return 0 if abs(value) < DEADZONE else value

# --- EV3 Classes ---

PYUDEV_CONTEXT = pyudev.Context()

class EV3MotorNotFound(Exception): pass

class EV3Motor:
	def __init__(self, address):
		devices = PYUDEV_CONTEXT.list_devices(subsystem='tacho-motor', LEGO_ADDRESS=address)
		try: self.device = next(d for d in devices)
		except StopIteration: raise EV3MotorNotFound(address)

		self.pos = open(os.path.join(self.device.sys_path, 'position'), 'r+')
		self.duty_cycle_sp = open(os.path.join(self.device.sys_path, 'duty_cycle_sp'), 'w', 0)
		self.duty_cycle = open(os.path.join(self.device.sys_path, 'duty_cycle'), 'r')
		self.max_speed = int(open(os.path.join(self.device.sys_path, 'max_speed'), 'r').read())
		self.reset()

	def reset(self):
		self.set_pos(0)
		self.set_duty_cycle_sp(0)
		self.send_command('run-direct')

	def get_pos(self):
		self.pos.seek(0)
		return int(self.pos.read())

	def set_pos(self, new_pos):
		return self.pos.write(str(int(new_pos)))

	def get_duty_cycle(self):
		self.duty_cycle.seek(0)
		return int(self.duty_cycle.read())

	def set_duty_cycle_sp(self, new_duty_cycle_sp):
		in_max = 100
		self.duty_cycle_sp.write(str(
			int(min(max(new_duty_cycle_sp, -in_max), in_max))
		))

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

b = EV3Motor('ev3-ports:outB')
c = EV3Motor('ev3-ports:outC')

try:
	while True:
		ls_x, ls_y = [dead(v / 32.0 - 1) for v in wm.state['classic']['l_stick']]
		rs_x, rs_y = [dead(v / 16.0 - 1) for v in wm.state['classic']['r_stick']]
		
		speed = ls_y * 100
		
		if (bool(classic['buttons'] & cwiid.CLASSIC_BTN_A) == True):
			b.set_duty_cycle_sp(99)
			c.set_duty_cycle_sp(99)
		else:
			b.set_duty_cycle_sp(speed + rs_x * 50)
			c.set_duty_cycle_sp(speed - rs_x * 50)
finally:
	b.send_command('stop')
	c.send_command('stop')