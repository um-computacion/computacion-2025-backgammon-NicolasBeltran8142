import random

class Dados:

    def __init__(self):
        self.__values__ = (0, 0)

    def tirar(self):
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        self.__values__ = (dado1, dado2)
        return self.__values__

    def obtener_valores(self):
        return self.__values__
