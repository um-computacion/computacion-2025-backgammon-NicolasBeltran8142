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
    def mostrar_tablero(self):
        print("\nEstado del tablero:")
        for i, punto in enumerate(self.puntos):
            contenido = "".join(["B" if f.color == "blanco" else "N" for f in punto])
            print(f"Punto {i:2}: {contenido if contenido else '.'}")

    def mover_ficha(self, origen, destino, color):
        if not (0 <= origen < 24 and 0 <= destino < 24):
            raise ValueError("Los puntos deben estar entre 0 y 23")

        punto_origen = self._puntos_[origen]
        punto_destino = self._puntos_[destino]

        if not punto_origen:
            raise ValueError(f"No hay fichas en el punto {origen}")

        ficha = punto_origen[-1]
        if ficha._color_ != color:
            raise ValueError(f"La ficha en el punto {origen} no es del color {color}")

        if punto_destino and punto_destino[-1]._color_ != color:
            raise ValueError(f"No se puede mover al punto {destino}, ocupado por el oponente")

        ficha._position_ = destino
        punto_origen.pop()
        punto_destino.append(ficha)