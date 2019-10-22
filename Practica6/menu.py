import pymysql
import hashlib

class Usuarios(object):

    def __init__(self, nombre, contrasena):
        self.nombre = nombre
        self.contrasena = contrasena
        self.idUsuario = -1

    def setIdUsuario(self, idUsuario):
        self.idUsuario = idUsuario

    def getIdUsuario(self):
        return self.idUsuario

    def getNombre(self):
        return self.nombre

    def getContrasena(self):
        return self.contrasena

def conectarBD():
    try:
        conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="Coco27+1", db="Practica6")
        return conn
    except:
        print("Error en la conexion de la BD")
        exit(0)

def desConectarBD(conn):
    conn.commit()
    conn.close()

def cifrar_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

#----------------------- REGISTRAR USUARIO-----------------------
def verificarNombreUsuarios(nombreDado):
    conn = conectarBD()
    try:

        cursor = conn.cursor()
        cursor.execute("SELECT (nombre) FROM Jugador")

        #fetchone()
        for nombre in cursor.fetchall():
            if nombreDado == nombre[0]:
                #print(nombre)
                #desConectarBD(conn)
                return True
    except:
        print("Saliendo error en la base")
        exit(0)
    finally:
        desConectarBD(conn)
    return False

def registarUsuarioBD(usuario):
    conn = conectarBD()
    try:
        cursor = conn.cursor()
        contrasena = usuario.getContrasena()
        contrasena1 = cifrar_string(contrasena)
        cursor.execute("INSERT INTO Jugador (nombre, password) VALUES (%s, %s)", (usuario.getNombre(), contrasena1))
    except:
        print("Saliendo error en la base")
        exit(0)
    finally:
        desConectarBD(conn)


def solicitarDatosUsuario():
    nombre = input("Nombre de usuario\n")
    contrasena = input("Contrasena\n")
    if not verificarNombreUsuarios(nombre):
        usuario = Usuarios(nombre, contrasena)
        return usuario
    else:
        return None


#----------------------- REGISTRAR USUARIO-----------------------

#----------------------- INGRESAR-----------------------
def solicitarDatosUsuarioRegistro():
    nombre = input("Nombre de usuario\n")
    contrasena = input("Contrasena\n")
    usuario = Usuarios(nombre, contrasena)
    return usuario

def verificarUsuario(usuario):
    conn = conectarBD()
    try:
        cursor = conn.cursor()
        contrasena = cifrar_string(usuario.getContrasena())
        cursor.execute("SELECT pk_id_jugador, nombre, password FROM Jugador WHERE nombre = %s AND password = %s",(usuario.getNombre(), contrasena,) )

        #fetchone()
        record = cursor.fetchall()

        for nombre in record:
            usuario = Usuarios(nombre[1], nombre[2])
            usuario.setIdUsuario(int(nombre[0]))
            return True, usuario
        return False, None
    except:
        print("Error en la base")
        exit(0)
    finally:
        desConectarBD(conn)


#----------------------- INGRESAR-----------------------

#----------------------- Busqueda jugadores para crear partida -----------------------
def busquedaJugadoresCrearPartida(usuario):
    conn = conectarBD()
    cursor = conn.cursor()
    contrasena = cifrar_string(usuario.getContrasena())
    cursor.execute("SELECT pk_id_jugador, nombre FROM Jugador WHERE nombre != %s", (usuario.getNombre()))
    #fetchone()
    record = cursor.fetchall()
    desConectarBD(conn)
    return record
#----------------------- Busqueda jugadores para crear partida -----------------------

#----------------------- Guardar tablero inicial -----------------------
def guardarTableroInicial(tablero, idCreador, idOponente):

    conn = conectarBD()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Partida "+
        "(tablero_cifrado, fk_id_jugador_en_turno, fk_id_creador, fk_id_oponente) "+
        "VALUES (%s, %s, %s, %s)", (tablero, idCreador, idCreador, idOponente, ))

        cursor.execute("SELECT LAST_INSERT_ID()")
        record = cursor.fetchone()
        return record[0]
    except:
        print("Error en la base")
        exit(0)
    finally:
        desConectarBD(conn)
#----------------------- Guardar tablero inicial -----------------------

#----------------------- tablero lista a tablero string -----------------------

