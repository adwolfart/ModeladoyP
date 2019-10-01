import threading
import time

#listas que se utilizan como banda transportadoras
listaPiezas = []
listaPiezasEnsamblador = []
listaPaqueteFinalizados = []

#bool que se usa para verificar si ya se ha cumplido la condicion para terminar la simulacion
mataHilos = True

#clase que modela un paquete
class Paquete(object):

    def __init__(self, tipo, listaPiezasPaquete):
        self.tipo = tipo
        self.listaPiezasPaquete = listaPiezasPaquete
        milisegundos = int(round(time.time() * 1000))
        self.identificador = tipo+str(milisegundos)

    def getTipo(self):
        return self.tipo

    def getListaPiezasPaquete(self):
        return self.listaPiezasPaquete

    def getIdentificador(self):
        return self.identificador

#clase que modela una pieza
class Pieza(object):

    def __init__(self, tipo):
        self.tipo = tipo
        milisegundos = int(round(time.time() * 1000))
        self.identificador = tipo+str(milisegundos)

    def getTipoPieza(self):
        return self.tipo

    def getIdentificador(self):

        return self.identificador


#clase que modela al productor de piezas
#se extiende de la clase Thread para modificar el metodo run
class Productor(threading.Thread):

    def __init__(self, tipoPieza, tiempo):
        self.tiempo = tiempo
        self.tipoPieza = tipoPieza
        threading.Thread.__init__(self)

    #funcion que crea piezas cada ciertos segundo
    def crearPieza(self):
        nuevaPieza = Pieza(self.tipoPieza)
        time.sleep(self.tiempo)
        return nuevaPieza

    #funcion que crea piezas constantemente hasta que se cumple la condicion para finalizar los hilos
    def run (self):
        while mataHilos:
            pieza = self.crearPieza()
            print("Se crea la pieza con id: "+pieza.getIdentificador())
            listaPiezas.append(pieza)

    def getTiempo(self):
        return self.tiempo

#clase que modela el Ensamblador, tambien extiende de Thread
class Ensamblador(threading.Thread):

    def __init__(self, tipoPieza, tiempo, listaCantTipo):
        self.tipoPieza = tipoPieza
        self.tiempo = tiempo
        self.listaCantTipo = listaCantTipo
        self.listaPiezasRecolectadas = []
        threading.Thread.__init__(self)

    #funcion que crea piezas del Ensamblador, revisando cuantas piezas van en cada pieza nueva
    def crearPiezaEnsamblador(self, i):

        cantidadTotalPiezas = 0
        for np in self.listaCantTipo:
            cantidadTotalPiezas = cantidadTotalPiezas + np[1]
        tupla = self.listaCantTipo[i]
        tipoPiezaS = tupla[0]
        cantidadPiezasS = tupla[1]
        j = 0
        while j < len(listaPiezas):
            piezaP = listaPiezas[j]
            if tipoPiezaS == piezaP.getTipoPieza():
                cuantasPiezas = 0
                for k in self.listaPiezasRecolectadas:
                    if k.getTipoPieza() == piezaP.getTipoPieza():
                        cuantasPiezas = cuantasPiezas + 1
                if cuantasPiezas < cantidadPiezasS:
                    self.listaPiezasRecolectadas.append(piezaP)
                    del listaPiezas[j]
                break
            j = j + 1

        if len(self.listaPiezasRecolectadas)==cantidadTotalPiezas:
            nuevaPieza = Pieza(self.tipoPieza)
            listaPiezasEnsamblador.append(nuevaPieza)
            print("Se crea la pieza con id: "+nuevaPieza.getIdentificador())
            del self.listaPiezasRecolectadas[0:len(self.listaPiezasRecolectadas)]
            time.sleep(self.tiempo)

    #funcino run que es modificada para que cree piezas del Ensamblador cada ciertos segundos
    def run (self):
        i = 0
        while mataHilos:
            if i == len(self.listaCantTipo):
                i = 0
            self.crearPiezaEnsamblador(i)
            i = i + 1

    def getTiempo(self):
        return self.tiempo

#clase que empaqueta las piezas extiende de Thread
class Empaquetador(threading.Thread):

    def __init__(self, tipoPieza, tipoPiezaEntrada, tiempo, tamPaquete, numPaquetes):
        self.tiempo = tiempo
        self.tipoPieza = tipoPieza
        self.tamPaquete = tamPaquete
        self.listaPiezasPaquete = []
        self.tipoPiezaEntrada = tipoPiezaEntrada
        self.numPaquetes = numPaquetes
        threading.Thread.__init__(self)

    #funcion que revisa la banda y recogue las piezas para empaquetar
    def crearPaquete(self):

        i = 0
        while i < len(listaPiezasEnsamblador):
            piezaP = listaPiezasEnsamblador[i]
            print("---------------")
            if piezaP.getTipoPieza() == self.tipoPiezaEntrada:

                self.listaPiezasPaquete.append(piezaP)
                del listaPiezasEnsamblador[i]

            if len(self.listaPiezasPaquete) == self.tamPaquete:
                nuevoPaquete = Paquete(self.tipoPieza, self.listaPiezasPaquete)
                print("Se creo el paquete:"+str(nuevoPaquete.getIdentificador()))
                listaPaqueteFinalizados.append(nuevoPaquete)
                del self.listaPiezasPaquete[0:len(self.listaPiezasPaquete)]

            if len(listaPaqueteFinalizados) == self.numPaquetes:
                global mataHilos
                mataHilos = False

            i = i + 1

    #funcion run modificada que se ejecuta hasta que se cumple la condicion
    def run (self):

        while mataHilos:
            self.crearPaquete()


#funciion que modela el problema A

def ejercicioA():
    #crea piezas de tipo A cada 1 segundo
    p = Productor("A", 1)
    #crea piezas de tipo B cada 2 segundo
    p1 = Productor("B", 2)
    #crea piezas de tipo C cada 4 segundo. para crear las piezas necesita dos de tipo A y tres de tipo B
    e = Ensamblador("C", 4, [("A", 2), ("B", 3)])
    #Empaquetador que crea paquetes de tipo P, guarda piezas de tipo C, cada 0 segundos, va crear 5 paquetes con
    #5 piezas cada paquete
    empa = Empaquetador("P", "C", 0, 5, 5)
    #inicia los hilos
    p.start()
    p1.start()
    e.start()
    empa.start()



ejercicioA()
