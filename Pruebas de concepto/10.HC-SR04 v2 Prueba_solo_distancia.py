import RPi.GPIO as GPIO
import time
import signal
import sys

# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
pinTrigger = 4
pinEcho = 3
ledrojo = 20
ledverde = 21

def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup() 
	sys.exit(0)

signal.signal(signal.SIGINT, close)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)
GPIO.setup(ledrojo, GPIO.OUT)
GPIO.setup(ledverde, GPIO.OUT)

while True:
	
	# set Trigger to HIGH
	GPIO.output(pinTrigger, True)
	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(pinTrigger, False)

	startTime = time.time()
	stopTime = time.time()

	# save start time
	cont = 0
	while cont < 50 and 0 == GPIO.input(pinEcho):
		startTime = time.time()
		cont = cont+1
##		print(cont)

	# save time of arrival

	while cont < 50 and 1 == GPIO.input(pinEcho):
		stopTime = time.time()
		cont = cont+1

	# time difference between start and arrival
	TimeElapsed = stopTime - startTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2
	
	if (distance <= 20):
            GPIO.output(ledrojo, False)
            GPIO.output(ledverde, True)
	else:
            GPIO.output(ledverde, False)
            GPIO.output(ledrojo, True)
            
	#print ("Distance: %.1f cm" % distance)
	time.sleep(0.05)
	