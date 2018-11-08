class CustomException(Exception):
    def __init__(self, ind, texto, el):
        self.ind = ind
        self.texto = texto
        self.el = el
        self.Eliminar_A(self.ind, self.texto, self.el)

    def Eliminar_A(self, ind, texto, el):
        ind+=1
        texto2 = texto[ind:].split(" ")
        lista = []
        for i in texto2:
            lista.append(i[::-1])
        texto3 = " ".join(lista)
        el.codigo += texto3

