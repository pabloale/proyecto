#!/usr/bin/python

import time
import bluetooth
import RPi.GPIO as GPIO

from Classes import DataSensores, DataSensoresCollection

CANT_MUESTRAS_SENSOR_DIST = 10
MAX_LENGTH_COLA = 1000
TIEMPO_ENTRE_ENVIOS_BLUE = 0.5

lecturas_distancia = [0, 0]
lecturas_sensores = [0, 0, 0, 0]
dataSensoresCollection = DataSensoresCollection(MAX_LENGTH_COLA)

def moduloBluetooth():
    
    global TIEMPO_ENTRE_ENVIOS_BLUE
    global lecturas_sensores
    global dataSensoresCollection
    
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 1
    server_socket.bind(("",port))
    server_socket.listen(1)
     
    client_socket,address = server_socket.accept()
    print("Accepted connection from ",address)
    while 1:
        dataSensores = dataSensoresCollection.popleft()
        if (dataSensores is not None):
            dataSensores.imprimirData()
            print(dataSensores.concatenarData())
            client_socket.send(dataSensores.concatenarData())
        else:
            client_socket.send("")
        #print(lecturas_sensores)
        data = client_socket.recv(2).decode()
        print("Received: %s" %data)
        if (data == "CF"):
            data = client_socket.recv(1024).decode()
            ##confActuadorLed<bool>;confActuadorVibracion<bool>;peso<int>
            configData = data.split(';')
            print("Paq config: ", data, " && ", configData)
            dataSensoresCollection.setConfig(DataConfigActuadores(configData[0], configData[1], configData[2]))
        if (data == "q"):
            print("Quit")
            break
        time.sleep(TIEMPO_ENTRE_ENVIOS_BLUE)

    client_socket.close()
    server_socket.close()
    
    return

def readFuerzaResist(adcnum, clockpin, mosipin, misopin, cspin, index):
    
    global CANT_MUESTRAS_SENSOR_DIST
    global TIEMPO_ENTRE_ENVIOS_BLUE
    global lecturas_sensores

    while True:
        h = 0
        resultado = 0
        while (h < CANT_MUESTRAS_SENSOR_DIST):
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
        
        lecturas_sensores[index] = resultado / CANT_MUESTRAS_SENSOR_DIST
        time.sleep(TIEMPO_ENTRE_ENVIOS_BLUE)
    
    return resultado / CANT_MUESTRAS_SENSOR_DIST

def readDistance(triggerpin, echopin, topeLectura, index):

    global TIEMPO_ENTRE_ENVIOS_BLUE
    global lecturas_distancia
    distance = 0
    
    VEL_ULTRASONIDO = 34300 #34300 cm/s
    
    # set GPIO input and output channels
    GPIO.setup(triggerpin, GPIO.OUT)
    GPIO.setup(echopin, GPIO.IN)
    
    while True:
        distance = 0
        while distance <= 0 or distance > topeLectura:
            
            GPIO.output(triggerpin, GPIO.LOW)
            #print("esperando que el sensor se estabilice")
            #time.sleep(2)
            time.sleep(0.00001)
            #print("calculando distancia")
            
            # set Trigger to HIGH
            GPIO.output(triggerpin, GPIO.HIGH)
            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(triggerpin, GPIO.LOW)
            
            #print("por calcular el tiempo de respuesta")
            
            pulse_start_time = time.time()
            pulse_end_time = time.time()
            
            # save start time
            while GPIO.input(echopin)==0:
                pulse_start_time = time.time()
                #print("while PIN_ECHO = 0")
            # save time of arrival
            while GPIO.input(echopin)==1:
                pulse_end_time = time.time()
                #print("while PIN_ECHO = 1")
            
            #print("tiempo de respuesta calculado")
            # time difference between start and arrival
            pulse_duration = pulse_end_time - pulse_start_time
            # multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
            distance = round(pulse_duration * VEL_ULTRASONIDO / 2, 2)
            #print("Distance de ", index, ": ", distance, "cm")
            time.sleep(TIEMPO_ENTRE_ENVIOS_BLUE/2)
        
        #print("seteo distancia", index)
        lecturas_distancia[index] = distance
        #print("sleep", index)
        time.sleep(TIEMPO_ENTRE_ENVIOS_BLUE)
        #print("fin sleep", index)
    
    return distance

#LED_VERDE_IZQ - LED_VERDE_DER - LED_ROJO_IZQ - LED_ROJO_DER - VIBRADOR
def activarActuadores(LED_VERDE_IZQ, LED_VERDE_DER, LED_ROJO_IZQ, LED_ROJO_DER, VIBRADOR, configActVibr, configActLed, verdeActivo, rojoActivo):
    
    #print("actuadores:", verdeActivo, rojoActivo)
    if (configActLed):
        GPIO.output(LED_VERDE_IZQ, verdeActivo)
        GPIO.output(LED_VERDE_DER, verdeActivo)
        GPIO.output(LED_ROJO_IZQ, rojoActivo)
        GPIO.output(LED_ROJO_DER, rojoActivo)
    if (configActVibr):
        GPIO.output(VIBRADOR, rojoActivo)
    
    return


