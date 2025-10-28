"""Módulo que contiene las clases Checker y Punto, y la función validar_movimiento."""


class Checker:
    """
    Represents a game piece (checker) with a color and current position.
    The position can be:
        - an integer from 0 to 23 (on the board),
        - "bar" (captured),
        - "off" (borne off),
        - or None (unplaced).
    """

    def __init__(self, color, position=None):
        self._color_ = color
        self._position_ = position

        if position not in range(24) and position not in [None, "bar", "off"]:
            raise ValueError("Invalid position")

    @property
    def color(self):
        """Returns the color of the checker."""
        return self._color_

    @property
    def posicion(self):
        """Returns the current position of the checker."""
        return self._position_

    def mover_a(self, nueva_posicion):
        """
        Moves the checker to a new position.

        Args:
            nueva_posicion (int or str): Target position (0–23, "bar", or "off").

        Raises:
            ValueError: If the position is invalid.
        """
        if nueva_posicion not in range(24) and nueva_posicion not in ["bar", "off"]:
            raise ValueError("Invalid new position")
        self._position_ = nueva_posicion

    def __repr__(self):
        return f"Checker({self._color_}, {self._position_})"

    def __eq__(self, other):
        return (
            isinstance(other, Checker)
            and self._color_ == other._color_
            and self._position_ == other._position_
        )

    def __hash__(self):
        return hash((self._color_, self._position_))


class Punto:
    """
    Represents a point on the board. It may contain checkers belonging to a player.

    Attributes:
        _jugador_ (str): The owner of the point.
        _cantidad_ (int): Number of checkers on the point.
    """

    def __init__(self, jugador=None, cantidad=0):
        self._jugador_ = jugador
        self._cantidad_ = cantidad

    def esta_vacio(self):
        """Returns True if the point has no checkers."""
        return self._cantidad_ == 0

    def es_del_jugador(self, jugador):
        """Returns True if the point belongs to the given player."""
        return self._jugador_ == jugador

    def es_del_oponente(self, jugador):
        """Returns True if the point belongs to the opponent."""
        return self._jugador_ is not None and self._jugador_ != jugador

    def esta_bloqueado(self, jugador):
        """
        Returns True if the point is blocked for the given player.
        A point is blocked if it belongs to the opponent and has more than one checker.
        """
        return self.es_del_oponente(jugador) and self._cantidad_ > 1


def validar_movimiento(tablero, jugador, origen, destino, valor_dado):
    """
    Validates whether a move is legal based on basic game rules.

    Args:
        tablero (list of Punto): The current board state.
        jugador (str): The player's identifier ("Jugador1" or "Jugador2").
        origen (int): Origin point index (0–23).
        destino (int): Destination point index (0–23).
        valor_dado (int): The value of the die used for the move.

    Returns:
        bool: True if the move is valid, False otherwise.
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
