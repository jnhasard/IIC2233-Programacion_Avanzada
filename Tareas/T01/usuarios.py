import simulacion


class Usuario:
    def __init__(self, ids, nombre, clave, recurso_id, tipo, fecha):
        self.ids = ids
        self.nombre = nombre
        self.clave = clave
        self.recurso_id = recurso_id
        self.tipo = tipo
        self.fecha = fecha


class Anaf(Usuario):
    def __init__(self, ids, nombre, clave, recurso_id, tipo, fecha):
        super().__init__(ids, nombre, clave, recurso_id, tipo, fecha)

    # consultas básicas
    def leer_usuario(self, lista):
        ind_id = lista[0].index("id:string")
        ind_nombre = lista[0].index("nombre:string")
        ind_contraseña = lista[0].index("contraseña:string")
        ind_recurso = lista[0].index("recurso_id:string")
        intento = True
        while intento:
            try:
                index = int(input("Indique el id del Usuario que busca: ")) + 1
                intento = False
            except:
                print("Elija un id valido")
        if index < len(lista):
            print(
                "\n--ID: " + lista[index][ind_id] + "\n--Nombre:" + lista[index]
                [ind_nombre] + "\n--Clave: " + lista[index]
                [ind_contraseña])
            if len(lista[index][ind_recurso]) > 0:
                print("--Recurso_id: " + lista[index][ind_recurso] + "\n")
            else:
                print("")
        else:
            print("Intentelo con un usuario existente")
            self.leer_usuario(lista)

    def leer_incendio(self, lista):
        ind_id = lista[0].index("id:string")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_potencia = lista[0].index("potencia:int")
        ind_fecha = lista[0].index("fecha_inicio:string")
        intento = True
        while intento:
            try:
                index = int(input("Indique el id del Incendio: ")) + 1
                intento = False
            except:
                print("Elija un id valido")
        if index < len(lista):
            incendio = simulacion.Incendio(lista[index][ind_id],
                                           str(lista[index][ind_lat]),
                                           str(lista[index][ind_lon]),
                                           str(lista[index][ind_potencia]),
                                           lista[index][ind_fecha], self.fecha)
            print("\n--ID: " + incendio.ids +
                  "\n--Latitud:" + str(incendio.lat) +
                  "\n--Longitud: " + str(incendio.lon) +
                  "\n--Potencia: " + str(incendio.potencia) +
                  "\n--Fecha inicio: " + str(incendio.fecha_inicio) +
                  "\n--Porcentaje de extincion: " + str(incendio.porcentaje)
                  + "%" +
                  "\n--Recursos utilizados: " + ", ".join(incendio.recursos)
                  + "\n")
        else:
            print("Intentelo con un incendio valido")
            self.leer_incendio(lista)

    def leer_recurso(self, lista):
        ind_id = lista[0].index("id:string")
        ind_tipo = lista[0].index("tipo:string")
        ind_velocidad = lista[0].index("velocidad:int")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_autonomia = lista[0].index("autonomia:int")
        ind_delay = lista[0].index("delay:int")
        ind_extincion = lista[0].index("tasa_extincion:int")
        ind_costo = lista[0].index("costo:int")
        intento = True
        while intento:
            try:
                index = int(input("Indique el id del Recurso que busca: ")) + 1
                intento = False
            except:
                print("Elija un id valido")
        if index < len(lista):
            recurso = simulacion.Recurso(lista[index][ind_id],
                                         lista[index][ind_tipo],
                                         lista[index][ind_velocidad],
                                         lista[index][ind_lat],
                                         lista[index][ind_lon],
                                         lista[index][ind_autonomia],
                                         lista[index][ind_delay],
                                         lista[index][ind_extincion],
                                         lista[index][ind_costo])
            print("\n--ID: " + str(recurso.ids) +
                  "\n--Tipo: " + str(recurso.tipo) +
                  "\n--Velocidad: " + str(recurso.velocidad) +
                  "\n--Latitud:" + str(recurso.lat) +
                  "\n--Longitud: " + str(recurso.lon) +
                  "\n--Autonomia: " + str(recurso.autonomia) +
                  "\n--Delay: " + str(recurso.delay) +
                  "\n--Tasa de Extincion: " + str(recurso.tasa_extincion) +
                  "\n--Costo: " + str(recurso.costo) +
                  "\n--Estado actual: " + str(recurso.estado) + "\n")
            if recurso.estado != "Standby":
                print("--Tiempo trabajado: " + str(recurso.tiempo_trabajado) +
                      "\n--Tiempo de trabajo restante: " +
                      str(int(recurso.autonomia) - recurso.tiempo_trabajado))
        else:
            print("Intentelo con un recurso valido")
            self.leer_recurso(lista)

    def agregar_usuario(self, lista):
        ind_id = lista[0].index("id:string")
        ind_nombre = lista[0].index("nombre:string")
        ind_contraseña = lista[0].index("contraseña:string")
        ind_recurso = lista[0].index("recurso_id:string")
        nombre = input("\nCual es su nombre: ")
        clave = input("Cual es su clave: ")
        recurso = input("Cual es su id de recurso: ")
        nuevo_usuario = [None, None, None, None]
        nuevo_usuario[ind_nombre] = nombre
        nuevo_usuario[ind_recurso] = recurso
        nuevo_usuario[ind_contraseña] = clave
        nuevo_usuario[ind_id] = str(int(lista[len(lista) - 1][ind_id]) + 1)
        salida = open("usuarios.csv", "a")
        salida.writelines((",").join(nuevo_usuario) + "\n")
        salida.close()
        print("Usuario agregado con exito!\n")

    def agregar_pronostico(self, lista):
        ind_id = lista[0].index("id:string")
        ind_fechai = lista[0].index("fecha_inicio:string")
        ind_fechat = lista[0].index("fecha_termino:string")
        ind_tipo = lista[0].index("tipo:string")
        ind_valor = lista[0].index("valor:float")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_radio = lista[0].index("radio:int")
        nuevo_pronostico = [None, None, None, None, None, None, None, None]
        nuevo_pronostico[ind_id] = str(int(lista[len(lista) - 1][ind_id]) + 1)
        nuevo_pronostico[ind_fechai] = input("\n--Indique la Fecha de inicio: ")
        nuevo_pronostico[ind_fechat] = input("--Indique la Fecha de termino: ")
        nuevo_pronostico[ind_tipo] = input("--Ingrese el Tipo: ")
        nuevo_pronostico[ind_valor] = input("--Ingrese el Valor: ")
        nuevo_pronostico[ind_lat] = (input("--Ingrese la Latitud geografica: "))
        nuevo_pronostico[ind_lon] = \
            (input("--Ingrese la Longitud geografica: "))
        nuevo_pronostico[ind_radio] = input("--Ingrese el Radio: ")
        salida = open("meteorologia.csv", "a")
        salida.writelines((",").join(nuevo_pronostico) + "\n")
        salida.close()
        print("Pronostico agregado con exito!\n")

    def agregar_incendios(self, lista):
        ind_id = lista[0].index("id:string")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_potencia = lista[0].index("potencia:int")
        ind_fecha = lista[0].index("fecha_inicio:string")
        nuevo_incendio = [None, None, None, None, None]
        nuevo_incendio[ind_id] = str(int(lista[len(lista) - 1][ind_id]) + 1)
        nuevo_incendio[ind_lat] = (input("\n--Ingrese la Latitud geografica: "))
        nuevo_incendio[ind_lon] = (input("--Ingrese la Longitud geografica: "))
        nuevo_incendio[ind_potencia] = (input("--Ingrese la Potencia: "))
        nuevo_incendio[ind_fecha] = input("--Indique la Fecha de inicio: ")
        salida = open("incendios.csv", "a")
        salida.writelines((",").join(nuevo_incendio) + "\n")
        salida.close()
        print("Incendio agregado con exito!\n")

    # consultas avanzadas
    def incendios_activos(self, lista):
        ind_id = lista[0].index("id:string")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_potencia = lista[0].index("potencia:int")
        ind_fecha = lista[0].index("fecha_inicio:string")
        for index in range(len(lista) - 1):
            if index != 0:
                incendio = simulacion.Incendio(lista[index][ind_id],
                                               str(lista[index][ind_lat]),
                                               str(lista[index][ind_lon]),
                                               str(lista[index][ind_potencia]),
                                               lista[index][ind_fecha],
                                               self.fecha)
                if incendio.fecha_inicio. \
                        calcular_mins(simulacion.Fecha(self.fecha)) >= 0:
                    if incendio.punto_poder > 0:
                        print("\n--Fecha inicio: " + str(incendio.fecha_inicio)
                              + "\n--Recursos utilizados: " +
                              ", ".join(incendio.recursos) +
                              "\n--Porcentaje de extinción: " +
                              str(incendio.porcentaje) + "\n")

    def incendios_apagados(self, lista):
        ind_id = lista[0].index("id:string")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_potencia = lista[0].index("potencia:int")
        ind_fecha = lista[0].index("fecha_inicio:string")
        for index in range(len(lista) - 1):
            if index != 0:
                incendio = simulacion.Incendio(lista[index][ind_id],
                                               str(lista[index][ind_lat]),
                                               str(lista[index][ind_lon]),
                                               str(lista[index][ind_potencia]),
                                               lista[index][ind_fecha],
                                               self.fecha)
                if incendio.punto_poder <= 0:
                    print("\n--Fecha inicio: " + str(incendio.fecha_inicio)
                          + "\n--Recursos utilizados: " +
                          ", ".join(incendio.recursos) +
                          "\n--Porcentaje de extinción: " +
                          str(incendio.porcentaje) +
                          "\n--Fecha final: " + str(incendio.fecha_final) +
                          "\n")

    def estrategia(self, lista, lista_rec, lista_met):
        ind_id = lista[0].index("id:string")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_potencia = lista[0].index("potencia:int")
        ind_fecha = lista[0].index("fecha_inicio:string")
        intento = True
        while intento:
            try:
                index = int(input("Indique el id del Incendio que quiere " +
                                  "apagar: ")) + 1
                intento = False
            except:
                print("Elija un incendio valido")
        incendio = simulacion.Incendio(lista[index][ind_id],
                                       str(lista[index][ind_lat]),
                                       str(lista[index][ind_lon]),
                                       str(lista[index][ind_potencia]),
                                       lista[index][ind_fecha], self.fecha)
        intento = True
        while intento:
            try:
                tipo = int(input(
                    "Que estrategia desea ustilizar para extinguir el incendio?:"
                    "\n1--Cantidad de recursos\n2--" +
                    "Tiempo de Extincion\n3--Costo Economico"))
                intento = False
            except:
                print("Elija un numero valido")
        if tipo == 1:
            print("Calculando estrategia...")
        elif tipo == 2:
            print("Calculando estrategia...")
        elif tipo == 3:
            print("Calculando estrategia...")
            self.costo(incendio, lista_rec, lista_met)

    def costo(self, incendio, lista, met):
        nombre = "Reportes Estrategias de Extinción/" + incendio.ids + "_" \
                 + self.nombre + "_" + "costo.txt"
        salida = open(nombre, "w")
        ind_id = lista[0].index("id:string")
        ind_tipo = lista[0].index("tipo:string")
        ind_velocidad = lista[0].index("velocidad:int")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_autonomia = lista[0].index("autonomia:int")
        ind_delay = lista[0].index("delay:int")
        ind_extincion = lista[0].index("tasa_extincion:int")
        ind_costo = lista[0].index("costo:int")
        usados = []
        incendio.simular(met)
        aux = 123456789876542345678834567892421342
        ok = False
        for i in lista:
            if not ok:
                ok = True
                continue
            if float(i[ind_costo]) <= aux:
                aux = float(i[ind_costo])
        ok = False
        for index in lista:
            if not ok:
                ok = True
                continue
            if float(index[ind_costo]) == aux and incendio.punto_poder > 0 and\
                            (index[ind_id] in usados) == False:
                usados.append(index)
                rec = simulacion.Recurso(index[ind_id],
                                             index[ind_tipo],
                                             index[ind_velocidad],
                                             index[ind_lat],
                                             index[ind_lon],
                                             index[ind_autonomia],
                                             index[ind_delay],
                                             index[ind_extincion],
                                             index[ind_costo])
                rec.estado = "En camino"
                rec.fecha_salida = self.fecha
                incendio.punto_poder -= float(rec.tasa_extincion) * \
                                        (incendio.fecha_inicio.calcular_mins
                                         (incendio.fecha_actual))
                incendio.recursos.append(rec.ids)
                string = ("Recurso: " + rec.ids + ", tipo -->" + rec.tipo +
                          "\nFecha salida:" + str(
                    rec.fecha_salida) + "\nFecha llegada:" +
                          "\nRegreso a la base:")
                salida.write(string)

        salida.close()


