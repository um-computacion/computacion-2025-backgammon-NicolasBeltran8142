from core.checker import Checker

class Board:
    def __init__(self):
        self._puntos_ = [[] for _ in range(24)]

    def inicializar_fichas(self):
        # Blancas
        for _ in range(2):
            self._puntos_[0].append(Checker("blanco", 0))
        for _ in range(5):
            self._puntos_[11].append(Checker("blanco", 11))
        for _ in range(3):
            self._puntos_[16].append(Checker("blanco", 16))
        for _ in range(5):
            self._puntos_[18].append(Checker("blanco", 18))

        # Negras
        for _ in range(2):
            self._puntos_[23].append(Checker("negro", 23))
        for _ in range(5):
            self._puntos_[12].append(Checker("negro", 12))
        for _ in range(3):
            self._puntos_[7].append(Checker("negro", 7))
        for _ in range(5):
            self._puntos_[5].append(Checker("negro", 5))

