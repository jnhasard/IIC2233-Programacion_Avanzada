from random import randint, expovariate, choice
from threading import Thread, Lock
import time


def spawn_alumnos(grafo):
    while True:
        time.sleep(expovariate(1/5))
        alumno = Persona(grafo.nodos[0])
        grafo.agregar(alumno)
        alumno.start()


class Nodo:
    def __init__(self, valor, conexiones=None):
        self.valor = valor
        self.conexiones = []
        self.ocupado = False
        if conexiones is not None:
            for i in conexiones:
                self.conexiones.append(i)


    def agregar_conexion(self, conexion):
        self.conexiones.append(conexion)

    def __repr__(self):
        return repr(self.valor)


class Persona(Thread):
    globals()[id] = 0
    lock = Lock()
    def __init__(self, posicion):
        super().__init__()
        self.nombre = globals()[id]
        globals()[id] += 1
        self.hp = randint(80,120)
        self.resistance = randint(1,3)
        self.pieza_actual = posicion

    def run(self):
        while self.pieza_actual != 60 and self.hp > 0:
            t0 = time.time()
            with self.lock.acquire():
                self.pieza_actual.ocupado = False
                print(self.nombre, "Estoy en una pieza nueva")
                tiempo = randint(1, 3)
                self.hp -= tiempo*(6-self.resistance)
                time.sleep(tiempo)
            t1 = time.time()
            self.hp -= (t1-t0)*(6-self.resistance)

            self.pieza_actual = choice(self.pieza_actual.conexiones)

            if self.hp <= 0:
                print(self.nombre, "Me mori")
                self.muerto = True
            if self.pieza_actual == 60:
                print(self.nombre, "GANEEEEEEE!")


class Limpiador(Thread):

    def __init__(self):
        super().__init__()
        self.grafo = grafo

    def run(self):
        for i in self.grafo.nodos:
            if i.valor.muerto == True:
                print("Me estoy llevando un pobre difunto =(")
                grafo.nodos.pop(grafo.nodos.index(i))


class Grafo:

    def __init__(self):
        self.nodos = []
        self.inicio = None
        self.final = None

    def agregar(self, nodo):
        self.nodos.append(nodo)

class TorneoDeLosTresProgramadores(Thread):

    def __init__(self):
        super().__init__()
        self.time = time.time()
        self.llegados = 0

    def run(self):
        self.time = time.time()
        spawner = Thread(target=spawn_alumnos, args=(grafo), daemon=False)
        spawner.start()


with open("laberinto.txt", "r") as lab:
    grafo = Grafo()
    grafo.inicio = Nodo(lab.readline().strip())
    grafo.final = Nodo(lab.readline().strip())

    recorridos = dict()
    recorridos[1] = list()
    a = 1
    for i in lab:
        linea = i.strip().split(",")
        if int(linea[0]) == a:

            recorridos[a].append(linea[1])
        else:
            a += 1
            recorridos[a] = [linea[1]]

    for key in recorridos:

        grafo.nodos.append(Nodo(key, recorridos[key]))

torneo = TorneoDeLosTresProgramadores()
torneo.start()