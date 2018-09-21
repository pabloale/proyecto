import RPi.GPIO as GPIO
import time

try:
        GPIO.setmode(GPIO.BCM)
        
        PIN_TRIGGER = 4 #BCM GPIO 04 // BOARD PIN 07
        PIN_ECHO = 17 #BCM GPIO 17 // BOARD PIN 11
        
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        
        print("esperando que el sensor se estabilice")
        
        time.sleep(2)
        
        print("calculando distancia")
        
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        
        time.sleep(0.00001)
        
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        
        print("por calcular el tiempo de respuesta")
        
        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
            #print("while PIN_ECHO = 0")
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()
            print("while PIN_ECHO = 1")
        
        print("tiempo de respuesta calculado")
        
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print("Distance:", distance, "cm")

finally:
        GPIO.cleanup()