#!/usr/bin/env python2

import os
import pyudev

# --- EV3 CLASS ---

PYUDEV_CONTEXT = pyudev.Context()

class motorNotFound(Exception): pass

class motor:
	def __init__(self, address):
		devices = PYUDEV_CONTEXT.list_devices(subsystem='tacho-motor', LEGO_ADDRESS='ev3-ports:out' + str(address))
		try: self.device = next(d for d in devices)
		except StopIteration: raise motorNotFound(address)

		self.pos = open(os.path.join(self.device.sys_path, 'position'), 'r+')
		self.duty_cycle_sp = open(os.path.join(self.device.sys_path, 'duty_cycle_sp'), 'w', 0)
		self.duty_cycle = open(os.path.join(self.device.sys_path, 'duty_cycle'), 'r')
		self.max_speed = int(open(os.path.join(self.device.sys_path, 'max_speed'), 'r').read())
		self.reset()

	def reset(self):
		self.setPos(0)
		self.setSpeed(0)
		self.sendCommand('run-direct')

	def getPos(self):
		self.pos.seek(0)
		return int(self.pos.read())

	def setPos(self, new_pos):
		return self.pos.write(str(int(new_pos)))

	def getSpeed(self):
		self.duty_cycle.seek(0)
		return int(self.duty_cycle.read())

	def setSpeed(self, new_duty_cycle_sp):
		in_max = 100
		self.duty_cycle_sp.write(str(
			int(min(max(new_duty_cycle_sp, -in_max), in_max))
		))

	def stoppingAction(self, newMode):
		with open(os.path.join(self.device.sys_path, 'stop_action'), 'w') as mode:
			mode.write(str(newMode))

	def sendCommand(self, newMode):
		with open(os.path.join(self.device.sys_path, 'command'),
				'w') as command:
			command.write(str(newMode))

	def hold(self):
		self.stoppingAction('hold')
		self.sendCommand('run-to-rel-pos')

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


if __name__ == "__main__":
	Arm = motor('B')
	from time import sleep
	while True:
		Arm.hold()
		sleep(1)
		Arm.reset()
		sleep(1)
	print("A module for controlling motors and\nreading sensors for the LEGO EV3")