def tableroListaToTableroString(tableroLista):
    salida = ""
    for fila in tableroLista:
        for col in fila:
            salida = salida + col + ","
        salida = salida[0:len(salida)-1]
        salida = salida + "|"
    salida = salida[0:len(salida)-1]
    return salida

#----------------------- tablero lista a tablero string -----------------------

#----------------------- tablero string a tablero lista -----------------------
def tableroStringToTableroLista(tableroString):
    listaColumnas = []
    columnas = tableroString.split("|")
    for col in columnas:
        listaFilas = []
        filas = col.split(",")
        for fil in filas:
            listaFilas.append(fil)
        listaColumnas.append(listaFilas)
    return listaColumnas
#----------------------- tablero string a tablero lista -----------------------

#----------------------- imprimir tablero lista -----------------------
def imprimirTableroLista(listaTablero):

    tableroString = ""
    for col in listaTablero:
        for fila in col:
            tableroString = tableroString + fila + "\t"
        tableroString = tableroString + "\n"
    print("\n"+tableroString)
#----------------------- imprimir tablero lista -----------------------

#----------------------- jugar -----------------------
def jugarPartida(listaTablero, indiceColumna, turno):

    j = 0
    while j < len(listaTablero):

        if j == 0 and listaTablero[j][indiceColumna] != "-":
            print("Seleccionar otro numero")
            j = -1
            return listaTablero, turno, j
            #break

        elif listaTablero[j][indiceColumna] != "-":
            if turno:
                listaTablero[j-1][indiceColumna] = "1"
                turno = not turno
            else:
                listaTablero[j-1][indiceColumna] = "2"
                turno = not turno
            return listaTablero, turno, j-1
            #break
        elif j == 5:
            if turno:
                listaTablero[j][indiceColumna] = "1"
                turno = not turno
            else:
                listaTablero[j][indiceColumna] = "2"
                turno = not turno
            return listaTablero, turno, j
            #break

        j = j + 1
    j = -1
    return listaTablero, turno, j
#----------------------- jugar -----------------------

#----------------------- busca ganador -----------------------
def verificaGanador(listaTablero, i, j, numeroTurno):

    #verifica Diagonal Arriba Derecha
    contadorVueltas = 0
    encontrados = 0
    k = j
    l = i
    while contadorVueltas <= 4 and l <= 6 and k >= 0:
        if listaTablero[k][l] == str(numeroTurno):
            encontrados = encontrados + 1
        else:
            break
        if encontrados == 4:
            return True
        k = k - 1
        l = l + 1
        contadorVueltas = contadorVueltas + 1

    #verifica Derecha
    contadorVueltas = 0
    encontrados = 0
    l = i
    while contadorVueltas <= 4 and l <= 6:
        if listaTablero[j][l] == str(numeroTurno):
            encontrados = encontrados + 1
        else:
            break
        if encontrados == 4:
            return True
        l = l + 1

    #verificar Diagonal Abajo Derecha
    contadorVueltas = 0
    encontrados = 0
    l = i
    k = j
    while contadorVueltas <= 4 and l <= 6 and k <= 5:
        if listaTablero[k][l] == str(numeroTurno):
            encontrados = encontrados + 1
        else :
            break
        if encontrados == 4:
            return True
        l = l + 1
        k = k + 1

    #verifica abajo
    contadorVueltas = 0
    encontrados = 0
    k = j
    while contadorVueltas <= 4 and k <= 5:
        if listaTablero[k][i] == str(numeroTurno):
            encontrados = encontrados + 1
        else :
            break
        if encontrados == 4:
            return True
        k = k + 1

    #verifica Diagonal Abajo Izquierda
    contadorVueltas = 0
    encontrados = 0
    k = j
    l = i
    while contadorVueltas <= 4 and k <= 5 and l >= 0:
        if listaTablero[k][l] == str(numeroTurno):
            encontrados = encontrados + 1
        else :
            break
        if encontrados == 4:
            return True
        k = k + 1
        l = l - 1

    #verificar Izquierda
    contadorVueltas = 0
    encontrados = 0
    l = i
    while contadorVueltas <= 4 and l >= 0:
        if listaTablero[j][l] == str(numeroTurno):
            encontrados = encontrados + 1
        else:
            break
        if encontrados == 4:
            return True
        l = l - 1

    #verificar Diagonal Izquierda Arriba
    contadorVueltas = 0
    encontrados = 0
    k = j
    l = i
    while contadorVueltas <= 4 and k >= 0 and l >= 0:
        if listaTablero[k][l] == str(numeroTurno):
            encontrados = encontrados + 1
        else:
            break
        if encontrados == 4:
            return True
        l = l - 1
        k = k - 1

    return False
