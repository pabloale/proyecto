#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import multiprocessing
from multiprocessing.pool import ThreadPool

from Functions import moduloBluetooth, readFuerzaResist, readDistance, activarActuadores, lecturas_distancia, lecturas_sensores

#Configuracion de pines de la placa
SPICLK = 11 #BCM GPIO 11 // BOARD PIN 23
SPIMISO = 9 #BCM GPIO 09 // BOARD PIN 21
SPIMOSI = 10 #BCM GPIO 10 // BOARD PIN 19
SPICS = 8 #BCM GPIO 08 // BOARD PIN 24

#Pines de lectura analogicos (MCP3008)
SENSOR_FUERZA_SUPERIOR_DERECHO = 0; #CH0 // PIN 1
SENSOR_FUERZA_INFERIOR_DERECHO = 1; #CH1 // PIN 2
SENSOR_FUERZA_INFERIOR_IZQUIERDO = 6; #CH6 // PIN 7
SENSOR_FUERZA_SUPERIOR_IZQUIERDO = 7; #CH7 // PIN 8

#Pines sensor de distancia
DISTANCE_PIN_TRIGGER_ABAJO = 4 #BCM GPIO 04 // BOARD PI0N 07
DISTANCE_PIN_ECHO_ABAJO = 3 #BCM GPIO 03 // BOARD PIN 05

DISTANCE_PIN_TRIGGER_ARRIBA = 17 #BCM GPIO 17 // BOARD PIN 11
DISTANCE_PIN_ECHO_ARRIBA = 27 #BCM GPIO 27 // BOARD PIN 13

#Pines de los actuadores
LED_VERDE_IZQUIERDO = 19 #BCM GPIO 19 // BOARD PIN 35
LED_ROJO_IZQUIERDO = 26 #BCM GPIO 26 // BOARD PIN 37
LED_VERDE_DERECHO = 16 #BCM GPIO 16 // BOARD PIN 36
LED_ROJO_DERECHO = 20 #BCM GPIO 20 // BOARD PIN 38
VIBRADOR = 21 #BCM GPIO 21 // BOARD PIN 40

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Seteo de modo de pines
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

GPIO.setup(LED_VERDE_DERECHO, GPIO.OUT)
GPIO.setup(LED_ROJO_DERECHO, GPIO.OUT)
GPIO.setup(LED_VERDE_IZQUIERDO, GPIO.OUT)
GPIO.setup(LED_ROJO_IZQUIERDO, GPIO.OUT)
GPIO.setup(VIBRADOR, GPIO.OUT)

#Umbrales de lectura de los sensores
UMBRAL_LECTURA_INFERIOR = 200
UMBRAL_LECTURA_POSTERIOR = 400
UMBRAL_LECTURA_ABAJO = 10
UMBRAL_LECTURA_ARRIBA = 10
TOPE_LECTURA_ABAJO = 40
TOPE_LECTURA_ARRIBA = 50

#configuracion de lectura
ultima_lectura = 0
tolerancia = 5

#Configuracion de threads
pool = ThreadPool(processes=6)
DEBUG = 1

pool.apply_async(moduloBluetooth)

