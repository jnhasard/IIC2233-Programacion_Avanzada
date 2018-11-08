from math import pi, sqrt

def leer(archivo):
    data = open(archivo, "r")
    leible = data.readlines()
    lista = []
    for i in leible:
        lista.append(i.strip().split(","))
    return lista
lista_met = leer("meteorologia.csv")
lista_inc = leer("incendios.csv")

class Incendio:
    def __init__(self, ids, lat, lon, potencia, fecha_inicio, fecha_actual):
        self.ids = ids
        self.lat = lat
        self.lon = lon
        self.potencia = potencia
        self.fecha_inicio = Fecha(fecha_inicio)
        self.fecha_actual = Fecha(fecha_actual)
        self.mins_transcurridas = self.fecha_inicio.\
            calcular_mins(self.fecha_actual)
        self.tasa = 500/60 #metros por minuto
        self.punto_poder_inicial = ((1) ** 2) * pi * \
                                   float(self.potencia)
        self.radio = self.tasa * float(self.mins_transcurridas)
        self.punto_poder = (self.radio ** 2) * pi * float(self.potencia)
        if self.punto_poder_inicial != 0:
            self.porcentaje = (self.punto_poder_inicial - self.punto_poder) / \
                              self.punto_poder_inicial * 100
        else:
            self.porcentaje = 0
        if self.porcentaje < 0:
            self.porcentaje = 0
        self.recursos = []
        self.x = float(self.lat)*110
        self.y = float(self.lon)*110
        self.fecha_final = ""

    def pronostico(self, pronostico):

        inic_act = pronostico.fecha_inicio.calcular_mins(self.fecha_actual)
        # >0 comenzo antes de la fecha actual
        ter_act = pronostico.fecha_termino.calcular_mins(self.fecha_actual)
        # <=0 termina despues de la fecha actual, caso contrario termina antes
        inic_inic = pronostico.fecha_inicio.calcular_mins(self.fecha_inicio)
        # >= 0 empieza antes que el incendio, caso contrario comienz despues
        ter_inic = pronostico.fecha_termino.calcular_mins(self.fecha_inicio)
        # >= 0 termina antes de que empiece el incendio
        mins = 0

        if inic_act > 0 and ter_inic < 0 and self.intersectan(pronostico):
            if ter_act <= 0 and inic_inic >= 0:
                mins = self.mins_transcurridas
            elif ter_act <= 0 and inic_inic < 0:
                mins = pronostico.fecha_inicio.calcular_mins\
                    (self.fecha_actual)
            elif ter_act > 0 and inic_inic < 0:
                mins = pronostico.fecha_inicio.calcular_mins\
                    (pronostico.fecha_termino)
            elif ter_act > 0 and inic_inic >= 0:
                mins = self.fecha_inicio.calcular_mins(self.fecha_actual)
            if pronostico.tipo == "VIENTO":
                self.tasa += 60 * (pronostico.valor) / 100 * mins
            elif pronostico.tipo == "TEMPERATURA":
                if float(pronostico.valor) > 30:
                    self.tasa += 25 * ((pronostico.valor) - 30) * mins/60
            elif pronostico.tipo == "LLUVIA":
                self.tasa -= 50 * pronostico.valor * mins/60
            self.actualizar(mins)

    def intersectan(self, pronostico):
        dist_x = abs(self.x-pronostico.x)
        dist_y = abs(self.y-pronostico.y)
        dist = sqrt(dist_x**2+dist_y**2)
        radios = self.radio + pronostico.radio
        if dist < radios:
            return True
        else:
            return False

    def simular(self, lista):
        ind_id = lista[0].index("id:string")
        ind_fechai = lista[0].index("fecha_inicio:string")
        ind_fechat = lista[0].index("fecha_termino:string")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_tipo = lista[0].index("tipo:string")
        ind_valor = lista[0].index("valor:float")
        ind_radio = lista[0].index("radio:int")
        for index in range(len(lista)-1):
            if index != 0:
                met = Meteorologia(lista[index][ind_id],
                                    lista[index][ind_fechai],
                                    lista[index][ind_fechat],
                                    lista[index][ind_tipo],
                                    lista[index][ind_valor],
                                    lista[index][ind_lat],
                                    lista[index][ind_lon],
                                    lista[index][ind_radio])
                self.pronostico(met)

    def actualizar(self, mins):
        self.radio += self.tasa*mins
        self.punto_poder = (self.radio ** 2) * pi * float(self.potencia)


class Fecha:
    def __init__(self, original):
        fecha = original.split()[0]
        horas = original.split()[1]
        fecha = fecha.split("-")
        horas = horas.split(":")
        self.año = int(fecha[0])
        self.mes = int(fecha[1])
        self.dia = int(fecha[2])
        self.hora = int(horas[0])
        self.minuto = int(horas[1])
        self.segundo = int(horas[2])
        self.original = original

    def __str__(self):
        return self.original

    def convertir(self):
        bis = self.año // 4
        añosendias = 365 * (self.año - 1) + bis
        mesendias = 0
        for i in range(self.mes):
            if i == 0:
                continue
            elif i == 1 or i == 3 or i == 5 or i == 7 or i == 8 or i == 10 or\
                            i == 12:
                mesendias += 31
            else:
                if i == 2:
                    if self.año % 4 == 0:
                        mesendias += 29
                    else:
                        mesendias += 28
                else:
                    mesendias += 30
        suma_final = (añosendias + mesendias + (self.dia - 1))*24*60 \
                     + self.hora * 60 + self.minuto + self.segundo/60
        return suma_final

    def calcular_mins(self, otra):
        return (otra.convertir()-self.convertir())


class Meteorologia:
    def __init__(self, ids, fecha_inicio, fecha_termino, tipo, valor,
                 lat, lon, radio):
        self.ids = ids
        self.fecha_inicio = Fecha(fecha_inicio)
        self.fecha_termino = Fecha(fecha_termino)
        self.tipo = tipo
        self.valor = float(valor)
        self.lat = float(lat)
        self.lon = float(lon)
        self.radio = int(radio)
        self.x = int(self.lat) * 110
        self.y = int(self.lon) * 110


class Recurso:
    def __init__(self, ids, tipo, vel, lat, lon, autonomia, delay,
                 tasa_extincion, costo):
        self.ids = ids
        self.tipo = tipo
        self.velocidad = vel
        self.lat = lat
        self.lon = lon
        self.autonomia = autonomia
        self.delay = delay
        self.tasa_extincion = tasa_extincion
        self.costo = costo
        self.estado = "Standby"
        self.fecha_salida = ""
        self.tiempo_trabajado = 0










#
# incendio = Incendio(lista_inc[1][0],lista_inc[1][1],lista_inc[1][2],lista_inc[1][3],lista_inc[1][4], "2017-03-06 05:01:10" )
# incendio.simular(lista_met)
# print(incendio.punto_poder_inicial)