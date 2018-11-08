from PyQt5.QtCore import pyqtSignal, QThread, QSize, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QProgressBar
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.uic import loadUiType
import sys
from back import Character
import time

class Nexo_grafico(QObject):
    dano = pyqtSignal(int)
    def __init__(self, pos, child, parent, thr):
        super().__init__()
        self.nexo = child
        self.nexo.comunicador = self.comunicador
        self.nexo.elcomunicador()
        self.dano.connect(thr.recibir_dano)
        self.nexo.setPixmap(QPixmap("tower"))
        self.nexo.move(pos[0], pos[1])
        self.nexo.setScaledContents(True)
        self.nexo.resize(80, 80)
        self.life = QProgressBar(parent)
        self.life.resize(self.nexo.geometry().width(), 5)
        self.life.setMinimum(0)
        self.life.setMaximum(thr.vida)
        self.life.setValue(thr.vida)
        self.life.move(self.nexo.x(), self.nexo.y() - 7)
        self.nexo.show()

    def comunicador(self, hit):
        self.dano.emit(hit)


class Nexo(QThread):
    def __init__(self, pos, child, parent):
        super().__init__()
        self.vida = 1200
        self.inhibidor = True
        self.grafico = Nexo_grafico(pos, child, parent, self)
        self.x_fill = (
            self.grafico.nexo.x(),
            self.grafico.nexo.x() + self.grafico.nexo.geometry().width())
        self.y_fill = (
            self.grafico.nexo.y(),
            self.grafico.nexo.y() + self.grafico.nexo.geometry().height())

    def recibir_dano(self, hit):
        if not self.inhibidor:
            print("recibien2")
            self.vida -= hit
            self.grafico.life.setValue(self.vida)
            if self.vida <= 0:
                self.grafico.nexo.hide()

    def run(self):
        self.sleep(0.1)
            #recibir muerte

class Torre_grafico(QObject):
    dano = pyqtSignal(int)
    def __init__(self, pos, child, parent, thr):
        super().__init__()
        self.torre = child
        self.torre.comunicador = self.comunicador
        self.torre.elcomunicador()
        self.dano.connect(thr.recibir_dano)
        self.torre.setPixmap(QPixmap("cannon_tower"))
        self.torre.move(pos[0], pos[1])
        self.torre.setScaledContents(True)
        self.torre.resize(80, 80)
        self.life = QProgressBar(parent)
        self.life.resize(self.torre.geometry().width(), 5)
        self.life.setMinimum(0)
        self.life.setMaximum(thr.vida)
        self.life.setValue(thr.vida)
        self.life.move(self.torre.x(), self.torre.y() - 7)
        self.torre.show()

    def comunicador(self, hit):
        self.dano.emit(hit)

class Torre(QThread):
    def __init__(self, pos, child, parent):
        super().__init__()
        self.vida = 250
        self.inhibidor = True
        self.grafico = Torre_grafico(pos, child, parent, self)
        self.x_fill = (
            self.grafico.torre.x(),
            self.grafico.torre.x() + self.grafico.torre.geometry().width())
        self.y_fill = (
            self.grafico.torre.y(),
            self.grafico.torre.y() + self.grafico.torre.geometry().height())

    def run(self):
        self.sleep(0.1)
        if not self.inhibidor:
            pass
            #recibir muerte

    def recibir_dano(self, hit):
        print("recibien2")
        self.vida -= hit
        self.grafico.life.setValue(self.vida)
        if self.vida <= 0:
            self.grafico.torre.hide()


class Inhibidor_grafico(QObject):
    dano = pyqtSignal(int)
    def __init__(self, pos, child, parent, thr):
        super().__init__()
        self.inhibidor = child
        self.inhibidor.comunicador = self.comunicador
        self.inhibidor.elcomunicador()
        self.dano.connect(thr.recibir_dano)
        self.inhibidor.setPixmap(QPixmap("inhibidor"))
        self.inhibidor.move(pos[0], pos[1])
        self.inhibidor.setScaledContents(True)
        self.inhibidor.resize(80, 80)
        self.inhibidor.Shape(1)
        self.inhibidor.setFrameShadow(32)
        self.life = QProgressBar(parent)
        self.life.resize(self.inhibidor.geometry().width(), 5)
        self.life.setMinimum(0)
        self.life.setMaximum(thr.vida)
        self.life.setValue(thr.vida)
        self.life.move(self.inhibidor.x(), self.inhibidor.y() - 7)
        self.inhibidor.show()

    def comunicador(self, hit):
        self.dano.emit(hit)


class Inhibidor(QThread):
    def __init__(self, pos, child, parent):
        super().__init__()
        self.vida = 250
        self.grafico = Inhibidor_grafico(pos, child, parent, self)
        self.x_fill = (
            self.grafico.inhibidor.x(),
            self.grafico.inhibidor.x() + self.grafico.inhibidor.geometry().width())
        self.y_fill = (
            self.grafico.inhibidor.y(),
            self.grafico.inhibidor.y() + self.grafico.inhibidor.geometry().height())

    def run(self):
        time.sleep(0.1)
        print("hola")
        if not self.inhibidor:
            pass
            #recibir muerte

    def recibir_dano(self, hit):
        print("recibien2")
        self.vida -= hit
        self.grafico.life.setValue(self.vida)
        if self.vida <= 0:
            self.grafico.inhibidor.hide()

class myFill:
    def __init__(self, x_fill, y_fill):
        self.x_fill = x_fill
        self.y_fill = y_fill

class label(QLabel):
    msj = pyqtSignal(myFill)
    msj2 = pyqtSignal()
    ataque = pyqtSignal(int)
    miobject = pyqtSignal(int)
    def __init__(self, parent):
        super().__init__(parent)
        self.x_fill = (self.x(),self.x() + self.geometry().width())
        self.y_fill = (self.y(),self.y() + self.geometry().height())
        print(self.x_fill, self.y_fill)

    def elcomunicador(self):
        print("elcom")
        self.miobject.connect(self.comunicador)

    def actualizar(self):
        self.x_fill = (self.x(),self.x() + self.geometry().width())
        self.y_fill = (self.y(),self.y() + self.geometry().height())

    def enterEvent(self, event):
        self.actualizar()
        print(self.x_fill)
        self.msj.emit(myFill(self.x_fill, self.y_fill))
        pass
        #self.papa.personaje.victima = False
    def leaveEvent(self, event):
        self.msj2.emit()
        pass
        #self.papa.personaje.victima = False

    def underAttack(self, int):
        print("underAT")
        print(int)
        self.miobject.emit(50)