#proceso principal
while True:
    lectura_cambio = False
    
    lectura_actual_inferior_izquierdo = pool.apply_async(readFuerzaResist, (SENSOR_FUERZA_INFERIOR_IZQUIERDO, SPICLK, SPIMOSI, SPIMISO, SPICS, 0))
    lectura_actual_superior_izquierdo = pool.apply_async(readFuerzaResist, (SENSOR_FUERZA_SUPERIOR_IZQUIERDO, SPICLK, SPIMOSI, SPIMISO, SPICS, 1))
    lectura_actual_inferior_derecho = pool.apply_async(readFuerzaResist, (SENSOR_FUERZA_INFERIOR_DERECHO, SPICLK, SPIMOSI, SPIMISO, SPICS, 2))
    lectura_actual_superior_derecho = pool.apply_async(readFuerzaResist, (SENSOR_FUERZA_SUPERIOR_DERECHO, SPICLK, SPIMOSI, SPIMISO, SPICS, 3))
    
    #lectura_distancia_abajo_async = pool.apply_async(readDistance, (DISTANCE_PIN_TRIGGER_ABAJO, DISTANCE_PIN_ECHO_ABAJO, TOPE_LECTURA_ABAJO, 0))
    #lectura_distancia_arriba_async = pool.apply_async(readDistance, (DISTANCE_PIN_TRIGGER_ARRIBA, DISTANCE_PIN_ECHO_ARRIBA, TOPE_LECTURA_ARRIBA, 1))
    
    # retorno_inferior_izquierdo = lectura_actual_inferior_izquierdo.get()
    # retorno_superior_izquierdo = lectura_actual_superior_izquierdo.get()
    # retorno_inferior_derecho = lectura_actual_inferior_derecho.get()
    # retorno_superior_derecho = lectura_actual_superior_derecho.get()
    retorno_inferior_izquierdo = lecturas_sensores[0]
    retorno_superior_izquierdo = lecturas_sensores[1]
    retorno_inferior_derecho = lecturas_sensores[2]
    retorno_superior_derecho = lecturas_sensores[3]
    
    #retorno_distancia_abajo = lectura_distancia_abajo_async.get()
    #retorno_distancia_arriba = lectura_distancia_arriba_async.get()
    retorno_distancia_abajo = lecturas_distancia[0]
    retorno_distancia_arriba = lecturas_distancia[1]
    
    #print("sensor INF IZQ: ", retorno_inferior_izquierdo, " \tSensor SUP IZQ: ", retorno_superior_izquierdo, " \tSensor INF DER: ", retorno_inferior_derecho, " \tSensor SUP DER: ", retorno_superior_derecho)
    #print("sensor iizq: ", retorno_inferior_izquierdo)
    #print("sensor sizq: ", retorno_superior_izquierdo)
    #print("sensor ider: ", retorno_inferior_derecho)
    #print("sensor sder: ", retorno_superior_derecho)
    #print("Terminaron")
    #print("distancia abajo: ", retorno_distancia_abajo)
    #print("distancia arriba: ", retorno_distancia_arriba)
    
    lado_izquierdo = retorno_inferior_izquierdo + retorno_superior_izquierdo
    lado_derecho = retorno_inferior_derecho + retorno_superior_derecho
    
    #LED_VERDE_IZQUIERDO - LED_VERDE_DERECHO - LED_ROJO_IZQUIERDO - LED_ROJO_DERECHO - VIBRADOR
    activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW)
    
    superior_izquierdo_activo = retorno_superior_izquierdo > UMBRAL_LECTURA_POSTERIOR
    inferior_izquierdo_activo = retorno_inferior_izquierdo > UMBRAL_LECTURA_INFERIOR
    inferior_derecho_activo = retorno_inferior_derecho > UMBRAL_LECTURA_INFERIOR
    superior_derecho_activo = retorno_superior_derecho > UMBRAL_LECTURA_POSTERIOR
    
    distancia_abajo_lejos = retorno_distancia_abajo > UMBRAL_LECTURA_ABAJO
    distancia_arriba_lejos = retorno_distancia_arriba > UMBRAL_LECTURA_ARRIBA
    
    #No hay nadie sentado
    if (not superior_izquierdo_activo and not inferior_izquierdo_activo and not inferior_derecho_activo and not superior_derecho_activo):
        activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW)
    #Hay alguien sentado
    #Controlo la distancia de la espalda y cabeza, si se activaron esta mal sentado
    elif (distancia_abajo_lejos or distancia_arriba_lejos):
        activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
    #4 sensores de presion activos, está bien sentado: Activados sensores SUPERIOR e INFERIOR IZQ e INFERIOR Y SUPERIOR DER
    elif (superior_izquierdo_activo and inferior_izquierdo_activo and inferior_derecho_activo and superior_derecho_activo):
        activarActuadores(GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW)
    #algun sensor no esta activado, no está bien sentado
    else:
        activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)

            # #1 sensor activado
            # #Solo el sensor de SUPERIOR IZQUIERDO se activó
            # elif (superior_izquierdo_activo and not inferior_izquierdo_activo and not inferior_derecho_activo and not superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
            # #Solo el sensor de INFERIOR IZQUIERDO se activó
            # elif (not superior_izquierdo_activo and inferior_izquierdo_activo and not inferior_derecho_activo and not superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
            # #Solo el sensor de SUPERIOR DERECHO se activó
            # elif (not superior_izquierdo_activo and not inferior_izquierdo_activo and not inferior_derecho_activo and superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
            # #Solo el sensor de INFERIOR DERECHO se activó
            # elif (not superior_izquierdo_activo and not inferior_izquierdo_activo and inferior_derecho_activo and not superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)

            # #2 sensores activos
            # #Activados sensores SUPERIOR IZQ e INFERIOR IZQ
            # elif (superior_izquierdo_activo and inferior_izquierdo_activo and not inferior_derecho_activo and not superior_derecho_activo):
                # activarActuadores(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH)
            # #Activados sensores INFERIOR IZQ y SUPERIOR DER
            # elif (not superior_izquierdo_activo and inferior_izquierdo_activo and not inferior_derecho_activo and superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
            # #Activados sensores INFERIOR DER Y SUPERIOR DER
            # elif (not superior_izquierdo_activo and not inferior_izquierdo_activo and inferior_derecho_activo and superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
            # #Activados sensores SUPERIOR IZQ y SUPERIOR DER
            # elif (superior_izquierdo_activo and not inferior_izquierdo_activo and not inferior_derecho_activo and superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
            # #Activados sensores SUPERIOR IZQ e INFERIOR DER
            # elif (superior_izquierdo_activo and not inferior_izquierdo_activo and inferior_derecho_activo and not superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)
            # #Activados sensores INFERIOR IZQ e INFERIOR DER
            # elif (not superior_izquierdo_activo and inferior_izquierdo_activo and inferior_derecho_activo and not superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.HIGH)

            # #3 sensores activos
            # #Activados sensores SUPERIOR e INFERIOR IZQ y SUPERIOR DER
            # elif (superior_izquierdo_activo and inferior_izquierdo_activo and not inferior_derecho_activo and superior_derecho_activo):
                # activarActuadores(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH)
            # #Activados sensores SUPERIOR e INFERIOR IZQ y INFERIOR DER
            # elif (superior_izquierdo_activo and inferior_izquierdo_activo and inferior_derecho_activo and not superior_derecho_activo):
                # activarActuadores(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH)
            # #Activados sensores SUPERIOR IZQ e INFERIOR Y SUPERIOR DER
            # elif (superior_izquierdo_activo and not inferior_izquierdo_activo and inferior_derecho_activo and superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
            # #Activados sensores INFERIOR IZQ e INFERIOR Y SUPERIOR DER
            # elif (not superior_izquierdo_activo and inferior_izquierdo_activo and inferior_derecho_activo and superior_derecho_activo):
                # activarActuadores(GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
        
        
        
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



