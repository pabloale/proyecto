import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time

VIB = 21

#Seteo de modo de pines
GPIO.setup(VIB, GPIO.OUT)

while True:
    GPIO.output(VIB, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(VIB, GPIO.LOW)
    time.sleep(1)
    
GPIO.cleanup()