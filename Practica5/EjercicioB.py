import threading
from threading import Thread,Semaphore
import time

#semaforo para manipular los problemas de concurrencia
semaforo = Semaphore(1); #Crear variable semáforo
#listas que son utilizadas como bandas transportadoras
listaPiezas = []
listaPiezasEnsamblador = []
listaPiezasEnsamblador1 = []
listaPaqueteFinalizados = []
mataHilos = True

#se usa para verificar si se esta ejecutando un hilo en algun momento
entro = False
#cuenta las piezas que se van creando
contadorPiezas = 0

#clase que modela los paquetes
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

#clase que modela las piezas
class Pieza(object):

    def __init__(self, tipo):
        self.tipo = tipo
        milisegundos = int(round(time.time() * 1000))
        self.identificador = tipo+str(milisegundos)

    def getTipoPieza(self):
        return self.tipo

    def getIdentificador(self):

        return self.identificador


#clase que modela al productor de piezas. se puede crear varias piezas y dependiendo de la pieza la guarda en el
#lugar correspondiente
class Productor(threading.Thread):

    def __init__(self, tipoPieza, tiempo):
        self.tiempo = tiempo
        self.tipoPieza = tipoPieza
        threading.Thread.__init__(self)


    def crearPieza(self):
        nuevaPieza = Pieza(self.tipoPieza)
        if revisaPiezasCreadas():
            global mataHilos
            mataHilos = False
        time.sleep(self.tiempo)
        return nuevaPieza

    #funcion que guarda la pieza en la banda correspondiente depende de la pieza que es creada
    def run (self):
        global contadorPiezas
        while mataHilos:
            pieza = self.crearPieza()
            contadorPiezas = contadorPiezas + 1
            if pieza.getTipoPieza() == "C":
                listaPiezasEnsamblador.append(pieza)
            elif pieza.getTipoPieza() == "D":
                if entro:
                    semaforo.acquire();
                listaPiezasEnsamblador1.append(pieza)
            else:
                listaPiezas.append(pieza)
            print("Se crea la pieza: "+str(contadorPiezas)+ " con id: "+pieza.getIdentificador())


    def getTiempo(self):
        return self.tiempo

#clase que modela a Ensamblador
class Ensamblador(threading.Thread):

    def __init__(self, tipoPieza, tiempo, listaCantTipo):
        self.tipoPieza = tipoPieza
        self.tiempo = tiempo
        self.listaCantTipo = listaCantTipo
        self.listaPiezasRecolectadas = []
        threading.Thread.__init__(self)

    #funcion que crea piezas cada cierto tiempo. crear las piezas si en la banda hay las piezas correspondientes
    def crearPiezaEnsamblador(self, i):

        global contadorPiezas

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
            contadorPiezas = contadorPiezas + 1
            print("Se crea la pieza: "+str(contadorPiezas)+" con id: "+nuevaPieza.getIdentificador())
            del self.listaPiezasRecolectadas[0:len(self.listaPiezasRecolectadas)]
            if revisaPiezasCreadas():
                global mataHilos
                mataHilos = False
            time.sleep(self.tiempo)

    #funcion que se ejecuta hasta que se cunple la condicion
    def run (self):

        i = 0
        while mataHilos:
            if i == len(self.listaCantTipo):
                i = 0
            self.crearPiezaEnsamblador(i)
            i = i + 1

    def getTiempo(self):
        return self.tiempo


#clase que modela el segundo Ensamblador que hay en la mecanismo
class Ensamblador1(threading.Thread):

    def __init__(self, tipoPieza, tiempo, listaCantTipo):
        self.tipoPieza = tipoPieza
        self.tiempo = tiempo
        self.listaCantTipo = listaCantTipo
        self.listaPiezasRecolectadas = []
        threading.Thread.__init__(self)

    #funcion que crea piezas cada cierto tiempo. crear las piezas si en la banda hay las piezas correspondientes
    def crearPiezaEnsamblador(self, i):

        global contadorPiezas
        cantidadTotalPiezas = 0
        for np in self.listaCantTipo:
            cantidadTotalPiezas = cantidadTotalPiezas + np[1]

        tupla = self.listaCantTipo[i]
        tipoPiezaS = tupla[0]
        cantidadPiezasS = tupla[1]

        j = 0
        while j < len(listaPiezasEnsamblador):

            piezaP = listaPiezasEnsamblador[j]
            if tipoPiezaS == piezaP.getTipoPieza():
                cuantasPiezas = 0
                for k in self.listaPiezasRecolectadas:
                    if k.getTipoPieza() == piezaP.getTipoPieza():
                        cuantasPiezas = cuantasPiezas + 1

                if cuantasPiezas < cantidadPiezasS:

                    self.listaPiezasRecolectadas.append(piezaP)
                    del listaPiezasEnsamblador[j]
                break
            j = j + 1
        if len(self.listaPiezasRecolectadas)==cantidadTotalPiezas:
            nuevaPieza = Pieza(self.tipoPieza)
            if entro:
                semaforo.acquire()
            listaPiezasEnsamblador1.append(nuevaPieza)
            contadorPiezas = contadorPiezas + 1
            print("Se crea la pieza: "+str(contadorPiezas)+ " con id: "+nuevaPieza.getIdentificador())
            del self.listaPiezasRecolectadas[0:len(self.listaPiezasRecolectadas)]
            if revisaPiezasCreadas():
                global mataHilos
                mataHilos = False
            time.sleep(self.tiempo)

    #funcion que se ejecuta hasta que se cunple la condicion
    def run (self):
        i = 0
        while mataHilos:
            if i == len(self.listaCantTipo):
                i = 0
            self.crearPiezaEnsamblador(i)
            i = i + 1

    def getTiempo(self):
        return self.tiempo


