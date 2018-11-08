from PyQt5.QtCore import pyqtSignal, QThread, QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.uic import loadUiType
import sys
from Nexo import Nexo, Torre, Inhibidor, label
from back import Character
from contrincante import Malo
import time

class Mapa:
    def __init__(self, personaje, objetos):
        self.personaje = personaje
        self.personaje.mapa = objetos
        #self.objetos = objetos

widget = loadUiType('untitled.ui')


class MainWindow(widget[0], widget[1]):
    env_mapa = pyqtSignal(list)
    move_left = pyqtSignal()
    move_right = pyqtSignal()
    move_up = pyqtSignal()
    move_down = pyqtSignal()
    rotate = pyqtSignal(tuple)
    rotate2 = pyqtSignal(tuple)
    attack = pyqtSignal()
    pos = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initGui()
        self.playing = False
        self.fondo = QImage("space.png").scaled(QSize(self.frameGeometry().width(), self.frameGeometry().height()))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(self.fondo))  # 10 = Windowrole
        self.setPalette(palette)
        self.setMouseTracking(True)
        self.centralwidget.setMouseTracking(True)
        self.mapa = []

        #Edificios
        self.nexo_grafico = label(self)
        self.nexo_grafico2 = label(self)
        self.nexo = Nexo((50, 50), self.nexo_grafico, self)
        self.nexo2 = Nexo((self.frameGeometry().width() - 100, self.frameGeometry().height() - 150),
                          self.nexo_grafico2, self)
        self.nexo_grafico.hide()
        self.nexo_grafico2.hide()
        self.inhibidor_grafico = label(self)
        self.inhibidor_grafico2 = label(self)
        self.inhibidor = Inhibidor((120, 120), self.inhibidor_grafico, self)
        self.inhibidor2 = Inhibidor((self.frameGeometry().width() - 170, self.frameGeometry().height() - 220),
                                    self.inhibidor_grafico2, self)
        self.torre_grafico = label(self)
        self.torre_grafico2 = label(self)
        self.torre = Torre((190, 190), self.torre_grafico, self)
        self.torre2 = Torre((self.frameGeometry().width() - 240, self.frameGeometry().height() - 290),
                            self.torre_grafico2, self)

        self.nexo_grafico.hide()
        self.nexo_grafico2.hide()
        self.torre_grafico.hide()
        self.torre_grafico2.hide()
        self.inhibidor_grafico.hide()
        self.inhibidor_grafico2.hide()

        self.mapa.append(self.nexo)
        self.mapa.append(self.nexo2)
        self.mapa.append(self.inhibidor)
        self.mapa.append(self.inhibidor2)
        self.mapa.append(self.torre)
        self.mapa.append(self.torre2)



    def initGui(self):
        self.iniciar.clicked.connect(self.partida)
        self.show()

    def keyPressEvent(self, event):
        if self.playing:
            if event.key()==65:
                self.move_left.emit()
            if event.key()==68:
                self.move_right.emit()
            if event.key()==87:
                self.move_up.emit()
            if event.key()==83:
                self.move_down.emit()

    def partida(self):
        self.playing = True
        self.iniciar.hide()
        self.borrar.hide()
        self.label.hide()
        self.c1 = QLabel(self)
        self.c2 = QLabel(self)
        self.c3 = QLabel(self)
        lista = [self.c1, self.c2, self.c3]
        x = int(self.frameGeometry().width() * 1/4) - 50
        monos = ["hernan", "chau", "rick"]
        n = 0
        for i in lista:
            i.setGeometry(x, int(self.frameGeometry().height() * 0.5) - 200, 100, 100)
            x += int(self.frameGeometry().width() * 1/4) - 20
            i.setPixmap(QPixmap(monos[n]))
            i.setScaledContents(True)
            i.resize(200, 200)
            n += 1
            i.show()
        self.c1.resize(100,200)
        self.label1 = QPushButton(self)
        self.label2 = QPushButton(self)
        self.label3 = QPushButton(self)
        self.label1.setGeometry(0,0,200,50)
        self.label2.setGeometry(0, 0, 200, 50)
        self.label3.setGeometry(0, 0, 200, 50)
        self.label1.setText("Hernan el Destructor")
        self.label1.move(int(self.frameGeometry().width() * 1/4) - 100, int(self.frameGeometry().height() * 0.5))
        self.label2.setText("Chau la Hechicera")
        self.label2.move(int(self.frameGeometry().width() * 2/4) - 100, int(self.frameGeometry().height() * 0.5))
        self.label3.setText("JH el Cientifico")
        self.label3.move(int(self.frameGeometry().width() * 3/4) - 100, int(self.frameGeometry().height() * 0.5))
        self.label1.show()
        self.label2.show()
        self.label3.show()
        self.label1.clicked.connect(self.crear_campeon)

    def crear_campeon(self):
        self.fondo = QImage("dirt.png").scaled(QSize(self.frameGeometry().width(), self.frameGeometry().height()))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(self.fondo))
        self.setPalette(palette)
        self.personaje_grafico = label(self)
        self.personaje = Character(self, 270, 280, "")
        self.contrincante_grafico = label(self)
        self.contrincante = Malo(self, 500, 500, "")
        self.move_left.connect(self.personaje.move_left)
        self.move_right.connect(self.personaje.move_right)
        self.move_up.connect(self.personaje.move_up)
        self.move_down.connect(self.personaje.move_down)
        self.rotate.connect(self.personaje.campeon_graphic.rotate)
        self.rotate2.connect(self.personaje.rotate)
        self.attack.connect(self.personaje.attack)
        self.env_mapa.connect(self.personaje.recibir_mapa)
        #self.pos.connect(self.contrincante.move)
        self.nexo_grafico.msj.connect(self.personaje.victim)
        self.nexo_grafico.msj2.connect(self.personaje.no_victim)
        self.nexo_grafico2.msj.connect(self.personaje.victim)
        self.nexo_grafico2.msj2.connect(self.personaje.no_victim)
        self.torre_grafico.msj.connect(self.personaje.victim)
        self.torre_grafico.msj2.connect(self.personaje.no_victim)
        self.torre_grafico2.msj.connect(self.personaje.victim)
        self.torre_grafico2.msj2.connect(self.personaje.no_victim)
        self.inhibidor_grafico.msj.connect(self.personaje.victim)
        self.inhibidor_grafico.msj2.connect(self.personaje.no_victim)
        self.inhibidor_grafico2.msj.connect(self.personaje.victim)
        self.inhibidor_grafico2.msj2.connect(self.personaje.no_victim)
        self.env_mapa.emit(self.mapa)
        self.label1.hide()
        self.label2.hide()
        self.label3.hide()
        self.c1.hide()
        self.c2.hide()
        self.c3.hide()
        self.playing = True
        self.personaje.start()
        self.nexo.start()
        self.nexo2.start()
        self.nexo_grafico.show()
        self.nexo_grafico2.show()
        self.nexo.grafico.life.show()
        self.nexo2.grafico.life.show()
        self.torre.start()
        self.torre2.start()
        self.contrincante.start()
        self.torre_grafico.show()
        self.torre_grafico2.show()
        self.torre.grafico.life.show()
        self.torre2.grafico.life.show()
        self.inhibidor_grafico.show()
        self.inhibidor_grafico2.show()
        self.inhibidor.grafico.life.show()
        self.inhibidor2.grafico.life.show()
        self.personaje_grafico.show()
        self.personaje.campeon_graphic.life.show()
        self.contrincante_grafico.show()
        self.contrincante.campeon_graphic.life.show()
        #self.pos.emit((self.personaje_grafico.x(),self.personaje_grafico.y()))


    def mouseMoveEvent(self, event):
        if self.playing:
            self.rotate.emit((event.x(), event.y()))
            self.rotate2.emit((event.x(), event.y()))

    def mousePressEvent(self, event):
        if event.button() == 1:
            self.attack.emit()

app = QApplication(sys.argv)
hola = MainWindow()
sys.exit(app.exec_())