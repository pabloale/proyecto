from Classes import DataSensores

'''class DataSensores:
    
    UMBRAL_LECTURA_ABAJO = 10
    UMBRAL_LECTURA_ARRIBA = 10
    
    def __init__(self, sensorPresionIzqAdelante, sensorDistanciaAbajo, sensorDistanciaArriba):
        
        self.sensorPresionIzqAdelante = sensorPresionIzqAdelante
        self.sensorDistanciaAbajo = sensorDistanciaAbajo
        self.sensorDistanciaArriba = sensorDistanciaArriba
    
    def procesarDatos(self):
        self.distAbajoLejos = self.sensorDistanciaAbajo > self.UMBRAL_LECTURA_ABAJO
        self.distArribaLejos = self.sensorDistanciaArriba > self.UMBRAL_LECTURA_ARRIBA
        
        self.ladoIzqActivo = (False or True) and not False and not False
        self.ladoDerActivo = (False or True) and not False and not False
    
    def lejosRespaldo(self):
        
        return self.distAbajoLejos or self.distArribaLejos
    
    def bienSentado(self):
        return not self.lejosRespaldo() and True
    
    def concatenarData(self):
        stringRetorno = str(self.sensorPresionIzqAdelante) + ";" + str(self.lejosRespaldo())
        stringRetorno = stringRetorno + str(self.bienSentado()) + ";" + str(self.ladoIzqActivo) + ";" + str(self.ladoDerActivo) + ";" + str(self.distAbajoLejos) + ";" + str(self.distArribaLejos)
        return stringRetorno
'''
print("Hello World")

data = DataSensores(0.5, 9, 11, 0.5, 0, 0)

data.imprimirData()

print(data.concatenarData())

#data = DataSensores(0.5, "9", "11")

#data.procesarDatos()

#print(data.concatenarData())