class Tema:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def quitar(self, obj):
        pass

    def notificar(self):
        for observador in self.observadores:
            observador.update()


class TemaConcreto(Tema):
    def __init__(self):
        self.estado = None

    def set_estado(self, value):
        self.estado = value
        self.notificar()

    def get_estado(self):
        return self.estado


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(Observador):
    def __init__(self, obj):
        self.observador_a = obj
        #import pdb; pdb.set_trace()
        self.observador_a.agregar(self)
        #cuando se inicia se agrega la clase a la lista  

    def update(self):
        print("Actualización dentro de ObservadorConcretoA")
        self.estado = self.observador_a.get_estado()
        print("Estado = ", self.estado)


class ConcreteObserverB(Observador):
    def __init__(self, obj):
        self.observador_b = obj
        self.observador_b.agregar(self)

    def update(self):
        print("Actualización dentro de ObservadorConcretoB")
        self.estado = self.observador_b.get_estado()
        print("Estado = ", self.estado)


tema1 = TemaConcreto()
observador_a = ConcreteObserverA(tema1)
observador_b = ConcreteObserverB(tema1)
tema1.set_estado(1)
# print(observador_a.__dict__)
print("---" * 25)
print(Tema.__dict__)


#para entender mejor
#update es en metodo en el que finaliza y en el que se le puede poner una cierta utilidad
#al definir tema1 tenemos una lista vacia observadores[]
#instanciamos observador_a y se agrega observador_a  a la lista 
#cuando se hace un tema1.set_estado(1) tambien se llama a notificar()
#y notificar al iterar la lista hace un update y update es un metodo que esta definido en concreteObserverB y ahi termina 
