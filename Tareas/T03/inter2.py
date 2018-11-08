from comandos_basicos import dicc
import errores


def interprete(consulta):
    global dicc
    if consulta[0] != "do_if":
        pendientes = list(filter(lambda x: type(x) is list, consulta))
        if len(pendientes) > 0:
            if pendientes[0][0] not in dicc:
                pendientes = []
        nueva = [dicc[i] if str(i) in dicc else i for i in consulta]
        if len(pendientes) == 0:
            ret = None
            if consulta[0] in ["asignar", "graficar", "extraer_columna",]:
                if len(consulta) != 3:
                    raise errores.ArgumentoInvalido(consulta[0], consulta[1:])
                ret = nueva[0](nueva[1],nueva[2])
            elif consulta[0] in ["LEN", "PROM", "DESV", "MEDIAN", "VAR"]:
                if len(consulta) != 2:
                    raise errores.ArgumentoInvalido(consulta[0],consulta[1:])
                ret = nueva[0](nueva[1])
            elif consulta[0] in ["filtrar", "operar", "comparar", "do_if"]:
                if len(consulta) != 4:
                    raise errores.ArgumentoInvalido(consulta[0],consulta[1:])
                ret = nueva[0](nueva[1], nueva[2], nueva[3])
            elif consulta[0] in ["evaluar", "comparar_columna"]:
                if len(consulta) != 5:
                    raise errores.ArgumentoInvalido(consulta[0],consulta[1:])
                ret = nueva[0](nueva[1], nueva[2], nueva[3], nueva[4])
            elif consulta[0] == "crear_funcion":
                ret = nueva[0](nueva[1], nueva[2:])
            return ret
        else:
            prox = [interprete(i) if type(i) is list else i for i in nueva]
            if consulta[0] in ["asignar", "graficar", "extraer_columna",]:
                return prox[0](prox[1],prox[2])
            elif consulta[0] in ["LEN", "PROM", "DESV", "MEDIAN", "VAR"]:
                return prox[0](prox[1])
            elif consulta[0] in ["filtrar", "operar", "comparar", "do_if"]:
                return prox[0](prox[1], prox[2], prox[3])
            elif consulta[0] in ["evaluar", "comparar_columna"]:
                return prox[0](prox[1], prox[2], prox[3], prox[4])
    else:
        return dicc["do_if"](consulta[1], consulta[2], consulta[3])


def do_if(consulta_a, consulta_b, consulta_c):
    if interprete(consulta_b):
        return interprete(consulta_a)
    else:
        return interprete(consulta_c)

dicc["do_if"] = do_if

# a= [
# 	["asignar", "x", ["extraer_columna", "registros", "tiempo_sano"]],
# 	["asignar", "y", ["extraer_columna", "registros", "muertos_avistados"]],
# 	["comparar", ["PROM", "x"], ">", ["DESV", "y"]],
# 	["asignar", "filtrado", ["filtrar", "x", ">", 100]],
# 	["asignar", "funcion_normal", ["evaluar", ["crear_funcion", "normal", 0, 0.5], -3, 5, 0.1]],
# 	["PROM", "filtrado"],
# 	["VAR", "funcion_normal"],
# 	["do_if", ["VAR", "funcion_normal"], ["comparar_columna", "funcion_normal", ">", "DESV", "x"], ["PROM", "x"]],
# 	["graficar", "filtrado", "numerico"],
# 	["graficar", "normal", "rango: -3,5,0.1"],
# 	["asignar", "gamma", ["evaluar", ["crear_funcion", "gamma", 2, 0.16666666666666666], 0, 40, 4e-05]],
# 	["comparar_columna", "x", ">", "DESV", "gamma"],
# 	["graficar", "x", "rango: 0.00004, 40, 0.00004"],
# 	["graficar", "x", "normalizado"]
# ]
#
# respuestas = ""
# contador = 0
# for i in a:
#     contador += 1
#     respuestas += "----- Consulta " + str(contador) + "-----\n"
#     try:
#         text = str(interprete(i))
#         respuestas += text + "\n"
#         print(text)
#     except (errores.ArgumentoInvalido, errores.ReferenciaInvalida, AssertionError) as err:
#         print(err)
#         respuestas += str(err) + "\n"
#
# salida = open("resultados.txt", "w")
# salida.writelines(respuestas)
# salida.close()