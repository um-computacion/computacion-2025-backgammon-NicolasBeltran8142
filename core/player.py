"""Módulo que contiene las clases Jugador y TurnManager."""
from .checker import Checker


class Jugador:
    """
    Represents a Backgammon player.
    Manages name, color, checkers, score, and win condition.

    Attributes:
        nombre (str): Player's name.
        color (str): Player's checker color ("blanco" or "negro").
        puntos (int): Accumulated score.
        fichas_fuera (int): Number of checkers borne off.
        fichas (list): List of 15 Checker objects belonging to the player.
    """

    def __init__(self, nombre, color):
        """
        Initializes a player with a name, color, and 15 checkers.

        Args:
            nombre (str): Player's name.
            color (str): Checker color ("blanco" or "negro").
        """
        self.nombre = nombre
        self.color = color
        self.puntos = 0
        self.fichas_fuera = 0
        self.fichas = [Checker(color, None) for _ in range(15)]

    def __str__(self):
        return f"{self.nombre} plays with {self.color} checkers"

    def sumar_puntos(self, cantidad, verbose=True):
        """
        Adds points to the player's score.

        Args:
            cantidad (int): Number of points to add.
            verbose (bool): Whether to print the update.
        """
        self.puntos += cantidad
        if verbose:
            print(f"{self.nombre} gains {cantidad} points. Total: {self.puntos}")

    def sacar_ficha(self, verbose=True):
        """
        Marks one checker as borne off.

        Args:
            verbose (bool): Whether to print the update.
        """
        self.fichas_fuera += 1
        if verbose:
            print(
                f"{self.nombre} has borne off a checker. Total off: {self.fichas_fuera}"
            )

    def ha_ganado(self):
        """
        Checks if the player has won (all checkers are off the board).

        Returns:
            bool: True if all checkers are in "off" position.
        """
        return all(f._position_ == "off" for f in self.fichas)

    def fichas_en_estado(self, estado):
        """
        Returns checkers in a specific state.

        Args:
            estado (str): Checker state ("bar", "off", or None).

        Returns:
            list: Checkers matching the given state.
        """
        return [f for f in self.fichas if f._position_ == estado]

    def fichas_en_punto(self, punto):
        """
        Returns checkers at a specific board point.

        Args:
            punto (int): Board point index.

        Returns:
            list: Checkers located at that point.
        """
        return [f for f in self.fichas if f._position_ == punto]

    def puede_sacar_fichas(self, board):
        """
        Checks if the player can start bearing off checkers.

        Args:
            board (Board): The game board.

        Returns:
            bool: True if all active checkers are in the home board.
        """
        if self.color == "blanco":
            # White's home board is points 18-23
            rango_casa = range(18, 24)
        else:
            # Black's home board is points 0-5
            rango_casa = range(6)
        
        # Check if all checkers not yet borne off are in the home board
        return all(f._position_ in rango_casa or f._position_ == "off" for f in self.fichas if f._position_ != 'bar')


class TurnManager:
    """
    Manages turn rotation between two players.

    Attributes:
        jugadores (list): List of two Jugador objects.
        indice_actual (int): Index of the current player.
    """

    def __init__(self, jugador1, jugador2):
        """
        Initializes the turn manager with two players.

        Args:
            jugador1 (Jugador): First player.
            jugador2 (Jugador): Second player.
        """
        self.jugadores = [jugador1, jugador2]
        self.indice_actual = 0

    def jugador_actual(self):
        """
        Returns the player whose turn it is.

        Returns:
            Jugador: Current player.
        """
        return self.jugadores[self.indice_actual]

    def siguiente_turno(self):
        """
        Switches to the next player's turn.
        """
        self.indice_actual = (self.indice_actual + 1) % len(self.jugadores)

    def mostrar_turno(self, verbose=True):
        """
        Prints the current player's turn.

        Args:
            verbose (bool): Whether to print the turn info.
        """
        if verbose:
            jugador = self.jugador_actual()
            print(f"\nTurn: {jugador.nombre} ({jugador.color})")
