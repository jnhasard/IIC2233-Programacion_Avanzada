import matplotlib.pyplot as plt
from comandos_numerico import LEN, PROM, DESV, MEDIAN, VAR
from comandos_datos import extraer_columna, filtrar, operar, evaluar, intervalos
from comandos_bool import comparar, comparar_columna
from probabilidades import normal, exponencial, gamma


def asignar(variable, dato):
    global dicc
    if str(variable) not in dicc:
        dicc[variable] = dato
    return "asignar"


def crear_funcion(nombre_modelo, *parametros):
    if nombre_modelo == "normal":
        u = parametros[0][0]
        o = parametros[0][1]
        return normal(u,o)
    elif nombre_modelo == "exponencial":
        v = parametros[0][0]
        return exponencial(v)
    elif nombre_modelo == "gamma":
        v = parametros[0][0]
        k = parametros[0][1]
        return gamma(v,k)


def graficar(columna, opcion):
    if type(opcion) is str:
        if opcion == "numerico":
            plt.plot(columna)
        elif opcion == "normalizado":
            suma = sum(columna)
            rango = range(0,LEN(columna))
            plt.plot(list(map(lambda x: x/suma, rango)), columna)
        elif "rango" in opcion:
            rango = opcion.split(": ")[1].split(",")
            aux = intervalos(rango[0], rango[1], rango[2])
            a, b, c, d = aux[0], aux[1], aux[2], aux[3]
            lista = [i for i in range(a, b)][::c]
            lista = list(map(lambda x: x / d, lista))
            if LEN(lista) == LEN(columna):
                # if LEN(lista) != LEN(columna):
                #     lista = lista[:LEN(columna)]
                if a > b and c < 0:
                    plt.plot(lista, columna)
                elif a < b and c > 0:
                    plt.plot(lista, columna)
                else:
                    raise AssertionError("lista con valores neg")
            else:
                raise AssertionError("largo de rango es distinto a columna")
        else:
            raise AssertionError("opcion invalida")
    elif type(opcion) is list:
        if LEN(opcion) <= LEN(columna):
            plt.plot(opcion, columna)
    plt.ylabel('some numbers')
    plt.show()
    return "graficar"


dicc = {"asignar": asignar, "crear_funcion": crear_funcion,
        "graficar": graficar, "extraer_columna": extraer_columna,
        "filtrar": filtrar, "operar": operar, "evaluar": evaluar, "LEN": LEN,
        "PROM":PROM, "DESV": DESV, "MEDIAN": MEDIAN, "VAR": VAR,
        "comparar_columna": comparar_columna, "comparar":comparar}