#!/usr/bin/python
import os
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
#GPIO.setwarnings(false)
GPIO.setup(26,GPIO.IN)

print ("")

while True:
    print ("aqsd")
    #os.system('date')
    print (GPIO.input(26))
    time.sleep(1)
    print ("holis")

#GPIO.output(26,GPIO.LOW)