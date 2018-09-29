#!/usr/bin/python

from datetime import datetime
from collections import deque

class DataSensores:

    UMBRAL_LECTURA_ADELANTE = 200
    UMBRAL_LECTURA_ATRAS = 400
    
    UMBRAL_LECTURA_ABAJO = 10
    UMBRAL_LECTURA_ARRIBA = 10
    
    # fecha
    
    # sensorPresionIzqAdelante
    # sensorPresionIzqAtras
    # sensorPresionDerAdelante
    # sensorPresionDerAtras
    # sensorDistanciaAbajo
    # sensorDistanciaArriba
    
    # actuadorVibrador
    # actuadorLuces
    
    # configActuadorVibrador
    # configActuadorLuces
    # configPeso
    
    # izqAtrasActivo
    # izqAdelanteActivo
    # derAdelanteActivo
    # derAtrasActivo
    
    # distAbajoLejos
    # distArribaLejos
    
    def __init__(self, sensorPresionIzqAdelante, sensorPresionIzqAtras, sensorPresionDerAdelante, sensorPresionDerAtras, sensorDistanciaAbajo, sensorDistanciaArriba):
        self.fecha = datetime.now()
        
        self.sensorPresionIzqAdelante = sensorPresionIzqAdelante
        self.sensorPresionIzqAtras = sensorPresionIzqAtras
        self.sensorPresionDerAdelante = sensorPresionDerAdelante
        self.sensorPresionDerAtras = sensorPresionDerAtras
        self.sensorDistanciaAbajo = sensorDistanciaAbajo
        self.sensorDistanciaArriba = sensorDistanciaArriba
    
    def configUmbrales(self, umbralSensoresAdelante, umbralSensoresAtras, umbralSensorAbajo, umbralSensorArriba):
        self.UMBRAL_LECTURA_ADELANTE = umbralSensoresAdelante
        self.UMBRAL_LECTURA_ATRAS = umbralSensoresAtras
        self.UMBRAL_LECTURA_ABAJO = umbralSensorAbajo
        self.UMBRAL_LECTURA_ARRIBA = umbralSensorArriba
    
    def configActuadores(self, configActuadorVibrador, configActuadorLuces, configPeso):
        self.configActuadorVibrador = configActuadorVibrador
        self.configActuadorLuces = configActuadorLuces
        self.configPeso = configPeso
    
    def procesarDatos(self):
        self.lado_izquierdo = self.sensorPresionIzqAdelante + self.sensorPresionIzqAtras
        self.lado_derecho = self.sensorPresionDerAdelante + self.sensorPresionDerAtras
        
        self.izqAtrasActivo = self.sensorPresionIzqAtras > self.UMBRAL_LECTURA_ATRAS
        self.izqAdelanteActivo = self.sensorPresionIzqAdelante > self.UMBRAL_LECTURA_ADELANTE
        self.derAdelanteActivo = self.sensorPresionDerAdelante > self.UMBRAL_LECTURA_ADELANTE
        self.derAtrasActivo = self.sensorPresionDerAtras > self.UMBRAL_LECTURA_ATRAS

        self.distAbajoLejos = self.sensorDistanciaAbajo > self.UMBRAL_LECTURA_ABAJO
        self.distArribaLejos = self.sensorDistanciaArriba > self.UMBRAL_LECTURA_ARRIBA
    
    #No hay nadie sentado
    def noHayNadieSentado(self):
        return not self.izqAtrasActivo and not self.izqAdelanteActivo and not self.derAdelanteActivo and not self.derAtrasActivo
    
    #Controlo la distancia de la espalda y cabeza, si se activaron esta mal sentado
    def lejosRespaldo(self):
        return self.distAbajoLejos or self.distArribaLejos
        
    #4 sensores de presion activos, está bien sentado: Activados sensores SUPERIOR e INFERIOR IZQ e INFERIOR Y SUPERIOR DER
    def bienSentado(self):
        return not self.lejosRespaldo() and self.izqAtrasActivo and self.izqAdelanteActivo and self.derAdelanteActivo and self.derAtrasActivo
    
    def imprimirData(self):
        print("sensor ATRAS IZQ: ", self.sensorPresionIzqAtras, " \tSensor ADELA IZQ: ", self.sensorPresionIzqAdelante, " \tSensor ATRAS DER: ", self.sensorPresionDerAtras, " \tSensor ADELA DER: ", self.sensorPresionDerAdelante)
    
    def concatenarData(self):
        return str(self.fecha) + ";" + str(self.sensorPresionIzqAtras) + ";" + str(self.sensorPresionIzqAdelante) + ";" + str(self.lado_izquierdo) + ";" + str(self.sensorPresionDerAdelante) + ";" + str(self.sensorPresionDerAtras) + ";" + str(self.lado_derecho) + ";" + str(self.sensorDistanciaAbajo) + ";" + str(self.sensorDistanciaArriba)



class DataSensoresCollection:
    
    def __init__(self, dataSensores):
        self.queue = deque([dataSensores])
    
    def append(self, dataSensores):
        self.queue.append(dataSensores)
    
    def popleft(self):
        return self.queue.popleft()

