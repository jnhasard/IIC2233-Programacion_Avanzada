from random import randint
from Listasjh import jhlist

class Infeccion:
    def __init__(self, tipo):
        self.tipo = tipo
        if tipo == "Virus":
            self.contagiosidad = 1.5
            self.mortalidad = 1.2
            self.resistencia = 1.5
            self.visibilidad = 0.5
        elif tipo == "Bacteria":
            self.contagiosidad = 1
            self.mortalidad = 1
            self.resistencia = 0.5
            self.visibilidad = 0.7
        elif tipo == "Parásito":
            self.contagiosidad = 0.5
            self.mortalidad = 1.5
            self.resistencia = 1
            self.visibilidad = 0.45

    def __repr__(self):
        return self.tipo

class Cura:
    def __init__(self, pob_inicial, infeccion):
        self.dia = 0
        self.gente_sana = pob_inicial -1
        self.pob_inicial = pob_inicial
        self.infeccion = infeccion
        self.gente_infectada = self.pob_inicial - self.gente_sana
        self.gente_muerta = 0
        self.proba = 0
        self.descubierto = False
        self.progress = 0
        self.cura = False

    def descubrimiento(self, infecciones, muertes):
        self.gente_sana -= infecciones
        self.gente_infectada += infecciones - muertes
        self.gente_muerta += muertes
        self.dia += 1
        self.proba = (self.infeccion.visibilidad * self.gente_infectada *
                      (self.gente_muerta**2)) / (self.pob_inicial**3)
        random = randint(0,100)
        if (self.proba*100) > random:
            self.descubierto = True
            print("Se ha descubierto oficialmente la INFECCION\n"
                  "Ahora se buscara la cura")

    def progreso(self, infecciones, muertes, mundo):
        self.gente_sana -= infecciones
        self.gente_infectada += infecciones - muertes
        self.gente_muerta += muertes
        self.dia += 1
        self.progress -= +self.gente_sana/(2*self.pob_inicial)
        if (self.progress % 1) != 0:
            self.progress = int(self.progress) + 1
        else:
            self.progress = int(self.progress)
        print("\nProgreso:", "|" * self.progress, " "*(98-self.progress), "|\n")
        if self.progress >= 100:
            self.progress = 100
            self.cura = True
            vivos = jhlist()
            for i in mundo:
                if i.valor.clasificacion != "Muerto":
                    vivos.agregar(i)
            pais = randint(0,len(vivos)-1)
            print("Se ha descubierto la CURA\nEsta se encuentra en",
                  vivos[pais], "y comenzará inmediatamente a repartirla")


