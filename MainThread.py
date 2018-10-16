#!/usr/bin/python

import RPi.GPIO as GPIO
import signal
import sys
import time
import multiprocessing
from multiprocessing.pool import ThreadPool

from Classes import DataSensores
from Functions import moduloBluetooth, readFuerzaResist, readDistance, activarActuadores, lecturas_distancia, lecturas_sensores, dataSensoresCollection, TIEMPO_ENTRE_LECTURAS_ENVIOS

def close(signal, frame):
    print("\nLimpiando la configuracion de pines...\n")
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, close)

#Configuracion de pines de la placa
SPICLK = 11 #BCM GPIO 11 // BOARD PIN 23
SPIMISO = 9 #BCM GPIO 09 // BOARD PIN 21
SPIMOSI = 10 #BCM GPIO 10 // BOARD PIN 19
SPICS = 8 #BCM GPIO 08 // BOARD PIN 24

#Pines de lectura analogicos (MCP3008)
SENSOR_FUERZA_SUPERIOR_DER = 0; #CH0 // PIN 1
SENSOR_FUERZA_INFERIOR_DER = 1; #CH1 // PIN 2
SENSOR_FUERZA_INFERIOR_IZQ = 6; #CH6 // PIN 7
SENSOR_FUERZA_SUPERIOR_IZQ = 7; #CH7 // PIN 8

#Pines sensor de distancia
DISTANCE_PIN_TRIGGER_ABAJO = 4 #BCM GPIO 04 // BOARD PI0N 07
DISTANCE_PIN_ECHO_ABAJO = 3 #BCM GPIO 03 // BOARD PIN 05

DISTANCE_PIN_TRIGGER_ARRIBA = 17 #BCM GPIO 17 // BOARD PIN 11
DISTANCE_PIN_ECHO_ARRIBA = 27 #BCM GPIO 27 // BOARD PIN 13

#Pines de los actuadores
LED_VERDE_IZQ = 19 #BCM GPIO 19 // BOARD PIN 35
LED_VERDE_DER = 16 #BCM GPIO 16 // BOARD PIN 36
LED_ROJO_IZQ = 26 #BCM GPIO 26 // BOARD PIN 37
LED_ROJO_DER = 20 #BCM GPIO 20 // BOARD PIN 38
VIBRADOR = 21 #BCM GPIO 21 // BOARD PIN 40

# use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Seteo de modo de pines
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

GPIO.setup(LED_VERDE_IZQ, GPIO.OUT)
GPIO.setup(LED_VERDE_DER, GPIO.OUT)
GPIO.setup(LED_ROJO_IZQ, GPIO.OUT)
GPIO.setup(LED_ROJO_DER, GPIO.OUT)
GPIO.setup(VIBRADOR, GPIO.OUT)

#Config de lectura de los sensores
TOPE_LECTURA_ABAJO = 40
TOPE_LECTURA_ARRIBA = 50

#Configuracion de threads
pool = ThreadPool(processes=7)
DEBUG = 1

lectura_distancia_abajo_async = pool.apply_async(readDistance, (DISTANCE_PIN_TRIGGER_ABAJO, DISTANCE_PIN_ECHO_ABAJO, TOPE_LECTURA_ABAJO, 0))
lectura_distancia_arriba_async = pool.apply_async(readDistance, (DISTANCE_PIN_TRIGGER_ARRIBA, DISTANCE_PIN_ECHO_ARRIBA, TOPE_LECTURA_ARRIBA, 1))
#retorno_distancia_abajo = lectura_distancia_abajo_async.get()
#retorno_distancia_arriba = lectura_distancia_arriba_async.get()

lectura_actual_inferior_izquierdo = pool.apply_async(readFuerzaResist, (SENSOR_FUERZA_INFERIOR_IZQ, SPICLK, SPIMOSI, SPIMISO, SPICS, 0))
lectura_actual_superior_izquierdo = pool.apply_async(readFuerzaResist, (SENSOR_FUERZA_SUPERIOR_IZQ, SPICLK, SPIMOSI, SPIMISO, SPICS, 1))
lectura_actual_inferior_derecho = pool.apply_async(readFuerzaResist, (SENSOR_FUERZA_INFERIOR_DER, SPICLK, SPIMOSI, SPIMISO, SPICS, 2))
lectura_actual_superior_derecho = pool.apply_async(readFuerzaResist, (SENSOR_FUERZA_SUPERIOR_DER, SPICLK, SPIMOSI, SPIMISO, SPICS, 3))
# retorno_inferior_izquierdo = lectura_actual_inferior_izquierdo.get()
# retorno_superior_izquierdo = lectura_actual_superior_izquierdo.get()
# retorno_inferior_derecho = lectura_actual_inferior_derecho.get()
# retorno_superior_derecho = lectura_actual_superior_derecho.get()

pool.apply_async(moduloBluetooth)

#proceso principal
while True:
    retorno_inferior_izquierdo = lecturas_sensores[0]
    retorno_superior_izquierdo = lecturas_sensores[1]
    retorno_inferior_derecho = lecturas_sensores[2]
    retorno_superior_derecho = lecturas_sensores[3]
    
    retorno_distancia_abajo = lecturas_distancia[0]
    retorno_distancia_arriba = lecturas_distancia[1]
    
    config = dataSensoresCollection.getConfig()
    
    dataSensores = DataSensores(retorno_superior_izquierdo, retorno_superior_derecho, retorno_inferior_izquierdo, retorno_inferior_derecho, retorno_distancia_abajo, retorno_distancia_arriba, config.getPeso())
    
    #dataSensores.imprimirData()
    #print(dataSensores.concatenarData())
    
    if (dataSensores.noHayNadieSentado()):
        ##TODO comentar cuando vaya a produccion
        dataSensoresCollection.append(dataSensores)
        
        activarActuadores(LED_VERDE_IZQ, LED_VERDE_DER, LED_ROJO_IZQ, LED_ROJO_DER, VIBRADOR, config.getConfigActuadorVibrador(), config.getConfigActuadorLed(), GPIO.LOW, GPIO.LOW)
    elif (dataSensores.bienSentado()):
        dataSensoresCollection.append(dataSensores)
        
        activarActuadores(LED_VERDE_IZQ, LED_VERDE_DER, LED_ROJO_IZQ, LED_ROJO_DER, VIBRADOR, config.getConfigActuadorVibrador(), config.getConfigActuadorLed(), GPIO.HIGH, GPIO.LOW)
    else: #algun sensor no esta activado, no está bien sentado
        dataSensoresCollection.append(dataSensores)
        
        activarActuadores(LED_VERDE_IZQ, LED_VERDE_DER, LED_ROJO_IZQ, LED_ROJO_DER, VIBRADOR, config.getConfigActuadorVibrador(), config.getConfigActuadorLed(), GPIO.LOW, GPIO.HIGH)
    
    time.sleep(TIEMPO_ENTRE_LECTURAS_ENVIOS)