#----------------------- busca ganador -----------------------

#----------------------- VALIDA EMPATE -----------------------

def validaEmpate(listaTablero):
    for fila in listaTablero:
        for col in fila:
            if col == "-":
                return False
    return True

#----------------------- VALIDA EMPATE -----------------------


#----------------------- guardar partida -----------------------
def guardaPartida(finalizo, tableroLista, idJugadorTurno, resultadoEnumInt, idPartida):

    conn = conectarBD()
    try:
        cursor = conn.cursor()
        tableroString = tableroListaToTableroString(tableroLista)
        if finalizo:
            cursor.execute("UPDATE Partida SET tablero_cifrado = %s, fk_id_jugador_en_turno = %s, resultado = %s "+
            "WHERE pk_id_partida = %s", (tableroString, idJugadorTurno, resultadoEnumInt, idPartida))
        else:
            cursor.execute("UPDATE Partida SET tablero_cifrado = %s, fk_id_jugador_en_turno = %s "+
            "WHERE pk_id_partida = %s", (tableroString, idJugadorTurno, idPartida))

    except:
        print("Error en la base")
        exit(0)
    finally:
        desConectarBD(conn)


#----------------------- guardar partida -----------------------

#----------------------- ver partida usuario -----------------------
def verPartidas(usuario):
    conn = conectarBD()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Partida WHERE fk_id_creador = %s", (str(usuario.getIdUsuario())))
        #fetchone()
        record = cursor.fetchall()

        listaSalida = []
        for fila in record:
            if fila[5] == None:
                listaSalida.append(fila)

        return listaSalida
    except:
        print("Error en la base")
        exit(0)
    finally:
        desConectarBD(conn)

#----------------------- ver partida usuario -----------------------

#----------------------- Busqueda jugadores por id -----------------------
def busquedaJugadoresPorId(idUsuarioString):
    conn = conectarBD()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT pk_id_jugador, nombre FROM Jugador WHERE pk_id_jugador = %s", (idUsuarioString))
        #fetchall()
        record = cursor.fetchone()
        return record
    except:
        print("Error en la base")
        exit(0)
    finally:
        desConectarBD(conn)

#----------------------- Busqueda jugadores por id -----------------------

#----------------------- estadisticas -----------------------
def estadisticas(usuario):
    conn = conectarBD()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Partida WHERE fk_id_creador = %s", (str(usuario.getIdUsuario())))
        #fetchone()
        record = cursor.fetchall()
        listaSalida = []
        for fila in record:
            if fila[5] != None:
                listaSalida.append(fila)

        return listaSalida
    except:
        print("Error en la base")
        exit(0)
    finally:
        desConectarBD(conn)

#----------------------- estadisticas -----------------------

