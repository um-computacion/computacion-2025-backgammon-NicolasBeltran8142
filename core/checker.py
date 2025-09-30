class Checker:
    """
    Representa una ficha del juego. Tiene color y posición actual.
    La posición puede ser un número (0–23), 'bar' (capturada) o 'off' (borneada).
    """

    def __init__(self, color, position=None):
        self._color_ = color
        self._position_ = position

        if position not in range(24) and position not in [None, "bar", "off"]:
            raise ValueError("Posición inválida")

    @property
    def color(self):
        return self._color_

    @property
    def posicion(self):
        return self._position_

    def mover_a(self, nueva_posicion):
        if nueva_posicion not in range(24) and nueva_posicion not in ["bar", "off"]:
            raise ValueError("Nueva posición inválida")
        self._position_ = nueva_posicion

    def __repr__(self):
        return f"Checker({self._color_}, {self._position_})"

    def __eq__(self, other):
        return (
            isinstance(other, Checker) and
            self._color_ == other._color_ and
            self._position_ == other._position_
        )

    def __hash__(self):
        return hash((self._color_, self._position_))


class Punto:
    """
    Representa un punto del tablero. Puede tener fichas de un jugador.
    """

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
    """
    Valida si un movimiento es legal según las reglas básicas del juego.
    """
    if origen not in range(24) or destino not in range(24):
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
