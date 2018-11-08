import time

def is_prime(number):
    if number < 2:
        return False
    if number % 2 == 0:
        return False
    else:
        for i in range(3, number):
            if not number % i:
                return False
        return True

n = 1000
primes = [2]

for i in range(100000000000000000):
    if is_prime(i):
        primes.append(i)
    if len(primes) == int(n):
        break

def is_malvado(n):
    while True:
        numero = "{0:b}".format(n)
        unos = 0
        for i in numero:
            if i == "1":
                unos += 1
        if unos % 2 == 0:
            return n
        n += 1


with open("chatayudantes.iic2233","rb") as file:
    datos = file.read()

contador = 0
datos1 = []
aux = 0

for byte in datos:
    if contador != 3:
        aux += byte
        contador += 1
    else:
        aux += byte
        datos1.append(aux)
        aux = 0
        contador = 0

datos2 = bytearray()
for byte in datos1:
    byte = str(byte)
    byte = "0"*(3-len(byte))+byte
    elbyte = ""
    for numero in byte:
        if numero == "9":
            elbyte += "1"
        elif numero == "1":
            elbyte += "9"
        elif numero == "2":
            elbyte += "8"
        elif numero == "8":
            elbyte += "2"
        elif numero == "7":
            elbyte += "3"
        elif numero == "3":
            elbyte += "7"
        elif numero == "4":
            elbyte += "6"
        elif numero == "6":
            elbyte += "4"
        elif numero == "5":
            elbyte += "0"
        elif numero == "0":
            elbyte += "5"
    datos2 += bytes([int(elbyte[::-1])])

wav = bytearray()
gif = bytearray()



contador_primos = 0
contadorp = 0
primo = primes[0]
wav_bool = True

contadorm = 0
malvado = is_malvado(1)
for byte in datos2:
    if len(wav) != 9783:
        if wav_bool:
            wav += bytes([byte])
            contadorp += 1
            if contadorp == primo:
                contadorp = 0
                wav_bool = False
                contador_primos += 1
                primo = primes[contador_primos]
        else:
            gif += bytes([byte])
            contadorm += 1
            if contadorm == malvado:
                malvado = is_malvado(contadorm+1)
                contadorm = 0
                wav_bool = True
    else:
        gif += bytes([byte])

a=0
b=512
with open("sonido.wav", "wb") as salida_sonido:
    tiempo = time.time()
    print("Buffering sonido.....")
    while b< len(wav):
        salida_sonido.write(wav[a:b])
        a=b
        if b + 512 > 9783:
            b = 9783
        else:
            b+=512
        tiempo_aux = time.time() - tiempo
        print("|{0:^15s}|{1:^15s}|{2:^15s}|{3:^15s}|".format("Total", "Procesado", "Sin Procesar", "Deltatime"))
        print("|---------------+---------------+---------------+---------------|")
        print("|{0:^15d}|{1:^15d}|{2:^15d}|{3:^15f}|".format(len(wav), a, len(wav) - a, tiempo_aux))
        print("|---------------+---------------+---------------+---------------|")
    salida_sonido.write(wav[a:b])
    a = b
    print("|{0:^15s}|{1:^15s}|{2:^15s}|{3:^15s}|".format("Total", "Procesado", "Sin Procesar", "Deltatime"))
    print("|---------------+---------------+---------------+---------------|")
    print("|{0:^15d}|{1:^15d}|{2:^15d}|{3:^15f}|".format(len(wav), a, len(wav) - a, tiempo_aux))
    print("|---------------+---------------+---------------+---------------|")

with open("img.gif", "wb") as salida_gif:
    a = 0
    b = 1024
    print("\n\n\n\nBuffering image.....")
    tiempo = time.time()
    while b< len(gif):
        salida_gif.write(gif[a:b])
        a=b
        if b + 1024 > len(gif):
            b = len(gif)
        else:
            b+=1024
        tiempo_aux = time.time() - tiempo
        print("|{0:^15s}|{1:^15s}|{2:^15s}|{3:^15s}|".format("Total", "Procesado", "Sin Procesar", "Deltatime"))
        print("|---------------+---------------+---------------+---------------|")
        print("|{0:^15d}|{1:^15d}|{2:^15d}|{3:^15f}|".format(len(gif), a, len(gif) - a, tiempo_aux))
        print("|---------------+---------------+---------------+---------------|")
    salida_gif.write(gif[a:b])
    a = b
    print("|{0:^15s}|{1:^15s}|{2:^15s}|{3:^15s}|".format("Total","Procesado","Sin Procesar","Deltatime"))
    print("|---------------+---------------+---------------+---------------|")
    print("|{0:^15d}|{1:^15d}|{2:^15d}|{3:^15f}|".format(len(gif), a, len(gif) - a, tiempo_aux))
    print("|---------------+---------------+---------------+---------------|")




