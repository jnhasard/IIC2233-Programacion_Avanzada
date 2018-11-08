port = 8080
host = "127.0.0.1"
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtMultimedia import QSound
from functools import partial
import sys
import random
from random import randint
from client import Client
from numpy.random import choice

widget = loadUiType('interfaz.ui')

class MainWindow(widget[0], widget[1]):
    nombre = pyqtSignal()
    pedir = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.labels = {}
        self.botones = {}
        self.labels_puntajes = []
        self.opciones = []
        self.labels_otros = {}
        self.otros = {}
        self.mitimer = None
        self.cancion = None
        self.la_proxima1 = False
        self.setupUi(self)
        self.initGui()
        self.fondo = QImage("fondo.png").scaled(QSize(self.frameGeometry().width(), self.frameGeometry().height()))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(self.fondo))
        self.setPalette(palette)
        self.primera_cancion = True
        self.la_proxima = False
        self.boton_ingreso.clicked.connect(self.crear_cliente)
        self.boton_puntajes.clicked.connect(self.abrir_puntajes)

    def initGui(self):
        self.show()

    def keyPressEvent(self, key):
        if key.key() == 16777220:
            self.crear_cliente()

    def avanzar(self):
        self.label_usuario.setText("Usuario: " + self.nombre_usuario.text())
        self.label_puntaje.setText("Puntaje: " + str(self.cliente.puntaje))
        self.label_puntaje_2.setText("Puntaje: " + str(self.cliente.puntaje))
        self.stackedWidget.setCurrentIndex(1)

    def crear_cliente(self):
        self.boton_ingreso.clicked.disconnect()
        nombre = self.nombre_usuario.text()
        self.cliente = Client(port, host, nombre, self)
        self.boton_ingreso.clicked.connect(self.cambiar_nombre)
        self.volver_puntajes.clicked.connect(self.volver_sala)

    def cambiar_nombre(self):
        self.ingrese_nombre.setText("Nombre ya usado, intente nuevamente:")
        for i in self.salas:
            self.labels[i].hide()
            self.labels[i + "tiempo"].hide()
            self.labels[i + "cancion"].hide()
            self.botones[i].hide()
            self.labels[i + "contador"].hide()
        self.stackedWidget.setCurrentIndex(0)
        self.boton_ingreso.clicked.connect(self.enviar_nombre)

    def enviar_nombre(self):
        nombre = self.nombre_usuario.text()
        self.cliente.nombre(nombre)

    def post_cambio(self):
        for i in self.salas:
            self.labels[i].show()
            self.labels[i + "tiempo"].show()
            self.labels[i + "cancion"].show()
            self.botones[i].show()
            self.labels[i + "contador"].show()

    def reproducir(self, tupla):
        if self.primera_cancion:
            self.primera_cancion = False
        else:
            self.cancion.stop()
        self.cancion = QSound("songs/" + tupla[0], self)
        self.cancion.play()

    def recibir_salas(self, salas):
        self.salas = salas
        n = 100
        for i in self.salas:
            self.labels[i] = QLabel(self)
            self.labels[i].setText(i)
            self.labels[i].setGeometry(50,n,100,50)
            self.labels[i].show()
            self.labels[i + "tiempo"] = QLabel(self)
            self.labels[i + "tiempo"].setText("")
            self.labels[i + "tiempo"].setGeometry(150, n, 100, 50)
            self.labels[i + "tiempo"].show()
            self.labels[i + "cancion"] = QLabel(self)
            art = choice(self.salas[i]["canciones"], 2, False)
            self.labels[i + "cancion"].setText(art[0].split("-")[0] + ", " + art[1].split("-")[0])
            self.labels[i + "cancion"].setGeometry(200, n, 250, 100)
            self.labels[i + "cancion"].show()
            self.botones[i] = QPushButton(self)
            self.botones[i].setText(i)
            self.botones[i].setGeometry(500, n, 100, 50)
            self.botones[i].show()
            self.labels[i + "contador"] = QLabel(self)
            self.labels[i + "contador"].setText("")
            self.labels[i + "contador"].setGeometry(600, n, 100, 50)
            self.labels[i + "contador"].show()
            n += 100
        for i in self.botones:
            self.botones[i].clicked.connect(partial(self.abrir_sala, i))

    def actualizar_salas(self, tupla):
        self.salas = tupla[0]
        self.otros = tupla[1]
        contador = 0
        for sala in self.salas:
            self.labels[sala + "tiempo"].setText(str(self.salas[sala]["tiempo"]) + " segundos")
            for otro in self.otros:
                if self.otros[otro]["sala"] == sala:
                    contador += 1
            self.labels[sala + "contador"].setText(str(contador) + " jugadores")
            contador = 0

    def abrir_sala(self, nombre):
        self.nombre_sala = nombre
        self.cliente.sala = nombre
        self.timer.setText(str(self.salas[nombre]["tiempo"]))
        self.nombre_sala_label.setText(nombre)
        for i in self.botones:
            self.botones[i].hide()
        for i in self.labels:
            self.labels[i].hide()
        self.n = 150
        for otros in self.otros:
            if self.otros[otros]["sala"] == self.nombre_sala:
                self.labels_otros[otros] = QLabel(self)
                self.labels_otros[otros].setText(otros + "\n--> " + str(self.otros[otros]["puntos"]) + " puntos\n--> " + str(self.otros[otros]["tiempo"]))
                self.labels_otros[otros].setGeometry(650, self.n, 140, 50)
                self.labels_otros[otros].show()
                self.n += 60
        self.stackedWidget.setCurrentIndex(2)
        self.opciones = [self.opcion1, self.opcion2, self.opcion3, self.opcion4]
        pregunta = random.randint(0, 1)
        if pregunta == 0:
            self.pregunta.setText("¿Qué canción está sonando?")
        else:
            self.pregunta.setText("¿Qué artista está tocando?")
        ops = choice(self.salas[nombre]["canciones"], 4, False)
        if self.salas[nombre]["cancion_actual"] not in ops:
            la_buena = randint(0,3)
            ops[la_buena] = self.salas[nombre]["cancion_actual"]
        print("correcta", self.salas[nombre]["cancion_actual"])
        for i in range(4):
            print(ops[i])
            if pregunta == 0:
                self.opciones[i].setText(ops[i].split("-")[1].strip(".wav"))
            else:
                self.opciones[i].setText(ops[i].split("-")[0].strip(".wav"))
            if ops[i] != self.salas[nombre]["cancion_actual"]:
                self.opciones[i].clicked.connect(partial(self.puntaje, 0))
            else:
                self.opciones[i].clicked.connect(partial(self.puntaje, 1))
            self.opciones[i].hide()
        self.cliente.reproducir(nombre, self.salas[nombre]["cancion_actual"])
        self.boton_volver.clicked.connect(self.volver_sala)
        self.mitimer = QTimer(self)
        self.mitimer.timeout.connect(self.en_sala)
        self.mitimer.start(1000)

    def en_sala(self):
        if self.la_proxima and str(self.salas[self.nombre_sala]["tiempo"]) != "0":
            self.cliente.caracteristicas["tiempo"] = "-"
            self.la_proxima = False
            self.la_proxima1 = False
            self.correcto.hide()
            self.cliente.reproducir(self.nombre_sala, self.salas[self.nombre_sala]["cancion_actual"])
            pregunta = random.randint(0, 1)
            if pregunta == 0:
                self.pregunta.setText("¿Qué canción está sonando?")
            else:
                self.pregunta.setText("¿Qué artista está tocando?")
            ops = choice(self.salas[self.nombre_sala]["canciones"], 4, False)
            if self.salas[self.nombre_sala]["cancion_actual"] not in ops:
                la_buena = randint(0, 3)
                ops[la_buena] = self.salas[self.nombre_sala]["cancion_actual"]
            print("correcta", self.salas[self.nombre_sala]["cancion_actual"])
            for i in range(4):
                print(ops[i])
                if pregunta == 0:
                    self.opciones[i].setText(ops[i].split("-")[1].strip(".wav"))
                else:
                    self.opciones[i].setText(ops[i].split("-")[0].strip(".wav"))
                if ops[i] != self.salas[self.nombre_sala]["cancion_actual"]:
                    self.opciones[i].clicked.disconnect()
                    self.opciones[i].clicked.connect(partial(self.puntaje, 0))
                else:
                    self.opciones[i].clicked.disconnect()
                    self.opciones[i].clicked.connect(partial(self.puntaje, 1))
                self.opciones[i].show()
        if str(self.salas[self.nombre_sala]["tiempo"]) == "0" or self.la_proxima1:
            self.la_proxima = True
        if str(self.salas[self.nombre_sala]["tiempo"]) == "1":
            self.la_proxima1 = True
        for otros in self.otros:
            if self.otros[otros]["sala"] == self.nombre_sala and otros not in self.labels_otros:
                self.labels_otros[otros] = QLabel(self)
                self.labels_otros[otros].setGeometry(650, self.n, 140, 50)
                self.labels_otros[otros].show()
                self.n += 60
        for otros in self.labels_otros:
            if self.otros[otros]["sala"] != self.nombre_sala:
                self.labels_otros[otros].hide()
            self.labels_otros[otros].setText(
                otros + "\n--> " + str(self.otros[otros]["puntos"]) + " puntos\n--> " + str(self.otros[otros]["tiempo"]))
        self.timer.setText(str(self.salas[self.nombre_sala]["tiempo"]))

    def puntaje(self, a):
        if a == 1:
            self.correcto.setText("Respuesta correcta!\n" + str(int(self.salas[self.nombre_sala]["tiempo"]) * 100) + " puntos")
            self.cliente.caracteristicas["tiempo"] = self.salas[self.nombre_sala]["tiempo"]
            self.cliente.caracteristicas["record"][self.nombre_sala]["correctas"] += 1
        else:
            self.cliente.caracteristicas["record"][self.nombre_sala]["incorrectas"] += 1
            self.correcto.setText("Respuesta incorrecta..")
        print(self.cliente.caracteristicas["record"][self.nombre_sala])
        self.cliente.puntaje += a * int(self.salas[self.nombre_sala]["tiempo"]) * 100
        self.label_puntaje_2.setText("Puntaje: " + str(self.cliente.puntaje))
        self.label_puntaje.setText("Puntaje: " + str(self.cliente.puntaje))
        for i in self.opciones:
            i.hide()
        self.correcto.show()

    def volver_sala(self):
        if self.mitimer:
            self.mitimer.stop()
        self.cliente.sala = "-"
        self.cliente.caracteristicas["tiempo"] = "-"
        self.la_proxima = False
        if self.cancion:
            self.cancion.stop()
        self.correcto.setText("Esperando canción\nsiguiente...")
        self.correcto.show()
        self.n = 150
        for i in self.labels_otros:
            self.labels_otros[i].hide()
        self.labels_otros = {}
        for i in self.botones:
            self.botones[i].show()
        for i in self.labels:
            self.labels[i].show()
        for i in self.opciones:
            i.show()
        for i in self.labels_puntajes:
            for label in self.labels_puntajes[i]:
                label.hide()
        self.stackedWidget.setCurrentIndex(1)

    def abrir_puntajes(self):
        for i in self.botones:
            self.botones[i].hide()
        for i in self.labels:
            self.labels[i].hide()
        self.y = 120
        self.stackedWidget.setCurrentIndex(3)
        self.labels_puntajes = {}
        self.lista = []
        puntajes = []
        for i in self.otros:
            puntajes.append(self.otros[i]["puntos"])
        puntajes.sort(reverse=True)
        print(self.otros)
        for puntaje in puntajes:
            print(puntaje)
            for cliente in self.otros:
                if puntaje == self.otros[cliente]["puntos"]:
                    if cliente not in self.lista:
                        self.lista.append(cliente)
                    if cliente not in self.labels_puntajes:
                        self.labels_puntajes[cliente] = [QLabel(self), QLabel(self), QLabel(self), QLabel(self)]
                    self.labels_puntajes[cliente][0].setText(cliente)
                    self.labels_puntajes[cliente][1].setText(str(self.otros[cliente]["puntos"]))
                    mejor = []
                    print(self.otros[cliente])
                    for sala in self.otros[cliente]["record"]:
                        mejor.append(self.otros[cliente]["record"][sala]["correctas"])
                    mejor.sort(reverse=True)
                    for lasala in self.otros[cliente]["record"]:
                        if mejor[0] == self.otros[cliente]["record"][lasala]["correctas"]:
                            mejorsala = lasala
                    self.labels_puntajes[cliente][2].setText(mejorsala)
                    peor = []
                    for sala in self.otros[cliente]["record"]:
                        peor.append(self.otros[cliente]["record"][sala]["incorrectas"])
                    peor.sort(reverse=True)
                    for lasala in self.otros[cliente]["record"]:
                        if peor[0] == self.otros[cliente]["record"][lasala]["incorrectas"]:
                            peorsala = lasala
                    self.labels_puntajes[cliente][3].setText(peorsala)
                    #self.lista.append(self.labels_puntajes[cliente])
        print(self.lista)
        for cliente in self.lista:
            self.labels_puntajes[cliente][0].setGeometry(10, self.y, 100, 100)
            self.labels_puntajes[cliente][1].setGeometry(300, self.y, 100, 100)
            self.labels_puntajes[cliente][2].setGeometry(500, self.y, 100, 100)
            self.labels_puntajes[cliente][3].setGeometry(700, self.y, 100, 100)
            self.labels_puntajes[cliente][0].show()
            self.labels_puntajes[cliente][1].show()
            self.labels_puntajes[cliente][2].show()
            self.labels_puntajes[cliente][3].show()
            self.y += 35






app = QApplication(sys.argv)
interfaz = MainWindow()
sys.exit(app.exec_())