class ArgumentoInvalido(Exception):
    def __init__(self, comando, *args):
        string = "Error de consulta: {}(".format(comando)
        for i in args[0]:
            if i is list:
                string += str(i[0]) + "*"
            else:
                string += str(i) + ", "
        string = string.strip(", ")
        string += ")"
        super().__init__("Causa: Argumento invalido\n" + string)


class ReferenciaInvalida(Exception):
    def __init__(self, comando, *args):
        string = "Error de consulta: {}(".format(comando)
        for i in args[0]:
            if i is list:
                string += str(i[0]) + "*"
            else:
                string += str(i) + ", "
        string = string.strip(", ")
        string += ")"
        super().__init__("Causa: Referencia invalida\n" + string)

class ErrordeTipo(Exception):
    def __init__(self, comando, *args):
        string = "Error de consulta: {}(".format(comando)
        for i in args[0]:
            if i is list:
                string += str(i[0]) + "*"
            else:
                string += str(i) + ", "
        string = string.strip(", ")
        string += ")"
        super().__init__("Causa: Error de tipo\n" + string)


class ErrorMatematico(Exception):
    def __init__(self, comando, *args):
        string = "Error de consulta: {}(".format(comando)
        for i in args[0]:
            if i is list:
                string += str(i[0]) + "*"
            else:
                string += str(i) + ", "
        string = string.strip(", ")
        string += ")"
        super().__init__("Causa: Error matematico\n" + string)


class ImposibleProcesar(Exception):
    def __init__(self, comando, *args):
        string = "Error de consulta: {}(".format(comando)
        for i in args[0]:
            if i is list:
                string += str(i[0]) + "*"
            else:
                string += str(i) + ", "
        string = string.strip(", ")
        string += ")"
        super().__init__("Causa: Imposible procesar\n" + string)


