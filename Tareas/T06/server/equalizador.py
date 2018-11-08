import random
with open("songs/Reggaeton/Daddy_Yankee_Feat_Varios_-_Llegamos_A_La_Disco_Off.wav", "rb") as file:
    cancion = file.read()
header = []
print("Largo de la cancion", len(cancion))
f = random.uniform(0.5,3)
print("Cambiador de frecuencia:", f)
for i in cancion[:44]:
    header.append(i)
num = (int(int.from_bytes(cancion[24:28], byteorder="little") * f)).to_bytes(4, byteorder="little")
header[24] = num[0]
header[25] = num[1]
header[26] = num[2]
header[27] = num[3]

header_bytes = bytearray()
for i in header:
    header_bytes += bytes([i])
opcion = int(input("Desea agregar segundo efecto o no?\n1-Si\n2-No\n"))
if opcion == 1:
    bitspersample = int(int.from_bytes(header[34:36], byteorder="little") / 8)
    print("bitspersample", bitspersample)
    n = 0
    boolean = True
    byt = bytearray()

    for i in range(44, len(cancion), 2):
        if n%2 == 0:
            byt += int((int.from_bytes(cancion[i:i+2], byteorder="little") +
                           int.from_bytes(cancion[i-2:i], byteorder="little")) / 2).to_bytes(2, byteorder="little")
        else:
            byt += int((int.from_bytes(cancion[i:i+2], byteorder="little") +
                                int.from_bytes(cancion[i-2:i], byteorder="little")) / 2).to_bytes(2, byteorder="little")
        n += 1

    header_bytes += byt

else:
    for i in cancion[44:]:
        header_bytes += bytes([i])


with open("hola.wav", "wb") as file:
    file.write(header_bytes)


