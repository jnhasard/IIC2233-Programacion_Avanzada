from collections import defaultdict,deque

def funcion():
    return []

class Camion:
    def __init__(self, capacidad, urgencia):
        self.capacidad = capacidad
        self.urgencia = urgencia
        self.carga = defaultdict(funcion)
        self.peso_disp = capacidad
        self.carga_lista = []

    def __str__(self):
        return "camion con carga "+ str(self.carga_lista)

    def agregar_producto(self,producto):
        self.carga[producto.tipo].append(producto.nombre)
        self.peso_disp-=producto.peso
        self.carga_lista.append(producto)

class cdb:
    def __init__(self):
        self.fila = deque()
        self.bodega = []

    def recibir_camion(self,camion):
        ind=0
        if len(self.fila)!= 0:
            for i in self.fila:
                if camion.urgencia == i.urgencia:
                    ind = self.fila.index(i)
            self.fila.insert(ind,camion)
        else: self.fila.append(camion)
    #recibe y pone segun urgencia

    def enviar_camion(self):
        print(self.fila.pop(), "fue enviado")

    def rellenar_camion(self):
        # rellenar ultimo camion
        aux = int(self.fila[0].peso_disp)
        for i in self.bodega:
            if i.peso == aux:
                self.fila[0].agregar_producto(i)
                self.fila[0].peso_disp -= i.peso
                aux = self.fila[0].peso_disp
                self.bodega.remove(i)
            else:
                aux -= 1
        self.enviar_camion()

    def mostrar_productos_por(self,tipo):
        aux = []
        for i in self.bodega:
            if i.tipo == tipo and i.nombre not in aux:
                aux.append(i.nombre)
        aux2 = []
        for i in aux:
            count = 0
            for b in self.bodega:
                if i == b.nombre:
                    count+=1
            aux2.append(count)

        for i in range(len(aux)):
            print(aux[i],":",aux2[i])

        #revisa Q de elementos en stock del tipo que se recibio y los muestra

    def recibir_donacion(self,prod):
        self.bodega.append(prod)
    #agrega a bodega de manera ordenada

class Producto:
    def __init__(self, tipo, nombre, peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso


#poblar el programa
bodega = cdb()
data = open("productos.txt", "r")
for i in data:
    aux = i.split(",")
    nuevo_prod = Producto(aux[0],aux[1],int(aux[2]))
    bodega.recibir_donacion(nuevo_prod)

data2 = open("camiones.txt", "r")
for i in data2:
    aux1 = i.split(",")
    nuevo_camion = Camion(int(aux1[0]),int(aux1[1]))
    bodega.recibir_camion(nuevo_camion)

bodega.rellenar_camion()