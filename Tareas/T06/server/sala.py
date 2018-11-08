import threading
import random
import time
class Sala(threading.Thread):
    def __init__(self, nombre, canciones):
        super().__init__()
        self.nombre = nombre
        self.nombres_canciones = canciones
        if ".DS_Store" in self.nombres_canciones:
            self.nombres_canciones.remove(".DS_Store")
        self.canciones = {}
        self.bajar_canciones()
        self.tiempo = 0

    def bajar_canciones(self):
        for i in self.nombres_canciones:
            if i != ".DS_Store":
                with open("songs/" + self.nombre + "/" + i, "rb") as file:
                    self.canciones[i] = file.read()

    def run(self):
        while True:
            if self.tiempo == 0:
                self.tiempo = 20
                self.cancion_actual = random.choice(self.nombres_canciones)
                print(self.cancion_actual)
            self.tiempo -=1
            time.sleep(1)
