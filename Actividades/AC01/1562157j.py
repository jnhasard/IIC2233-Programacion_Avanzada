class Fundacion:
    def __init__(self, nombre, web, direccion):
        self.nombre = nombre
        self.web = web
        self.direccion = direccion
        self.cuadrillas = []
    def crear(self, fecha, lugar):
        cuadrilla = Cuadrilla(1,fecha,lugar, self.nombre)
        return cuadrilla
    def agregar(self, voluntario, cuadrilla):
        if cuadrilla.fund == self.nombre:
            if len(cuadrilla.voluntarios)<4:
                if voluntario.postular(cuadrilla):
                    cuadrilla.voluntarios.append(voluntario)
                    print("voluntario agregado")
            else: print("esta cuadrilla esta llena")
        else: print("esta cuadrilla no pertenece a esa fundacion")
class Cuadrilla:
    def __init__(self, nid, fecha, lugar, fundac):
        self.nid = nid
        self.inicio = fecha
        self.fin = fecha + 7
        self.lugar = lugar
        self.voluntarios = []
        self.fund = fundac
class Voluntario:
    def __init__(self, nombre, tel, mail):
        self.nombre = nombre
        self.tel = tel
        self.mail = mail
        self.fechas = []
    def postular(self, cuadrilla):
        fecha=cuadrilla.inicio
        a=0
        aux=[]
        aux+=self.fechas
        for i in range(7):
            if str(fecha+1) in aux:
                print("No puedes formar parte de esta cuadrilla porque vas a estar ocupado con otra")
                a=1
                return False
            else:
                aux.append(str(fecha))
            fecha += 1
        if a ==0:
            self.fechas+=aux
            self.fechas.sort
            return True

            print("estas inscrito, tienes ocupados los dias", self.fechas)
fund = Fundacion("manu maquina","www.hola.cl","oxford 515")
fund2 = Fundacion("manu seco", "www.chao.cl", "los dominicos")
c1 = fund.crear(6,"santiago")
c2 = fund.crear(8,"antofagasta")
c3 = fund2.crear(1, "arica")
c4 = fund2.crear(12, "tierra de fuego")
manu = Voluntario("manu",14542346,"manu@mino.cl")
jak = Voluntario("jak",1542456,"jak@mino.cl")
felipe = Voluntario("felipe",1143456,"felipe@mino.cl")
chuma = Voluntario("chuma",1443556,"chuma@mino.cl")

fund.agregar(manu,c1)
fund.agregar(jak,c2)
fund2.agregar(chuma,c3)
fund2.agregar(felipe,c4)


