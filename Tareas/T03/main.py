from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
from inter2 import interprete
import errores
import matplotlib.pyplot as plt


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()
        self.contador = 0
        self.respuestas = ""

    def process_consult(self, querry_array):
        # Agrega en pantalla la solución. Muestra los graficos!!
        print(querry_array)
        for i in querry_array[0]:
            self.contador += 1
            self.respuestas += "----- Consulta " + str(self.contador) + "-----\n"
            try:
                text = "Probando funcion\nConsulta " + str(self.contador) + "\n"
                self.add_answer(text)
                if str(i[0]) == "graficar":
                    self.add_answer("Graficando")
                    self.respuestas += "Grafico\n"
                    print(i)
                    interprete(i)
                else:
                    text = str(interprete(i))
                    self.respuestas += text + "\n"
                    self.add_answer(text + "\n")
            except (errores.ArgumentoInvalido, errores.ReferenciaInvalida, AssertionError) as err:
                self.add_answer(err)
                self.respuestas += str(err) + "\n"


    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        print(querry_array)
        self.add_answer("Guardando archivo...")
        salida = open("resultados.txt", "w")
        salida.writelines(self.respuestas)
        salida.close()
        self.add_answer("Archivo guardado!")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())

