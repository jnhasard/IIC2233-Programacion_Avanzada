from PyQt5.QtCore import pyqtSignal, QThread, QObject, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QShortcut, QProgressBar
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.uic import loadUiType
from itertools import cycle
import sys
import time
import math


class MoveMyImageEvent:

    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

class Graphic_Character(QObject):
    def __init__(self, parent, inicial_cords, max_health=100):

        super().__init__()
        self.campeon = parent.personaje_grafico
        # Paths para cada direccion
        self.fotos = cycle(["guerrero_0", "guerrero_3","guerrero_1", "guerrero_0", "guerrero_4","guerrero_2"])
        # self.left_campeon_paths = cycle(["Greencampeon", "Greencampeon2", "Greencampeon3"])
        # self.right_campeon_paths = cycle(["Greencampeon3", "Greencampeon2", "Greencampeon"])
        # self.down_campeon_paths = cycle(
        #     ["Greencampeon_vertical", "Greencampeon2_vertical", "Greencampeon3_vertical", "Greencampeon4_vertical"])
        # self.up_campeon_paths = cycle(
        #     ["Greencampeon3_vertical", "Greencampeon2_vertical", "Greencampeon_vertical", "Greencampeon4_vertical"])


        self.campeon.setScaledContents(True)
        self.campeon.resize(50, 50)
        self.campeon.actualizar()
        self.x_fill = self.campeon.x_fill
        self.y_fill = self.campeon.y_fill
        self.center = (300, 300)
        self.campeon.move(inicial_cords[0], inicial_cords[1])
        self.life = QProgressBar(parent)
        self.mousecords = (1,1)
        self.__pixmap = QPixmap(next(self.fotos))
        self.campeon.setVisible(True)
        self.campeon.setAlignment(Qt.AlignCenter)
        self.life.resize(self.campeon.geometry().width(), 5)
        self.life.setMinimum(0)
        self.life.setMaximum(max_health)
        self.life.setValue(100)
        self.life.move(self.campeon.x(), self.campeon.y() - 7)
        self.speed = 3.5
        self._size = (50, 50)
        self.angle = 0
        self.rotation = 0
        self.campeon.setVisible(True)
        self.vertical = False
        self.signal = None
        self.moving = "left"
        self.alive = True

    def move_image(self, myImageEvent):
        self.rotate(self.mousecords)
        self.campeon.move(myImageEvent.x, myImageEvent.y)
        self.life.move(myImageEvent.x, myImageEvent.y - 7)
        self.campeon.setPixmap(QPixmap(self.__pixmap))
        #self.__pixmap = QPixmap(next(self.fotos))

    def rotate(self, mouse_cords):

        self.mousecords = mouse_cords
        distance_x = self.mousecords[0] - self.center[0]
        distance_y = self.mousecords[1] - self.center[1]

        try:
            new_angle = math.degrees(math.atan(distance_y / distance_x))
        except:
            new_angle = self.angle
            return
        if distance_x < 0:
            new_angle = 180 + new_angle
        if distance_x > 0 and distance_y < 0:
            new_angle = 360 + new_angle
        self.angle = new_angle
        return

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle
        self.updatePixmap()

    def updatePixmap(self):
        self.__pixmap = QPixmap(next(self.fotos))
        self.__pixmap = self.__pixmap.transformed(QTransform().rotate(self.angle))
        self.__pixmap = self.__pixmap.scaled(self._size[0], self._size[1])
        self.campeon.setPixmap(self.__pixmap)
        self.campeon.show()
        #self.campeon.setPixmap(QPixmap(next(self.fotos)))
    #     if self.moving == "left":
    #         self.campeon.setPixmap(QtGui.QPixmap("campeon_Images/" + next(self.left_campeon_paths)))
    #     elif self.moving == "right":
    #         self.campeon.setPixmap(QtGui.QPixmap("campeon_Images/" + next(self.right_campeon_paths)))
    #         elif self.moving == "up":
    #     self.campeon.setPixmap(QtGui.QPixmap("campeon_Images/" + next(self.up_campeon_paths)))
    #     elif self.moving == "down":
    #
    # self.campeon.setPixmap(QtGui.QPixmap("campeon_Images/" + next(self.down_campeon_paths)))

