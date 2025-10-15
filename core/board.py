from core.checker import Checker

class Board:
    """
    Represents the Backgammon board, composed of 24 numbered points (0 to 23).
    Each point can hold a stack of checkers belonging to a player.

    Attributes:
        _puntos_ (list): A list of 24 slots, each containing a stack of checkers.
        historial_de_jugadas (list): A record of all moves made during the game.
    """

    def __init__(self):
        """
        Initializes the board with 24 empty points and an empty move history.
        """
        self._puntos_ = [[] for _ in range(24)]
        self.historial_de_jugadas = []

    def inicializar_fichas(self):
        """
        Places the initial checkers on the board according to standard setup.
        """
        posiciones = {
            "blanco": {0: 2, 11: 5, 16: 3, 18: 5},
            "negro": {23: 2, 12: 5, 7: 3, 5: 5}
        }
        for color, puntos in posiciones.items():
            for punto, cantidad in puntos.items():
                for _ in range(cantidad):
                    self._puntos_[punto].append(Checker(color, punto))

    def mover_ficha(self, origen, destino, color):
        """
        Moves a checker from the origin point to the destination, validating basic rules.

        Args:
            origen (int): Index of the origin point (0–23).
            destino (int): Index of the destination point (0–23).
            color (str): Color of the player making the move ("blanco" or "negro").

        Raises:
            ValueError: If the move is invalid due to range, color mismatch, or blocked destination.
        """
        if not (0 <= origen < 24 and 0 <= destino < 24):
            raise ValueError("Points must be between 0 and 23")

        punto_origen = self._puntos_[origen]
        punto_destino = self._puntos_[destino]

        if not punto_origen:
            raise ValueError(f"No checkers at point {origen}")

        ficha = punto_origen[-1]
        if ficha._color_ != color:
            raise ValueError(f"The checker at point {origen} does not match color {color}")

        captura = False
        if punto_destino and punto_destino[-1]._color_ != color and len(punto_destino) == 1:
            punto_destino.pop()
            captura = True

        ficha._position_ = destino
        punto_origen.pop()
        punto_destino.append(ficha)

        self.registrar_jugada(color, origen, destino, captura)

    def eliminar_ficha_si_unica(self, punto, color):
        """
        Removes a checker from the point if it's the only one and matches the given color.

        Args:
            punto (int): Index of the point (0–23).
            color (str): Player color.

        Returns:
            Checker: The removed checker.

        Raises:
            ValueError: If the point is out of range or conditions are not met.
        """
        if not (0 <= punto < 24):
            raise ValueError("Point must be between 0 and 23")

        casilla = self._puntos_[punto]
        if len(casilla) == 1 and casilla[0]._color_ == color:
            ficha = casilla.pop()
            return ficha
        else:
            raise ValueError("Cannot remove checker: invalid conditions")

    def puede_entrar_desde_bar(self, color, entrada):
        """
        Checks if a checker can re-enter from the bar to the specified point.

        Args:
            color (str): Player color.
            entrada (int): Entry point (0–5 for blanco, 18–23 for negro).

        Returns:
            bool: True if entry is allowed, False if blocked.
        """
        punto = self._puntos_[entrada]
        return not punto or punto[-1]._color_ == color or len(punto) < 2

    def intentar_reingreso(self, color):
        """
        Attempts to re-enter a checker from the bar onto the board.

        Args:
            color (str): Player color.

        Returns:
            int or None: Entry point if successful, None if all are blocked.
        """
        entradas = range(0, 6) if color == "blanco" else range(18, 24)
        for entrada in entradas:
            if self.puede_entrar_desde_bar(color, entrada):
                self._puntos_[entrada].append(Checker(color, entrada))
                print(f"{color} re-enters at point {entrada}")
                return entrada
        print(f"{color} cannot re-enter: all points are blocked.")
        return None

    def registrar_jugada(self, jugador, origen, destino, captura=False):
        """
        Records a move in the game history.

        Args:
            jugador (str): Player color.
            origen (int): Origin point.
            destino (int): Destination point.
            captura (bool): Whether a capture occurred.
        """
        jugada = {
            "jugador": jugador,
            "origen": origen,
            "destino": destino,
            "captura": captura
        }
        self.historial_de_jugadas.append(jugada)

    def mostrar_historial(self):
        """
        Prints the history of moves made during the game.
        """
        print("\nMove history:")
        for j in self.historial_de_jugadas:
            texto = f"{j['jugador']} moved from {j['origen']} to {j['destino']}"
            if j["captura"]:
                texto += " (capture)"
            print(texto)

    def mostrar_tablero(self):
        """
        Prints the current state of the board in a visual format.
        """
        print("\nWelcome to Backgammon Compucation 2025\n")

        print("TOP ZONE (13 → 24):")
        print(" ".join([f"{i:2}" for i in range(12, 24)]))
        print(" ".join([
            "".join(["B" if f._color_ == "blanco" else "N" for f in self._puntos_[i]]) if self._puntos_[i] else "--"
            for i in range(12, 24)
        ]))

        print("\n" + "-" * 50 + "\n")

        print("BOTTOM ZONE (12 → 1):")
        print(" ".join([f"{i:2}" for i in reversed(range(12))]))
        print(" ".join([
            "".join(["B" if f._color_ == "blanco" else "N" for f in self._puntos_[i]]) if self._puntos_[i] else "--"
            for i in reversed(range(12))
        ]))
