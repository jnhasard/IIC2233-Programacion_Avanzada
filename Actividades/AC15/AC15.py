import re
import requests

with open("AC15.txt") as file:
    a = file.readlines()
uno = True
dos = False
tres = False
parrafo1 = ""
parrafo2 = ""
parrafo3 = ""
for i in a:
    if uno:
        if i == "\n":
            uno = False
            dos = True
            continue
        parrafo1 += i.strip()
    if dos:
        if i == "\n":
            dos = False
            tres = True
            continue
        parrafo2 += i.strip()
    if tres:
        parrafo3 += i.strip()
p1 = re.split("@", parrafo1)
p2 = re.split("@", parrafo2)
p3 = re.split("@", parrafo3)
print("Parrafo 1:")
for i in p1[1:]:
    if not re.match("[A-z]*[0-9][A-z]*", i):
        print(i, end=" ")
print("\n\nParrafo 2:")
for i in p2:
    if re.match("[A-z]*\.correcta[A-z]*", i):
        num = i.index(".correcta")
        print(i[0:num] + i[num+9:], end=" ")
print("\n\nParrafo 3:")
print("Debe", end=" ") #tiene mayuscula en el texto, lo puse manual para que se vea bonito :)
for i in p3:
    if re.match("[a-z]*\.[a-z]*", i):
        num = i.index(".")
        print(i[0:num] + i[num + 1:], end=" ")
print()
diccionario = {}
print("\nBienvenido a PrograPedia\nIngresar exit para salir")
ingrese = ""
while ingrese != "exit":
    ingrese = input("Ingrese su consulta: ")
    if ingrese != "exit":
        if ingrese in diccionario:
            r = diccionario[ingrese]

        else:
            r = requests.get("https://es.wikipedia.org/w/api.php?",
                             params={"action": "query", "explaintext":"","titles": ingrese, "prop": "extracts", "format": "json"})
            diccionario[ingrese] = r

        pagina = r.json()
        if list(pagina["query"]["pages"].keys())[0] != "-1":
            print("Titulo:", pagina["query"]["pages"][list(pagina["query"]["pages"].keys())[0]]["title"])
            print("ID:",list(pagina["query"]["pages"].keys())[0])
            print("url: https://es.wikipedia.org/wiki/" + ingrese)
            print("Contenido:\n", pagina["query"]["pages"][list(pagina["query"]["pages"].keys())[0]]["extract"])
        else:
            print("Ingrese una consulta valida")
        print()


