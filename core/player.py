"""Modulo que contiene las clases Jugador y TurnManager."""

from .checker import Checker


class Jugador:
    """
    Representa a un jugador de Backgammon.
    Administra nombre, color, fichas, puntaje y condicion de victoria.

    Atributos:
        nombre (str): Nombre del jugador.
        color (str): Color de sus fichas ("blanco" o "negro").
        puntos (int): Puntaje acumulado.
        fichas_fuera (int): Cantidad de fichas retiradas del tablero.
        fichas (list): Lista de 15 objetos Checker que pertenecen al jugador.
    """

    def __init__(self, nombre, color):
        """
        Inicializa un jugador con nombre, color y 15 fichas.

        Args:
            nombre (str): Nombre del jugador.
            color (str): Color de las fichas ("blanco" o "negro").
        """
        self.nombre = nombre
        self.color = color
        self.puntos = 0
        self.fichas_fuera = 0
        self.fichas = [Checker(color, None) for _ in range(15)]

    def __str__(self):
        """
        Representacion en texto del jugador.

        Returns:
            str: Descripcion del jugador y su color de fichas.
        """
        return f"{self.nombre} juega con fichas {self.color}"

    def sumar_puntos(self, cantidad, verbose=True):
        """
        Suma puntos al puntaje del jugador.

        Args:
            cantidad (int): Cantidad de puntos a sumar.
            verbose (bool): Si se debe imprimir el resultado.
        """
        self.puntos += cantidad
        if verbose:
            print(f"{self.nombre} gana {cantidad} puntos. Total: {self.puntos}")

    def sacar_ficha(self, verbose=True):
        """
        Marca una ficha como retirada del tablero.

        Args:
            verbose (bool): Si se debe imprimir el resultado.
        """
        self.fichas_fuera += 1
        if verbose:
            print(
                f"{self.nombre} ha retirado una ficha. Total fuera: {self.fichas_fuera}"
            )

    def ha_ganado(self):
        """
        Verifica si el jugador ha ganado (todas sus fichas estan fuera).

        Returns:
            bool: True si todas las fichas estan en posicion "off".
        """
        return all(f._position_ == "off" for f in self.fichas)

    def fichas_en_estado(self, estado):
        """
        Devuelve las fichas que estan en un estado especifico.

        Args:
            estado (str): Estado de la ficha ("bar", "off" o None).

        Returns:
            list: Fichas que coinciden con el estado dado.
        """
        return [f for f in self.fichas if f._position_ == estado]

    def fichas_en_punto(self, punto):
        """
        Devuelve las fichas que estan en un punto especifico del tablero.

        Args:
            punto (int): Indice del punto en el tablero.

        Returns:
            list: Fichas ubicadas en ese punto.
        """
        return [f for f in self.fichas if f._position_ == punto]

    def puede_sacar_fichas(self, board):
        """
        Verifica si el jugador puede comenzar a retirar fichas.

        Args:
            board (Board): El tablero de juego.

        Returns:
            bool: True si todas las fichas activas estan en la zona de salida.
        """
        if self.color == "blanco":
            # Zona de salida del blanco: puntos 18 a 23
            rango_casa = range(18, 24)
        else:
            # Zona de salida del negro: puntos 0 a 5
            rango_casa = range(6)

        return all(
            f._position_ in rango_casa or f._position_ == "off"
            for f in self.fichas
            if f._position_ != "bar"
        )


class TurnManager:
    """
    Administra la rotacion de turnos entre dos jugadores.

    Atributos:
        jugadores (list): Lista de dos objetos Jugador.
        indice_actual (int): Indice del jugador actual.
    """

    def __init__(self, jugador1, jugador2):
        """
        Inicializa el gestor de turnos con dos jugadores.

        Args:
            jugador1 (Jugador): Primer jugador.
            jugador2 (Jugador): Segundo jugador.
        """
        self.jugadores = [jugador1, jugador2]
        self.indice_actual = 0

    def jugador_actual(self):
        """
        Devuelve el jugador que tiene el turno actual.

        Returns:
            Jugador: Jugador activo.
        """
        return self.jugadores[self.indice_actual]

    def siguiente_turno(self):
        """
        Cambia al turno del siguiente jugador.
        """
        self.indice_actual = (self.indice_actual + 1) % len(self.jugadores)

    def mostrar_turno(self, verbose=True):
        """
        Muestra en consola el turno actual.

        Args:
            verbose (bool): Si se debe imprimir el turno.
        """
        if verbose:
            jugador = self.jugador_actual()
            print(f"\nTurno: {jugador.nombre} ({jugador.color})")
