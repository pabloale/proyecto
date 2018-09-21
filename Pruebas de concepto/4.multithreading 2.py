#!/usr/bin/python

import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BOARD)
import multiprocessing
from  multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=2)



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
    return prueba;
    
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
    return "puto";
                
if __name__=='__main__':
    async_result = pool.apply_async(firstLED, ())
    async_result_dos = pool.apply_async(secondLED, ())

    retorno = async_result.get()
    retorno_dos = async_result_dos.get()
    
    print(retorno)
    print(retorno_dos)
    print("All done")
    GPIO.cleanup()