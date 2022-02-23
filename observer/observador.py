from vmc.modelo import REGISTROS_ACUMULADOS
from datetime import datetime
import os

class Tema:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def notificar(self):
        for observador in self.observadores:
            observador.archivo_txt()


class TemaConcreto(Tema):
    def __init__(self):
        pass

    def crear_txt(self):
        self.notificar()


class Observador:
    def archivo_txt(self):
        raise NotImplementedError("Delegación de creacion de texto")


class ConcreteObserverA(Observador):
    def __init__(self, obj):
        self.observador_a = obj
        self.observador_a.agregar(self) 

    def archivo_txt(self):
        fecha_actual = datetime.now().strftime("%m%d%Y_%H%M%S%f")
        nombre_archivo = f"{fecha_actual}_registros.txt" 
        
        ruta_carpeta_logs = os.path.abspath("logs")
        ruta_nombre_archivo = os.path.join(ruta_carpeta_logs, nombre_archivo)

        if len(REGISTROS_ACUMULADOS) >= 1:
            with open(f"{ruta_nombre_archivo}", "w") as archivo:
                for reporte in REGISTROS_ACUMULADOS:
                    archivo.write(reporte + "\n")
