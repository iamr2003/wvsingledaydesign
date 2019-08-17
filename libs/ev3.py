#!/usr/bin/env python2

import os
import pyudev
from time import sleep
import array
import fcntl
import sys

# --- EV3 CLASS ---
PYUDEV_CONTEXT = pyudev.Context()

class sensor:
	def __init__(self, address):
		self.sensorDisconnectedMessage = False
		self.address = address
		self.connect(address)

	def connect(self, address):
		sensors = PYUDEV_CONTEXT.list_devices(subsystem='lego-sensor', LEGO_ADDRESS='ev3-ports:in' + str(address))
		try:
			self.isSensor = next(c for c in sensors)
			self.sensorDisconnectedMessage = False
		except: pass

		try:
			self.value_f = open(os.path.join(self.isSensor.sys_path, 'value0'), 'r')
			self.distance_f = open(os.path.join(self.isSensor.sys_path, 'units'), 'r')
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Sensor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)

	def mode(self, input):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write(input)
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)

	def getValue(self):
		try:
			self.value_f.seek(0)
			return int(self.value_f.read())
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)

	def colorReflect(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('COL-REFLECT')
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)

	def colorColor(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('COL-COLOR')
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)

	def touch(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('TOUCH')
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)

	def ultraIN(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('US-DIST-IN')
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)

	def ultraCM(self):
		try:
			with open(os.path.join(self.isSensor.sys_path, 'mode'), 'w') as mode:
				mode.write('US-DIST-CM')
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)

	def ultraDistance(self):
		try:
			return (self.getValue() / 10)
		except:
			if (self.sensorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.sensorDisconnectedMessage = True
			self.connect(self.address)


class motor:
	def __init__(self, address):
		self.motorDisconnectedMessage = False
		self.address = address
		self.connect(address)

	def connect(self, port):
		devices = PYUDEV_CONTEXT.list_devices(subsystem='tacho-motor', LEGO_ADDRESS='ev3-ports:out' + str(port))
		self.posOffset = 0
		try: 
			self.device = next(d for d in devices)
			self.motorDisconnectedMessage = False
		except StopIteration: 
			if (self.motorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.motorDisconnectedMessage = True
			self.connect(self.address)

	def reset(self):
		try:
			with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
				file.write('reset')
		except:
			if (self.motorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.motorDisconnectedMessage = True
			self.connect(self.address)

	def sendCommand(self, newMode):
		try:
			with open(os.path.join(self.device.sys_path, 'command'),'w') as file:
				file.write(str(newMode))
		except:
			if (self.motorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.motorDisconnectedMessage = True
			self.connect(self.address)

	def getPos(self):
		try:
			with open(os.path.join(self.device.sys_path, 'position'),'r') as file:
				file.seek(0)
				return int(file.read().replace("\n", "")) - self.posOffset
		except:
			if (self.motorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.motorDisconnectedMessage = True
			self.connect(self.address)

	# self.dutySpeed.write(str(int(min(max(newDutySpeed, -100), 100))))
	def run(self, speed):
		try:
			with open(os.path.join(self.device.sys_path, 'duty_cycle_sp'), 'w') as file:
				file.write(str(int(min(max(speed, -100), 100))))
			with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
				file.write("run-direct")
		except:
			if (self.motorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.motorDisconnectedMessage = True
			self.connect(self.address)

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
		except:
			if (self.motorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.motorDisconnectedMessage = True
			self.connect(self.address)

	def moveRel(self, distance, speed):
		# try:
		with open(os.path.join(self.device.sys_path, 'speed_sp'), 'w') as file:
			file.write(str(int(speed)))
		with open(os.path.join(self.device.sys_path, 'position_sp'), 'w') as file:
			file.write(str(distance))
		with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
			file.write('run-to-rel-pos')
		# except:
		# 	if (self.motorDisconnectedMessage == False):
		# 		print("Motor " + str(self.address) + " disconnected!")
		# 		self.motorDisconnectedMessage = True
		# 	self.connect(self.address)

	def moveAbs(self, distance, speed):
		try:
			with open(os.path.join(self.device.sys_path, 'speed_sp'), 'w') as file:
				file.write(str(speed))
			with open(os.path.join(self.device.sys_path, 'position_sp'), 'w') as file:
				file.write(str(int(distance) - self.posOffset))
			with open(os.path.join(self.device.sys_path, 'command'), 'w') as file:
				file.write('run-to-abs-pos')
		except:
			if (self.motorDisconnectedMessage == False):
				print("Motor " + str(self.address) + " disconnected!")
				self.motorDisconnectedMessage = True
			self.connect(self.address)

class buttons:
	def __init__(self):
		self.BUF_LEN = (0x2ff + 7) / 8
		self.buf = array.array('B', [0] * self.BUF_LEN)

		with open('/dev/input/by-path/platform-gpio_keys-event', 'r') as fd:
			self.ret = fcntl.ioctl(fd, self.EVIOCGKEY(len(self.buf)), self.buf)
	
	def EVIOCGKEY(self, length):
		return 2 << (14+8+8) | length << (8+8) | ord('E') << 8 | 0x18

	def test_bit(self, bit, bytes):
		return bool(bytes[bit / 8] & (1 << (bit % 8)))

	def getCode(self, button):
		if (button == 'center'):
			return 28
		elif (button == 'left'):
			return 105
		elif(button == 'right'):
			return 106
		elif(button == 'up'):
			return 103
		elif(button == 'down'):
			return 108
		elif(button == 'back'):
			return 14

	def getButton(self, buttonCode):
		if self.ret < 0:
			print "ioctl error", self.ret
			sys.exit(1)

		key_state = self.test_bit(buttonCode, self.buf)
		print key_state

class led:
	def __init__(self, led):
		if (led == 'left'):
			self.path = '/sys/class/leds/led0:'
		elif (led == 'right'):
			self.path = '/sys/class/leds/led1:'
		else:
			print("That isn't a led")
			sys.exit()

	def setColor(self, red = 0, green = 0):
		with open(self.path + 'green:brick-status/brightness', 'w') as greenFile:
			greenFile.write(str(green))
		with open(self.path + 'red:brick-status/brightness', 'w') as redFile:
			redFile.write(str(red))

	def reset(self):
		self.setColor(0, 0)
		

if __name__ == "__main__":
	print("A module for controlling motors and\nreading sensors for the LEGO EV3")