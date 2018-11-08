from DES import Contenido, Alumno, Profesor, Tareos, Docencia, Coordinador
from Simulacion import Simulacion
import matplotlib.pyplot as plt
from lectura_csv import nuevas

with open("contenidos.csv", "r") as contents:
    contents.readline()
    contenidos = []
    for _ in range(12):
        linea = contents.readline().strip().split(",")
        contenidos.append(Contenido(linea[0], linea[1], linea[2], linea[3], linea[4], linea[5]))

with open("integrantes.csv", "r") as integrantes:
    alumnos = []
    profesores = []
    docencia = []
    tareos = []
    personas = integrantes.readlines()
    secciones = 0
    sec = []
    coordinador = None
    for persona in personas:
        linea = persona.strip().split(",")
        if linea[1] == "Alumno":
            alumnos.append(Alumno(linea[0], linea[2], 0.1, 0.7, 0.15, 0.05, 2, 12, 0.2))
        elif linea[1] == "Profesor":
            profesores.append(Profesor(linea[0],linea[2]))
        elif linea[1] == "Tareas":
            tareos.append(Tareos(linea[0]))
        elif linea[1] == "Docencia":
            docencia.append(Docencia(linea[0]))
        else:
            coordinador = Coordinador(linea[0], 0.1)
        if linea[2] not in sec and linea[2].isdigit():
            sec.append(linea[2])
            secciones += 1

sim = Simulacion(contenidos, alumnos, profesores, docencia, tareos, coordinador, secciones)
sim.run()


nuevo = []
aux = 0
for i in sim.notasc:
    for b in range(aux, i[1]):
        nuevo.append(i[0])
    aux = i[1]
while len(nuevo) < 12:
    nuevo.append(nuevo[-1])
lista = [i for i in range(12)]

plt.plot(lista, sim.notas_act, label="Actividades")
plt.plot(lista, sim.notast, label="Tareas")
plt.plot(lista, nuevo, label="Controles")
plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
plt.ylabel("Notas promedio")
plt.xlabel("Semana")
plt.title("Notas Promedio vs Semanas")
plt.show()

while True:
    nombre = input("\n\n\nIngrese el nombre del alumno al que quiere investigar o 1 para continuar")
    if nombre == "1":
        break
    alumno = None
    for i in sim.alumnos:
        if i.nombre == nombre:
            alumno = i
    if alumno != None:
        opcion = int(input("1.Cualidades\n2.Notas\n3.Exit "))
        if opcion == 1:
            print(alumno, "\n--Nivel de programacion:", alumno.nivel_programacion,
                  "\n--Confianza:", alumno.confianza,
                  "\n--Manejo de contenidos:", alumno.manejo_de_contenidos, "\n")
        elif opcion == 2:
            print(alumno, "\n--Notas actividades:", str(alumno.notas_act).lstrip("[").strip("]"),
                  "\n--Notas controles:", str(alumno.notas_cont).lstrip("[").strip("]"),
                  "\n--Notas tareas:", str(alumno.notas_tar).lstrip("[").strip("]"),
                  "\nPromedio final:", alumno.promedio, "\n")
        else: break
    else:
        print("Ingrese un alumno valido")

salida = open("parametros.csv", "w")
salida.writelines("Cantidad_profesores,Cantidad_ayudantes,Cantidad_alumnos\n" + str(len(profesores))
                  + "," + str(len(docencia) + len(tareos) + 1) + "," + str(len(alumnos)))
escenarios = int(input("Quiere probar con distintos escenarios?\n 1 si quiere 2 si no quiere "))
if escenarios == 1:
    try:
        sims = []
        for i in range(len(nuevas["prob_55_creditos"])):
            with open("integrantes.csv", "r") as integrantes:
                alumnos = []
                profesores = []
                docencia = []
                tareos = []
                personas = integrantes.readlines()
                secciones = 0
                sec = []
                coordinador = None
                for persona in personas:
                    linea = persona.strip().split(",")
                    if linea[1] == "Alumno":
                        alumnos.append(Alumno(linea[0], linea[2], nuevas["prob_40_creditos"][i],
                                              nuevas["prob_50_creditos"][i],
                                              nuevas["prob_55_creditos"][i], nuevas["prob_60_creditos"][i],
                                              nuevas["nivel_inicial_confianza_inferior"][i],
                                              nuevas["nivel_inicial_confianza_superior"][i],
                                              nuevas["prob_visitar_profesor"][i]))
                    elif linea[1] == "Profesor":
                        profesores.append(Profesor(linea[0], linea[2]))
                    elif linea[1] == "Tareas":
                        tareos.append(Tareos(linea[0]))
                    elif linea[1] == "Docencia":
                        docencia.append(Docencia(linea[0]))
                    else:
                        coordinador = Coordinador(linea[0], nuevas["prob_atraso_notas_Mavrakis"][i])
                    if linea[2] not in sec and linea[2].isdigit():
                        sec.append(linea[2])
                        secciones += 1

            sims.append(Simulacion(contenidos, alumnos, profesores, docencia, tareos, coordinador, secciones))
            sims[i].run()
    except:
        print("Ocurrio un error")