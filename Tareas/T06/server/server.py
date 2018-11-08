port = 8080
host = "127.0.0.1"
import socket
import threading
import pickle
import json
import os
from sala import Sala
import time

if "usuarios.json" not in os.listdir():
    with open("usuarios.json", "w") as file:
        file.write("{}")

class Server:
    def __init__(self, port, host):
        self.host = host
        self.port = port
        self.counter = 0
        self.mandando_cancion = False
        self.actualizar_db()
        self.clientes = {}
        self.salas = {}
        self.threads_salas = []
        self.crear_salas()
        self.s_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        self.accept_connections()

    def crear_salas(self):
        self.musica = {}
        for i in os.listdir("songs"):
            if not i.startswith("."):
                self.musica[i] = {"canciones": {}, "tiempo": 20, "cancion_actual": "-"}
                self.musica[i]["canciones"] = os.listdir("songs/" + i)
                if ".DS_Store" in self.musica[i]["canciones"]:
                    self.musica[i]["canciones"].remove(".DS_Store")
                self.salas[i] = Sala(i, os.listdir("songs/" + i))
                self.salas[i].start()
                self.threads_salas.append(threading.Thread(target=self.actualizar_salas, args=(i,)))
                self.threads_salas[-1].start()


    def bind_and_listen(self):
        self.s_servidor.bind((self.host, self.port))
        self.s_servidor.listen()
        print("Servidor escuchando en {} : {}...".format(self.host, self.port))

    def accept_connections(self):
        thread = threading.Thread(target=self.aceptar_conexiones)
        thread.start()

    def aceptar_conexiones(self):
        while True:
            client_socket, _ = self.s_servidor.accept()
            cliente = (threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            ))
            cliente.start()


    def listen_client_thread(self, client_socket):
        self.send(("musica", self.musica), client_socket)
        while True:
            try:
                response_bytes_length = client_socket.recv(4)
                response_length = int.from_bytes(response_bytes_length, byteorder="big")
                response = b""
                print("largo", response_length)
                while len(response) < response_length:
                    response += client_socket.recv(256)
                print(pickle.loads(response))
                recibido = pickle.loads(response)
                if recibido != "":
                    self.handle_command(recibido, client_socket)
            except:
                print("Cliente se salio", client_socket)
                for i in self.clientes:
                    if self.clientes[i] == client_socket:
                        self.clientes_puntos[i]["sala"] = "-"
                        eliminame = i
                with open("usuarios.json", "w") as file:
                    js = json.dumps(self.clientes_puntos)
                    file.write(js)
                self.actualizar_db()
                del self.clientes[eliminame]
                print(self.clientes)
                break

    def handle_command(self, recibido, client_socket):
        if recibido[0] == "username":
            if recibido[1] in self.clientes:
                print("desaprobado")
                self.send("username1", client_socket)
            else:
                print("aprobado")
                #self.actualizar_db()
                if recibido[1] in self.clientes_puntos:
                    print("puntos")
                    self.send(["puntos", self.clientes_puntos[recibido[1]]["puntos"],
                               self.clientes_puntos[recibido[1]]["record"]], client_socket)
                else:
                    self.send("username2", client_socket)
                    self.clientes_puntos[recibido[1]] = {"puntos": 0, "sala": "-", "tiempo": "-"}
                self.clientes[recibido[1]] = client_socket
            print("clientes",self.clientes.keys())
            print("puntos",self.clientes_puntos.keys())
        elif recibido[0] == "cancion":
            print("cancion")
            self.send(["cancion", recibido[2], self.salas[recibido[1]].canciones[recibido[2]], recibido[1]], client_socket)
        elif recibido == "recibida":
            print("ok")
            self.mandando_cancion = False
        elif recibido[0] == "caracteristicas":
            print(recibido)
            print(self.clientes_puntos[recibido[1]["nombre"]])
            print(self.clientes_puntos[recibido[1]["nombre"]]["puntos"])
            self.clientes_puntos[recibido[1]["nombre"]]["puntos"] = recibido[1]["puntos"]
            self.clientes_puntos[recibido[1]["nombre"]]["sala"] = recibido[1]["sala"]
            self.clientes_puntos[recibido[1]["nombre"]]["tiempo"] = recibido[1]["tiempo"]
            self.clientes_puntos[recibido[1]["nombre"]]["record"] = recibido[1]["record"]
            print(self.clientes_puntos)
        else: print(recibido)

    def actualizar_salas(self, nombre):
        while True:
            if not self.mandando_cancion:
                self.counter = 0
                for cliente in self.clientes:
                    self.send(("actualizacion", nombre, self.salas[nombre].tiempo,
                               self.salas[nombre].cancion_actual, self.clientes_puntos), self.clientes[cliente])
            else:
                self.counter += 1
                print("pausado")
                if self.counter > 30:
                    self.mandando_cancion = False
                    self.counter = 0
            time.sleep(1)

    def send(self, msg, socket):
        msg_bytes = pickle.dumps(msg)
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        if len(msg_bytes) > 10000:
            print("debe ser una cancion")
            self.mandando_cancion = True
        socket.sendall(msg_length + msg_bytes)

    def actualizar_db(self):
        with open("usuarios.json") as file:
            self.clientes_puntos = json.load(file)


if __name__ == "__main__":
    server = Server(port, host)