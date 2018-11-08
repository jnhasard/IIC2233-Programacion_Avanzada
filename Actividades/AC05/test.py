import unittest


class TestearFromato(unittest.TestCase):

    def test_archivo(self):
        entrada = open("mensaje_marciano.txt", "r")
        texto = entrada.readlines()
        sumacar = 0
        suma = 0
        for i in texto:
            lista = i.lstrip().rstrip().split(" ")
            for chunk in lista:
                for numero in chunk:
                    self.assertIsInstance(numero, str)
                    sumacar += 1
                    try:
                        suma += int(numero)
                    except: pass
        self.assertEqual(suma, 253)
        self.assertEqual(sumacar, 408)

class TestearMensaje(unittest.TestCase):

    def test_codificacion(self):
        entrada = open("mensaje_marciano.txt", "r")
        texto = entrada.readlines()
        for i in texto:
            lista = i.lstrip().rstrip().split(" ")
            for chunk in lista:
                for numero in chunk:
                    self.assertIn(numero, ["0","1"])

    def test_incorrectos(self):
        entrada = open("mensaje_marciano.txt", "r")
        texto = entrada.readlines()
        for i in texto:
            lista = i.lstrip().rstrip().split(" ")
            for chunk in lista:
                self.assertIn(len(chunk), [6,7])




suite = unittest.TestLoader().loadTestsFromTestCase(TestearMensaje)
unittest.TextTestRunner().run(suite)
