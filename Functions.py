#!/usr/bin/python

import bluetooth
import RPi.GPIO as GPIO

CANTIDAD_MUESTRAS = 10
lecturas_distancia = [0, 0]
lecturas_sensores = [0, 0, 0, 0]

def moduloBluetooth():
    
    global lecturas_sensores
    
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 1
    server_socket.bind(("",port))
    server_socket.listen(1)
     
    client_socket,address = server_socket.accept()
    print("Accepted connection from ",address)
    while 1:
        data = client_socket.recv(1024).decode()
        print("Received: %s" %data)
        print(lecturas_sensores)
        if (data == "0"):    #if '0' is sent from the Android App
            client_socket.send(str(lecturas_sensores[0]))
        if (data == "1"):    #if '1' is sent from the Android App
            client_socket.send(str(lecturas_sensores[1]))
        if (data == "2"):    #if '2' is sent from the Android App
            client_socket.send(str(lecturas_sensores[2]))
        if (data == "3"):    #if '3' is sent from the Android App
            client_socket.send(str(lecturas_sensores[3]))
        if (data == "q"):
            print("Quit")
            break

    client_socket.close()
    server_socket.close()
    
    return

def readFuerzaResist(adcnum, clockpin, mosipin, misopin, cspin, index):
    
    global CANTIDAD_MUESTRAS
    global lecturas_sensores
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
    
    lecturas_sensores[index] = resultado / CANTIDAD_MUESTRAS
    
    return resultado / CANTIDAD_MUESTRAS

def readDistance(triggerpin, echopin, topeLectura, index):

    global lecturas_distancia
    distance = 0
    
    VEL_ULTRASONIDO = 34300 #34300 cm/s
    
    while distance <= 0 or distance > topeLectura:
        
        GPIO.setup(triggerpin, GPIO.OUT)
        GPIO.setup(echopin, GPIO.IN)
        
        GPIO.output(triggerpin, GPIO.LOW)
        
        #print("esperando que el sensor se estabilice")
        
        #time.sleep(2)
        
        #print("calculando distancia")
        
        GPIO.output(triggerpin, GPIO.HIGH)
        
        time.sleep(0.00001)
        
        GPIO.output(triggerpin, GPIO.LOW)
        
        #print("por calcular el tiempo de respuesta")
        
        pulse_start_time = 0
        pulse_end_time = 0
        
        while GPIO.input(echopin)==0:
            pulse_start_time = time.time()
            #print("while PIN_ECHO = 0")
        while GPIO.input(echopin)==1:
            pulse_end_time = time.time()
            #print("while PIN_ECHO = 1")
        
        #print("tiempo de respuesta calculado")
        
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * VEL_ULTRASONIDO / 2, 2)
        #print("Distance:", distance, "cm")
        
    lecturas_distancia[index] = distance
    
    return distance

#LED_VERDE_IZQUIERDO - LED_VERDE_DERECHO - LED_ROJO_IZQUIERDO - LED_ROJO_DERECHO - VIBRADOR
def activarActuadores(ledVerdeIzq, ledVerdeDer, ledRojoIzq, ledRojoDer, vibrador):
    
    print("actuadores:", ledVerdeIzq, ledVerdeDer, ledRojoIzq, ledRojoDer, vibrador)
    #GPIO.output(LED_VERDE_IZQUIERDO, ledVerdeIzq)
    #GPIO.output(LED_VERDE_DERECHO, ledVerdeDer)
    #GPIO.output(LED_ROJO_IZQUIERDO, ledRojoIzq)
    #GPIO.output(LED_ROJO_DERECHO, ledRojoDer)
    #GPIO.output(VIBRADOR, vibrador)
    
    return


