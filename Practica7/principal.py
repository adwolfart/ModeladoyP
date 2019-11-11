from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import numpy

def creaImagen():
    img = Image.new('RGBA', (125, 125), "white")

    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 0), (74, 24)), fill="black")
    draw.rectangle(((25, 25), (99, 49)), fill="black")
    draw.rectangle(((50, 50), (124, 74)), fill="black")
    draw.rectangle(((0, 75), (49, 124)), fill="black")
    img.save('image.png')

def procesaImagen(nombreImagen):
    ima = Image.open(nombreImagen)
    np_ima = numpy.array(ima)
    altura = len(np_ima) / 50
    base = len(np_ima[0]) / 50
    if (len(np_ima) % 50 != 0 or len(np_ima[0]) % 50 != 0):
        print("Altura y base mala")
        exit(0)

    arrTablero = []
    i = 25
    while i < len(np_ima):
        j = 25
        arrFila = []
        while j < len(np_ima[i]):
            if np_ima[i][j][0] == 0:
                arrFila.append(1)
            else:
                arrFila.append(0)
            j = j + 50
        arrTablero.append(arrFila)
        i = i + 50

    return arrTablero


def procesaTexto(textoVertical, textoHorizontal):
    arrVertical = []
    arrHorizontal = []

    sepComasTexVer = textoVertical.split(",")
    for sepComas in sepComasTexVer:
        sepGuionTexVer = sepComas.split("_")
        arrGuion = []
        for sepGuion in sepGuionTexVer:
            arrGuion.append(sepGuion)
        arrVertical.append(arrGuion)

    sepComasTexHor = textoHorizontal.split(",")
    for sepComas in sepComasTexHor:
        sepGuionTexHor = sepComas.split("_")
        arrGuion = []
        for sepGuion in sepGuionTexHor:
            arrGuion.append(sepGuion)
        arrHorizontal.append(arrGuion)

    return arrVertical, arrHorizontal

def validaAcostado(arrTab, arrHor):

    nuevoTab = cambiarArreglo(arrTab)

    numVal = len(arrHor)
    numFilTab = len(nuevoTab)

    return nuevoTab, arrHor


def validacion(fila, validaciones):

    contador = 0
    i = 0
    while i < len(validaciones):
        indiceFila = 0
        numValidacion = validaciones[i]
        j = 0
        while j < len(fila):
            if numValidacion == 0:
                indiceFila = j
                break
            if fila[j] == 1:
                contador = contador + 1
                fila[j] = 2
                numValidacion = numValidacion - 1
            j = j + 1

        if j < len(fila):
            if fila[j] == 1:
                return False
        if numValidacion != 0:
            return False
        i = i + 1

    return True




def cambiarArreglo(arrTab):

    altura = len(arrTab)
    base = len(arrTab[0])

    arrSalida = []

    i = 0
    while i < base:
        arrTempo = []
        j = 0
        while j < altura:
            arrTempo.append(-1)
            j = j + 1
        arrSalida.append(arrTempo)
        i = i + 1

    i = 0
    while i < len(arrTab):
        j = 0
        while j < len(arrTab[0]):
            arrSalida[j][i]=arrTab[i][j]
            j = j + 1
        i = i + 1
    return arrSalida


def validaImagen(nomIma, lateral, arriba):

    arrTab = procesaImagen(nomIma)
    resultados = procesaTexto(lateral, arriba)
    arrVer = resultados[0]
    arrHor = resultados[1]
    arrValidaciones = validaAcostado(arrTab, arrHor)
    #nuevoTab =  arrValidaciones[0]
    nuevoTab =  cambiarArreglo(arrTab)
    vali = arrHor
    listVali = []
    for arrVal in vali:
        listTemp = []
        for val in arrVal:
            valTemp = int(val)
            listTemp.append(valTemp)
        listVali.append(listTemp)

    i = 0
    while i < len(nuevoTab):
        valor = validacion(nuevoTab[i], listVali[i])
        if not valor:
            print("no valido")
            return False
        i = i + 1

    vali1 = arrVer
    listVali1 = []
    for arrVal in vali1:
        listTemp = []
        for val in arrVal:
            valTemp = int(val)
            listTemp.append(valTemp)
        listVali1.append(listTemp)

    i = 0
    while i < len(arrTab):
        valor = validacion(arrTab[i], listVali1[i])
        if not valor:
            print("no valido")
            return False
        i = i + 1
    return True
