#!/usr/bin/python

import configparser
from datetime import datetime
from collections import deque

class DataSensores:

    UMBRAL_LECTURA_ADELANTE = 200
    UMBRAL_LECTURA_ATRAS = 400
    
    UMBRAL_LECTURA_ABAJO = 10
    UMBRAL_LECTURA_ARRIBA = 10
    
    
    def __init__(self, sensorPresionIzqAtras, sensorPresionDerAtras, sensorPresionIzqAdelante, sensorPresionDerAdelante, sensorDistanciaAbajo, sensorDistanciaArriba, peso):
        self.fecha = datetime.now()
        
        self.sensorPresionIzqAtras = sensorPresionIzqAtras
        self.sensorPresionDerAtras = sensorPresionDerAtras
        self.sensorPresionIzqAdelante = sensorPresionIzqAdelante
        self.sensorPresionDerAdelante = sensorPresionDerAdelante
        self.sensorDistanciaAbajo = sensorDistanciaAbajo
        self.sensorDistanciaArriba = sensorDistanciaArriba
        
        self.configUmbrales(peso)
        
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

    def configUmbrales(self, peso):
        if (peso <= 50):
            self.UMBRAL_LECTURA_ADELANTE = 100
            self.UMBRAL_LECTURA_ATRAS = 200
            self.UMBRAL_LECTURA_ABAJO = 20
            self.UMBRAL_LECTURA_ARRIBA = 30
        elif (peso > 50 and peso <= 70):
            self.UMBRAL_LECTURA_ADELANTE = 150
            self.UMBRAL_LECTURA_ATRAS = 300
            self.UMBRAL_LECTURA_ABAJO = 20
            self.UMBRAL_LECTURA_ARRIBA = 30
        elif (peso > 70 and peso <= 90):
            self.UMBRAL_LECTURA_ADELANTE = 200
            self.UMBRAL_LECTURA_ATRAS = 400
            self.UMBRAL_LECTURA_ABAJO = 20
            self.UMBRAL_LECTURA_ARRIBA = 30
        elif (peso > 90):
            self.UMBRAL_LECTURA_ADELANTE = 250
            self.UMBRAL_LECTURA_ATRAS = 500
            self.UMBRAL_LECTURA_ABAJO = 20
            self.UMBRAL_LECTURA_ARRIBA = 30
    
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


class DataConfigActuadores:

    def __init__(self, configActuadorLed, configActuadorVibrador, configPeso):
        self.configActuadorLed = configActuadorLed
        self.configActuadorVibrador = configActuadorVibrador
        self.configPeso = configPeso

    def getConfigInicial(self):
        #levanto la configuracion inicial
        configParser = configparser.ConfigParser()
        configParser.read('/home/pi/Desktop/config.ini')
        self.configActuadorLed = (configParser.get('CONFIG', 'ACT_LED') == "True")
        self.configActuadorVibrador = (configParser.get('CONFIG', 'ACT_VIB') == "True")
        self.configPeso = int(configParser.get('CONFIG', 'PESO'))

    def guardarConfig(self, configActuadorLed, configActuadorVibrador, configPeso):
        self.configActuadorLed = (configActuadorLed == "true")
        self.configActuadorVibrador = (configActuadorVibrador == "true")
        self.configPeso = int(configPeso)
        configParser = configparser.ConfigParser()
        configParser.read('/home/pi/Desktop/config.ini')
        configParser.set('CONFIG', 'ACT_LED', str(configActuadorLed == "true"))
        configParser.set('CONFIG', 'ACT_VIB', str(configActuadorVibrador == "true"))
        configParser.set('CONFIG', 'PESO', str(int(configPeso)))
        with open('/home/pi/Desktop/config.ini', 'w') as f:
            configParser.write(f)
    
    def getConfigActuadorLed(self):
        return self.configActuadorLed

    def getConfigActuadorVibrador(self):
        return self.configActuadorVibrador
    
    def getPeso(self):
        return self.configPeso


class DataSensoresCollection:
    
    def __init__(self, maxLength):
        self.queue = deque([], maxLength)
        self.dataConfig = DataConfigActuadores(False, False, 65)
        self.dataConfig.getConfigInicial()
    
    def append(self, dataSensores):
        self.queue.append(dataSensores)
    
    def popleft(self):
        if (self.len() != 0):
            return self.queue.popleft()

    def len(self):
        return len(self.queue)

    def getConfig(self):
        return self.dataConfig

    def setConfig(self, configActuadorLed, configActuadorVibrador, configPeso):
        self.dataConfig.guardarConfig(configActuadorLed, configActuadorVibrador, configPeso)

