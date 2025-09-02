from .checker import Checker
class Board:
    def __init__(self):
        self._puntos_ = [[] for _ in range(24)] 

    def inicializar_fichas(self):
        posiciones = {
            "blanco": {0: 2, 11: 5, 16: 3, 18: 5},
            "negro": {23: 2, 12: 5, 7: 3, 5: 5}
        }
        for color, puntos in posiciones.items():
            for punto, cantidad in puntos.items():
                for _ in range(cantidad):
                    ficha = Checker(color, punto)
                    self._puntos_[punto].append(ficha)