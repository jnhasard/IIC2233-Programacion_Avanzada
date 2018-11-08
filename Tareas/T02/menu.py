from Listasjh import jhlist
from Enfermedad import Infeccion, Cura
import os, shutil

def menu(mundo):
    xdia = jhlist()
    dia = 0
    print("Bienvenido a PANDEMIC")
    while True:
        try:
            tipo = int(input("Elija el tipo de infeccion: " +
                             "\n1-Bacteria\n2-Virus\n3-Parásito\n--->  "))
            if tipo == 1:
                infec = Infeccion("Bacteria")
            elif tipo == 2:
                infec = Infeccion("Virus")
            elif tipo == 3:
                infec = Infeccion("Parásito")
            break
        except:
            print("Elija un numero entre 1 y 3")
    while True:
        inicio = input("En que pais quiere comenzar a infectar: ")
        if not mundo.finder(inicio):
            print("Elija un pais existente en la base de datos")
            continue
        else:
            mundo[mundo.finder(inicio)].valor.infectados = 1
            mundo[mundo.finder(inicio)].valor.pob_anterior = jhlist(1,0)
            mundo[mundo.finder(inicio)].valor.clasificacion = "Infectado"
            break
    pob_inicial = 0
    for i in mundo:
        pob_inicial += i.valor.pob_inicial
    cura = Cura(pob_inicial, infec)
    Juego = True
    paises_diario = jhlist()
    muertes_diario = 0
    infectados_diario = 0
    while Juego:
        while True:
            try:
                op = int(input("MENU dia:"+ str(dia) + "\n1--Pasar de Dia\n"
                                                       "2--Estadisticas\n"
                                                       "3--Guardar Partida\n"
                                                       "4--Salir del Juego\n"
                                                       "---> "))
                if op != 1 and op != 2 and op != 3 and op != 4:
                    raise IndexError
                else:
                    break
            except:
                print("Escoja un menu válido")
        if op == 1:
            paises_diario = jhlist()
            muertes_diario = 0
            infectados_diario = 0
            dia += 1
            cola = jhlist()
            for pais in mundo:
                if pais.valor.clasificacion == "Infectado":
                    cerrar_f = (pais.valor.infectados / pais.valor.pob_inicial)\
                               > 0.5 or\
                        (pais.valor.muertes / pais.valor.pob_inicial) > 0.25
                    cerrar_a = (pais.valor.infectados / pais.valor.pob_inicial)\
                               > 0.8 or\
                        (pais.valor.muertes / pais.valor.pob_inicial) > 0.2
                    if cerrar_f and pais.valor.frontera:
                        cola.agregar(pais.valor.gobierno.agregar(mundo,
                            1))
                    if cerrar_a and pais.valor.aeropuerto:
                        cola.agregar(pais.valor.gobierno.agregar(mundo,
                            2))
                    if (pais.valor.poblacion / pais.valor.pob_inicial) < (2/3):
                        cola.agregar(pais.valor.gobierno.agregar(mundo, 3))
                    if cura.cura and not pais.valor.aeropuerto:
                        cola.agregar(pais.valor.gobierno.agregar(mundo, 4))
                        cola.agregar(pais.valor.gobierno.agregar(mundo, 5))
                    if len(cola) > 0:
                        cola.sort()
                    paises_diario.suma(pais.valor.traslado(mundo))
                    aux = pais.valor.contagio(infec)
                    infectados_diario += aux[0].valor
                    muertes_diario += aux[1].valor
                    mundo[mundo.finder(str(pais))].valor.dias += 1
                    if pais.valor.cura:
                        mundo[mundo.finder(str(pais))].\
                            valor.repartir_cura(mundo)
                        mundo[mundo.finder(str(pais))].valor.curar()
            if not cura.descubierto and not cura.cura:
                cura.descubrimiento(infectados_diario, muertes_diario)
            elif cura.descubierto and not cura.cura:
                cura.progreso(infectados_diario, muertes_diario, mundo)
            string = "Dia " + str(dia) + "\n--> Infectados: " + \
                     str(infectados_diario) + "\n--> Muertos: " + \
                     str(muertes_diario)
            xdia.agregar(string)
            if len(cola) >= 3:
                for i in range(3):
                    mundo[mundo.finder(cola[i].valor[2])].valor.gobierno.\
                        ejecutar(cola[i].valor[1], mundo)
            elif len(cola) < 3 and len(cola) > 0:
                for i in cola:
                    mundo[mundo.finder(i.valor[2])].valor.gobierno.\
                        ejecutar(i.valor[1], mundo)
        elif op == 2:
            while True:
                try:
                    est = int(input("---MENU ESTADISTICAS---\n"
                                    "1-Resumen del dia\n"
                                    "2-Por pais\n"
                                    "3-Global\n"
                                    "4-Muertes e infecciones por dia\n"
                                    "5-Promedio muertes e infecciones\n--->"))
                    if est != 1 and est != 2 and est != 3 and est != 4 and \
                                    est != 5:
                        raise IndexError
                    break
                except:
                    print("Elija un numero valido")
            if est == 1:
                print(" >> RESUMEN DEL DIA ", dia, "<<")
                print("-" * 20 + "+" + "-" * 5)
                print("Gente infectada"+ " "*5 + "| " + str(infectados_diario))
                print("-" * 20 + "+" + "-" * 5)
                print("Gente muerta" + " "*8 + "| " + str(muertes_diario))
                print("-" * 20 + "+" + "-" * 5)
                print("Paises infectados" + " "*3 + "| " + str(paises_diario))
                print("-" * 20 + "+" + "-" * 5)
            elif est == 2:
                while True:
                    paisest = input("Que pais quiere elegir: ")
                    if not mundo.finder(paisest):
                        print("Elija un pais existente en la base de datos")
                        continue
                    else:
                        break
                paisest = mundo[mundo.finder(paisest)].valor
                print("\nRESUMEN DEL DIA", dia, "--", paisest)
                print("-" * 20 + "+" + "-" * 10)
                print("Gente viva", " " * 8 , "|", paisest.poblacion)
                print("-" * 20 + "+" + "-" * 10)
                print("Gente infectada", " " * 3 , "|", paisest.pob_anterior[0])
                print("-" * 20 + "+" + "-" * 10)
                print("Gente muerta", " " * 6, "|", paisest.pob_anterior[1])
                print("-" * 20 + "+" + "-" * 10)
            elif est == 3:
                while True:
                    opest = int(input("1-Mostrar paises limpios\n"
                                      "2-Mostrar paises infectados\n"
                                      "3-Mostrar paises muertos\n--> "))
                    if opest != 1 and opest != 2 and opest != 3:
                        raise IndexError
                    else:
                        break
                cont = 1
                total_vivo = 0
                total_muerta = 0
                total_infectada = 0
                total_sana = 0
                for i in mundo:
                    total_vivo += i.valor.poblacion
                    total_muerta += i.valor.muertes
                    total_infectada += i.valor.infectados
                    total_sana += i.valor.pob_inicial
                    if opest == 1 and i.valor.clasificacion == "Limpio":
                        print(cont, ")", i.valor)
                        cont += 1
                    elif opest == 2 and i.valor.clasificacion == "Infectado":
                        print(cont, ")", i.valor)
                        cont += 1
                    elif opest == 3 and i.valor.clasificacion == "Muerto":
                        print(cont, ")", i.valor)
                        cont += 1
                total_sana -= total_infectada
                print("--------------")
                print("Total vivos:", total_vivo, "\nTotal muertos:",
                      total_muerta, "\nTotal infectados:", total_infectada,
                      "\nTotal sana:", total_sana, "\n")
            elif est == 4:
                print("")
                for i in xdia:
                    print(i)
                print("")
            elif est == 5:
                while True:
                    try:
                        tasa = int(input("1-Tasa del dia\n2-Tasa acumulada\n"
                                         "--> "))
                        break
                    except:
                        print("Elija una opcion valida")
                total_muerta = 0
                total_vivo = 0
                for i in mundo:
                    total_vivo += i.valor.poblacion
                    total_muerta += i.valor.muertes
                print("Muertos" + " "*len(str(muertes_diario)) + "/ Vivos")
                if tasa == 1:
                    print(muertes_diario, " "*5 , "/", total_vivo)
                if tasa == 2:
                    print(total_muerta, " "*5, "/", total_vivo)
        elif op == 3:
            carpeta = os.getcwd() + "/Partidas Guardadas"
            if not os.path.exists(carpeta):
                os.mkdir("Partidas Guardadas")
            nombre = input("Como le quiere llamar a la partida: ")
            carpeta = os.getcwd() + "/Partidas Guardadas/" + nombre
            if not os.path.exists(carpeta):
                os.mkdir("Partidas Guardadas/" + nombre)
            archivo = open("Partidas Guardadas/" + nombre + "/Partida", "w")
            srcfile = "random_airports.csv"
            dstroot = "Partidas Guardadas/" + nombre +"/"
            shutil.copy(srcfile, dstroot)
            print("Guardando su partida...")
            archivo.close()


        elif op == 4:
            Juego = False