class Piloto(Usuario):
    def __init__(self, ids, nombre, clave, recurso_id, tipo, fecha, lista):
        super().__init__(ids, nombre, clave, recurso_id, tipo, fecha)
        ind_id = lista[0].index("id:string")
        ind_tipo = lista[0].index("tipo:string")
        ind_velocidad = lista[0].index("velocidad:int")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_autonomia = lista[0].index("autonomia:int")
        ind_delay = lista[0].index("delay:int")
        ind_extincion = lista[0].index("tasa_extincion:int")
        ind_costo = lista[0].index("costo:int")
        for i in lista:
            if i[ind_id] == self.recurso_id:
                index = lista.index(i)
        recurso = simulacion.Recurso(lista[index][ind_id],
                                     lista[index][ind_tipo],
                                     lista[index][ind_velocidad],
                                     lista[index][ind_lat],
                                     lista[index][ind_lon],
                                     lista[index][ind_autonomia],
                                     lista[index][ind_delay],
                                     lista[index][ind_extincion],
                                     lista[index][ind_costo])
        self.recurso = recurso
        self.inc_id = -1

    def leer_recurso(self, nada):
        intento = True
        while intento:
            try:
                index = input("Indique el id del Recurso que busca: ")
                intento = False
            except:
                print("Elija un id valido")
        if index == self.recurso_id:
            print("\n--ID: " + self.recurso.ids +
                  "\n--Tipo: " + self.recurso.tipo +
                  "\n--Velocidad: " + self.recurso.velocidad +
                  "\n--Latitud:" + self.recurso.lat +
                  "\n--Longitud: " + self.recurso.lon +
                  "\n--Autonomia: " + self.recurso.autonomia +
                  "\n--Delay: " + self.recurso.delay +
                  "\n--Tasa de Extincion: " + self.recurso.tasa_extincion +
                  "\n--Costo: " + self.recurso.costo +
                  "\n--Estado actual: " + self.recurso.estado + "\n")
            if self.recurso.estado != "Standby":
                print("--Tiempo trabajado: " +
                      str(self.recurso.tiempo_trabajado) +
                      "\n--Tiempo de trabajo restante: " +
                      str(int(self.recurso.autonomia) -
                          self.recurso.tiempo_trabajado))
        else:
            print(
                "Usted no esta asociado con este recurso," +
                " no puede ver la informacion")

    def leer_incendio(self, lista):
        intento = True
        while intento:
            try:
                index = int(input("Escriba el id del incendio a investigar: ")) \
                        + 1
                intento = False
            except:
                print("Elija un id valido")
        if index == self.inc_id:
            ind_id = lista[0].index("id:string")
            ind_lat = lista[0].index("lat:float")
            ind_lon = lista[0].index("lon:float")
            ind_potencia = lista[0].index("potencia:int")
            ind_fecha = lista[0].index("fecha_inicio:string")
            incendio = simulacion.Incendio(lista[index][ind_id],
                                           str(lista[index][ind_lat]),
                                           str(lista[index][ind_lon]),
                                           str(lista[index][ind_potencia]),
                                           lista[index][ind_fecha], self.fecha)
            print("\n--ID: " + incendio.ids +
                  "\n--Latitud:" + str(incendio.lat) +
                  "\n--Longitud: " + str(incendio.lon) +
                  "\n--Potencia: " + str(incendio.potencia) +
                  "\n--Fecha inicio: " + str(incendio.fecha_inicio) +
                  "\n--Porcentaje de extincion: " +
                  str(incendio.porcentaje) + "%" +
                  "\n--Recursos utilizados: " + ", ".
                  join(incendio.recursos) + "\n")
        else:
            print(
                "Usted no esta asociado a este incendio," +
                " no puede acceder a su informacion")

    def barra_estado(self):
        print(
            "\n+-----------------------------------------------------------" +
            "---------------------------------------------------------+")
        print(
            "- LAT:" + self.recurso.lat + " - LON: " + self.recurso.lon +
            " - ESTADO: " + self.recurso.estado +
            " - TIEMPO TRABAJADO: " + str(
                self.recurso.tiempo_trabajado) + " - TIEMPO RESTANTE: " + str(
                int(self.recurso.autonomia) - self.recurso.tiempo_trabajado))
        print(
            "+---------------------------------------------------------------" +
            "-----------------------------------------------------+\n")


