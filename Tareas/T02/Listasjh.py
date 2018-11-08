class Nodo:
    def __init__(self, valor=None):
        self.siguiente = None
        self.valor = valor

    def __repr__(self):
        return str(self.valor)

class jhlist:
    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for arg in args:
            self.agregar(arg)

    def agregar(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = Nodo(valor)
            self.cola = self.cola.siguiente

    def existe(self, nombre):
        ind = 0
        nodo = self.cabeza
        if nodo:
            while nodo.siguiente:
                if str(nodo.valor) == nombre:
                    return True
                nodo = nodo.siguiente
                ind += 1
            if nodo.valor == nombre:
                return True
            return False
        return False

    def finder(self, nombre):
        ind = 0
        nodo = self.cabeza
        if nodo:
            while nodo.siguiente:
                if str(nodo.valor) == nombre:
                    return ind
                nodo = nodo.siguiente
                ind += 1
            if str(nodo.valor) == nombre:
                return ind
        return False

    def __getitem__(self, key):
        nodo = self.cabeza
        largo = 0
        while nodo.siguiente :
            if largo == key:
                return nodo
            nodo = nodo.siguiente
            largo += 1
        if largo == key:
            return nodo
        else:
            raise IndexError

    def __len__(self):
        largo = 0
        nodo = self.cabeza
        if nodo:
            while nodo.siguiente:
                largo += 1
                nodo = nodo.siguiente
            largo += 1
        return largo

    def __setitem__(self, key, valor):
        largo = 0
        nodo = self.cabeza
        se_agrego = False
        if nodo:
            if key == 0:
                aux = self.cabeza
                self.cabeza = Nodo(valor)
                self.cabeza.siguiente = aux
            else:
                while nodo.siguiente:
                    largo += 1
                    if key == largo:
                        aux = nodo.siguiente
                        nodo.siguiente = Nodo(valor)
                        nodo.siguiente.siguiente = aux
                        se_agrego = True
                    nodo = nodo.siguiente
                if not se_agrego:
                    nodo.siguiente = valor
        else:
            self.cabeza = valor
        del self[key+1]

    def __delitem__(self, key):
        largo = 0
        nodo = self.cabeza
        if nodo:
            if key == 0:
                self.cabeza = self.cabeza.siguiente
            else:
                while nodo.siguiente:
                    largo += 1
                    if key == largo:
                        nodo.siguiente = nodo.siguiente.siguiente
                        break
                    nodo = nodo.siguiente

    def suma(self, otra):
        for i in range(len(otra)):
            self.agregar(otra[i])
        return self

    def sort(self):
        lista = []
        for i in self:
            lista.append(i.valor)
        lista.sort(reverse = True)
        for x in range(len(self)):
            self[x] = lista[x]

    def __repr__(self):
        rep = ""
        nodo_actual = self.cabeza
        while nodo_actual:
            rep += '{0}, '.format(str(nodo_actual.valor))
            nodo_actual = nodo_actual.siguiente
        rep = rep.strip(", ")
        return rep
