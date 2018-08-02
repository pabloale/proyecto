#!/usr/bin/python

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time

import multiprocessing
from  multiprocessing.pool import ThreadPool
CANTIDAD_MUESTRAS = 10


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


def asd(adcnum, clockpin, mosipin, misopin, cspin):
    
    GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
    GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
    GPIO.output(LED_ROJO_IZQUIERDO, GPIO.LOW)
    GPIO.output(LED_ROJO_DERECHO, GPIO.LOW)
    GPIO.output(VIBRADOR, GPIO.LOW)
    
    return


#Configuracion de threads
pool = ThreadPool(processes=4)
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
fsr_inferior_izquierdo = 0;
fsr_inferior_derecho = 2;
fsr_superior_derecho = 4;
fsr_superior_izquierdo = 7;


#configuracion de lectura
ultima_lectura = 0
tolerancia = 5

#proceso principal
while True:
    lectura_cambio = False
    
    lectura_actual_inferior_izquierdo = pool.apply_async(readadc, (fsr_inferior_izquierdo, SPICLK, SPIMOSI, SPIMISO, SPICS))
    lectura_actual_superior_izquierdo = pool.apply_async(readadc, (fsr_superior_izquierdo, SPICLK, SPIMOSI, SPIMISO, SPICS))
    lectura_actual_inferior_derecho = pool.apply_async(readadc, (fsr_inferior_derecho, SPICLK, SPIMOSI, SPIMISO, SPICS))
    lectura_actual_superior_derecho = pool.apply_async(readadc, (fsr_superior_derecho, SPICLK, SPIMOSI, SPIMISO, SPICS))
    
    retorno_inferior_izquierdo = lectura_actual_inferior_izquierdo.get()
    retorno_superior_izquierdo = lectura_actual_superior_izquierdo.get()
    retorno_inferior_derecho = lectura_actual_inferior_derecho.get()
    retorno_superior_derecho = lectura_actual_superior_derecho.get()
    
    print("sensor INF IZQ: ", retorno_inferior_izquierdo, " Sensor SUP IZQ: ", retorno_superior_izquierdo, " Sensor INF DER: ", retorno_inferior_derecho, " Sensor SUP DER: ", retorno_superior_derecho)
    #print("sensor sizq: ", retorno_superior_izquierdo)
    #print("sensor ider: ", retorno_inferior_derecho)
    #print("sensor sder: ", retorno_superior_derecho)
    #print("Terminaron")
    
    LED_VERDE_IZQUIERDO = 5
    LED_ROJO_IZQUIERDO = 6
    LED_VERDE_DERECHO = 13
    LED_ROJO_DERECHO = 19
    VIBRADOR = 21
    UMBRAL_LECTURA_INFERIOR = 200
    UMBRAL_LECTURA_POSTERIOR = 400
    
    GPIO.setup(LED_VERDE_DERECHO, GPIO.OUT)
    GPIO.setup(LED_ROJO_DERECHO, GPIO.OUT)
    GPIO.setup(LED_VERDE_IZQUIERDO, GPIO.OUT)
    GPIO.setup(LED_ROJO_IZQUIERDO, GPIO.OUT)
    GPIO.setup(VIBRADOR, GPIO.OUT)
    
    lado_izquierdo = retorno_inferior_izquierdo + retorno_superior_izquierdo
    lado_derecho = retorno_inferior_derecho + retorno_superior_derecho
    
    GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
    GPIO.output(LED_ROJO_IZQUIERDO, GPIO.LOW)
    GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
    GPIO.output(LED_ROJO_DERECHO, GPIO.LOW)
    GPIO.output(VIBRADOR, GPIO.LOW)
    
    #No hay nadie sentado
    if (retorno_superior_izquierdo < UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo < UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho < UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho < UMBRAL_LECTURA_POSTERIOR):
        GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
        GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
        GPIO.output(LED_ROJO_IZQUIERDO, GPIO.LOW)
        GPIO.output(LED_ROJO_DERECHO, GPIO.LOW)
        GPIO.output(VIBRADOR, GPIO.LOW)
    else: #Hay alguien sentado (algun sensor se activo)
        #Solo el sensor de SUPERIOR IZQUIERDO se activó
        if (retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo < UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho < UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho < UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Solo el sensor de INFERIOR IZQUIERDO se activó
        elif (retorno_superior_izquierdo < UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho < UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho < UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Solo el sensor de SUPERIOR DERECHO se activó
        elif (retorno_superior_izquierdo < UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo < UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho < UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Solo el sensor de INFERIOR DERECHO se activó
        elif (retorno_superior_izquierdo < UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo < UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho < UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #2 sensores activos
        #Activados sensores SUPERIOR IZQ e INFERIOR IZQ
        elif (retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho < UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho < UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Activados sensores INFERIOR IZQ y SUPERIOR DER
        elif (retorno_superior_izquierdo < UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho < UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Activados sensores INFERIOR DER Y SUPERIOR DER
        elif (retorno_superior_izquierdo < UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo < UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.HIGH)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.LOW)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Activados sensores SUPERIOR IZQ y SUPERIOR DER
        elif (retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo < UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho < UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Activados sensores SUPERIOR IZQ e INFERIOR DER
        elif (retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo < UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho < UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Activados sensores INFERIOR IZQ e INFERIOR DER
        elif (retorno_superior_izquierdo < UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho < UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #3 sensores activos
        #Activados sensores SUPERIOR e INFERIOR IZQ y SUPERIOR DER
        elif (retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho < UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Activados sensores SUPERIOR e INFERIOR IZQ y INFERIOR DER
        elif (retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho < UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_VERDE_DERECHO, GPIO.LOW)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_ROJO_DERECHO, GPIO.HIGH)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Activados sensores SUPERIOR IZQ e INFERIOR Y SUPERIOR DER
        elif (retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo < UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.HIGH)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.LOW)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #Activados sensores INFERIOR IZQ e INFERIOR Y SUPERIOR DER
        elif (retorno_superior_izquierdo < UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_VERDE_DERECHO, GPIO.HIGH)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_ROJO_DERECHO, GPIO.LOW)
            GPIO.output(VIBRADOR, GPIO.HIGH)
        #4 sensores activos
        #Activados sensores SUPERIOR e INFERIOR IZQ e INFERIOR Y SUPERIOR DER
        elif (retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR and retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR and retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR and retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR):
            GPIO.output(LED_VERDE_IZQUIERDO, GPIO.HIGH)
            GPIO.output(LED_VERDE_DERECHO, GPIO.HIGH)
            GPIO.output(LED_ROJO_IZQUIERDO, GPIO.LOW)
            GPIO.output(LED_ROJO_DERECHO, GPIO.LOW)
        
        
        
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

GPIO.cleanup()
time.sleep(0.5)

