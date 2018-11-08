from random import random, randint, expovariate, uniform, choice
from numpy.random import triangular

class Contenido:
    """
    Esta clase representa cada contenido, lo hice para facilitar mas que nada los rangos de nota de cada 
    uno y sus dificultades
    """
    def __init__(self, nombre, dificultad, r1, r2, r3, r4):
        """
        :param nombre: Nombre del contenido
        :type nombre: str
        :param dificultad: numero de dificultad del contenido
        :type dificultad: str
        :param r1, r2, r3, r4: Son los 4 rangos de hora para las notas
        :type r1, r2, r3, r4: str
        """
        self.nombre = nombre
        self.dificultad = dificultad
        self.r1 = r1.split("-")
        self.r2 = r2.split("-")
        self.r3 = r3.split("-")
        self.r4 = r4.split("-")

    def __str__(self):
        return self.nombre


class Alumno:
    """
    Esta clase representa a los alumnos que cursan el ramo
    """
    def __init__(self, nombre, seccion, prob40, prob50, prob55, prob60, confianzai, confianzaf, probprofe):
        """
        :param nombre: Nombre del alumno
        :type nombre: str
        :param seccion: Seccion del alumno
        :type seccion: str
        :param prob40: probabilidad de tener 40 creditos
        :type prob40: float
        :param prob50: probabilidad de tener 50 creditos
        :type prob50: float
        :param prob55: probabilidad de tener 55 creditos
        :type prob55: float
        :param prob60: probabilidad de tener 60 creditos
        :type prob60: float
        :param confianzai: confianza base inicial
        :type prob40: float
        :param confianzaf: confianza tope inicial
        :type prob40: float
        :param probprofe: probabilidad de ir a hablar con el profe teniendo promedio sobre 5
        :type prob40: float
        """
        self.nombre = nombre
        self.seccion = int(seccion)
        creditos = random()
        if creditos <= prob40:
            self.cantidad_de_creditos = 40
        elif creditos > prob40 and creditos <= (prob40 + prob50):
            self.cantidad_de_creditos = 50
        elif creditos > (prob40 + prob50) and creditos <= (prob40 + prob50 + prob55):
            self.cantidad_de_creditos = 55
        else:
            self.cantidad_de_creditos = 60
        # 0 == Eficiente, 1 == Artisitico, 2 == Teorico
        self.prob_profe = probprofe
        self.personalidad = randint(0, 2)
        self.manejo_de_contenidos = 0
        self.nota_esperada_t = []
        self.nota_esperada_a = []
        self.nota_esperada_c = []
        self.confianza = uniform(confianzai, confianzaf)
        self.nivel_programacion = uniform(2, 10)
        self.progreso = 0
        self.horas_dedicadas = 0
        self.horas_semana_anterior = 0
        self.horas_semana_anteanterior = 0
        self.calculo_horas_dedicadas()
        self.reunion = False
        self.dias = 0
        self.nota_examen = 0
        self.promedio = 1
        self.v = 0
        self.w = 0
        self.notas_act = []
        self.notas_tar = []
        self.notas_cont = []
        self.preguntas = int(triangular(1, 3, 10))
        self.examen = 0
        self.manejos = []


    def calculo_horas_dedicadas(self):
        """
        actualiza la cantidad de horas que dedicara el alumno esa semana dependiendo de los creditos que tomo 
        """
        self.horas_semana_anteanterior = self.horas_semana_anterior
        self.horas_semana_anterior = self.horas_dedicadas
        if self.cantidad_de_creditos == 40:
            self.horas_dedicadas = randint(10, 25)
        elif self.cantidad_de_creditos == 50:
            self.horas_dedicadas = randint(10, 15)
        elif self.cantidad_de_creditos == 55:
            self.horas_dedicadas = randint(5, 15)
        elif self.cantidad_de_creditos == 60:
            self.horas_dedicadas = randint(5, 10)


    def calculo_manejo_de_contenidos(self, contenido, hrs):
        """
        calcula el manejo de contenidos para la semana
        :param contenido: El contenido de la semana
        :type contenido: Contenido
        :param hrs: horas que dedicara esta semana
        :type hrs: int
        """
        self.manejo_de_contenidos = (1/int(contenido.dificultad)) * hrs


    def extra_personalidad(self, contenido):
        """
        sumara al alumno a la nota correspondiente a su personalidad
        :param contenido: el contenido que se le evaluo
        :type contenido: Contenido
        :return: cuanto se suma a la evaluacion
        """
        if self.personalidad == 0:
            if contenido.nombre == "Funcional" or contenido.nombre == "Threading":
                return 1
            else: return 0
        elif self.personalidad == 1:
            if contenido.nombre == "GUI" or contenido.nombre == "Webservices":
                return 1
            else: return 0
        elif self.personalidad == 2:
            if contenido.nombre == "Metaclases":
                return 1
            else: return 0


    def calculo_nota_esperada(self, contenido, hrs, tipo):
        """
        calcula la nota esperada para alguna evaluacion
        :param contenido: el contenido evaluado
        :type contenido: Contenido
        :param hrs: horas dedicadas 
        :type hrs: int
        :param tipo: el tipo de evaluacion (tipo0 tarea, tipo1 actividad, tipo2 control)
        :type tipo: int
        """
        r1 = list(range(int(contenido.r1[0]), int(contenido.r1[1]) + 1))
        r2 = list(range(int(contenido.r2[0]), int(contenido.r2[1]) + 1))
        r3 = list(range(int(contenido.r3[0]), int(contenido.r3[1]) + 1))
        r4 = list(range(int(contenido.r4[0]), int(contenido.r4[1]) + 1))
        nota = 0
        if hrs <= r1[-1]:
            nota = round(uniform(1.1,3.9),2)
        elif hrs <= r2[-1]:
            nota = round(uniform(4,5.9),2)
        elif hrs <= r3[-1]:
            nota = round(uniform(6,6.9),2)
        elif hrs >= r4[-1]:
            nota = 7
        if tipo == 0:
            self.nota_esperada_t.append(nota)
        elif tipo == 1:
            self.nota_esperada_a.append(nota)
        else:
            self.nota_esperada_c.append(nota)


    def calculo_confianza(self, numero, tipo):
        """
        va actualizando la confianza
        :param numero: el numero de evaluacion 
        :type numero: int
        :param tipo: el tipo de evaluacion (tipo0 tarea, tipo1 actividad, tipo2 control)
        :type tipo: int 
        """
        # tipo0 tarea, tipo1 activ, tipo2 control
        confianza_notas = 0
        if tipo == 0:
            confianza_notas = 3*(self.notas_tar[numero] - self.nota_esperada_t[numero])
        elif tipo == 1:
            confianza_notas = 5*(self.notas_act[numero] - self.nota_esperada_a[numero])
        elif tipo == 2:
            confianza_control = self.notas_cont[numero[1]] - self.nota_esperada_c[numero[1]]
            confianza_actividad = 5 * (self.notas_act[numero[0]] - self.nota_esperada_a[numero[0]])
            confianza_notas = confianza_control + confianza_actividad
        self.confianza = self.confianza + confianza_notas


    def calculo_nivel_programacion(self):
        """
        calcula el nivel de programacion semana a semana
        """
        self.nivel_programacion = 1.05 * (1 + self.v*0.08 - self.w*0.15) * self.nivel_programacion


    def actividad(self, contenido, exigencia):
        """
        se ejecuta una actividad en clases
        :param contenido: el contenido evaluado
        :type contenido: Contenido
        :param exigencia: la exigencia definida por los ayudantes
        :type exigencia: float
        """
        hrs = self.horas_semana_anterior*0.3*(3/7) + self.horas_dedicadas * 0.3 * (4/7)
        self.calculo_manejo_de_contenidos(contenido, hrs)
        self.calculo_nota_esperada(contenido, hrs, 1)
        progreso_pep = 0.7 * self.manejo_de_contenidos + 0.2 * self.nivel_programacion + 0.1 * self.confianza
        progreso_funcionalidad = 0.3 * self.manejo_de_contenidos + 0.7 * self.nivel_programacion + 0.1 * self.confianza
        progreso_contenidos = 0.7 * self.manejo_de_contenidos + 0.2 * self.nivel_programacion + 0.1 * self.confianza
        progreso_total = progreso_contenidos*0.4 + progreso_funcionalidad*0.4 + progreso_pep*0.2
        nota = min(max(progreso_total/exigencia * 7, 1),7)
        nota += self.extra_personalidad(contenido)
        self.notas_act.append(round(nota,2))


    def control(self, contenido, exigencia):
        """
        se ejecuta cuando hay control sorpresa
        :param contenido: el contenido evaluado
        :type contenido: Contenido
        :param exigencia: la exigencia determinada por los ayudantes
        :type exigencia: float
        """
        hrs = self.horas_semana_anterior * 0.3 * (3 / 7) + self.horas_dedicadas * 0.3 * (4 / 7)
        self.calculo_manejo_de_contenidos(contenido, hrs)
        self.calculo_nota_esperada(contenido, hrs, 2)
        progreso_contenidos = 0.7 * self.manejo_de_contenidos + 0.05 * self.nivel_programacion + 0.25 * self.confianza
        progreso_funcionalidad = 0.3 * self.manejo_de_contenidos + 0.2 * self.nivel_programacion + 0.5 * self.confianza
        progreso_total = progreso_contenidos * 0.7 + progreso_funcionalidad * 0.3
        nota = min(max(progreso_total / exigencia * 7, 1), 7)
        self.notas_cont.append(round(nota, 2))


    def tarea(self, contenidos, exigencia):
        """
        se ejecuta cuando el alumno hace una tarea
        :param contenidos: los contenidos que abarca la tarea
        :type contenidos: list(Contenidos)
        :param exigencia: la exigencia determinada por los ayudantes
        :type exigencia: float
        """
        hrs1 = self.horas_semana_anteanterior * 0.7 * (2/7) + self.horas_semana_anterior * 0.7 * (5 / 7)
        hrs2 = self.horas_semana_anterior * 0.7 * (2 / 7) + self.horas_dedicadas * 0.7 *(5 / 7)
        self.calculo_manejo_de_contenidos(contenidos[0], hrs1)
        aux_contenidos = self.manejo_de_contenidos
        self.calculo_manejo_de_contenidos(contenidos[1], hrs2)
        self.manejo_de_contenidos += aux_contenidos
        self.manejo_de_contenidos /= 2
        self.calculo_nota_esperada(contenidos[0], hrs1, 0)
        self.calculo_nota_esperada(contenidos[1], hrs2, 0)
        self.nota_esperada_t[-1] += self.nota_esperada_t.pop(-2)
        self.nota_esperada_t[-1] /= 2
        progreso_pep = 0.5 * (hrs1 + hrs2) / 2 + 0.5 * self.nivel_programacion
        progreso_contenidos = 0.7 * self.manejo_de_contenidos + 0.1 * self.nivel_programacion + 0.2 * (hrs1 + hrs2) / 2
        progreso_funcionalidad = 0.5 * self.manejo_de_contenidos + 0.1 * self.nivel_programacion + 0.4 * (hrs1 + hrs2) / 2
        progreso_total = 0.2* progreso_pep + 0.4 * progreso_funcionalidad + 0.4 * progreso_contenidos
        nota = min(max(progreso_total / exigencia * 7, 1), 7)
        self.notas_tar.append(round(nota, 2))


    def mostrar_notas(self, tipo, numero):
        """
        entrega la nota que se este pidiendo, se usa para sacar promedios principalmente
        :param tipo: el tipo de evaluacion
        :type tipo: int
        :param numero: el numero de evaluacion (tipo0 tarea, tipo1 actividad, tipo2 control)
        :type numero: int
        """
        if tipo == 0:
            return self.notas_tar[numero]
        elif tipo == 1:
            return self.notas_act[numero]
        elif tipo == 2:
            return self.notas_cont[numero]


    def __str__(self):
        return self.nombre + " de la seccion: " + str(self.seccion)


