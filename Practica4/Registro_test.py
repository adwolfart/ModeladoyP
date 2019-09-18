from Registro import Registro
from BaseDatos import BaseDeDatos

import unittest

class BaseDeDatos_test(unittest.TestCase):

    #Creacion de BD por txt y por parametros
    def test_creaBD(self):
        base = BaseDeDatos()
        self.assertEqual(base.crearBD("nombre, apellido, edad"), "Se creo la BD")

    def test_creaBDTxt(self):
        base = BaseDeDatos()
        self.assertEqual(base.crearBDTxt("hermanos"), "Se creo la BD")

    #agregarRegistro a una nueva BD
    def test_nuevoRegistro(self):
        base = BaseDeDatos()
        base.crearBD("nombre, apellido, edad")
        registro = Registro()
        self.assertEqual(registro.nuevoRegistro("arturo, de la Cruz, 25", base), "Registro agregado")

    #devolver registro por busqueda
    def test_devolverRegistro(self):
        base = BaseDeDatos()
        base.crearBD("numeroCuenta, correo, edad")
        registro = Registro()
        registro.nuevoRegistro("00000001, 00000001@ciencias.unam.mx, 25", base)
        registro.nuevoRegistro("00000002, 00000002@ciencias.unam.mx, 25", base)
        registro.nuevoRegistro("00000003, 00000003@ciencias.unam.mx, 20", base)
        registro.nuevoRegistro("00000004, 00000004@ciencias.unam.mx, 20", base)
        registro.nuevoRegistro("00000005, 00000005@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000006, 00000006@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000007, 00000007@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000008, 00000008@ciencias.unam.mx, 30", base)
        self.assertEqual(registro.devolverRegistro("edad = 20", base)[0], "00000003|00000003@ciencias.unam.mx|20\n00000004|00000004@ciencias.unam.mx|20")

    def test_eliminarRegistro(self):
        base = BaseDeDatos()
        base.crearBD("numeroCuenta, correo, edad")
        registro = Registro()
        registro.nuevoRegistro("00000001, 00000001@ciencias.unam.mx, 25", base)
        registro.nuevoRegistro("00000002, 00000002@ciencias.unam.mx, 25", base)
        registro.nuevoRegistro("00000003, 00000003@ciencias.unam.mx, 20", base)
        registro.nuevoRegistro("00000004, 00000004@ciencias.unam.mx, 20", base)
        registro.nuevoRegistro("00000005, 00000005@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000006, 00000006@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000007, 00000007@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000008, 00000008@ciencias.unam.mx, 30", base)
        self.assertEqual(registro.eliminarRegistro("edad = 20", base), "Se han eliminado correctamente")


    def test_modificarRegistros(self):
        base = BaseDeDatos()
        base.crearBD("numeroCuenta, correo, edad")
        registro = Registro()
        registro.nuevoRegistro("00000001, 00000001@ciencias.unam.mx, 25", base)
        registro.nuevoRegistro("00000002, 00000002@ciencias.unam.mx, 25", base)
        registro.nuevoRegistro("00000003, 00000003@ciencias.unam.mx, 20", base)
        registro.nuevoRegistro("00000004, 00000004@ciencias.unam.mx, 20", base)
        registro.nuevoRegistro("00000005, 00000005@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000006, 00000006@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000007, 00000007@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000008, 00000008@ciencias.unam.mx, 30", base)
        self.assertEqual(registro.modificarRegistros("edad = 20", "numeroCuenta=indefinido", base), "Actualizacion correcta")

    def test_escribirArchivos(self):
        base = BaseDeDatos()
        base.crearBD("numeroCuenta, correo, edad")
        registro = Registro()
        registro.nuevoRegistro("00000001, 00000001@ciencias.unam.mx, 25", base)
        registro.nuevoRegistro("00000002, 00000002@ciencias.unam.mx, 25", base)
        registro.nuevoRegistro("00000003, 00000003@ciencias.unam.mx, 20", base)
        registro.nuevoRegistro("00000004, 00000004@ciencias.unam.mx, 20", base)
        registro.nuevoRegistro("00000005, 00000005@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000006, 00000006@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000007, 00000007@ciencias.unam.mx, 30", base)
        registro.nuevoRegistro("00000008, 00000008@ciencias.unam.mx, 30", base)
        self.assertEqual(registro.escribirArchivos("nomArch", base), "Escritura correcta")







if __name__ == "__main__":
    unittest.main()