#clase que modela a un empaquetador.
class Empaquetador(threading.Thread):

    def __init__(self, tipoPieza, tipoPiezaEntrada, tiempo, tamPaquete):
        self.tiempo = tiempo
        self.tipoPieza = tipoPieza
        self.tamPaquete = tamPaquete
        self.listaPiezasPaquete = []
        self.tipoPiezaEntrada = tipoPiezaEntrada
        threading.Thread.__init__(self)

    #crea paquetes dependiendo de las especificaciones
    def crearPaquete(self):
        global entro
        i = 0
        entro = True
        while i < len(listaPiezasEnsamblador1):
            piezaP = listaPiezasEnsamblador1[i]
            if piezaP.getTipoPieza() == self.tipoPiezaEntrada:

                self.listaPiezasPaquete.append(piezaP)
                del listaPiezasEnsamblador1[i]

            if len(self.listaPiezasPaquete) == self.tamPaquete:
                nuevoPaquete = Paquete(self.tipoPieza, self.listaPiezasPaquete)
                print("Se creo el paquete:"+str(nuevoPaquete.getIdentificador()))
                listaPaqueteFinalizados.append(nuevoPaquete)
                del self.listaPiezasPaquete[0:len(self.listaPiezasPaquete)]

            if revisaPiezasCreadas():
                global mataHilos
                mataHilos = False

            i = i + 1
        entro = False
        semaforo.release()

    #funcion que se ejecuta hasta que se cumple la condicion de finalizar
    def run (self):

        while mataHilos:
            self.crearPaquete()

#clase que modela a un empaquetador.
class Empaquetador1(threading.Thread):

    def __init__(self, tipoPieza, tipoPiezaEntrada, tiempo, tamPaquete):
        self.tiempo = tiempo
        self.tipoPieza = tipoPieza
        self.tamPaquete = tamPaquete
        self.listaPiezasPaquete = []
        self.tipoPiezaEntrada = tipoPiezaEntrada
        threading.Thread.__init__(self)

    #crea paquetes dependiendo de las especificaciones
    def crearPaquete(self):

        global entro
        entro = True
        i = 0
        while i < len(listaPiezasEnsamblador1):
            piezaP = listaPiezasEnsamblador1[i]
            if piezaP.getTipoPieza() == self.tipoPiezaEntrada:
                self.listaPiezasPaquete.append(piezaP)
                del listaPiezasEnsamblador1[i]

            if len(self.listaPiezasPaquete) == self.tamPaquete:
                nuevoPaquete = Paquete(self.tipoPieza, self.listaPiezasPaquete)
                print("Se creo el paquete:"+str(nuevoPaquete.getIdentificador()))
                listaPaqueteFinalizados.append(nuevoPaquete)
                del self.listaPiezasPaquete[0:len(self.listaPiezasPaquete)]

            if revisaPiezasCreadas():
                global mataHilos
                mataHilos = False

            i = i + 1
        semaforo.release()
        entro = False

    def run (self):
        while mataHilos:
            self.crearPaquete()

#funcion que se ejecuta hasta que se cumple la condicion de finalizar
def revisaPiezasCreadas():

    if contadorPiezas >= 200:
        return True
    else:
        return False

#funcion que crea el ejercicio B
def ejercicioA():
    #productor de tipos A,B,C y D. se crean cada 2 segundos
    p = Productor("A", 2)
    p1 = Productor("B", 2)
    p2 = Productor("C", 2)
    p3 = Productor("D", 2)
    #Ensambladores de tipo E y F, se crean paquetes cada 2 segundos, las listas representan los tipos de piezas
    #y la cantidad que necesita
    ensamblador1 = Ensamblador("E", 2, [("A", 2), ("B", 2)])
    ensamblador2 = Ensamblador1("F", 2, [("C", 2), ("E", 1)])
    #Empaquetador que crea paquetes de tipo P y Q, necesita piezas de tipo F y D, los crea cada 0 sengundos y
    #para crear un paquete necesita 5 y 10 piezas
    empaquetador1 = Empaquetador("P", "F", 0, 5)
    empaquetador2 = Empaquetador1("Q", "D", 0, 10)

    #inicia los hilos
    p.start()
    p1.start()
    p2.start()
    p3.start()
    ensamblador1.start()
    ensamblador2.start()
    empaquetador1.start()
    empaquetador2.start()


ejercicioA()
