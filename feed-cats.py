#!/usr/bin/python
"""
Filename	: feed-cats.py
Author		: Jeff R Hengesbach
Written		: FeB 2020

Description:
This script runs the cat feeder for the specified number of  seconds. 
To prevent clogs/jamming every 2 seconds a short reverse direction is done.

Usage: feed-cats.py num-seconds

Motor: 35 RPM: https://smile.amazon.com/gp/product/B01MQNHXON
	Note: You want a slower/powerful motor, not a fast-low torque motor
	I'm very pleased with the 35 RPM listed here
Motor Hat: https://smile.amazon.com/gp/product/B0721MTJ3P
	Note: Not the lowest cost motor hat, but it does not consume GPIOs
	like the cheaper cost units.  I've used this one in multiple projects
	and am very pleased.  You will need a seperate 12v Power supply for it.

Using AdaFruits MotorHat v0.1 Page/Code
https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/overview

Updates

"""
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

import time
import atexit
import RPi.GPIO as GPIO
import signal
import sys

###########################################
# Define our GPOIs and Such Here
###########################################

#Motor Controller Hat
Motor_hat = Raspi_MotorHAT(addr=0x6f)
Cat_Feeder = Motor_hat.getMotor(2)

def setup():
	#GPIO According to PIN
	GPIO.setmode(GPIO.BOARD)
	#Set Motor Speed
	Cat_Feeder.setSpeed(255)  #0 - 255

def main():
	runTime=int(sys.argv[1])
	counter=1

	print ("Feeding the Cats!")
		
	#Start off with short Anti-Clog counter rotation
	Cat_Feeder.run(Raspi_MotorHAT.BACKWARD)
	time.sleep(0.2)
	Cat_Feeder.run(Raspi_MotorHAT.FORWARD)

	while counter <= runTime:
		time.sleep(1)

		#Anti-Clog short counter rotation
		if counter % 2 == 0:
			Cat_Feeder.run(Raspi_MotorHAT.BACKWARD)
			time.sleep(0.2)
			Cat_Feeder.run(Raspi_MotorHAT.FORWARD)
		counter += 1
			

	Cat_Feeder.run(Raspi_MotorHAT.RELEASE) #Motor Stop

def destroy():
  #Stop the Motor
	Cat_Feeder.run(Raspi_MotorHAT.RELEASE)
	#Proper GPIO cleanup
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	main()
