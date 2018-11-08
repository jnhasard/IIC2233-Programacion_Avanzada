from comandos_bool import comparar
lista = ["+", "-", "*", "/", "==", ">", "<", ">=", "<=", "!="]

def operaciones(simbolo, a, b):
    if simbolo == "+":
        return a + b
    elif simbolo == "-":
        return a - b
    elif simbolo == "*":
        return a * b
    elif simbolo == "/":
        return a / b


def extraer_columna(nombre_archivo, columna):
    with open(nombre_archivo + ".csv", "r") as arch:
        aux = next(arch).strip().split(";")
        ind = aux.index(list(filter(lambda x: columna in x, aux))[0])
        return [float(i.split(";")[ind]) for i in arch]


def filtrar(columna, simbolo, valor):
    global lista
    if simbolo in lista:
        return list(i for i in filter(lambda x: comparar(float(x), simbolo, valor), columna))
    else:
        raise AssertionError("Simbolo invalido")


def operar(columna, simbolo, valor):
    global lista
    if simbolo in ["+", "-", "*", "/", ">=<"]:
        if simbolo == ">=<" and valor >= 0:
            return list(map(lambda x: round(x,valor), columna))
        else:
            return list(
                map(lambda x: operaciones(simbolo, float(x), valor), columna))
    else:
        raise AssertionError("Simbolo invalido")


def evaluar(funcion, inicio, final, intervalo):
    aux = intervalos(inicio, final, intervalo)
    lista = [i for i in range(aux[0],aux[1])][::aux[2]]
    lista = list(map(lambda x: x/(aux[3]), lista))
    return list(map(lambda x: funcion(x), lista))


def intervalos(inicio, final, intervalo):
    a = [abs(float(inicio)), abs(float(final)), abs(float(intervalo))]
    a.sort()
    a = list(filter(lambda x: x != 0, a))
    b = a[0]
    elevar = 0
    if b%1 != 0:
        if "e-" in str(intervalo):
            elevar = int(str(intervalo).split("e-")[1])
        else:
            elevar = len(str(intervalo).split(".")[1])
    intervalo = int(float(intervalo) * 10 ** elevar)
    inicio = int(float(inicio) * 10 ** elevar)
    final = int(float(final) * 10 ** elevar)
    return [inicio, final, intervalo, 10**elevar]