class Character(QThread):
    trigger = pyqtSignal(MoveMyImageEvent)
    golpe = pyqtSignal(int)

    def __init__(self, parent, x, y, mono):
        super().__init__()
        self.mapa = []
        self.victima = False
        self.__position = (300, 300)
        self.center = (300, 300)
        self.alive = True
        self.speed = 3.5
        self.max_health = 100
        self.angle = 0
        self.mousecords = (1,1)
        self.mover = "arriba"
        self.health = self.max_health
        self.campeon_graphic = Graphic_Character(parent, (x, y), self.max_health)
        self.x_fill = self.campeon_graphic.x_fill
        self.y_fill = self.campeon_graphic.y_fill
        self.__position = (self.campeon_graphic.campeon.x(), self.campeon_graphic.campeon.y())
        self.position = self.__position
        self.campeon_graphic.position = self.position
        self.trigger.connect(self.campeon_graphic.move_image)
        self.victima = False



    def victim(self, myFill):
        self.victima = True
        self.golpe.connect(self.sender().underAttack)
        print("hola")
        self.victima_fill = (myFill.x_fill, myFill.y_fill)

    def no_victim(self):
        print("chao")
        self.victima = False

    def rotate(self, mouse_cords):

        self.mousecords = mouse_cords
        distance_x = self.mousecords[0] - self.center[0]
        distance_y = self.mousecords[1] - self.center[1]

        try:
            new_angle = math.degrees(math.atan(distance_y / distance_x))
        except:
            print("falle")
            new_angle = self.angle
            return
        if distance_x < 0:
            new_angle = 180 + new_angle
        if distance_x > 0 and distance_y < 0:
            new_angle = 360 + new_angle
        self.angle = new_angle
        return

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = angle

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.rotate(self.mousecords)
        self.__position = value
        self.center = (self.campeon_graphic.campeon.x() + (0.5 * self.campeon_graphic.campeon.geometry().width()),
                       self.campeon_graphic.campeon.y() + (0.5 * self.campeon_graphic.campeon.geometry().height()))
        self.trigger.emit(MoveMyImageEvent(self.campeon_graphic, self.position[0], self.position[1]))
        self.campeon_graphic.center = self.center
        self.campeon_graphic.campeon.actualizar()
        self.x_fill = self.campeon_graphic.campeon.x_fill
        self.y_fill = self.campeon_graphic.campeon.y_fill
        self.collision()

    def collision(self):
        for objeto in self.mapa:
            if (objeto.x_fill[0]<self.x_fill[0]<objeto.x_fill[1]) or (objeto.x_fill[0]<self.x_fill[1]<objeto.x_fill[1]):
                if (objeto.y_fill[0]<self.y_fill[0]<objeto.y_fill[1]) or (objeto.y_fill[0]<self.y_fill[1]<objeto.y_fill[1]):
                    if self.moviendo == "arriba":
                        for i in range(5):
                            self.move_down()
                    elif self.moviendo == "abajo":
                        for i in range(5):
                            self.move_up()
                    # elif self.moviendo == "izquierda":
                    #     for i in range(5):
                    #         self.move_right()
                    # elif self.moviendo == "derecha":
                    #     for i in range(5):
                    #         self.move_left()

    def run(self):
        while True:
            time.sleep(0.05)

    def recibir_mapa(self, map):
        self.mapa = map

    def move_left(self):
        self.moviendo = "izquierda"
        self.position = (self.position[0] - self.speed * (math.cos(math.radians(self.angle))),
                         self.position[1] + (math.sin(math.radians(self.angle))) * self.speed)

    def move_right(self):
        self.moviendo = "derecha"
        self.position = (self.position[0] + self.speed * (math.cos(math.radians(self.angle))),
                         self.position[1] - (math.sin(math.radians(self.angle))) * self.speed)

    def move_up(self):
        self.moviendo = "arriba"
        self.position= (self.position[0] + self.speed * (math.cos(math.radians(self.angle)) ),
                        self.position[1] + (math.sin(math.radians(self.angle)) ) * self.speed)

    def move_down(self):
        self.moviendo = "abajo"
        self.position = (self.position[0] - self.speed * (math.cos(math.radians(self.angle))),
                         self.position[1] - (math.sin(math.radians(self.angle))) * self.speed)

    def attack(self):
        if self.victima:
            if (self.victima_fill[0][0] - 40 < self.x_fill[0] < self.victima_fill[0][1]+40) or \
                    (self.victima_fill[0][0] - 40 < self.x_fill[1] < self.victima_fill[0][1]+40):
                if (self.victima_fill[1][0] - 40 < self.y_fill[0] < self.victima_fill[1][1] + 40) or \
                        (self.victima_fill[1][0] - 40 < self.y_fill[1] < self.victima_fill[1][1] + 40):
                    self.hit()

    def hit(self):
        self.golpe.emit(50)
        print("ataque")