class Jefe(Usuario):
    def __init__(self, ids, nombre, clave, recurso_id, tipo, fecha, lista):
        super().__init__(ids, nombre, clave, recurso_id, tipo, fecha)
        ind_id = lista[0].index("id:string")
        ind_tipo = lista[0].index("tipo:string")
        ind_velocidad = lista[0].index("velocidad:int")
        ind_lat = lista[0].index("lat:float")
        ind_lon = lista[0].index("lon:float")
        ind_autonomia = lista[0].index("autonomia:int")
        ind_delay = lista[0].index("delay:int")
        ind_extincion = lista[0].index("tasa_extincion:int")
        ind_costo = lista[0].index("costo:int")
        for i in lista:
            if i[ind_id] == self.recurso_id:
                index = lista.index(i)
        recurso = simulacion.Recurso(lista[index][ind_id],
                                     lista[index][ind_tipo],
                                     lista[index][ind_velocidad],
                                     lista[index][ind_lat],
                                     lista[index][ind_lon],
                                     lista[index][ind_autonomia],
                                     lista[index][ind_delay],
                                     lista[index][ind_extincion],
                                     lista[index][ind_costo])
        self.recurso = recurso
        self.inc_id = -1

    def leer_recurso(self, nada):
        intento = True
        while intento:
            try:
                index = input("Indique el id del Recurso que busca: ")
                intento = False
            except:
                print("Elija un id valido")
        if index == self.recurso_id:
            print("\n--ID: " + self.recurso.ids +
                  "\n--Tipo: " + self.recurso.tipo +
                  "\n--Velocidad: " + self.recurso.velocidad +
                  "\n--Latitud:" + self.recurso.lat +
                  "\n--Longitud: " + self.recurso.lon +
                  "\n--Autonomia: " + self.recurso.autonomia +
                  "\n--Delay: " + self.recurso.delay +
                  "\n--Tasa de Extincion: " + self.recurso.tasa_extincion +
                  "\n--Costo: " + self.recurso.costo +
                  "\n--Estado actual: " + self.recurso.estado + "\n")
            if self.recurso.estado != "Standby":
                print("--Tiempo trabajado: " +
                      str(self.recurso.tiempo_trabajado) +
                      "\n--Tiempo de trabajo restante: " +
                      str(int(self.recurso.autonomia) -
                          self.recurso.tiempo_trabajado))
        else:
            print(
                "Usted no esta asociado con este recurso, no puede ver " +
                "la informacion")

    def leer_incendio(self, lista):
        intento = True
        while intento:
            try:
                index = int(input("Escriba el id del incendio a investigar: "))\
                        + 1
                intento = False
            except:
                print("Elija un id valido")
        if index == (self.inc_id + 1):
            ind_id = lista[0].index("id:string")
            ind_lat = lista[0].index("lat:float")
            ind_lon = lista[0].index("lon:float")
            ind_potencia = lista[0].index("potencia:int")
            ind_fecha = lista[0].index("fecha_inicio:string")
            incendio = simulacion.Incendio(lista[index][ind_id],
                                           str(lista[index][ind_lat]),
                                           str(lista[index][ind_lon]),
                                           str(lista[index][ind_potencia]),
                                           lista[index][ind_fecha], self.fecha)
            print("\n--ID: " + incendio.ids +
                  "\n--Latitud:" + str(incendio.lat) +
                  "\n--Longitud: " + str(incendio.lon) +
                  "\n--Potencia: " + str(incendio.potencia) +
                  "\n--Fecha inicio: " + str(incendio.fecha_inicio) +
                  "\n--Porcentaje de extincion: " + str(
                incendio.porcentaje) + "%" +
                  "\n--Recursos utilizados: " + (", ").join(
                incendio.recursos) + "\n")
        else:
            print("Usted no esta asociado a este incendio, " +
                  "no puede acceder a su informacion")

    def barra_estado(self):
        print("\n+-------------------------------------------------------" +
              "-------------------------------------------------------------+")
        print(
            "- LAT:" + self.recurso.lat + " - LON: " + self.recurso.lon +
            " - ESTADO: " + self.recurso.estado +
            " - TIEMPO TRABAJADO: " + str(self.recurso.tiempo_trabajado) +
            " - TIEMPO RESTANTE: " +
            str(int(self.recurso.autonomia) - self.recurso.tiempo_trabajado))
        print("\n+-------------------------------------------------------" +
              "-------------------------------------------------------------+")
