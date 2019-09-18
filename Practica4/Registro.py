from BaseDatos import BaseDeDatos

class Registro(object):

    #funcino que agrega nuevos registros a una bd
    def nuevoRegistro(self, registro, BD):

        listaRegistroNuevo = registro.split(",")

        if len(listaRegistroNuevo)!=len(BD.getAtributos()):
            return "NO se puede agregar nuevo registro"

        i = 0
        listaAtributosBD = BD.getAtributos()

        listaSalida = []
        for nr in listaRegistroNuevo:
            nr = str(nr).replace(" ", "")
            listaSalida.append(nr)
            i = i + 1

        BD.anadirValores(listaSalida)
        return "Registro agregado"

    def devolverRegistro(self, cadBusqueda, BD):

        listaRegreso = []

        #revisa que las busquedas no sobrepase los atributos de la BD
        listaCadBusqueda = cadBusqueda.split(",")
        if len(listaCadBusqueda) > len(BD.getAtributos()):
            return "Los atributos de la cadena de busqueda superan a los atributos de la BD"

        #revisa que los atributos de busqueda esten en los atributos de la bd
        for ab in listaCadBusqueda:
            listaAtributos = ab.replace(" ", "").split("=")
            if len(listaAtributos) != 2:
                return "Mal construida la cadena de busqueda"

            elementoCadBusqueda = listaAtributos[0]
            if not elementoCadBusqueda in BD.getAtributos():
                return "Variable de cadena de busqueda no se encuentra en los atributos de la BD"

        listaAtributosCad = []
        for asig in listaCadBusqueda:
            asig = asig.replace(" ", "")
            listaElementos = asig.split("=")
            i = 0
            while i < len(listaElementos):
                if i == 0:
                    listaAtributosCad.append(listaElementos[i])
                i = i + 1

        listaIndices = []
        for atributo in listaAtributosCad:
            i = 0
            while i < len(BD.getAtributos()):
                if BD.getAtributos()[i] == atributo:
                    listaIndices.append(i)
                i = i + 1

        listaDatos = []
        for asig in listaCadBusqueda:
            listaElem = asig.replace(" ","").split("=")
            listaDatos.append(listaElem[1])

        matrizDatos = []
        matrizDatos.append(listaIndices)
        matrizDatos.append(listaDatos)

        listaIndicesRegreso = []
        i = 0
        listaValoresBD = BD.getValores()
        while i < len(listaValoresBD):

            igualLinea = True
            j = 0
            while j < len(matrizDatos[0]):

                if listaValoresBD[i][matrizDatos[0][j]] != matrizDatos[1][j]:
                    igualLinea = False
                j = j + 1

            if igualLinea:
                listaIndicesRegreso.append(i)

            i = i + 1

        for i in listaIndicesRegreso:
            listaRegreso.append(listaValoresBD[i])

        salida = ""
        for lista in listaRegreso:
            salidaTemporal = ""
            for listaTemporal in lista:
                salidaTemporal = salidaTemporal + listaTemporal + "|"
            salidaTemporal = salidaTemporal[:len(salidaTemporal)-1]
            salida = salida + salidaTemporal+"\n"

        salida = salida[:len(salida)-1]

        listaRegreso = [salida, listaIndicesRegreso]

        return listaRegreso


    def eliminarRegistro(self, cadBusqueda, BD):

        listaIndices = Registro.devolverRegistro(self, cadBusqueda, BD)[1]

        listaValoresBD = BD.getValores()

        listaIndicesRegreso = []
        i = 0
        while i < len(listaValoresBD):
            if not i in listaIndices:
                listaIndicesRegreso.append(i)
            i = i + 1

        listaRegreso = []
        for indices in listaIndicesRegreso:
            listaRegreso.append(listaValoresBD[indices])

        BD.setValores(listaRegreso)

        return "Se han eliminado correctamente"


    def modificarRegistros(self, cadBusqueda, cadNueva, BD):

        listaAsignacion = cadNueva.replace(" ", "").split(",")
        listaAtributos = BD.getAtributos()
        if len(listaAtributos) < len(listaAsignacion):
            return "Los atributos de la cadena de remplazo superan a los atributos de la BD"

        for asig in listaAsignacion:
            listaElementos = asig.split("=")
            if len(listaElementos) != 2:
                return "Esta mal formada la cadena de remplazo"


        for asig in listaAsignacion:
            asig = asig.split("=")
            esta = False
            for atributo in listaAtributos:
                if atributo == asig[0]:
                    esta = True
            if not esta:
                return "No se encontro atributo de cadena de remplazo en los atributos de la BD"

        listaValoresAtributos = []
        i = 0
        while i < len(listaAtributos):
            for asig in listaAsignacion:
                listaElementos = asig.split("=")
                if not listaElementos[1] in listaValoresAtributos:
                    listaValoresAtributos.append(listaElementos[1])
            i = i + 1

        listaIndices = []
        for asig in listaAsignacion :
            listaElementos = asig.split("=")
            i = 0
            while i < len(listaAtributos):
                if listaElementos[0] == listaAtributos[i]:
                    listaIndices.append(i)
                i = i + 1

        matrizDatos = [listaIndices, listaValoresAtributos]

        listaUsu = BD.getValores()
        listaDatos = []
        listaIndicesUsuarios = Registro.devolverRegistro(self, cadBusqueda, BD)[1]

        i = 0
        while i < len(listaUsu):
            if i in listaIndicesUsuarios:
                j = 0
                while j < len(listaIndices):
                    listaUsu[i][listaIndices[j]] = listaValoresAtributos[j]
                    j = j + 1
            i = i + 1


        BD.setValores(listaUsu)
        return "Actualizacion correcta"

    def escribirArchivos(self, nomArch, BD):

        atributos = BD.getAtributos()
        salAtri = ""
        for atri in atributos:
            salAtri = salAtri + atri + "|"
        salAtri = salAtri[:len(salAtri)-1]

        salida = ""
        listaValores = BD.getValores()
        for valores in listaValores:
            salidaTemp = ""
            for valor in valores:
                salidaTemp = salidaTemp + valor + "|"
            salida = salida + salidaTemp[:len(salidaTemp)-1]+"\n"
        salAtri = salAtri +"\n"+salida
        f = open(nomArch, "w")
        f.write(salAtri)
        f.close()
        return "Escritura correcta"
