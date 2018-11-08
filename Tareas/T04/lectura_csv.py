originales =  {"prob_40_creditos": 0.1,
               "prob_50_creditos": 0.7,
               "prob_55_creditos": 0.15,
               "prob_60_creditos": 0.05,
               "nivel_inicial_confianza_inferior": 2,
               "nivel_inicial_confianza_superior": 12,
               "prob_visitar_profesor": 0.2,
               "prob_atraso_notas_Mavrakis": 0.1,
               "porcentaje_progreso_tarea_mail": 0,
               "fiesta_mes": 0,
               "partido_futbol_mes": 0}
nuevas = {}
escenarios = []
with open("escenarios.csv", "r") as leer:
    next(leer)
    for i in leer:
        a = i.strip().split(",")
        nuevas[a[0]] = []
        for b in a:
            if b != a[0]:
                if b != "-":
                    nuevas[a[0]].append(float(b))
                else:
                    nuevas[a[0]].append(originales[a[0]])
        escenarios.append(nuevas)
for i in originales:
    if i not in nuevas:
        nuevas[i] = [originales[i] for b in range(len(nuevas["prob_55_creditos"]))]
