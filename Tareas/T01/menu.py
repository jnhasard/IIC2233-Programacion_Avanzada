import usuarios, simulacion


def menu(lista_us, lista_rec, lista_inc, lista_met):
    print("\nBienvenido a SuperLuchín\n")
    ind_id = lista_us[0].index("id:string")
    ind_nombre = lista_us[0].index("nombre:string")
    ind_contraseña = lista_us[0].index("contraseña:string")
    ind_recurso = lista_us[0].index("recurso_id:string")
    programa = True
    iniciar = True
    while programa:
        while iniciar:
            nombre = input("Cual es su nombre: ")
            clave = input("Cual es su clave: ")
            for i in lista_us:
                if i[ind_nombre] == nombre:
                    if i[ind_contraseña] == clave:
                        print("Usuario y contraseña correctos")
                        fecha = True
                        while fecha:
                            fyh = input("Elija una fecha y hora: ")
                            try:
                                simulacion.Fecha(fyh)
                                fecha = False
                            except:
                                print("ERROR >> FECHA INVALIDA")
                        iniciar = False
                        if len(i[ind_recurso]) > 0:
                            for b in lista_rec:
                                if i[ind_recurso] == b[0]:
                                    if b[1] == "BOMBEROS" or b[1] == "BRIGADA":
                                        usuario = \
                                            usuarios.Jefe(i[ind_id],
                                                          i[ind_nombre],
                                                          i[ind_contraseña],
                                                          i[ind_recurso],
                                                          "JEFE", fyh,
                                                          lista_rec)
                                    else:
                                        usuario = \
                                            usuarios.Piloto(
                                                i[ind_id],
                                                i[ind_nombre],
                                                i[ind_contraseña],
                                                i[ind_recurso],
                                                "PILOTO", fyh, lista_rec)
                        else:
                            usuario = usuarios.Anaf(i[ind_id], i[ind_nombre],
                                                    i[ind_contraseña],
                                                    i[ind_recurso], "ANAF",
                                                    fyh)
                    else:
                        print("Usuario o contraseña incorrecto/a")
        intento = True
        if usuario.tipo == "PILOTO" or usuario.tipo == "JEFE":
            while intento:
                try:
                    usuario.barra_estado()

                    op = int(input("MENU: \n1-Cambiar fecha y hora" +
                                   "\n2-Cerrar cesión\n3-Informacion incendio" +
                                   "\n4-Informacion recurso\nOpcion: "))
                    intento = False
                except:
                    print("Elija un numero")
        else:
            while intento:
                try:
                    op = int(input("MENU ANAF: \n1-Cambiar fecha y hora" +
                                   "\n2-Cerrar cesión\n3-Informacion incendio" +
                                   "\n4-Informacion recurso\n5-Informacion usario" +
                                   "\n6-Crear Usuario\n7-Agregar pronostico\n" +
                                   "8-Agregar incendio\n9-Incendios activos" +
                                   "\n10-Planificar estrategia de extincion\nOpcion: "))
                    intento = False
                except:
                    print("Elija un numero")

        if op == 1:
            fecha = True
            while fecha:
                fyh = input("Elija una fecha y hora: ")
                try:
                    simulacion.Fecha(fyh)
                    fecha = False
                except:
                    print("ERROR >> FECHA INVALIDA")
        elif op == 2:
            print("Cerrando cesion...")
            iniciar = True
        elif op == 3:
            usuario.leer_incendio(lista_inc)
        elif op == 4:
            usuario.leer_recurso(lista_rec)
        elif op == 5 and usuario.tipo == "ANAF":
            usuario.leer_usuario(lista_us)
        elif op == 6 and usuario.tipo == "ANAF":
            usuario.agregar_usuario(lista_us)
        elif op == 7 and usuario.tipo == "ANAF":
            usuario.agregar_pronostico(lista_met)
        elif op == 8 and usuario.tipo == "ANAF":
            usuario.agregar_incendios(lista_inc)
        elif op == 9 and usuario.tipo == "ANAF":
            usuario.incendios_activos(lista_inc)
        elif op == 10 and usuario.tipo == "ANAF":
            usuario.estrategia(lista_inc, lista_rec, lista_met)
