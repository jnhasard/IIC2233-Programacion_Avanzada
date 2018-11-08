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

    def obtener(self, posicion):
        nodo = self.cabeza

        for i in range(posicion):
            if nodo:
                nodo = nodo.siguiente
        if not nodo:
            raise Exception("Index fuera de range")
        else:
            return nodo.valor

    def __repr__(self):
        rep = '<<'
        nodo_actual = self.cabeza

        while nodo_actual:
            rep += '{0} - '.format(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
        rep = rep.strip(" - ")
        rep+= ">>"

        return rep

l = ListaLigada()
l.agregar_nodo(2)
l.agregar_nodo(4)
l.agregar_nodo(7)

print(l.obtener(2))
print(l.obtener(1))
print(l.obtener(0))
print(l.obtener(8))


print(l)