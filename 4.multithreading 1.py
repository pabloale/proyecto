#!/usr/bin/python

import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BOARD)
import threading
from threading import Thread 



def firstLED():
        i = 0
        blinks = 10
        prueba = 'hola'
        while (i < blinks):
                LEDUNO = 7
                GPIO.setup(LEDUNO, GPIO.OUT)
                GPIO.output(LEDUNO, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(LEDUNO, GPIO.LOW)
                time.sleep(0.2)
                print("Lo que sea")
                i = i+1
        return (prueba);
    
def secondLED():
        i = 0
        blinks = 5
        while (i < blinks):
                LEDDOS = 11
                GPIO.setup(LEDDOS, GPIO.OUT)
                GPIO.output(LEDDOS, GPIO.HIGH)
                time.sleep(0.4)
                GPIO.output(LEDDOS, GPIO.LOW)
                time.sleep(0.4)
                
                i = i+1
                print("HOLADOS")
        return;
                
if __name__=='__main__':
            first_thread = Thread(target = firstLED)
            second_thread = Thread(target = secondLED)
            first_thread.start()
            second_thread.start()
            
            first_thread.join()
            second_thread.join()
            print(pruebadevuelta)
            print("All done")
            GPIO.cleanup()
