#!/usr/bin/env python2

import os
import pyudev

# Todo add stop_action commands for holding a motor

# --- EV3 Classes ---

PYUDEV_CONTEXT = pyudev.Context()

class MotorNotFound(Exception): pass

class Motor:
	def __init__(self, address):
		devices = PYUDEV_CONTEXT.list_devices(subsystem='tacho-motor', LEGO_ADDRESS=address)
		try: self.device = next(d for d in devices)
		except StopIteration: raise MotorNotFound(address)

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

class ColorNotFound(Exception): pass

class Color:
	def __init__(self, address):
		colors = PYUDEV_CONTEXT.list_devices(subsystem='lego-sensor', LEGO_ADDRESS=address)
		try: self.color = next(c for c in colors)
		except IndexError: raise ColorNotFound(address)

		with open(os.path.join(self.color.sys_path, 'mode'), 'w') as mode:
			mode.write('COL-REFLECT')
		self.value_f = open(os.path.join(self.color.sys_path, 'value0'), 'r')

	def get_raw_value(self):
		self.value_f.seek(0)
		return int(self.value_f.read())