class Profesor:
    """
    clase que representa a los profesores
    """
    def __init__(self, nombre, seccion):
        """
        :param nombre: el nombre del profesor
        :type nombre: str
        :param seccion: la seccion a la que da catedra el profesor
        :type seccion: str
        """
        self.nombre = nombre
        self.seccion = int(seccion)
        self.alumnos_semanal = 0
        self.dia = 0

    def recibir_consultas(self, alumnos):
        """
        esta se ejecuta una vez a la semana para responder consultas de los alumnos
        :param alumnos: todos los alumnos que quisieron ir a hacer preguntas
        :type alumnos: list(Alumnos)
        """
        consulta2 = []
        largo = len(alumnos)
        while self.alumnos_semanal < 10 and len(alumnos) > 0:
            alumno = alumnos.pop(randint(0,len(alumnos)-1))
            if alumno.seccion == self.seccion:
                consulta2.append(alumno)
            else: continue
            #print("hable con", consulta2[-1])
            self.alumnos_semanal += 1
        for alumno in consulta2:
            alumno.reunion = True
            alumno.v = 1
        print(self, "tuvo reunion con", self.alumnos_semanal, "alumnos")
        self.alumnos_semanal = 0

    def __str__(self):
        return "Profesor(a) " + self.nombre + " de la seccion: " + str(self.seccion)


class Docencia:
    """
    representa a los ayudantes de docencia
    """
    def __init__(self, nombre):
        """
        :param nombre: nombre del ayudante
        :type nombre: str 
        """
        self.nombre = nombre
        self.respuestas = 200
        uno, dos, tres = 0, 0, 0
        while uno == dos or uno == tres or dos == tres:
            uno, dos, tres = randint(0,11), randint(0,11), randint(0,11)
        self.especialidades = [uno, dos, tres]


    def recibir_consultas(self):
        """
        funcion que le quita respuestas al ayudante de sus 200 disponibles
        """
        self.respuestas -= 1


    def __str__(self):
        return self.nombre


class Tareos:
    def __init__(self, nombre):
        self.nombre = nombre


class Coordinador:
    """
    representa al Malvado Dr. Mavrakis
    """
    def __init__(self, nombre, prob):
        """
        :param nombre: nombre del malvado
        :type nombre: str
        :param prob: probabilidad de atrasar notas
        :type prob: float
        """
        self.nombre = nombre
        self.exigencia_act = 0
        self.exigencia_tar = 0
        self.prob = prob


    def atrasar_notas(self):
        """
        funcion para decidir si atrasar notas o no
        """
        if random() < self.prob:
            return True
        return False
