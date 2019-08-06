#!/usr/bin/env python2

import os
import pyudev
from time import sleep

# --- EV3 CLASS ---

PYUDEV_CONTEXT = pyudev.Context()


class sensor:
	def __init__(self, address):
		sensors = PYUDEV_CONTEXT.list_devices(subsystem='lego-sensor', LEGO_ADDRESS='ev3-ports:in' + str(address))
		self.address = address
		try:
			self.isSensor = next(c for c in sensors)
			self.disconnectedMessage = False
		except: pass

		try:
			self.value_f = open(os.path.join(self.isSensor.sys_path, 'value0'), 'r')
			self.distance_f = open(os.path.join(self.isSensor.sys_path, 'units'), 'r')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Sensor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def mode(self, input):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write(input)
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def getValue(self):
		try:
			self.value_f.seek(0)
			return int(self.value_f.read())
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def colorReflect(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('COL-REFLECT')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def colorColor(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('COL-COLOR')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def touch(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('TOUCH')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def ultraIN(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('US-DIST-IN')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def ultraCM(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('US-DIST-CM')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def ultraDistance(self):
		try:
			return (self.getValue() / 10)
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)


class motor:
	def __init__(self, address):
		devices = PYUDEV_CONTEXT.list_devices(subsystem='tacho-motor', LEGO_ADDRESS='ev3-ports:out' + str(address))
		self.address = address
		self.posOffset = 0
		try: 
			self.device = next(d for d in devices)
			self.disconnectedMessage = False
		except StopIteration: pass

	def reset(self):
		try:
			with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
				file.write('reset')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def sendCommand(self, newMode):
		try:
			with open(os.path.join(self.device.sys_path, 'command'),'w') as file:
				file.write(str(newMode))
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def getPos(self):
		try:
			with open(os.path.join(self.device.sys_path, 'position'),'r') as file:
				file.seek(0)
				return int(file.read().replace("\n", "")) - self.posOffset
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	# self.dutySpeed.write(str(int(min(max(newDutySpeed, -100), 100))))
	def run(self, speed):
		try:
			with open(os.path.join(self.device.sys_path, 'duty_cycle_sp'), 'w') as file:
				file.write(str(int(min(max(speed, -100), 100))))
			with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
				file.write("run-direct")
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def braking(self, braking):
		try:
			if (braking == True):
				with open(os.path.join(self.device.sys_path, 'stop_action'), 'w') as file:
					file.write('hold')
				with open(os.path.join(self.device.sys_path, 'time_sp'), 'w') as file:
					file.write('0')
				with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
					file.write('run-timed')
			else:
				self.reset()
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def moveRel(self, distance, speed):
		try:
			with open(os.path.join(self.device.sys_path, 'speed_sp'), 'w') as file:
				file.write(str(speed))
			with open(os.path.join(self.device.sys_path, 'position_sp'), 'w') as file:
				file.write(str(distance))
			with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
				file.write('run-to-rel-pos')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def moveAbs(self, distance, speed):
		try:
			with open(os.path.join(self.device.sys_path, 'speed_sp'), 'w') as file:
				file.write(str(speed))
			with open(os.path.join(self.device.sys_path, 'position_sp'), 'w') as file:
				file.write(str(int(distance) - self.posOffset))
			with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
				file.write('run-to-abs-pos')
		except IOError:
			if (self.disconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.disconnectedMessage = True
			self.__init__(self.address)

	def resetPos(self):
		posOffset = self.getPos()

if __name__ == "__main__":
	print("A module for controlling motors and\nreading sensors for the LEGO EV3")