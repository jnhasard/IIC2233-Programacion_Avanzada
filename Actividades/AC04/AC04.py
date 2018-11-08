class Nodo:
    # Creamos la estructura del nodo

    def __init__(self, valor=None):
        self.siguiente = None
        self.valor = valor


class ListaLigada:
    def __init__(self):
        self.cola = None
        self.cabeza = None

    def agregar_nodo(self, valor):
        if not self.cabeza:
            # Revisamos si el nodo cabeza tiene un nodo asignado.
            # Si no tiene nodo, creamos un nodo
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            # Si ya tiene un nodo
            self.cola.siguiente = Nodo(valor)
            self.cola = self.cola.siguiente

    def existe(self, nombre):
        nodo = self.cabeza
        while nodo.siguiente != None:
            if str(nodo.valor) == nombre:
                return True
            nodo = nodo.siguiente
        if str(nodo.valor) == nombre:
            return True
        return False


    def encontrar(self, nombre):
        nodo = self.cabeza

        while nodo.siguiente != None:
            if str(nodo.valor) == nombre:
                return nodo
            nodo = nodo.siguiente
        if str(nodo.valor) == nombre:
            return nodo

    def __repr__(self):
        rep = ''
        nodo_actual = self.cabeza

        while nodo_actual:
            rep += '{0},'.format(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
        rep.strip(", ")
        return rep

class Isla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = ListaLigada()

    def __repr__(self):
        return str(self.nombre)


class Archipielago:
    def __init__(self, archivo):
        self.islas = ListaLigada()
        self.construir(archivo)

    def __repr__(self):
        string = ""
        nodo = self.islas.cabeza
        while nodo.siguiente != None:
            string += str(nodo.valor) + ":"+ str(nodo.valor.conexiones) + "\n"
            nodo = nodo.siguiente
        string += str(nodo.valor) + ":"+ str(nodo.valor.conexiones)
        return string

    def agregar_isla(self, nombre):
        self.islas.agregar_nodo(Isla(nombre))

    def conectadas(self, nombre_origen, nombre_destino):
        pass

    def agregar_conexion(self, nombre_origen, nombre_destino):
        if self.islas.existe(nombre_origen) and self.islas.existe(nombre_destino):
            self.islas.encontrar(nombre_origen).valor.conexiones.agregar_nodo(nombre_destino)
        elif self.islas.existe(nombre_origen) and not self.islas.existe(nombre_destino):
            self.agregar_isla(nombre_destino)
            self.islas.encontrar(nombre_origen).valor.conexiones.agregar_nodo(nombre_destino)
        elif not self.islas.existe(nombre_origen) and self.islas.existe(nombre_destino):
            self.agregar_isla(nombre_origen)
            self.islas.encontrar(nombre_origen).valor.conexiones.agregar_nodo(nombre_destino)
        else:
            self.agregar_isla(nombre_destino)
            self.agregar_isla(nombre_origen)
            self.islas.encontrar(nombre_origen).valor.conexiones.agregar_nodo(nombre_destino)

    def construir(self, archivo):
        entrada = open(archivo, "r")
        leer = entrada.readlines()
        for i in leer:
            self.agregar_isla(i.split(",")[0])
            self.agregar_isla(i.split(",")[1].strip())
            self.agregar_conexion(i.split(",")[0],i.split(",")[1].strip())
        entrada.close()

    def propagacion(self, nombre_origen, lista_Ant = None):
        puede_poblar = ListaLigada()
        isla_actual = self.islas.encontrar(nombre_origen).valor
        if isla_actual.conexiones.cabeza == None:
            print("No se puede propagar mas")
            return
        else:
            try:
                while isla_actual.conexiones.cabeza.siguiente != None:
                    if puede_poblar.existe(isla_actual.conexiones.cabeza.valor) == False:
                        puede_poblar.agregar_nodo(isla_actual.conexiones.cabeza)

                        return self.propagacion(isla_actual.conexiones.cabeza.valor, puede_poblar)
            except: print("falle")
if __name__ == '__main__':
    #No modificar desde esta linea
    #(puedes comentar lo que no este funcionando aun)
    arch = Archipielago("mapa.txt") # Instancia y construye
    print(arch)  #Imprime el Archipielago de una forma que se pueda entender
    print(arch.propagacion("Perresus"))
    print(arch.propagacion("Pasesterot"))
    print(arch.propagacion("Cartonat"))
    print(arch.propagacion("Womeston"))

# arch = Archipielago()
# arch.agregar_isla("hola")
# arch.agregar_isla("chao")
# arch.agregar_isla("py")
# arch.agregar_isla("isla")
# arch.agregar_isla("arch")
# arch.agregar_conexion("hola", "chao")
# print(arch)


