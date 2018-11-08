from comandos_numerico import LEN, PROM, DESV, MEDIAN, VAR


def comparar_columna(columna_1, simbolo, comando, columna_2):
    if comando is LEN:
        return comparar(LEN(columna_1), simbolo, LEN(columna_2))
    elif comando is PROM:
        return comparar(PROM(columna_1), simbolo, PROM(columna_2))
    elif comando is DESV:
        return comparar(DESV(columna_1), simbolo, DESV(columna_2))
    elif comando is MEDIAN:
        return comparar(MEDIAN(columna_1), simbolo, MEDIAN(columna_2))
    elif comando is VAR:
        return comparar(VAR(columna_1), simbolo, VAR(columna_2))


def comparar(a, simbolo , b):
    if simbolo == "<":
        return a < b
    elif simbolo == ">":
        return a > b
    elif simbolo == "==":
        return a == b
    elif simbolo == ">=":
        return a >= b
    elif simbolo == "<=":
        return a <= b
    elif simbolo == "!=":
        return a != b

