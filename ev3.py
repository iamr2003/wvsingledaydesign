#!/usr/bin/env python2

import os
import pyudev
from time import sleep

# --- EV3 CLASS ---

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
			return file.read().replace("\n", "")

	# self.dutySpeed.write(str(int(min(max(newDutySpeed, -100), 100))))
	def run(self, speed):
		with open(os.path.join(self.device.sys_path, 'duty_cycle_sp'), 'w') as file:
			file.write(str(int(min(max(speed, -100), 100))))
		with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
			file.write("run-direct")

	def breaking(self, breaking):
		if (breaking == True):
			with open(os.path.join(self.device.sys_path, 'stop_action'), 'w') as file:
				file.write('hold')
			with open(os.path.join(self.device.sys_path, 'time_sp'), 'w') as file:
				file.write('0')
			with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
				file.write('run-timed')
		else:
			self.reset()

	def moveRel(self, distance, speed):
		with open(os.path.join(self.device.sys_path, 'speed_sp'), 'w') as file:
			file.write(str(speed))
		with open(os.path.join(self.device.sys_path, 'position_sp'), 'w') as file:
			file.write(str(distance))
		with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
			file.write('run-to-rel-pos')

	def moveAbs(self, distance, speed):
		with open(os.path.join(self.device.sys_path, 'speed_sp'), 'w') as file:
			file.write(str(speed))
		with open(os.path.join(self.device.sys_path, 'position_sp'), 'w') as file:
			file.write(str(distance))
		with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
			file.write('run-to-abs-pos')


if __name__ == "__main__":
	print("A module for controlling motors and\nreading sensors for the LEGO EV3")