from Registro import Registro
from BaseDatos import BaseDeDatos


def menuSecundario(BD):
    registro = Registro()
    entra = True
    while entra :
        print("1.-Crear e insertar registro a BD\n2.-Devolver registro con busqueda\n"
        +"3.-Eliminar registro con busqueda\n4.-Modificar columnas\n5.-Escribir en txt\n"+
        "6.-Regresar")
        numero = None
        try:
            numero = int(input("Introduce una opcion: "))
        except Exception as e:
            numero = -1

        if numero == 1:
            canEntrada = input("Los valores de entrada deben ser separados por comas(,): ")
            print(registro.nuevoRegistro(canEntrada, BD), "\n")
        elif numero == 2:
            canEntrada = input("Los valores de busqueda deben ser separados por comas(,): ")
            print(registro.devolverRegistro(canEntrada, BD)[0], "\n")
        elif numero == 3:
            canEntrada = input("Los valores de busqueda para la eliminacion deben ser separados por comas(,): ")
            print(registro.eliminarRegistro(canEntrada, BD), "\n")
        elif numero == 4:
            canBusqueda = input("Los valores de busqueda para la modificacion deben ser separados por comas(,): ")
            canModificacion = input("Los valores de modificacion deben ser separados por comas(,): ")
            print(registro.modificarRegistros(canBusqueda, canModificacion, BD), "\n")
        elif numero == 5:
            nombreArch = input("Nombre del archivo: ")
            print(registro.escribirArchivos(nombreArch, BD))
        elif numero == 6:
            entra = False



def menu():
    entra = True
    while entra :
        print("1.-Crear BD\n2.-Restaurar BD\n3.-Salir")
        numero = None
        try:
            numero = int(input("Introduce una opcion: "))
        except Exception as e:
            numero = -1

        if numero == 1:
            atributos = input("Escribir los atributos de la BD separados por comas(,):")
            listaAtributos = atributos.replace(" ", "").split(",")
            bienConstruidos = True
            for atri in listaAtributos:
                if atri == "":
                    bienConstruidos = False

            if bienConstruidos:
                base = BaseDeDatos()
                base.crearBD(atributos)
                menuSecundario(base)
            else:
                print("Los atributos estan mal construidos")
        elif numero == 2:
            nomBD = input("Nombre del archivo donde se encuentra la BD:")
            f = open (nomBD, "r")
            atributosTxt = f.read()
            base = BaseDeDatos()
            base.crearBDTxt(atributosTxt)
            f.close()
            menuSecundario(base)

        elif numero == 3:
            print("Saliendo...")
            exit()










menu()
