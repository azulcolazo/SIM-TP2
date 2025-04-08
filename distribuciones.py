import math
import random
import matplotlib.pyplot as plt


def normal(n, media, desviacion):
    puntos = []
    for i in range(n):
        r1 = random.random()
        r2 = random.random()

        z1 = math.sqrt(-2*math.log(1-r1)) * math.cos(2*math.pi*r2)
        z2 = math.sqrt(-2*math.log(1-r1)) * math.sin(2*math.pi*r2)

        x1 = media + desviacion * z1
        x2 = media + desviacion * z2

        puntos.append(x1)
        puntos.append(x2)

    return puntos

def uniforme(n, a, b):
    puntos = []
    if a < b:
        for i in range(n):
            r = random.random()
            x = a + r * (b-a)
            puntos.append(x)
        return puntos
    else:
        print("imprimir error")


def poisson(n, media):
    puntos = []
    for i in range(n):
        p = 1
        x = -1
        a = math.exp(-media)

        while True:
            u = random.random()
            p = p * u
            x = x + 1

            if p < a:
                break

        puntos.append(x)
    return puntos


def exponencial(n, l):
    puntos = []

    for i in range(n):
        r = random.random()
        x = -1/l * math.log(1-r)
        puntos.append(x)

    return puntos
