#!/usr/bin/python

from datetime import datetime

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
        lado_izquierdo = self.sensorPresionIzqAdelante + self.sensorPresionIzqAtras
        lado_derecho = self.sensorPresionDerAdelante + self.sensorPresionDerAtras
        
        self.izqAtrasActivo = self.sensorPresionIzqAtras > self.UMBRAL_LECTURA_ATRAS
        self.izqAdelanteActivo = self.sensorPresionIzqAdelante > self.UMBRAL_LECTURA_ADELANTE
        self.derAdelanteActivo = self.sensorPresionDerAdelante > self.UMBRAL_LECTURA_ADELANTE
        self.derAtrasActivo = self.sensorPresionDerAtras > self.UMBRAL_LECTURA_ATRAS

        self.distAbajoLejos = self.sensorDistanciaAbajo > self.UMBRAL_LECTURA_ABAJO
        self.distArribaLejos = self.sensorDistanciaArriba > self.UMBRAL_LECTURA_ARRIBA
    
    def noHayNadieSentado(self):
        return not self.izqAtrasActivo and not self.izqAdelanteActivo and not self.derAdelanteActivo and not self.derAtrasActivo
    
    def lejosRespaldo(self):
        return self.distAbajoLejos or self.distArribaLejos
        
    def bienSentado(self):
        return not self.lejosRespaldo and self.izqAtrasActivo and self.izqAdelanteActivo and self.derAdelanteActivo and self.derAtrasActivo
    
    def concatenarData(self):
        return 'data procesada en forma de string'
    