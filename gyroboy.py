#!/usr/bin/env python2


# --- Library Imports ---

print('Importing joystick libraries')

import evdev
from evdev import ecodes
import threading

print('Importing other libraries')

import pyudev
import os
import time


# --- Joystick Reading Code ---

JOYSTICK = None
JOYSTICK_CAPS = {}
JOYSTICK_STATE = {}
JOYSTICK_DEFAULT_STATE = 0.0

class JoystickNotFound(Exception): pass

def map_range(in_min, in_max, out_min, out_max, value):
	return out_min + ((value - in_min) * (out_max - out_min) / (in_max - in_min))

def find_joystick(name):
	global JOYSTICK

	# Search for joystick
	devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
	try: JOYSTICK = next(d for d in devices if d.name == name)
	except StopIteration: raise JoystickNotFound(name)

	# Enumerate joystick axis capabilities
	for abs_id, abs_info in JOYSTICK.capabilities()[ecodes.EV_ABS]:
		JOYSTICK_CAPS[abs_id] = abs_info
		JOYSTICK_STATE[abs_id] = JOYSTICK_DEFAULT_STATE

def watch_joystick():
	for event in JOYSTICK.read_loop():

		# Ignore non axis inputs
		if event.type != ecodes.EV_ABS:
			continue

		# Update global joystick state
		caps = JOYSTICK_CAPS[event.code]
		JOYSTICK_STATE[event.code] = map_range(caps.min, caps.max, -1.0, 1.0, event.value)


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


class EV3GyroNotFound(Exception): pass

class EV3Gyro:
	EMAOFFSET = 0.0005

	def __init__(self, which=0):
		gyros = PYUDEV_CONTEXT.list_devices(subsystem='lego-sensor', LEGO_DRIVER_NAME='lego-ev3-gyro')
		try: self.gyro = list(gyros)[which]
		except IndexError: raise EV3GyroNotFound(which)

		with open(os.path.join(self.gyro.sys_path, 'mode'), 'w') as mode:
			mode.write('GYRO-RATE')

		self.value_f = open(os.path.join(self.gyro.sys_path, 'value0'), 'r')
		self.offset = 0

	def calibrate(self, duration=0.5, acceptable_variance=5):
		# Attempt calibration until stable
		while True:
			min_val = 1000
			max_val = -1000
			sum_val = 0
			readings = 0

			# Calculate motor statistics over the duration
			time_start = time.time()
			while (time.time() - time_start) < duration:
				value = self.get_raw_value()
				readings += 1
				sum_val += value
				max_val = max(value, max_val)
				min_val = min(value, min_val)

			# Check if variance is acceptable
			if (max_val - min_val) < acceptable_variance:
				break

		# Save average reading as the offset
		self.offset = sum_val / float(readings)

	def get_raw_value(self):
		self.value_f.seek(0)
		return int(self.value_f.read())

	def get_rate(self):
		raw_value = self.get_raw_value()
		self.offset = self.EMAOFFSET * raw_value + (1 - self.EMAOFFSET) * self.offset
		return raw_value - self.offset


# --- Global Variables ---

class LinkedMotors():
	def __init__(self, motor_left, motor_right):
		self.left = motor_left
		self.right = motor_right
	
	def getSum(self):
		pos_left = self.left.get_pos()
		pos_right = self.right.get_pos()

		return pos_left + pos_right


def balance(motors, gyro):
	START_TIME = time.time()
	time_now = time.time()
	time_top = time_now
	cLoop = 0
	ok = True
	cDrive = 0
	cSteering = 0

	motor_sum = 0
	motor_pos = 0

	gyro_angle = -0.25

	motor_deltas = [0]*4
	try:
		while ok:
			last_top = time_top
			time_top = time.time()
			tInt = time_top - last_top

			# Read gyros
			gyro_rate = gyro.get_rate()
			gyro_angle += gyro_rate * tInt

			# Read motors
			motor_sum_old = motor_sum
			motor_sum = motors.getSum()
			motor_delta = motor_sum - motor_sum_old

			motor_pos += motor_delta

			motor_deltas.append(motor_delta)
			motor_deltas.pop(0)
			motor_speed = sum(motor_deltas) / float(len(motor_deltas)) / tInt

			# Calculate drive factor
			cDrive = -JOYSTICK_STATE[ecodes.ABS_Y] * 250

			# Adjust for drive
			motor_pos = motor_pos - tInt * cDrive

			# Balancing equation
			power = (
				(-0.02 * cDrive) +                      # Lean when driving
				(0.8 * gyro_rate + 15 * gyro_angle) +   # Gyro factors
				(0.08 * motor_speed + 0.12 * motor_pos) # Motor factors
			)

			# Adjust for drive again?
			motor_pos = motor_pos - tInt * cDrive

			# if power > 100: power = 100
			# if power < -100: power = -100

			# Calculate steering factor
			cSteering = -JOYSTICK_STATE[ecodes.ABS_RX] * 15

			# Set motors
			motors.left.set_duty_cycle_sp(power + cSteering)
			motors.right.set_duty_cycle_sp(power - cSteering)

			# Detect if fallen
			if abs(power) < 100:
				time_ok = time_top
			if (time_top - time_ok) > 1.0:
				ok = False

			# Sleep until target loop timing
			time_now = time.time()
			time.sleep(max(0.01 - (time_now - time_top), 0))

# --- Entry Point ---

if __name__ == '__main__':

	motors = LinkedMotors(EV3Motor('ev3-ports:outB'), EV3Motor('ev3-ports:outC'))

	# 'Wireless Controller' for DS4
	find_joystick('8Bitdo SF30 Pro')
	joystick_thread = threading.Thread(target=watch_joystick)
	joystick_thread.daemon = True
	joystick_thread.start()

	print('Calibrating gyro')

	gyro = EV3Gyro()
	gyro.calibrate()

	print('Calibrated gyro')

	try:
		while True:
			balance(motors, gyro)
	finally:
		motors.left.send_command('stop')
		motors.right.send_command('stop')

