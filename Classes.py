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
    
    def __init__(self, sensorPresionIzqAtras, sensorPresionDerAtras, sensorPresionIzqAdelante, sensorPresionDerAdelante, sensorDistanciaAbajo, sensorDistanciaArriba):
        self.fecha = datetime.now()
        
        self.sensorPresionIzqAtras = sensorPresionIzqAtras
        self.sensorPresionDerAtras = sensorPresionDerAtras
        self.sensorPresionIzqAdelante = sensorPresionIzqAdelante
        self.sensorPresionDerAdelante = sensorPresionDerAdelante
        self.sensorDistanciaAbajo = sensorDistanciaAbajo
        self.sensorDistanciaArriba = sensorDistanciaArriba
        
        self.configActuadorVibrador = False
        self.configActuadorLuces = False
        self.configPeso = 65
        
        self.configUmbrales()
        
        self.lado_izquierdo = self.sensorPresionIzqAdelante + self.sensorPresionIzqAtras
        self.lado_derecho = self.sensorPresionDerAdelante + self.sensorPresionDerAtras
        
        self.izqAtrasActivo = self.sensorPresionIzqAtras > self.UMBRAL_LECTURA_ATRAS
        self.derAtrasActivo = self.sensorPresionDerAtras > self.UMBRAL_LECTURA_ATRAS
        self.izqAdelanteActivo = self.sensorPresionIzqAdelante > self.UMBRAL_LECTURA_ADELANTE
        self.derAdelanteActivo = self.sensorPresionDerAdelante > self.UMBRAL_LECTURA_ADELANTE

        self.ladoIzqActivo = (self.izqAtrasActivo or self.izqAdelanteActivo) and not self.derAtrasActivo and not self.derAdelanteActivo
        self.ladoDerActivo = (self.derAtrasActivo or self.derAdelanteActivo) and not self.izqAtrasActivo and not self.izqAdelanteActivo
        
        self.distAbajoLejos = self.sensorDistanciaAbajo > self.UMBRAL_LECTURA_ABAJO
        self.distArribaLejos = self.sensorDistanciaArriba > self.UMBRAL_LECTURA_ARRIBA

    def configUmbrales(self):
        if (self.configPeso <= 50):
            self.UMBRAL_LECTURA_ADELANTE = 100
            self.UMBRAL_LECTURA_ATRAS = 200
            self.UMBRAL_LECTURA_ABAJO = 20
            self.UMBRAL_LECTURA_ARRIBA = 20
        elif (self.configPeso > 50 and self.configPeso <= 70):
            self.UMBRAL_LECTURA_ADELANTE = 150
            self.UMBRAL_LECTURA_ATRAS = 300
            self.UMBRAL_LECTURA_ABAJO = 15
            self.UMBRAL_LECTURA_ARRIBA = 15
        elif (self.configPeso > 70 and self.configPeso <= 90):
            self.UMBRAL_LECTURA_ADELANTE = 200
            self.UMBRAL_LECTURA_ATRAS = 400
            self.UMBRAL_LECTURA_ABAJO = 10
            self.UMBRAL_LECTURA_ARRIBA = 10
        elif (self.configPeso > 90):
            self.UMBRAL_LECTURA_ADELANTE = 250
            self.UMBRAL_LECTURA_ATRAS = 500
            self.UMBRAL_LECTURA_ABAJO = 7
            self.UMBRAL_LECTURA_ARRIBA = 7
    
    def configActuadores(self, configActuadorVibrador, configActuadorLuces, configPeso):
        self.configActuadorVibrador = configActuadorVibrador
        self.configActuadorLuces = configActuadorLuces
        self.configPeso = configPeso
    
    def getConfigActuadorVibrador(self):
        return self.configActuadorVibrador
    
    def getConfigActuadorLed(self):
        return self.configActuadorLuces
    
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
        data = "ATRAS IZQ: " + str(self.sensorPresionIzqAtras) + "\t"
        data = data + "ATRAS DER: " + str(self.sensorPresionDerAtras) + "\t"
        data = data + "ADELA IZQ: " + str(self.sensorPresionIzqAdelante) + "\t"
        data = data + "ADELA DER: " + str(self.sensorPresionDerAdelante) + "\t"
        data = data + "ABAJO: " + str(self.sensorDistanciaAbajo) + "\t"
        data = data + "ARRIBA: " + str(self.sensorDistanciaArriba)
        print(data)
    
    def concatenarData(self):
        ##Fecha<DateTime>;
        ##SensorResAtrasIzq<float(8,4)>;SensorResAtrasDer<float(8,4)>;SensorResAdantIzq<float(8,4)>;SensorResAdantDer<float(8,4)>;
        ##SensorDistAbajo<float(8,4)>;SensorDistArriba<float(8,4)>;
        ##bienSentado<bool>;sentadoMalIzq<bool>;sentadoMalDer<bool>;sentadoLejosAbajo<bool>;sentadoLejosArriba<bool>
        stringRetorno = str(self.fecha) + ";"
        stringRetorno = stringRetorno + str(self.sensorPresionIzqAtras) + ";" + str(self.sensorPresionDerAtras) + ";" + str(self.sensorPresionIzqAdelante) + ";" + str(self.sensorPresionDerAdelante) + ";"
        stringRetorno = stringRetorno + str(self.sensorDistanciaAbajo) + ";" + str(self.sensorDistanciaArriba) + ";"
        stringRetorno = stringRetorno + str(self.bienSentado()) + ";" + str(self.ladoIzqActivo) + ";" + str(self.ladoDerActivo) + ";" + str(self.distAbajoLejos) + ";" + str(self.distArribaLejos)
        return stringRetorno


class DataSensoresCollection:
    
    def __init__(self, maxLength):
        self.queue = deque([], maxLength)
    
    def append(self, dataSensores):
        self.queue.append(dataSensores)
    
    def popleft(self):
        if (self.len() != 0):
            return self.queue.popleft()

    def len(self):
        return len(self.queue)