def menuPartida(usuario):

    print("\n-----------\tBienvenido "+usuario.getNombre()+"\t\t-----------")
    entrada = True
    while entrada:
        opcion = input("\n1) Crear una partida\n2) Jugar una partida\n3) Consultar estadísticas\n4) Salir\n")

        if opcion == "1":
            print("\nCrear una partida\nSeleccione el indice del jugador con el que desea jugar\n")
            listaJugadores = busquedaJugadoresCrearPartida(usuario)
            i = 0
            for jugador in listaJugadores:
                print(str(i)+"-"+jugador[1])
                i = i + 1
            indiceJugador = -1
            try:
                indiceJugador = int(input("\nIndice del jugador\n"))
            except ValueError:
                print("\nOppps! No es un indice.")
                continue

            usuarioRival = Usuarios(listaJugadores[indiceJugador][1], "SIN RESULTADO")
            usuarioRival.setIdUsuario(listaJugadores[indiceJugador][0])
            print("Jugara con "+listaJugadores[indiceJugador][1])

            if indiceJugador < len(listaJugadores):
                print("\nSe jugara una partida con el jugador "+listaJugadores[indiceJugador][1])
                tablero = "-,-,-,-,-,-,-|-,-,-,-,-,-,-|-,-,-,-,-,-,-|-,-,-,-,-,-,-|-,-,-,-,-,-,-|-,-,-,-,-,-,-"
                indiceBD = guardarTableroInicial(tablero, usuario.getIdUsuario(), listaJugadores[indiceJugador][0])

                listaTablero = tableroStringToTableroLista(tablero)

                turno = True
                seguirJugando = True
                while seguirJugando:

                    imprimirTableroLista(listaTablero)

                    indiceColumna = -1
                    solicitarNumero = True
                    while solicitarNumero:
                        try:
                            indiceColumna = int(input("\nIngrese un numero mayor o igual que 0 y menor o igual que 6, para indicar la columna. O 9 para guardar y salir\n"))
                            solicitarNumero = False
                        except ValueError:
                            print("\nOppps! No es un numero.")

                    if indiceColumna >= 0 and indiceColumna <= 6:
                        listaTemporalJuego = jugarPartida(listaTablero, indiceColumna, turno)
                        listaTablero = listaTemporalJuego[0]
                        turno = listaTemporalJuego[1]
                        numTurno = -1
                        if turno:
                            numTurno = 2
                        else:
                            numTurno = 1
                        if listaTemporalJuego[2] != -1:
                            gano = verificaGanador(listaTablero, indiceColumna, listaTemporalJuego[2], numTurno)
                            empate = validaEmpate(listaTablero)
                            if empate:
                                imprimirTableroLista(listaTablero)
                                seguirJugando = False
                                print("la partida se empato")
                                idTurno = -1
                                if turno:
                                    idTurno = usuarioRival.getIdUsuario()
                                else:
                                    idTurno = usuario.getIdUsuario()
                                guardaPartida(True, listaTablero, idTurno, 3, indiceBD)
                            elif gano:
                                imprimirTableroLista(listaTablero)
                                seguirJugando = False
                                idJugadorTurno = -1
                                resultado = -1
                                if turno:
                                    print("Gano "+usuarioRival.getNombre())
                                    idJugadorTurno = usuarioRival.getIdUsuario()
                                    resultado = 2
                                else:
                                    print("Gano "+usuario.getNombre())
                                    idJugadorTurno = usuario.getIdUsuario()
                                    resultado = 1

                                guardaPartida(True, listaTablero, idJugadorTurno, resultado, indiceBD)

                    elif indiceColumna == 9:
                        seguirJugando = False
                        idJugadorTurno = None
                        if turno:
                            idJugadorTurno = usuario.getIdUsuario()
                        else:
                            idJugadorTurno = usuarioRival.getIdUsuario()
                        guardaPartida(False, listaTablero, idJugadorTurno, None, indiceBD)
                    else :
                        print("\nOppps! Numero incorrecto.")

            else:
                print("\nIndice incorrecto")

        elif opcion == "2":
            print("Jugar una partida\nSeleccionar una partida pendiente\n")
            listaPartidas = verPartidas(usuario)
            i = 0
            for fila in listaPartidas:
                nombreRival = busquedaJugadoresPorId(str(fila[4]))
                print(str(i)+") nombre oponente "+nombreRival[1])
                i = i + 1

            solicitarNumero = True
            while solicitarNumero:
                try:
                    indiceColumna = int(input("\nSeleccione el indice de la partida a jugar\n"))
                    solicitarNumero = False
                except ValueError:
                    print("\nOppps! No es un numero.")

            nombreRival = None
            if indiceColumna < len(listaPartidas):
                nombreRival = busquedaJugadoresPorId( str(listaPartidas[indiceColumna][4]) )
                print("Jugara la partida "+str(indiceColumna)+" con el rival "+nombreRival[1])


                listaTablero = tableroStringToTableroLista(listaPartidas[indiceColumna][1])
                indiceBD = int(listaPartidas[indiceColumna][0])

                turno = True
                if listaPartidas[indiceColumna][2] == usuario.getIdUsuario():
                    turno = True
                else:
                    turno = False
                seguirJugando = True
                while seguirJugando:

                    imprimirTableroLista(listaTablero)

                    indiceColumna = -1
                    solicitarNumero = True
                    while solicitarNumero:
                        try:
                            indiceColumna = int(input("\nIngrese un numero mayor o igual que 0 y menor o igual que 6, para indicar la columna. O 9 para guardar y salir\n"))
                            solicitarNumero = False
                        except ValueError:
                            print("\nOppps! No es un numero.")

                    if indiceColumna >= 0 and indiceColumna <= 6:
                        listaTemporalJuego = jugarPartida(listaTablero, indiceColumna, turno)
                        listaTablero = listaTemporalJuego[0]
                        turno = listaTemporalJuego[1]
                        numTurno = -1
                        if turno:
                            numTurno = 2
                        else:
                            numTurno = 1
                        if listaTemporalJuego[2] != -1:
                            gano = verificaGanador(listaTablero, indiceColumna, listaTemporalJuego[2], numTurno)
                            empate = validaEmpate(listaTablero)
                            if empate:
                                imprimirTableroLista(listaTablero)
                                seguirJugando = False
                                print("la partida se empato")
                                idTurno = -1
                                if turno:
                                    idTurno = usuarioRival.getIdUsuario()
                                else:
                                    idTurno = usuario.getIdUsuario()
                                guardaPartida(True, listaTablero, idTurno, 3, indiceBD)
                            elif gano:
                                imprimirTableroLista(listaTablero)
                                seguirJugando = False
                                idJugadorTurno = -1
                                resultado = -1
                                if turno:
                                    print("Gano "+nombreRival[1])
                                    idJugadorTurno = int(nombreRival[0])
                                    resultado = 2
                                else:
                                    print("Gano "+usuario.getNombre())
                                    idJugadorTurno = usuario.getIdUsuario()
                                    resultado = 1

                                guardaPartida(True, listaTablero, idJugadorTurno, resultado, indiceBD)

                    elif indiceColumna == 9:
                        seguirJugando = False
                        idJugadorTurno = None
                        if turno:
                            idJugadorTurno = usuario.getIdUsuario()
                        else:
                            idJugadorTurno = int(nombreRival[0])
                        guardaPartida(False, listaTablero, idJugadorTurno, None, indiceBD)

                    else :
                        print("\nOppps! Numero incorrecto.")

            else:
                print("Indice incorrecto")

        elif opcion == "3":

            listaPartidas = estadisticas(usuario)
            print("\n")
            ganados = 0
            perdidos = 0
            empatados = 0
            for partidas in listaPartidas:
                if partidas[5] == "gana":
                    ganados = ganados + 1
                    nombreRival = busquedaJugadoresPorId( str(partidas[4]) )
                    print("La partida se jugo contra: " + nombreRival[1]+" y se gano :)")
                elif partidas[5] == "pierde":
                    perdidos = perdidos + 1
                    nombreRival = busquedaJugadoresPorId( str(partidas[4]) )
                    print("La partida se jugo contra: " + nombreRival[1]+" y se perdio :(")
                elif partidas[5] == "empate":
                    empatados = empatados + 1
                    nombreRival = busquedaJugadoresPorId( str(partidas[4]) )
                    print("La partida se jugo contra: " + nombreRival[1]+" y se empato :|")



            print("\nJuegos ganados: "+str(ganados)+"\nJuegos perdidos: "+str(perdidos)+"\nJuegos empatados: "+str(empatados))


        elif opcion == "4":
            print("opcion 4")
            entrada = False



def menuIngreso():

    entrar = True
    while (entrar):
        print("\n-----------\tConecta 4\t-----------\n")
        opcion = input("1) Registrar jugador\n2) Ingresar sistema\n3) Salir\n")
        if opcion == "1":
            print("\nSe registrara un nuevo jugador\n")
            usuarioNuevo = solicitarDatosUsuario()
            if usuarioNuevo != None:
                registarUsuarioBD(usuarioNuevo)
            else:
                print("\nEste usuario ya existe")

        elif opcion == "2":
            print("\nSe ingresara al sistema\n")
            usuarioSolicitante = solicitarDatosUsuarioRegistro()
            datosEntrada = verificarUsuario(usuarioSolicitante)

            if datosEntrada[0]:
                menuPartida(datosEntrada[1])
            else:
                print("\nno entra")

        elif opcion == "3":
            entrar = False
            print("Saliendo...")
        else:
            print("Opcion incorrecta")
        print("---------------------------------------")


menuIngreso()
