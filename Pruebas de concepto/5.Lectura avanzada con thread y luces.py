#!/usr/bin/python

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time
import multiprocessing
from  multiprocessing.pool import ThreadPool
CANTIDAD_MUESTRAS = 5


def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    
    global CANTIDAD_MUESTRAS
    h = 0
    resultado = 0
    
    while (h < CANTIDAD_MUESTRAS):
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
            h = h+1
        
            adcout >>= 1
            resultado = resultado + adcout
            #print("actual: ", adcnum, adcout)
            #print("total: ", adcnum, resultado)
    
    return resultado / CANTIDAD_MUESTRAS



#Configuracion de threads
pool = ThreadPool(processes=2)
DEBUG = 1
#Configuracion de pines de la placa
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

#Seteo de modo de pines
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#Pines de lectura analogicos (MCP3008)
fsr_uno = 0;
fsr_dos = 7;

#configuracion de lectura
ultima_lectura = 0
tolerancia = 5
prueba = 1

#proceso principal
while True:
    lectura_cambio = False
    
    lectura_actual_uno_async = pool.apply_async(readadc, (fsr_uno, SPICLK, SPIMOSI, SPIMISO, SPICS))
    lectura_actual_dos_async = pool.apply_async(readadc, (fsr_dos, SPICLK, SPIMOSI, SPIMISO, SPICS))

    retorno_uno = lectura_actual_uno_async.get()
    retorno_dos = lectura_actual_dos_async.get()
    
    #print("sensor uno: ", retorno_uno)
    #print("sensor dos: ", retorno_dos)
    #print("Terminaron")
    
    LEDUNO = 4
    GPIO.setup(LEDUNO, GPIO.OUT)
    
    if (retorno_uno > 800):
        GPIO.output(LEDUNO, GPIO.HIGH)
        
    else: 
        GPIO.output(LEDUNO, GPIO.LOW)
    
    LEDDOS = 17
    GPIO.setup(LEDDOS, GPIO.OUT)
    
    if (retorno_dos > 800):
        GPIO.output(LEDDOS, GPIO.HIGH)
    else: 
        GPIO.output(LEDDOS, GPIO.LOW)
        
    
    #diferencia_lectura = abs(lectura_actual - ultima_lectura)
    
    #if DEBUG:
            #print("lectura_actual:", lectura_actual)
            #print("diferencia_lectura:", diferencia_lectura)
            #print("ultima_lectura:", ultima_lectura)
    
    #if ( diferencia_lectura > tolerancia ):
            #lectura_cambio = True
            
    #if DEBUG:
            #print("lectura_cambio", lectura_cambio)
            
    #ultima_lectura = lectura_actual;
    
    prueba += 1

GPIO.cleanup()
time.sleep(0.5)