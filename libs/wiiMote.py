#!/usr/bin/env python2

import cwiid
from time import sleep


class wiiMote:
	def __init__(self):
		print('Press 1+2 on the wiimote now')
		sleep(1)
		self.wm = cwiid.Wiimote()
		print('Connected!')
		self.wm.led = 0b0011
		self.wm.rpt_mode = cwiid.RPT_BTN

	def disconnect(self):
		self.wm.close()

	def setRumble(self, set):
		self.wm.rumble = bool(set)

	def getRumble(self):
		return self.wm.state['rumble']

	def getState(self):
		try:
			return self.wm.state
		except KeyError:
			print("Controller disconnected!")

	def setLed(self, number):
		self.wm.led = int(number)

	def getLed(self):
		return self.wm.state['led']

	def getBattery(self):
		return self.wm.state['battery']

	def dead(self, value):
		return 0 if abs(value) < 0.2 else value

	def setClassic(self):
		self.wm.rpt_mode = cwiid.RPT_CLASSIC

	def setNunchuk(self):
		self.wm.rpt_mode = cwiid.RPT_NUNCHUK

	def setAccelerometer(self):
		self.wm.rpt_mode = cwiid.RPT_ACC

	def setMote(self):
		self.wm.rpt_mode = cwiid.RPT_BTN

	def setMode(self, newMode):
		self.wm.rpt_mode = newMode

	def getAccelerometer(self, axis):
		if (axis == "tilt"):
			return self.getState()['acc'][0]
		elif (axis == "role"):
			return self.getState()['acc'][1]
		elif (axis == "height"):
			return self.getState()['acc'][2]
		else:
			print("Thats not an axis")
			return None

	def getClassicJoistics(self):
		try:
			self.ls_x, self.ls_y = [self.dead(v / 32.0 - 1) for v in self.wm.state['classic']['l_stick']]
			self.rs_x, self.rs_y = [self.dead(v / 16.0 - 1) for v in self.wm.state['classic']['r_stick']]
			# return self.ls_y
			return {'leftY': self.ls_y, 'leftX': self.ls_x, 'rightY': self.rs_y, 'rightX': self.rs_x}
		except KeyError:
			print("Classic Controller disconnected!")	

	def getNunchukJoistic(self):
		try:
			valueX, valueY = [self.dead(v / 132.0 - 1) for v in self.wm.state['nunchuk']['stick']]
			return {"X": valueX, "Y": valueY}
		except KeyError:
			print("Classic Controller disconnected!")

	def getMoteButton(self, button):
		try:
			if (button == "A"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_A)
			elif (button == "B"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_B)
			elif (button == "1"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_1)
			elif (button == "2"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_2)
			elif (button == "UP"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_UP)
			elif (button == "DOWN"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_DOWN)
			elif (button == "LEFT"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_LEFT)
			elif (button == "RIGHT"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_RIGHT)
			elif (button == "PLUS"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_PLUS)
			elif (button == "MINUS"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_MINUS)
			elif (button == "HOME"):
				return bool(self.wm.state['buttons'] & cwiid.BTN_HOME)
			else:
				print("That's not a button!")
				return None
		except KeyError:
			print("Classic Controller disconnected!")

	def getClassicButton(self, button):
		try:
			if (button == "A"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_A)
			elif (button == "B"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_B)
			elif (button == "X"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_X)
			elif (button == "Y"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_Y)
			elif (button == "UP"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_UP)
			elif (button == "DOWN"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_DOWN)
			elif (button == "LEFT"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_LEFT)
			elif (button == "RIGHT"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_RIGHT)
			elif (button == "PLUS"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_PLUS)
			elif (button == "MINUS"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_MINUS)
			elif (button == "L"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_L)
			elif (button == "R"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_R)
			elif (button == "ZL"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_ZL)
			elif (button == "ZR"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_ZR)
			elif (button == "HOME"):
				return bool(self.wm.state['classic']['buttons'] & cwiid.CLASSIC_BTN_HOME)
			else:
				print("That's not a button!")
				return None
		except KeyError:
			print("Classic Controller disconnected!")


	def getNunchukButton(self, button):
		try:
			if (button == "C"):
				return bool(self.wm.state['nunchuk']['buttons'] & cwiid.NUNCHUK_BTN_C)
			elif (button == "Z"):
				return bool(self.wm.state['nunchuk']['buttons'] & cwiid.NUNCHUK_BTN_Z)
			else:
				print("That's not a button!")
				return None
		except KeyError:
			print("Classic Controller disconnected!")

if __name__ == "__main__":
	mote = wiiMote()
	mote.setRumble
	try:
		while True:
			mote.setRumble(True)
			sleep(2)
			mote.setRumble(False)
			sleep(2)
	finally:
		mote.disconnect()