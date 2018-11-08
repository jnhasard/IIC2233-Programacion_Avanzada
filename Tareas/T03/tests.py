import unittest
import comandos_datos
import comandos_basicos
import comandos_bool
import comandos_numerico
import numpy
import inter2


class TestearBasicos(unittest.TestCase):

    def test_asignar(self):
        comandos_basicos.asignar("x", 1)
        self.assertEquals(comandos_basicos.dicc["x"],1)


class TestearConjuntosDatos(unittest.TestCase):

    def tests_filtrar(self):
        self.assertEquals(comandos_datos.filtrar([i for i in range(1,100)],"<",10),[x for x in range(1,10)])

    def tests_evaluar(self):
        def cero(n):
            return 0
        self.assertEquals(comandos_datos.evaluar(cero, 1, 10, 1),[0 for x in range(1,10)])

class TestearNumerico(unittest.TestCase):

    def tests_PROM(self):
        self.assertEquals(comandos_numerico.PROM([1,2,3,4]), numpy.mean([1,2,3,4]))

    def tests_MEDIAN(self):
        self.assertEquals(comandos_numerico.MEDIAN([1,2,3,4]), numpy.median([1,2,3,4]))

    def tests_VAR(self):
        self.assertEquals(round(comandos_numerico.VAR([1,2,3,4])), round(numpy.var([1,2,3,4], ddof=1)))

    def tests_DESV(self):
        self.assertEquals(comandos_numerico.DESV([1,2,3,4]), numpy.std([1,2,3,4], ddof=1))

class TestearBool(unittest.TestCase):

    def tests_comparar(self):
        self.assertEquals(comandos_bool.comparar_columna([1,2], ">", comandos_numerico.LEN, [1]), True)