import os
import socket
import pickle
import sys
import threading

class Cliente:

    def __init__(self):
        self.C_DIR = os.getcwd()
        self.host = '192.168.0.21'
        self.port = 8081
        self.s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s_cliente.connect((self.host, self.port))  # El cliente revisa que el servidor esté disponible
            # Una vez que se establece la conexión, se pueden recibir mensajes
            recibidor = threading.Thread(target=self.receive, args=())
            recibidor.daemon = True
            self._isalive = True
            recibidor.start()

        except socket.error:
            print("No fue posible realizar la conexión")
            sys.exit()

    def send(self, mensaje):
        # Funcion para mandar comandos y archivos
        command = mensaje.split(" ")

        if command[0] == "logout":
            msj_final = "logout"
            self._isalive = False

        elif command[0] == "ls":
            # Muetra carpetas y archivos en el directorio del servidor
            mensaje = "ls"
            pass


        elif command[0] == "get":
            mensaje = command
            pass

        elif command[0] == "send":
            # le mandas un archivo al servidor
            file_path = get_abs_path(command[1])
            if os.path.exists(file_path):
                pass

            else:
                print(command[1] + " doesn't exist.")


        msj_final = mensaje
        msj_final_pickle = pickle.dumps(msj_final)
        self.s_cliente.send(msj_final_pickle)
        pass


    def receive(self):
        # Funcion que recibe cualquier dato mandado por el servidor
        while self._isalive:
            data = self.s_cliente.recv(2048)
            #data_decoded = data.decode('utf-8')
            mensaje = pickle.loads(data)
            if mensaje[0] == "img":
                numero = mensaje[2]
                nombre = mensaje[1]
                print(numero, nombre)
                with open("hola.gif", "wb") as file:
                    file.write(mensaje[2])
            else:
                print("Server", mensaje)
        return ""

    def desconectar(self):
        self._isalive = False
        msj_final = {'status': 'disconnect'}
        msj_final_pickle = pickle.dumps(msj_final)
        self.s_cliente.send(msj_final_pickle)

def get_path(path):
    abs_path = get_abs_path(path)
    if not os.path.exists(abs_path):
        return -1
    elif not os.path.isdir(abs_path):
        return 0
    else:
        return abs_path


def get_abs_path(path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.abspath(os.sep.join(C_DIR.split(os.sep) +
                                           path.split(os.sep)))

if __name__ == '__main__':
    client = Cliente()
    while True:
        inputing = input("\nIngrese comando: \n")
        client.send(inputing)

    # C_DIR = os.getcwd()
    # HOST = "localhost"
    # PORT = 8080
    #
    # S_DIR = receive()
    # connected = True
    # while connected:
    #     command = input(S_DIR + " $ ")
    #     commands = command.split(" ")
    #
    #     if command[0] == "logout":
    #         # Aviso al servidor que me desconecto
    #         connected = False
    #
    #     elif commands[0] == "ls":
    #         # Muetra carpetas y archivos en el directorio del servidor
    #         pass
    #
    #
    #     elif commands[0] == "get":
    #         # Le pides un archivo al servidor
    #         pass
    #
    #     elif commands[0] == "send":
    #         # le mandas un archivo al servidor
    #         file_path = get_abs_path(commands[1])
    #         if os.path.exists(file_path):
    #             pass
    #
    #         else:
    #             print(commands[1] + " doesn't exist.")
