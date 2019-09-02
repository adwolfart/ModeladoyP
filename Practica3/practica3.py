
#metodo que busca el número más repetido en una matriz
#parametro en una matriz de números
def mas_repetido(matriz):
    #try por si sucede un error poder manejarlo
    try:
        #el diccionario donde guardaremos los números y la frecuencia como van apareciendo
        diccionario = {}
        #recorremos la matris
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                #buscamos en el diccionario el número en turno de la matriz
                #lo guardamos en una variable
                valor = diccionario.get(matriz[i][j])
                #si exite el numero dentro del diccionario buscamos su valor y le agregamos 1
                if valor != None:
                    valor = valor + 1
                    diccionario.update({matriz[i][j]:valor})
                else: # si no existe el número dentro del diccionario lo añadimos con valor a 1
                    diccionario.update({matriz[i][j]:1})
        #buscamos el número más alto en el diccionario
        mas_alto(diccionario)
    except:
        print("Error")

#funcion que busca el número más grande dentro de un diccionario
#parametro es un diccionario
def mas_alto(diccionario):
    llave = -1
    valor = -1
    #recorremos el diccionario
    for key in diccionario:
        #si el valor del diccionario es más grande a la variable valor guardamos la llave y el valor
        if valor < diccionario[key]:
            llave = key
            valor = diccionario[key]
    #imprimimos la llave
    print(llave)

#--------------- 2B-----------------
def condensa(cadena):
    #diccionario para guardar el resultado
    diccionario = {}

    #llevar el contador de caracteres iguales continuos
    caracterTam = 0
    #caracter actual
    caracterActual = ''
    #recorre la palabra
    for i in range(len(cadena)):
        #si el caracter guardado es diferente al caracter actual de la cadena
        #si es diferente el caracter almacenado al caracter actual de la cadena
        #añade al diccionario el caracter nuevo y lo inicialoza a 1
        if caracterActual != cadena[i]:
            caracterActual = cadena[i]
            caracterTam = 1
            diccionario.update({cadena[i]:caracterTam})
        else : #si es el mismo caracter actualiza el caracter y le añade uno a su valor
            caracterTam = caracterTam + 1
            diccionario.update({cadena[i]:caracterTam})

    print("[")
    for key in diccionario:
        print("[", "'", key, "'", ", ", diccionario[key], "]")
    print("]")



#----------------3A--------------------

#funcion recursiva que toma una lista, un indice y donde guardaremos el resultado
def triangulo_linea(lista, indice, resultado):
    #si nuestro indice ha recorrido toda la lista nos devuelve el resultado
    tamLista = len(lista)
    if indice == tamLista:
        resultado.append(1)
        return resultado
    else:
        if indice == 0: # si es el primer elemento guardaremos un 1 en la lista
            resultado.append(1)
            indice = indice + 1
            return triangulo_linea(lista, indice, resultado)
        else:# en otro caso suma el indice actual y el anterior de la lista y lo guarda en el resultado
            resultado.append(lista[indice]+lista[indice-1])
            indice = indice + 1
            return triangulo_linea(lista, indice, resultado)

#funcino recursiva que va guardando las listas que genera triangulo_linea en una listas
#el parametro son n = maxima linea, i = indice que vamos, resultado = donde guardamos el resultado
def triangulo(n, i, resultado):
    #si el indice ya es mayor que n regresamos el resultado
    if  i > n:
        return resultado
    else: # en otro caso
        if i == 1: # si i = 1 llamamos por primera vez a la funcino recursiva
            resultado.append([1])
            i = i + 1
            return triangulo(n, i, resultado)
        else:#llamamos a la funcion recursiva
            resultado.append(triangulo_linea(resultado[len(resultado)-1], 0, []))
            i = i + 1
            return triangulo(n, i, resultado)

#funcion no recursiva que llama a otra funcion recursiva
def triangulo_pascal(n):
    if n == 0:
        print([])
    else:
        print(triangulo(n, 1, []))


#----------------3B--------------------

#funcion que llama a los metodos recursivos
def subcadena(cadena):
    lista = []
    lista.append("")
    listaParam = []
    listaParam.append(lista)
    print(subcadenasRecursivaGeneral(cadena, 1, listaParam))

#funcion recursiva que llama a otra funcion recursiva para llenar una lista de listas
def subcadenasRecursivaGeneral(cadena, i, lista):
    if len(cadena) == i-1:
        return lista
    else:
        lista.append(subcadenasRecursiva(cadena, 0, i, []))
        return subcadenasRecursivaGeneral(cadena, i+1, lista)

#funcion recursiva que nos regresa la lista de caracteres de longitug de la diferencia de j - i
def subcadenasRecursiva(cadena, i, j, lista):
    if len(cadena) == j-1:
        return lista
    else:
        subcadena = cadena[i:j]
        lista.append(subcadena)
        return subcadenasRecursiva(cadena, i+1, j+1, lista)

    

#menu
def menu():
    try:
        entra = True
        while entra:
            print("\n1 para mas_repetido\n2 para condensa\n3 triangulo de pascal\n4 para subcadenas\n5 para salir\n")
            param = int(input("Introduce una opción:"))
            if param == 1:
                mas_repetido([[1, 2, 3, 4], [2, 6, 1], [2, 3, 3, 1, 1, 1]])
            elif param == 2:
                opcion2 = input("Introduce una cadena:")
                condensa(opcion2)
            elif param == 3:
                opcion3 = int(input("Introduce un número para el triangulo:"))
                triangulo_pascal(opcion3)
            elif param == 4:
                opcion4 = input("Introduce una cadena:")
                subcadena(opcion4)
            elif param == 5:
                entra = False
                print("Saliendo...")
            else:
                print("Entrada invalida\nSaliendo...")
    except:
        print("Entrada invalida.\nSaliendo...")

menu()
#subcadena("abcd")
#condensa("aabbaaazzzz")

#llamada a la función para buscar el número más repetido en una matriz
#mas_repetido([[1, 2, 3, 4], [2, 6, 1], [2, 3, 3, 1, 1, 1]])
