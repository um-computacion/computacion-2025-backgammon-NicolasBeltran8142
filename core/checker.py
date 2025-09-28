class Checker:
    def __init__(self, color, position):
        if color not in ["blanco", "negro"]:
            raise ValueError("Color inválido")
        if not (0 <= position < 24):
            raise ValueError("Posición inválida")
        self._color_ = color
        self._position_ = position

    @property
    def color(self):
        return self._color_

    @property
    def posicion(self):
        return self._position_

    def mover_a(self, nueva_posicion):
        if not (0 <= nueva_posicion < 24):
            raise ValueError("Nueva posición inválida")
        self._position_ = nueva_posicion

    def __repr__(self):
        return f"Checker({self._color_}, {self._position_})"


class Punto:
    def __init__(self, jugador=None, cantidad=0):
        self._jugador_ = jugador
        self._cantidad_ = cantidad

    def esta_vacio(self):
        return self._cantidad_ == 0

    def es_del_jugador(self, jugador):
        return self._jugador_ == jugador

    def es_del_oponente(self, jugador):
        return self._jugador_ is not None and self._jugador_ != jugador

    def esta_bloqueado(self, jugador):
        return self.es_del_oponente(jugador) and self._cantidad_ > 1


def validar_movimiento(tablero, jugador, origen, destino, valor_dado):
    if not (0 <= origen < len(tablero)) or not (0 <= destino < len(tablero)):
        return False

    punto_origen = tablero[origen]
    punto_destino = tablero[destino]

    if punto_origen.esta_vacio() or not punto_origen.es_del_jugador(jugador):
        return False

    if abs(destino - origen) != valor_dado:
        return False

    if punto_destino.esta_bloqueado(jugador):
        return False

    if jugador == "Jugador1" and destino < origen:
        return False
    if jugador == "Jugador2" and destino > origen:
        return False

    return True
