import os
import socket
import threading
import pickle

class Servidor:
    def __init__(self):
        self.HOST = "192.168.0.21"
        self.PORT = 8080
        self.C_DIR = os.getcwd()
        self.s_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_servidor.bind((self.HOST, self.PORT))
        self.s_servidor.listen(1)
        self.cliente = None
        self.thread = threading.Thread(target=self.aceptar, daemon=True)
        self.thread.start()


    def aceptar(self):
        cliente_nuevo, address = self.s_servidor.accept()
        print('Cliente conectado')
        self.cliente = cliente_nuevo
        thread_cliente = threading.Thread(target=self.receive, args=())
        thread_cliente.daemon = True
        thread_cliente.start()

    def send(self, img):
        # Funcion para mandar comandos y archivos
        if self.cliente:
            msj_final = img
            msj_final_pickle = pickle.dumps(msj_final)
            self.cliente.send(msj_final_pickle)
        else:
            print('No hay cliente conectado')
        pass


    def receive(self):
        # Funcion que recibe cualquier dato mandado por el servidor
        while True:
            try:
                data = self.cliente.recv(2048)
                mensaje = pickle.loads(data)
                print('Cliente: {}'.format(mensaje))
                if mensaje == 'logout':
                    self.desconectar_cliente()
                elif mensaje == "ls":
                    self.send(os.listdir(self.C_DIR))
                elif mensaje[0] == "get":
                    if os.path.isfile(mensaje[1]):
                        with open(mensaje[1], "rb") as file:
                            a= file.read()
                            tamaño = os.stat(mensaje[1])
                            self.send("img " + mensaje[2] + " " + str(tamaño.st_size))
                            #self.cliente.send(pickle.dumps("img " + mensaje[2] + " " + str(a) + "hola"))
            except AttributeError as err:
                print('Cliente desconectado')
                print(err)
                break
        return ""

    def desconectar_cliente(self):
        self.cliente = None
        thread = threading.Thread(target=self.aceptar, daemon=True)
        thread.start()


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

    server = Servidor()
    texto = input('>    ')
    server.send(texto)
    while True:
        texto = input("Tu: ")
        server.send(texto)



    # while True:
    #     # Conectarse al servidor
    #
    #     connected = True
    #     while connected:
    #         # Recibir comandos
    #         message = receive()
    #
    #         action = ""
    #         if action == "ls":
    #             pass
    #
    #         elif action == "logout":
    #             pass
    #
    #
    #         elif action == "get":
    #             pass
    #
    #         elif action == "send":
    #             pass
