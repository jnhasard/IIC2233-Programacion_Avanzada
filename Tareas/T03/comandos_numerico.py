from math import sqrt


def LEN(x):
    return len(x)


def PROM(x):
    y = (i for i in x)
    return sum(y)/LEN(x)


def DESV(x):
    nuevo_x = (i for i in x)
    promedio = PROM(x)
    return ((sum(list(map(lambda y: (y - promedio)**2, nuevo_x))))/(LEN(x)-1))**(1/2)


def MEDIAN(x):
    if LEN(x)%2 == 0:
        return PROM([x[int(LEN(x)/2)-1],x[int(LEN(x)/2)]])
    else:
        return x[int(LEN(x)/2)]


def VAR(x):
    return DESV(x)**2