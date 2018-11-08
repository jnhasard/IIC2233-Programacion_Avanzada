from math import pi, e


def normal(u, o):
    def f(x):
        return ((1 / (2 * pi * (o ** 2))**(1/2)) * e**((-0.5) * ((x - u) / o) ** 2))
    return f


def exponencial(v):
    def f(x):
        return v * e**(-v * x)
    return f


def gamma(v, k):
    def f(x):
        return ((v ** k) / factorial(k - 1)) * x * (k - 1) * e**((-v * x))
    return f


def factorial(n):
    if n<=0:
        return 1
    return n*factorial(n-1)
