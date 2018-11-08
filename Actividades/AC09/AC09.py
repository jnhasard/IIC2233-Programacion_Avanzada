from collections import deque
from random import choice
from random import expovariate
from random import randint


class Persona:
    def __init__(self):
        self.personalidad = None
        self.rapidez = randint(5, 8)
        self.posicion = randint(0, 60)
        self.conductor = False
        self.muerto = False
        self.auto = False


class Generoso(Persona):
    def __init__(self):
        super().__init__()
        self.personalidad = 0.6


class Egoista(Persona):
    def __init__(self):
        super().__init__()
        self.personalidad = 0.3


class Vehiculo:
    def __init__(self, conductor):
        self.rapidez = randint(12, 20)
        self.capacidad = None
        self.conductor = conductor
        self.pasajeros = [conductor]


class Auto(Vehiculo):
    # El conductor usa un espacio
    def __init__(self, conductor):
        self.tipo = False
        super().__init__(conductor)
        self.capacidad = 4


class Camioneta(Vehiculo):
    # El conductor usa un espacio
    def __init__(self, conductor):
        self.tipo = True
        super().__init__(conductor)
        self.capacidad = 7


class Replica:
    def __init__(self):
        self.centro = randint(0, 100)

        if randint(0,10) > 3:
            self.probabilidad_no_caminando = 0.1
            self.probabilidad_no_auto = 0.15
            self.probabilidad_tsunami = 0
            self.potencia_tsunami = 0

        else:
            self.probabilidad_no_caminando = 0.3
            self.probabilidad_no_auto = 0.6
            self.probabilidad_tsunami = 0.7
            self.potencia_tsunami = randint(3, 8)
            self.alcance = self.potencia_tsunami * 4
            self.tsunami_no = self.potencia_tsunami / 10


class Simulacion:
    def __init__(self):
        self.tiempo_maximo = 200
        self.llegados_camioneta = 0
        self.llegaron_auto = 0
        self.llegados_pie = 0
        self.llegados_generoso = 0
        self.llegados_egoista = 0
        self.victimas_tsunami = 0
        self.victimas_replicaf = 0
        self.victimas_replicad = 0
        self.tiempo_simulacion = 0
        self.personas = []
        self.autos = []

    def proxima_ocurrencia(self):
        tiempo = round(expovariate(1/(randint(4,10))))
        self.tiempo_simulacion += tiempo
        return tiempo

    def run(self):
        tiempo = self.proxima_ocurrencia()
        self.tiempo_simulacion += tiempo
        # Poblamos el sistema
        for persona in range(0, 100):
            if randint(0,1) == 1:
                self.personas.append(Generoso())
            else:
                self.personas.append(Egoista())

        for auto in range(0, 25):
            while True:
                persona = choice(self.personas)
                if not persona.conductor:
                    persona.conductor = True
                    persona.auto = True
                    if randint(0,1) == 1:
                        self.autos.append(Camioneta(persona))
                    else:
                        self.autos.append(Auto(persona))
                    break

        while self.tiempo_simulacion < self.tiempo_maximo and len(self.personas) > 0:
            for auto in self.autos:
                inicio = auto.conductor.posicion
                final = auto.conductor.posicion + (auto.rapidez * tiempo)

                # Avanzan las personas del auto
                for pasajero in auto.pasajeros:
                    pasajero.posicion += auto.rapidez * tiempo

                # Vemos que personas se suben a los autos
                if auto.capacidad > 0:
                    for persona in self.personas:
                        if not persona.auto:
                            inicio_p = persona.posicion
                            final_p = persona.posicion + (tiempo * persona.rapidez)
                            if inicio_p in range(inicio, final) or final_p in range(inicio, final):
                                if randint(0,100) < auto.conductor.personalidad * 100:
                                    auto.capacidad -= 1
                                    persona.auto = True
                                    auto.pasajeros.append(persona)
                                    print('Vehiculo recogio persona')

                            # La persona camina
                            persona.posicion = final_p

            catastrofe = Replica()
            # Muere gente por replica
            for persona in self.personas:
                if not persona.auto:
                    persona.posicion += persona.rapidez * tiempo

                if persona.posicion >= 100:
                    if persona.auto:
                        print('Llego una persona {} a la base en auto'.format('egoista' if persona.personalidad ==
                                                                              0.3 else 'generoso'))
                        for auto in self.autos:
                            if persona in auto.pasajeros:
                                if auto.tipo:
                                    self.llegados_camioneta += 1
                                else:
                                    self.llegaron_auto += 1
                    else:
                        print('Llego una persona {} a la base caminando'.format('egoista' if persona.personalidad ==
                                                                              0.3 else 'generoso'))
                        self.llegados_pie += 1

                    if persona.personalidad == 0.3:
                        self.llegados_egoista += 1

                    if persona.personalidad == 0.6:
                        self.llegados_generoso += 1
                    self.personas.pop(self.personas.index(persona))

                if persona.posicion < 100:
                    if persona.auto:
                        if randint(0,100) < catastrofe.probabilidad_no_auto * 100:
                            persona.muerto = True
                            if catastrofe.probabilidad_tsunami != 0:
                                self.victimas_replicaf += 1
                            else:
                                self.victimas_replicad += 1
                            print('Murio persona por replica')
                            for auto in self.autos:
                                if persona in auto.pasajeros:
                                    auto.pasajeros.pop(auto.pasajeros.index(persona))
                                    auto.capacidad += 1
                            # Sacamos al muerto de la lista de personas
                            self.personas.pop(self.personas.index(persona))
                    else:
                        if randint(0,100) < catastrofe.probabilidad_no_caminando * 100:
                            persona.muerto = True
                            print('Murio persona por replica')
                            if catastrofe.probabilidad_tsunami != 0:
                                self.victimas_replicaf += 1
                            else:
                                self.victimas_replicad += 1
                            self.personas.pop(self.personas.index(persona))

                    # Ahora muere gente por tsunami
                    if catastrofe.probabilidad_tsunami != 0:
                        if persona.posicion in range(catastrofe.centro - int(catastrofe.alcance / 2), catastrofe.centro + int(catastrofe.alcance / 2)):
                            if randint(0, 100) < catastrofe.tsunami_no * 100:
                                persona.muerto = True
                                print('Murio persona por tsunami')
                                self.victimas_tsunami += 1
                                if persona.auto:
                                    for auto in self.autos:
                                        if persona in auto.pasajeros:
                                            auto.pasajeros.pop(auto.pasajeros.index(persona))
                                            auto.capacidad += 1
                                else:
                                    self.personas.pop(self.personas.index(persona))

            tiempo = self.proxima_ocurrencia()
            self.tiempo_simulacion += tiempo
suma = 0
for i in range(0,9):
    simular = Simulacion()
    simular.run()
    suma += simular.tiempo_simulacion
    print('llegados auto {}, llegados camioneta {}, llegados pie {}, llegados egoista {}, llegados generoso {}, victimas tsunami {}, victimas replica debil {}, victimas replica fuerte {}'.format(simular.llegaron_auto, simular.llegados_camioneta, simular.llegados_pie, simular.llegados_egoista, simular.llegados_generoso, simular.victimas_tsunami, simular.victimas_replicad, simular.victimas_replicaf))
print('promedio es', suma/10)
