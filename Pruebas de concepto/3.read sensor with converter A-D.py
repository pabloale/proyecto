#!/usr/bin/env python

import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
DEBUG = 1

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
            return -1
    GPIO.output(cspin, True)
    
    GPIO.output(clockpin, False) #start clock low
    GPIO.output(cspin, False) #bring CS low
    
    commandout = adcnum
    commandout |= 0x18 #start bit + single-ended bit
    commandout <<= 3
    for i in range(5):
            if (commandout & 0x80):
                GPIO.output(mosipin, True)
            else:
                GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
                
    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1
            
    GPIO.output(cspin, True)
    
    adcout >>= 1
    return adcout

SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

potentiometer_adc = 7;

last_read = 0
tolerance = 5

while True:
    trim_pot_changed = False
    
    trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
    
    pot_adjust = abs(trim_pot - last_read)
    
    if DEBUG:
            print("trim_pot:", trim_pot)
            print("pot_adjust:", pot_adjust)
            print("last_read:", last_read)
    
    if ( pot_adjust > tolerance ):
            trim_pot_changed = True
            
    if DEBUG:
            print("trim_pot_changed", trim_pot_changed)
            
    last_read = trim_pot;

time.sleep(0.5)
