class BaseDeDatos(object):

    def __init__(self):
        self.valores = []
        self.atributos = []

    def crearBD(self, atributos):
        listaAtributos = atributos.replace(" ", "").split(",")
        for atri in listaAtributos:
            self.atributos.append(atri)
        return"Se creo la BD"

    def crearBDTxt(self, txt):

        txt = txt[:len(txt)-1]
        valores = txt.split("\n")
        atribustosOriginales = ""
        i = 0
        while i < len(valores):
            if i == 0:
                atribustosOriginales = valores[i]
                listaAtributos = atribustosOriginales.split("|")
                for atri in listaAtributos:
                    self.atributos.append(atri)
            else :
                listaTemporal = []
                valoresOriginales = valores[i]
                listaValores = valoresOriginales.split("|")
                for valor in listaValores:
                    listaTemporal.append(valor)
                self.valores.append(listaTemporal)
            i = i + 1

        return "Se creo la BD"

    def getAtributos(self):
        return self.atributos

    def anadirValores(self, listaNueva):
        self.valores.append(listaNueva)

    def setValores(self, listaRemplazo):
        self.valores = listaRemplazo

    def getValores(self):
        return self.valores

    def __str__(self):
        return self.atributos
