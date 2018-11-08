from os import listdir, mkdir, path
import pickle
import datetime
import json

def encriptar(msj, n):
    nuevo = ""
    for i in msj:
        nuevo += chr((ord(i) + int(n)) % 26 + 97)
    return nuevo

class Usuario:
    def __init__(self, nombre, contacts, phone_number):
        self.nombre = nombre
        self.contacts = contacts
        self.fono = phone_number

    def __str__(self):
        return self.nombre


class Mensaje:
    def __init__(self, send_to, content, send_by, last_view_date, date):
        self.send_to = send_to
        self.content = content
        self.send_by = send_by
        self.last_view_date = last_view_date
        self.date = date

    def __getstate__(self):
        nueva = self.__dict__.copy()
        nueva.update({"content": encriptar(self.content, self.send_by)})
        return nueva

    def __setstate__(self, state):
        state.update({"last_view_date": datetime.datetime.now()})
        self.__dict__ = state

    def __str__(self):
        return self.content


def crear_usuarios():
    usuarios = []
    for usuario in listdir("db/usr"):
        with open("db/usr/"+usuario, "r") as persona:
            persona = json.load(persona)
        usuarios.append(Usuario(persona["name"], persona["contacts"], persona["phone_number"]))
    return usuarios


def crear_msjes():
    msjes = []
    for msje in listdir("db/msg"):
        with open("db/msg/"+msje, "r") as msg:
            msg = json.load(msg)
        msjes.append(Mensaje(msg["send_to"], msg["content"], msg["send_by"], msg["last_view_date"], msg["date"]))
    return msjes

mensajes = crear_msjes()
usuarios = crear_usuarios()

for mensaje in mensajes:
    for usuario in usuarios:
        if usuario.fono == mensaje.send_by:
            usuario.contacts.append(mensaje.send_to)

if not path.exists("secure_db"):
    mkdir("secure_db")
if not path.exists("secure_db/msg"):
    mkdir("secure_db/msg")
if not path.exists("secure_db/usr"):
    mkdir("secure_db/usr")

print(mensajes[0].last_view_date)
serial = pickle.dumps(mensajes[0])
m2 = pickle.loads(serial)
print(m2.last_view_date)
print(mensajes[0].last_view_date)

for usuario in usuarios:
    with open("secure_db/usr/" + str(usuario.fono), "w") as usr:
        json_string = json.dumps(usuario.__dict__)
        usr.write(json_string)


for mensaje in mensajes:
    with open("secure_db/msg/" + str(mensaje.date), "wb") as msj:
        mensaje.content = encriptar(mensaje.content, mensaje.send_by)
        pickle_string = pickle.dumps(mensaje.__dict__)
        msj.write(pickle_string)


