#!/usr/bin/python

import time
import select
import bluetooth
import RPi.GPIO as GPIO

from Classes import DataSensores, DataSensoresCollection

CANT_MUESTRAS_SENSOR_DIST = 10
MAX_LENGTH_COLA = 1000
TIEMPO_ENTRE_LECTURAS_ENVIOS = 0.5

lecturas_distancia = [0, 0]
lecturas_sensores = [0, 0, 0, 0]
dataSensoresCollection = DataSensoresCollection(MAX_LENGTH_COLA)
BLUE_DISCONNECTED = 0
BLUE_CONNECTED = 1
BLUE_QUIT = 2
ESTADO_BLUETOOTH = BLUE_DISCONNECTED

def moduloBluetooth():
    
    global TIEMPO_ENTRE_LECTURAS_ENVIOS
    global dataSensoresCollection
    global ESTADO_BLUETOOTH, BLUE_CONNECTED, BLUE_DISCONNECTED, BLUE_QUIT
    
    server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    #server_socket.setblocking(0)
    port = 1
    server_socket.bind(("",port))
    server_socket.listen(1)
    
    while ESTADO_BLUETOOTH is not BLUE_QUIT:
        print("esperando coneccion..")
        client_socket,address = server_socket.accept()
        client_socket.setblocking(0)
        print("Aceptada coneccion de ", address)
        ESTADO_BLUETOOTH = BLUE_CONNECTED
        
        while ESTADO_BLUETOOTH == BLUE_CONNECTED:
            try:
                readable, writable, exceptional = select.select([client_socket], [client_socket], [client_socket], 3)
                if len(writable) > 0:
                    # connection established, send some stuff
                    try:
                        dataSensores = dataSensoresCollection.popleft()
                        if (dataSensores is not None):
                            #dataSensores.imprimirData()
                            #print(dataSensores.concatenarData())
                            writable[0].send(dataSensores.concatenarData())
                        else:
                            writable[0].send("")
                    except bluetooth.BluetoothError as e:
                        print("Error coneccion SEND")
                        ESTADO_BLUETOOTH = BLUE_DISCONNECTED
                        break

                if len(readable) > 0:
                    data = readable[0].recv(2)
                    if data:
                        data = data.decode()
                        print("Recibido: %s" %data)
                        if (data == "CF"):
                            data = readable[0].recv(1024).decode()
                            ##confActuadorLed<bool>;confActuadorVibracion<bool>;peso<int>
                            configData = data.split(';')
                            print("Paq config: ", data, " && ", configData)
                            #Aca los tipos de datos tienen que ser tal cual es descrito en el comentario anterior -> bool-bool-int
                            #TODO probar como funciona desde la app
                            dataSensoresCollection.setConfig(configData[0], configData[1], configData[2])
                        if (data == "Q"):
                            print("SALIR")
                            ESTADO_BLUETOOTH = BLUE_QUIT
                            break
                    else:
                        print("Error coneccion RECV")
                        ESTADO_BLUETOOTH = BLUE_DISCONNECTED
                        break

                if len(exceptional) > 0:
                    print("Error coneccion EXPCEPTIONAL")
                    ESTADO_BLUETOOTH = BLUE_DISCONNECTED
                    break
            except select.error:
                print("Error coneccion SELECT")
                ESTADO_BLUETOOTH = BLUE_DISCONNECTED
                break
            except Exception as e:
                print("Error coneccion DESCONOCIDO")
                print(e)

            time.sleep(TIEMPO_ENTRE_LECTURAS_ENVIOS)

        print("Cerrando SOCKET..")
        client_socket.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
        client_socket.close()
    
    server_socket.close()
    
    return

def readFuerzaResist(adcnum, clockpin, mosipin, misopin, cspin, index):
    
    global CANT_MUESTRAS_SENSOR_DIST
    global TIEMPO_ENTRE_LECTURAS_ENVIOS
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
        time.sleep(TIEMPO_ENTRE_LECTURAS_ENVIOS)
    
    return resultado / CANT_MUESTRAS_SENSOR_DIST

def readDistance(triggerpin, echopin, topeLectura, index):

    global TIEMPO_ENTRE_LECTURAS_ENVIOS
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
            time.sleep(TIEMPO_ENTRE_LECTURAS_ENVIOS/2)
        
        #print("seteo distancia", index)
        lecturas_distancia[index] = distance
        #print("sleep", index)
        time.sleep(TIEMPO_ENTRE_LECTURAS_ENVIOS)
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


