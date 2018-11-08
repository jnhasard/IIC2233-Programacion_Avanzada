import threading
import socket
import pickle
import time
import os
from PyQt5.QtCore import QObject, pyqtSignal
if "songs" not in os.listdir():
    os.mkdir("songs")

class Client(QObject):
    nombre_usuario = pyqtSignal()
    avanzar = pyqtSignal()
    cancion = pyqtSignal(tuple)
    salas = pyqtSignal(dict)
    actualizar_salas = pyqtSignal(tuple)
    post_cambio = pyqtSignal()
    def __init__(self, port, host, nombre, parent):
        super().__init__(parent)
        self.nombre_usuario.connect(parent.cambiar_nombre)
        self.avanzar.connect(parent.avanzar)
        self.cancion.connect(parent.reproducir)
        self.salas.connect(parent.recibir_salas)
        self.actualizar_salas.connect(parent.actualizar_salas)
        self.post_cambio.connect(parent.post_cambio)
        self.sala = "-"
        self.caracteristicas = {"nombre": "-", "puntos": 0, "sala": "-", "tiempo": "-", "record": {}}
        self.host = host
        self.port = port
        self.puntaje = 0
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket_cliente.connect((self.host, self.port))
            thread = threading.Thread(target=self.listen_thread, daemon=True)
            thread.start()
        except:
            self.socket_cliente.close()
            exit()
        self.nombre(nombre)

    def nombre(self, nombre):
        self.send(("username", nombre))
        self._nombre = nombre
        self.caracteristicas["nombre"] = self._nombre

    def send(self, msg):
        msg_bytes = pickle.dumps(msg)
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        self.socket_cliente.sendall(msg_length + msg_bytes)


    def listen_thread(self):
        while True:
            response_bytes_length = self.socket_cliente.recv(4)
            response_length = int.from_bytes(response_bytes_length, byteorder="big")
            response = b""
            while len(response) < response_length:
                response += self.socket_cliente.recv(838860800)
            response = pickle.loads(response)
            if response == "username1":
                self.nombre_usuario.emit()
                print("Cambiando nombre de usuario")
            elif response == "username2":
                print("ahorasi")
                self.post_cambio.emit()
                for i in self.musica:
                    self.caracteristicas["record"][i] = {"correctas": 0, "incorrectas": 0}
                self.avanzar.emit()
                thread2 = threading.Thread(target=self.enviar_caracteristicas, daemon=True)
                thread2.start()
            elif response[0] == "cancion":
                if response[1] not in os.listdir("songs"):
                    print(response[1], "no estaba")
                    with open("songs/" + response[1], "wb") as file:
                        file.write(response[2])
                else:
                    print("estaba")
                self.send("recibida")
                self.cancion.emit((response[1], self.musica[response[3]]["tiempo"]))
            elif response[0] == "musica":
                self.musica = response[1]
                print(self.caracteristicas["record"])
                self.salas.emit(self.musica)
            elif response[0] == "puntos":
                self.puntaje = response[1]
                self.caracteristicas["puntos"] = response[1]
                self.caracteristicas["record"] = response[2]
                print("aaaa", self.caracteristicas["record"])
                self.avanzar.emit()
                self.post_cambio.emit()
                thread2 = threading.Thread(target=self.enviar_caracteristicas, daemon=True)
                thread2.start()
            elif response[0] == "actualizacion":
                self.musica[response[1]]["tiempo"] = response[2]
                self.musica[response[1]]["cancion_actual"] = response[3]
                self.otros_clientes = response[4]
                self.actualizar_salas.emit((self.musica, self.otros_clientes))

    def reproducir(self, sala, nombre):
        if nombre in os.listdir("songs"):
            self.cancion.emit((nombre, self.musica[sala]["tiempo"]))
        else:
            self.send(("cancion", sala, nombre))

    def enviar_caracteristicas(self):
        while True:
            self.caracteristicas["puntos"] = self.puntaje
            self.caracteristicas["sala"] = self.sala
            self.caracteristicas["nombre"] = self._nombre
            msg_bytes = pickle.dumps(("caracteristicas", self.caracteristicas))
            msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
            self.socket_cliente.sendall(msg_length + msg_bytes)
            time.sleep(3)
