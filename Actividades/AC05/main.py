
class Descifrador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.suma=0
        with open(self.nombre, "r") as self.archivo:
            lineas = self.archivo.readlines()
            self.codigo = ''
            self.texto = "".join(lineas).replace('\n', '')
            i = 0

    def lectura_archivo(self):
        with open(self.nombre, "r") as archivo:
            lineas = archivo.readlines()
            self.codigo = ''
            texto = "".join(lineas).replace('\n', '')
            for caracter in texto:
                try:
                    if caracter[0] == "a":
                        ind = texto.find(caracter)
                        raise CustomException.CustomException(ind, texto, self)
                except CustomException.CustomException as err:
                    print("El codigo tuvo el error 'Contiene a', arreglelo")
                    break
                self.codigo += caracter
            return self.codigo

    def elimina_incorrectos(self):
        lista=self.codigo.split(" ")
        self.codigo=''
        for i in lista:
            if len(i) < 6 or len(i) > 7:
                pass
            else:
                self.codigo+=' '+i
        return self.codigo

    def cambiar_binario(self, binario):
        lista = binario.split(' ')
        texto = []
        for x in lista[1:]:
            texto.append(chr(int(x, 2)))
        return texto

    def limpiador(self, lista):
        i = -1
        string = ''
        try:
            while i < len(lista):
                i += 1
                if '$' != lista[i]:
                    string += lista[i]
        except IndexError as err:
            print("El codigo tuvo el error {0}, arreglelo".format(err))
            while i < len(lista)-1:
                i += 1
                if '$' != lista[i]:
                    string += lista[i]
        return string

if __name__ == "__main__":
    try:
        des = Descifrador('mensaje_marciano.txt')
        codigo= des.lectura_archivo()
        codigo=des.elimina_incorrectos()
        try:
            lista = des.cambiar_binarios(des.codigo)
        except AttributeError as err:
            print("El codigo tuvo el error {0}, arreglelo".format(err))
            lista = des.cambiar_binario(des.codigo)
        texto = des.limpiador(lista)
        print(texto)
    except Exception as err:
        print('Esto no debiese imprimirse')
        print(err)

