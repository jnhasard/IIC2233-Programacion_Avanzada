__author__ = 'Ignacio Castaneda, Diego Iruretagoyena, Ivania Donoso, CPB'

import random
from datetime import datetime


def verificar_transferencia(funcion):
    def _verificar_transferencia(self, origen, destino, monto, clave):
        if origen not in self.cuentas:
            raise AssertionError("No existe cuenta de origen")
        if destino not in self.cuentas:
            raise AssertionError("No existe cuenta de destino")
        if monto > self.cuentas[origen].saldo:
            raise AssertionError("Cuenta de origen no tiene monto necesario")
        if self.cuentas[origen].clave != clave:
            raise AssertionError("Clave del origen incorrecta")
        return funcion(self, origen, destino, monto, clave)
    return _verificar_transferencia

def verificar_saldo(funcion):
    def _verificar_saldo(self, numero_cuenta):
        if numero_cuenta not in self.cuentas:
            raise AssertionError("No existe cuenta")
        return funcion(self, numero_cuenta)/5
    return _verificar_saldo

def verificar_inversion(funcion):
    def _verificar_inversion(self, cuenta, monto, clave):
        if cuenta not in self.cuentas:
            raise AssertionError("No existe cuenta")
        if monto > self.cuentas[cuenta].saldo:
            raise AssertionError("Cuenta no tiene monto necesario")
        if self.cuentas[cuenta].clave != clave:
            raise AssertionError("Clave del origen incorrecta")
        if monto > 10000000:
            raise AssertionError("Monto mayor a 10.000.000")
        return funcion(self, cuenta, monto, clave)
    return _verificar_inversion

def verificar_cuenta(funcion):
    def _verificar_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        aleat = numero
        if numero in self.cuentas:
            print("Numero de cuenta ya existe, creando uno de forma aleatoria")
            while aleat in self.cuentas:
                aleat = self.crear_numero()
        guion = False
        for i in rut:
            if not i.isdigit():
                if i == "-":
                    if guion:
                        raise AssertionError("Tiene mas de un guion")
                    else:
                        guion = True
                else:
                    raise AssertionError("Tiene un caracter no permitido")
        if not guion:
            raise AssertionError("El rut no contiene un guion")
        if len(clave) != 4:
            raise AssertionError("Clave no tiene 4 digitos")
        for i in clave:
            if not i.isdigit():
                raise AssertionError("Clave contiene caracteres que no son digitos")
        return funcion(self, nombre, rut, clave, aleat, saldo_inicial)
    return _verificar_cuenta



def log(funcion):
    def _log(*args, **kwargs):
        out = open("Log.txt", "a")
        string = str(datetime.now())
        string += "-" + funcion.__name__ + ":"
        for i in args:
            string += str(i) + " "
        aux = funcion(*args)
        string += str(aux)
        string += str(kwargs) + "\n"
        print(string)
        out.write(string)
        return aux
    return _log
"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las 
funciones/clases.
"""

class Banco:
    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()
    @log
    @verificar_saldo
    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5
    @log
    @verificar_transferencia
    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas 
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto
    @log
    @verificar_cuenta
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta
    @log
    @verificar_inversion
    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las 
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:
    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    try:
        bco.crear_cuenta("Juan", "192312333", "1234", bco.crear_numero())
    except AssertionError as error:
        print('Error: ', error)


    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar 
    las pruebas que estime necesaria para comprobar el funcionamiento de su 
    solucion.
    """
    try:
        print(bco.saldo(12))
    except AssertionError as error:
        print('Error: ', error)

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    try:
        bco.transferir(1, 2, 5000, "4321")
    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    try:
        bco.invertir(2, 200000, "1234")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    try:
        bco.invertir(2, 200000, "4321")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))
