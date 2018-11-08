import simulacion, menu, usuarios, os

carpeta = os.getcwd() + "/Reportes Estrategias de Extinción"
if not os.path.exists(carpeta):
    os.mkdir("Reportes Estrategias de Extinción")


def leer(archivo):
    data = open(archivo, "r")
    leible = data.readlines()
    lista = []
    for i in leible:
        lista.append(i.strip().split(","))
    return lista


lista_us = leer("usuarios.csv")
lista_rec = leer("recursos.csv")
lista_met = leer("meteorologia.csv")
lista_inc = leer("incendios.csv")

menu.menu(lista_us, lista_rec, lista_inc, lista_met)
