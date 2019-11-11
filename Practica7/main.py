"""
La parte de crear la imagen (punto 1) esta basado en el codigo de la siguiente liga:
https://github.com/monuszko/nonogram/blob/master/core/puzzle.py
Los archivos de texto que contenga las validaciones deben ser da la siguiente forma

1_2, 2_2, 3, 2, 1
3, 3, 3, 2, 2

La primera linea son las validaciones que se encuentran arriba del tablero
La segunda linea son las validaciones que se encuentran en el constado del tablero

Solo funcionan con tableros cuadrados
"""

from itertools import combinations_with_replacement as comb_repl
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from principal import validaImagen

def rotated_lists(list_of_lists, reverse=False):

    if reverse:
        list_of_lists.reverse()
    return [list(ls) for ls in zip(*list_of_lists)]

def inserteveryfifth(lst, item):

    newlst = lst[:]
    insertion_points = [x for x in range(len(newlst)) if x % 5 == 0 and x != 0]
    for i in reversed(insertion_points):
        newlst.insert(i, item)
    return newlst


_UNK = '*'
_EMP = '.'
_BLK = '@'

class Line:

    def __init__(self, pos, orient, length, numbers):
        self.numbers = numbers
        self.pos = pos
        self.orient = orient
        self.length = length

        self.gaps = tuple([0] + [1] * (len(self.numbers) - 1) + [0])

        self.fspaces = self.length - (len(self.numbers) - 1+sum(self.numbers))
        self.combs = []

    def gencombs(self):

        if sum(self.numbers) == 0:
            self.combs = [_EMP * self.length]
            return

        spacedistrib = comb_repl(range(len(self.gaps)), self.fspaces)

        for distrib in spacedistrib:

            allocated = list(self.gaps)
            for gapindex in distrib:
                allocated[gapindex] += 1

            comb = _EMP * allocated[0]
            for block, space in zip(self.numbers, allocated[1:]):
                comb += ((block * _BLK) + (space * _EMP))
            self.combs.append(comb)

    def coords(self):

        return [self.i_to_xy(i) for i in range(self.length)]

    def i_to_xy(self, i):
        if self.orient == 'row':
            return (i, self.pos)
        return (self.pos, i)

    def findfixed(self, solved_line):

        self.combs = self.updated_combs(solved_line)

        changed = []
        if not self.combs:
            return changed

        for i in range(self.length):
            if solved_line[i] != _UNK:
                continue

            for comb in self.combs:
                if comb[i] != self.combs[0][i]:
                    break
            else:
                coords = self.i_to_xy(i)
                changed.append((coords, comb[i]))

        return changed

    def updated_combs(self, solved_line):
        solved_indices = [i for i, ch in enumerate(solved_line) if ch != _UNK]
        newcombs = []
        for comb in self.combs:
            for ind in solved_indices:
                if comb[ind] != solved_line[ind]:
                    break
            else:
                newcombs.append(comb)

        return newcombs

    def valid(self):
        if self.combs:
            return True
        return False

    def strnums(self, sep=' '):
        return sep.join([str(nr) for nr in self.numbers])

