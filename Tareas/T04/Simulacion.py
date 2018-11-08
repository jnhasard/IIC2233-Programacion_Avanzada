from random import random, randint, expovariate, uniform, choice
from numpy.random import triangular


class Simulacion:
    """
    clase que simula todos los hechos
    """
    def __init__(self, contenidos, alumnos, profesores, docencia, tareos, coordinador, secciones):
        """
        :param contenidos: todos los contenidos del semestre
        :type contenidos: list(Contenidos)
        :param alumnos: todos los alumnos del semestre
        :type alumnos: list(Alumnos)
        :param profesores: todos los profesores del semestre
        :type profesores: list(Profesores)
        :param docencia: todos los ayudantes de docencia del semestre
        :type docencia: list(Docencia)
        :param tareos: todos los ayudantes de tarea del semestre
        :type tareos: list(Tareos)
        :param coordinador: el ayudante coordinador del semestre
        :type coordinador: Coordinador
        :param secciones: cantidad de secciones que hay
        :type secciones: int
        """
        self.contenidos = contenidos
        self.profesores = profesores
        self.alumnos = alumnos
        self.docencia = docencia
        self.tareos = tareos
        self.coordinador = coordinador
        self.secciones = secciones
        self.dias = 0
        self.semanas = -1
        self.exigencia_act = 0
        self.exigencia_tar = 0
        self.exigencia_cont = 0
        self.controles = 0
        self.control = False
        self.baja_notas = 0
        self.contador_baja_notas = 0
        self.promedio_c = 0
        self.promedio_act = 0
        self.promedio_t = 0
        self.contador_tareas = 0
        self.botaron = 0
        self.notast = []
        self.notasc = []
        self.notasa = []
        self.notas_act = []
        self.promedio_e = 0
        self.terminar = True
        self.numerox = [i for i in range(0,500)]

    # lunes
    def reu_docencia(self):
        """
        reunion donde se decide la exigencia de la actividad de la semana y del control (en caso de haber)
        """
        self.exigencia_act = 7 + uniform(1, 5) / float(self.contenidos[self.semanas].dificultad)
        self.exigencia_cont = 7 + uniform(1, 5) / float(self.contenidos[self.semanas].dificultad)
        print("Reunion Docencia de la semana", self.semanas)

    # martes
    def ayudantia(self):
        """
        simulacion de ayudantia
        """
        usados = []
        for seccion in range(1, self.secciones + 1):
            ay1, ay2 = 0, 0
            while ay1 == ay2 or ay1 in usados or ay2 in usados:
                ay1, ay2 = randint(0, len(self.docencia) - 1), randint(0, len(self.docencia) - 1)
            usados.append(ay1)
            usados.append(ay2)
            encargados = [self.docencia[ay1], self.docencia[ay2]]
            for ayudante in encargados:
                if self.semanas in ayudante.especialidades:
                    print(ayudante, "ayudó a la seccion", seccion, "en la ayudantia de", self.contenidos[self.semanas])
                    for alumno in self.alumnos:
                        if alumno.seccion == seccion:
                            alumno.manejo_de_contenidos *= 1.1

    # miercoles
    def consultas(self):
        """
        simulacion de alumnos consultando profesores de su seccion
        """
        consultas = []
        for profe in self.profesores:
            for alumno in self.alumnos:
                if alumno.seccion == profe.seccion:
                    if not alumno.reunion:
                        if alumno.promedio <= 5:
                            consultas.append(alumno)
                        elif random() < alumno.prob_profe:
                            consultas.append(alumno)
                    else:
                        alumno.reunion = False
            profe.recibir_consultas(consultas)
            consultas = []

    # jueves
    def catedra(self):
        """
        simulacion de catedra, en esta hay actividades y a veces controles sorpresa 
        """
        numero = 0
        numero1 = 0
        if random() <= 0.5 and self.controles < 5:
            self.control = True
            print("Control sorpresa numero", self.controles + 1)
        else:
            self.control = False
        usados = []
        for seccion in range(1, self.secciones + 1):
            ay1, ay2, ay3 = 0, 0, 0
            while ay1 == ay2 or ay2 == ay3 or ay1 == ay3 or ay1 in usados or ay2 in usados or ay3 in usados:
                ay1, ay2, ay3 = randint(0, len(self.docencia) - 1), randint(0, len(self.docencia) - 1), \
                                randint(0, len(self.docencia) - 1)
            usados.append(ay1)
            usados.append(ay2)
            usados.append(ay3)
            encargados = [self.docencia[ay1], self.docencia[ay2], self.docencia[ay3]]
            q = 0
            for alumno in self.alumnos:
                if alumno.seccion == seccion:
                    q += alumno.preguntas
            for ayudante in encargados:
                while ayudante.respuestas > 0 and q > 0:
                    alumno = choice(self.alumnos)
                    if alumno.preguntas > 0 and alumno.seccion == seccion:
                        alumno.manejo_de_contenidos *= 1.01
                        alumno.preguntas -= 1
                        ayudante.respuestas -= 1
                        q -= 1
                ayudante.respuestas = 200
        for seccion in range(1, self.secciones + 1):
            for alumno in self.alumnos:
                if alumno.seccion == seccion:
                    if random() < 0.1:
                        alumno.manejo_de_contenidos *= 1.1
                    alumno.actividad(self.contenidos[self.semanas], self.exigencia_act)
                    numero += 1
                    if self.control:
                        numero1 += 1
                        alumno.control(self.contenidos[self.semanas], self.exigencia_cont)
        print(numero, "alumnos rindieron la actividad", self.semanas + 1)
        if self.control:
            self.eventos.append([14, self.numerox.pop(), self.entregar_notas, [self.semanas, self.controles], 2])
            self.controles += 1
            print(numero1, "alumnos rindieron el control", self.controles)
        else:
            self.eventos.append([14, self.numerox.pop(), self.entregar_notas, self.semanas, 1])
        self.control = False

    # viernes
    def tareas(self):
        """
        simulacion de tareas, tanto de entrega de enunciado como de entrega de los alumnos 
        """
        if self.dias > 6:
            numero = 0
            for alumno in self.alumnos:
                numero += 1
                alumno.tarea([self.contenidos[self.semanas], self.contenidos[self.semanas - 1]], self.exigencia_tar)
            self.eventos.append([14, self.numerox.pop(), self.entregar_notas, self.contador_tareas, 0])
            self.contador_tareas += 1
            print("Tarea", self.contador_tareas, "entregada por", numero, "alumnos")
        if self.dias < 84:
            dificultad = (int(self.contenidos[self.semanas].dificultad) + int(
                self.contenidos[self.semanas + 1].dificultad)) / 2
            self.exigencia_tar = 7 + uniform(1, 5) / dificultad
            print("Tarea", self.contador_tareas + 1, "publicada")

    # domingos
    def conocimientos(self):
        """
        funcion que va actualizando los conocimientos de toda clase para cada alumno semana a semana
        """
        self.semanas += 1
        ap = []
        nop = []
        for alumno in self.alumnos:
            alumno.preguntas = int(triangular(1, 3, 10))
            alumno.calculo_nivel_programacion()
            alumno.calculo_horas_dedicadas()
            alumno.manejos.append(alumno.manejo_de_contenidos)
            alumno.calculo_manejo_de_contenidos(self.contenidos[self.semanas], alumno.horas_dedicadas)
            largo = len(alumno.notas_cont) + len(alumno.notas_tar) + len(alumno.notas_act)
            if largo > 0:
                alumno.promedio = round(
                    (sum(alumno.notas_cont) + sum(alumno.notas_act) + sum(alumno.notas_tar)) / largo, 2)
            if alumno.promedio > 3.94:
                ap.append(alumno)
            else:
                nop.append(alumno)

    # sin fecha definida
    def entregar_notas(self, numero, tipo):
        """
        funcion que entrega las notas a los alumnos 14 dias despues de haberlas entregado, aqui mismo el coordinador 
        decide si atrasarlas o no
        :param numero: numero de evaluacion a entregar
        :type numero: int
        :param tipo: tipo de evaluacion a entregar nota (tipo0 tarea, tipo1 actividad, tipo2 control)
        :type tipo: int
        """
        if self.coordinador.atrasar_notas():
            self.eventos.append([randint(2, 5), self.numerox.pop(), self.entregar_notas, numero, tipo])
        else:
            contador = 0
            self.promedio_t = 0
            self.promedio_act = 0
            self.promedio_c = 0
            for alumno in self.alumnos:
                contador += 1
                alumno.calculo_confianza(numero, tipo)
                if tipo == 0:
                    self.promedio_t += alumno.mostrar_notas(tipo, numero)
                elif tipo == 1:
                    if numero == 3:
                        if alumno.confianza < 20:
                            self.alumnos.pop(self.alumnos.index(alumno))
                            self.botaron += 1
                    self.promedio_act += alumno.mostrar_notas(tipo, numero)
                elif tipo == 2:
                    if numero[0] == 3:
                        if alumno.confianza < 20:
                            self.alumnos.pop(self.alumnos.index(alumno))
                            self.botaron += 1
                    self.promedio_c += alumno.mostrar_notas(2, numero[1])
                    self.promedio_act += alumno.mostrar_notas(1, numero[0])
                elif tipo == 3:
                    self.promedio_e += alumno.nota_examen
            if self.semanas == 5:
                print(self.botaron, "alumnos botaron el ramo tras la cuarta actividad")
            if self.contador_baja_notas < 3 and randint(0, 1) == 0:
                self.contador_baja_notas += 1
                print("U.u")
                if tipo == 0:
                    self.promedio_t = round(self.promedio_t / contador, 2) - 0.5
                    self.notast.append(self.promedio_t + 0.5)
                    self.notast.append(self.promedio_t + 0.5)
                if tipo == 1:
                    self.promedio_act = round(self.promedio_act / contador, 2) - 0.5
                    self.notasa.append(self.promedio_act + 0.5)
                    self.notas_act.append(self.promedio_act + 0.5)
                if tipo == 2:
                    self.promedio_act = round(self.promedio_act / contador, 2) - 0.5
                    self.promedio_c = round(self.promedio_c / contador, 2) - 0.5
                    self.notasa.append((self.promedio_act + 0.5 + self.promedio_c + 0.5) / 2)
                    self.notas_act.append(self.promedio_act + 0.5)
                    self.notasc.append((self.promedio_c + 0.5, self.semanas))
            else:
                if tipo == 0:
                    self.promedio_t = round(self.promedio_t / contador, 2)
                    self.notast.append(self.promedio_t)
                    self.notast.append(self.promedio_t)
                if tipo == 1:
                    self.promedio_act = round(self.promedio_act / contador, 2)
                    self.notasa.append(self.promedio_act + 0.5)
                    self.notas_act.append(self.promedio_act)
                if tipo == 2:
                    self.promedio_act = round(self.promedio_act / contador, 2)
                    self.promedio_c = round(self.promedio_c / contador, 2)
                    self.notasa.append((self.promedio_act + 0.5 + self.promedio_c + 0.5) / 2)
                    self.notas_act.append(self.promedio_act)
                    self.notasc.append((self.promedio_c, self.semanas))
            if tipo == 0:
                print("Se entregaron las notas de la tarea", numero + 1, "con promedio:", self.promedio_t)
            if tipo == 1:
                print("Se entregaron las notas de la actividad", numero + 1, "con promedio:", self.promedio_act)
            if tipo == 2:
                print("Se entregaron las notas de la actividad", numero[0] + 1, "con promedio:", self.promedio_act)
                print("Se entregaron las notas del control", numero[1] + 1, "con promedio:", self.promedio_c)
            if tipo == 3:
                print("Se entregaron las notas del examen con promedio:", round(self.promedio_e / contador, 2))


    def examen(self):
        """
        simulacion de examen para cada alumno 
        """
        promedio = []
        for i in range(len(self.notast)):
            promedio.append(((self.notasa[i] + self.notast[i] / 2), i))
        promedio.sort()
        temas_facil = [promedio[-1][1], promedio[-2][1]]
        temas_dif = [i[1] for i in promedio[:6]]
        temas = temas_dif + temas_facil
        exigencia = uniform(1, 5)
        for alumno in self.alumnos:
            for i in temas:
                progreso_c = 0.5 * alumno.manejos[i] + 0.1 * alumno.nivel_programacion + 0.4 * alumno.confianza
                progreso_f = 0.3 * alumno.manejos[i] + 0.2 * alumno.nivel_programacion + 0.5 * alumno.confianza
                progreso_total = 0.3 * progreso_c + 0.7 * progreso_f
                exigencia = 7 + exigencia / int(self.contenidos[i].dificultad)
                nota = min(max(progreso_total / exigencia * 7, 1), 7)
                alumno.nota_examen += (1 / 8) * nota
            alumno.nota_examen = round(alumno.nota_examen, 2)
        self.eventos.append([14, 4, self.entregar_notas, 0, 3])
        self.eventos.append([20, "terminar"])


    def run(self):
        """
        funcion que simula todo, maneja los eventos que van ocurriendo
        """
        self.promedio_confianzai = 0
        for i in self.alumnos:
            self.promedio_confianzai += i.confianza
        self.promedio_confianzai = (self.promedio_confianzai / len(self.alumnos))
        self.conocimientos()
        self.eventos = [[0, 1, self.reu_docencia], [1, 2, self.ayudantia], [2, 3, self.consultas], [3, 4, self.catedra],
                        [6, 5, self.conocimientos], [5, 6, self.tareas]]
        while self.semanas < 13:
            if self.eventos[0][2].__name__ == "entregar_notas":
                self.eventos[0][2](self.eventos[0][3], self.eventos[0][4])
                self.eventos.pop(0)
            else:
                self.eventos[0][2]()
                if self.eventos[0][2].__name__ == "tareas":
                    if self.contador_tareas < 6:
                        self.eventos.append([14, self.numerox.pop(), self.eventos.pop(0)[2]])
                    else:
                        self.eventos.pop(0)
                elif self.semanas < 11:
                    self.eventos.append([7, self.numerox.pop(), self.eventos.pop(0)[2]])
                else:
                    self.eventos.pop(0)
            if len(self.eventos) == 0 and self.terminar:
                self.eventos.append([5, self.numerox.pop(), self.examen])
                self.terminar = False
            if self.eventos[0][1] == "terminar":
                ap = []
                rep = []
                for alumno in self.alumnos:
                    largo = len(alumno.notas_cont) + len(alumno.notas_tar) + len(alumno.notas_act)
                    if largo > 0:
                        alumno.promedio = round(
                            (sum(alumno.notas_cont) + sum(alumno.notas_act) + sum(alumno.notas_tar)) / largo, 2)
                    if alumno.promedio > 3.94:
                        ap.append(alumno)
                    else:
                        rep.append(alumno)
                print(len(ap), "alumnos aprobaron el ramo y", len(rep), "alumnos lo reprobaron\nFelices Vacaciones!!")
                break
            tiempo_aux = self.eventos[0][0]
            for i in self.eventos:
                i[0] -= tiempo_aux
            self.dias += tiempo_aux
            self.eventos.sort()
        self.promedio_confianzaf = 0
        for i in self.alumnos:
            self.promedio_confianzaf += i.confianza
        self.promedio_confianzaf = (self.promedio_confianzaf / len(self.alumnos))
        print("ESTADISTICAS FINALES")
        print("--Alumnos que botaron el ramo:", self.botaron)
        print("--Confianza al inicio vs final:", self.promedio_confianzai, "vs", self.promedio_confianzaf)
        for i in range(6):
            ap_t = 0
            rep_t = 0
            for alumno in self.alumnos:
                if alumno.notas_tar[i] > 4:
                    ap_t += 1
                else:
                    rep_t += 1
            print("--La tarea", i + 1, "tuvo", round((ap_t / len(self.alumnos)) * 100, 2), "% de aprobacion y",
                  round((rep_t / len(self.alumnos)) * 100, 2), "% de reprobacion")
        for i in range(12):
            ap_a = 0
            rep_a = 0
            for alumno in self.alumnos:
                if alumno.notas_act[i] > 4:
                    ap_a += 1
                else:
                    rep_a += 1
            print("--La actividad", i + 1, "tuvo", round((ap_a / len(self.alumnos)) * 100, 2), "% de aprobacion y",
                  round((rep_a / len(self.alumnos)) * 100, 2), "% de reprobacion")
        prom1 = 0
        prom2 = 0
        prom3 = 0
        for i in self.alumnos:
            if ((i.notas_act[0] + i.notas_act[1] +i.notas_act[2] +i.notas_act[3])*0.4
                     + (i.notas_tar[0] + i.notas_tar[1]) * 0.6) > 4:
                prom1 += 1
            if ((i.notas_act[4] + i.notas_act[5] +i.notas_act[6] +i.notas_act[7])*0.4 +
                        (i.notas_tar[2] + i.notas_tar[3]) * 0.6) > 4:
                prom2 += 1
            if ((i.notas_act[8] + i.notas_act[9] +i.notas_act[10] +i.notas_act[11])*0.15
                     + (i.notas_tar[4] + i.notas_tar[5]) * 0.35 + i.nota_examen * 0.5) > 4:
                prom3 += 1
        alto = [[prom1, "primer"], [prom2, "segundo"], [prom3, "tercero"]]
        alto.sort()
        print("El mes con mayor aprobacion fue el", alto[-1][1])



