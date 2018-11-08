from Listasjh import jhlist
from random import randint

class Pais:
    def __init__(self, nombre, poblacion):
        self.nombre = nombre
        self.pob_anterior = jhlist(0,0)
        self.poblacion = int(poblacion)
        self.pob_inicial = int(poblacion)
        self.muertes = 0
        self.aeropuerto = False
        self.clasificacion = "Limpio"
        self.paises_vecinos = None
        self.aero = None
        self.infectados = 0
        self.mask = False
        self.dias = 0
        self.frontera = False
        self.cura = False
        self.gobierno = None

    def border(self):
        entrada = open("borders.csv", "r")
        leer = entrada.readlines()
        x = jhlist()
        y = jhlist()
        for i in leer:
            b = i.strip().split(";")
            if b[0] == self.nombre and not x.existe(b[1]):
                x.agregar(b[1])
            elif b[1] == self.nombre and not x.existe(b[0]):
                x.agregar(b[0])
        self.paises_vecinos = x
        if len(x) > 0:
            self.frontera = True

    def aeropuertos(self):
        entrada = open("random_airports.csv", "r")
        leer = entrada.readlines()
        x = jhlist()
        y = jhlist()
        for i in leer:
            b = i.strip().split(",")
            if b[0] == self.nombre and not x.existe(b[1]):
                x.agregar(b[1])
            elif b[1] == self.nombre and not x.existe(b[0]):
                x.agregar(b[0])
        self.aero = x
        if len(x) > 0:
            self.aeropuerto = True

    def traslado(self, mundo):
        poblacion = 0
        infectados = 0
        infectados_del_dia = jhlist()
        for inf in mundo:
            infectados += inf.valor.infectados
            poblacion += inf.valor.pob_inicial
        if self.frontera and (self.infectados / self.poblacion) >= 0.2:
            proba_traslado = min(((0.07 * self.infectados) /
                                  (self.poblacion * len(self.paises_vecinos))),
                                 1)
            for i in self.paises_vecinos:
                if mundo[mundo.finder(i.valor)].valor.frontera and mundo[
                    mundo.finder(i.valor)].valor.clasificacion == "Limpio":
                    if proba_traslado * 100 >= randint(0, 100):
                        mundo[mundo.finder(i.valor)].valor.clasificacion \
                            = "Infectado"
                        mundo[mundo.finder(i.valor)].valor.infectados += 1
                        print(mundo[mundo.finder(i.valor)],
                              "se infecto TERRESTREMENTE")
                        infectados_del_dia.agregar(mundo[mundo.finder(i.valor)])
        if self.aeropuerto and (infectados / poblacion) >= 0.04:  # via aerea
            proba_traslado = min(((0.07 * self.infectados) /
                                  (self.poblacion * len(self.aero))), 1)
            for b in self.aero:
                if mundo[mundo.finder(b.valor)].valor.frontera and mundo[
                    mundo.finder(b.valor)].valor.clasificacion == "Limpio":
                    if proba_traslado * 100 >= randint(0, 100):
                        mundo[mundo.finder(b.valor)].valor.clasificacion = \
                            "Infectado"
                        mundo[mundo.finder(b.valor)].valor.infectados += 1
                        print(mundo[mundo.finder(b.valor)],
                              "se infecto AEREAMENTE")
                        infectados_del_dia.agregar(mundo[mundo.finder(b.valor)])
        return infectados_del_dia

    def contagio(self, infec):
        aprox = max(1,self.infectados//1000000)
        contagio = 0
        for i in range(int(aprox)):
            contagio += randint(0,6)
        contagio /= int(aprox)
        proba_muerte = min(max(0.2, (self.dias ** 2) / 100000) *
                           infec.mortalidad, 1)
        self.muertes += int(proba_muerte*self.infectados)
        muertes_diaria = int(proba_muerte*self.infectados)
        self.poblacion -= int(proba_muerte*self.infectados)
        if self.mask:
            infec_diarios = int(contagio * 0.3 * self.infectados)
            self.infectados += int(contagio * 0.3*self.infectados)
        else:
            infec_diarios = int(contagio * self.infectados)
            self.infectados += int(contagio*self.infectados)
        if self.poblacion <= 0:
            self.poblacion = 0
            self.infectados = self.pob_inicial
            self.clasificacion = "Muerto"
            self.muertes = self.pob_inicial
            print(self.nombre, "ha muerto")
        if self.infectados >= self.pob_inicial:
            self.infectados = self.pob_inicial
        self.pob_anterior = jhlist()
        self.pob_anterior.agregar(infec_diarios)
        self.pob_anterior.agregar(muertes_diaria)
        return jhlist(infec_diarios, muertes_diaria)

    def repartir_cura(self, mundo):
        for i in self.aero:
            mundo[mundo.finder(i)].valor.cura = True

    def curar(self):
        random = randint(0,25)
        prob = randint(0,100)
        if random > prob:
            aux = self.poblacion * 0.25
            self.poblacion += int(aux)
            self.infectados -= int(aux)

    def __repr__(self):
        return self.nombre

class Gobierno:
    def __init__(self, pais):
        self.pais = pais

    def agregar(self, mundo, propuesta):
        if propuesta == 1:
            promedio = 0
            contador = 0
            for i in self.pais.paises_vecinos:
                promedio += mundo[mundo.finder(i)].valor.\
                                 poblacion/mundo[mundo.finder(i)]\
                    .valor.pob_inicial
                contador += 1
            promedio /= contador
            prioridad = promedio * self.pais.infectados / self.pais.poblacion
            return (prioridad, 1, str(self.pais))
        elif propuesta == 2:
            prioridad = 0.8 * self.pais.infectados / self.pais.poblacion
            return (prioridad, 2, str(self.pais))
        elif propuesta == 3:
            prioridad = 0.5 * self.pais.infectados / self.pais.poblacion
            return (prioridad, 3, str(self.pais))
        elif propuesta == 4:
            if self.pais.cura == True:
                prioridad = self.pais.infectados / self.pais.poblacion
                return (prioridad, 4, str(self.pais))
            else:
                prioridad = 0.7 * self.pais.infectados / self.pais.poblacion
                return (prioridad, 4, str(self.pais))
        elif propuesta == 5:
            if self.pais.cura == True:
                prioridad = self.pais.infectados / self.pais.poblacion
                return (prioridad, 5, str(self.pais))
            else:
                prioridad = 0.7 * self.pais.infectados / self.pais.poblacion
                return (prioridad, 5 , str(self.pais))

    def ejecutar(self, prop, mundo):
        if prop == 1:
            self.cerrar_frontera(mundo)
        elif prop == 2:
            self.cerrar_aero(mundo)
        elif prop == 3:
            self.entregar_mask(mundo)
        elif prop == 4:
            self.abrir_frontera(mundo)
        elif prop == 5:
            self.abrir_aero(mundo)

    def cerrar_aero(self, mundo):
        mundo[mundo.finder(str(self.pais))].valor.aeropuerto = False

    def cerrar_frontera(self, mundo):
        mundo[mundo.finder(str(self.pais))].valor.frontera = False

    def entregar_mask(self, mundo):
        mundo[mundo.finder(str(self.pais))].valor.mask = True

    def abrir_aero(self, mundo):
        mundo[mundo.finder(str(self.pais))].valor.aeropuerto = True

    def abrir_frontera(self, mundo):
        mundo[mundo.finder(str(self.pais))].valor.frontera = True

    def __repr__(self):
        return "Gobierno de " + str(self.pais)