class Board:
    def __init__(self, rows, cols):
        # Load rows, cols and produce some metadata:
        self.rows = []
        self.cols = []
        self.solved = dict()
        self.height = len(rows)
        self.width = len(cols)
        for nr, row in enumerate(rows):
            self.rows.append(Line(nr, 'row', self.width, row))
        for nr, col in enumerate(cols):
            self.cols.append(Line(nr, 'col', self.height, col))
        # For guessing and solving via contradictions:
        self.backups = []

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def isfull(self):
        return len(self.solved) == self.height * self.width

    def solve(self, no_hints=False, legend='*.@',
              separators='|-+', no_grouping=False, hide_progress=False):

        for line in self.rows + self.cols:
            line.gencombs()


        progress = True
        while progress:

            progress = self.basicsolve()
            if not self.valid():
                print("no es valido")
                break
            if progress and not hide_progress:
                self.display(no_grouping, no_hints, legend, separators)
            if self.isfull():
                break

            guess = self.keepguessing()
            if guess is not None:
                progress = True
                x, y, color = guess[0][0] + 1, guess[0][1] + 1, guess[1]
                if not hide_progress:
                    msg = 'From contradiction: ({0}, {1}) is "{2}"'
                    print(msg.format(x, y, color))
                self.solved[guess[0]] = guess[1]

    def basicsolve(self):
        initially_solved = len(self.solved)
        tocheck = self.rows + self.cols
        while len(tocheck) > 0:
            line = tocheck.pop()
            solved_line = [self.solved.get(xy, _UNK) for xy in line.coords()]
            changed = line.findfixed(solved_line)
            for coords, color in changed:
                self.solved[coords] = color
                crossing = self.get_crossing(line, coords)
                if crossing not in tocheck:
                    tocheck.insert(0, crossing)
        return len(self.solved) > initially_solved

    def get_crossing(self, line, coords):
        if line.orient == 'row':
            return self.cols[coords[0]]
        return self.rows[coords[1]]

    def valid(self):
        if all(l.valid() for l in self.rows + self.cols):
            return True
        return False

    def display(self, no_grouping=False, no_hints=False,
                legend='*.@', separators='|-+'):
        VSEP, HSEP, CSEP = separators[0], separators[1], separators[2]

        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                if (x, y) in self.solved:
                    if self.solved[(x, y)] == _EMP:
                        line.append(legend[1])
                    else:
                        line.append(legend[2])
                else:
                    line.append(legend[0])
            lines.append(line)

        self.crearImagen(lines)

    def crearImagen(self, lines):
        height = len(lines)
        width = 0
        for line in lines:
            width = width + 1

        height = 50*height
        width = 50*width
        img = Image.new('RGBA', (height, width), "white")
        draw = ImageDraw.Draw(img)


        iniciaY1 = 0
        iniciaY2 = 50
        for line in lines:
            iniciaX1 = 0
            iniciaX2 = 50
            for cr in line:
                if "@" == cr:
                    draw.rectangle( ( (iniciaX1, iniciaY1), (iniciaX2, iniciaY2)), fill="black")
                iniciaX1 = iniciaX1 + 50
                iniciaX2 = iniciaX2 + 50
            iniciaY1 = iniciaY1 + 50
            iniciaY2 = iniciaY2 + 50

        iniciaY1 = 0
        for line in lines:
            draw.rectangle( ( (0, iniciaY1), (width+1, iniciaY1+1)), fill="red")
            iniciaY1 = iniciaY1 + 50

        iniciaX1 = 0
        for cr in lines[0]:
            draw.rectangle( ( (iniciaX1, 0), (iniciaX1+1, height+1)), fill="red")
            iniciaX1 = iniciaX1 + 50

        img.save('image.png')

def leerArchivos(nombre):
    f = open(nombre, "r")
    mensaje = f.read()
    arrMensaje = mensaje.split("\n")
    f.close()
    rows = arrMensaje[0]
    rows.replace(" ", "")
    arrRows = rows.split(",")
    #1_2,2_2,3,2,1
    listFinalRows = []
    for r in arrRows:
        rTemp = r.split("_")
        listTemp = []
        for rr in rTemp:
            listTemp.append(int(rr.strip()))
        listFinalRows.append(listTemp)

    cols = arrMensaje[1]
    cols.replace(" ", "")
    arrCols = cols.split(",")
    listFinalCols = []
    for r in arrCols:
        rTemp = r.split("_")
        listTemp = []
        for rr in rTemp:
            listTemp.append(int(rr.strip()))
        listFinalCols.append(listTemp)
    return listFinalRows, listFinalCols


def principal(nombre):
    listFinal = leerArchivos(nombre)
    board = Board(listFinal[1], listFinal[0])
    lines = board.solve()

if __name__ == '__main__':

    cadena = input("1) resolver nonograma a partir de un archivo de texto\n"
    +"2) verificar un nonograma a partir de un archivo de texto y una imagen\n")
    if cadena == "1":
        arch = input("Nombre del archivo\n")
        try:
            principal(arch)
        except:
            print("Nombre del archivo erroneo")
            exit(0)
    elif cadena == "2":
        try:

            nomIma = input("Nombre de la imagen\n")
            nomArch = input("Nombre del archivo\n")
            f = open(nomArch, "r")
            mensaje = f.read()
            arrMensaje = mensaje.split("\n")
            f.close()
            valor = validaImagen(nomIma, arrMensaje[1], arrMensaje[0])
            if valor:
                print("Imagen correcta")
            else:
                print("Imagen incorrecta")
        except:
            print("Error en el nombre de la imagen o en el nombre del archivo de texto")
            exit(0)

    else:
        print("Entrda incorrecta saliendo")
