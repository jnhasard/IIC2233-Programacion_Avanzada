from Listasjh import jhlist
from Pais import Pais, Gobierno
from menu import menu

def big_bang():
    mundo = jhlist()
    entrada = open("population.csv", "r")
    for i in entrada.readlines():
        b = i.strip().split(",")
        if b[0] != "Pais":
            mundo.agregar(Pais(b[0], b[1]))
            mundo[mundo.finder(b[0])].valor.gobierno = Gobierno(
                mundo[mundo.finder(b[0])].valor)
    for i in range(len(mundo)):
        mundo[i].valor.border()
        mundo[i].valor.aeropuertos()
    return mundo

menu(big_bang())