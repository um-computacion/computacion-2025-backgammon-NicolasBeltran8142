from core.board import Board
from core.dados import Dice
from core.player import Jugador, TurnManager

class Game:
    """
    Coordinates the overall Backgammon game logic, including board state,
    dice rolls, player turns, move validation, and win conditions.

    Attributes:
        board (Board): The game board.
        dice (Dice): The dice manager.
        jugador1 (Jugador): Player 1 (white).
        jugador2 (Jugador): Player 2 (black).
        turnos (TurnManager): Manages turn rotation.
        last_roll (list): Last dice roll values.
        available_moves (list): Remaining moves based on dice.
        historial (list): History of moves made.
    """

    def __init__(self):
        """
        Initializes the game with a fresh board, players, dice, and turn manager.
        """
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Jugador("Jugador 1", "blanco")
        self.jugador2 = Jugador("Jugador 2", "negro")
        self.turnos = TurnManager(self.jugador1, self.jugador2)
        self.last_roll = []
        self.available_moves = []
        self.historial = []

        self.board.inicializar_fichas()
        self._asignar_fichas_a_jugadores()

    def _asignar_fichas_a_jugadores(self):
        """
        Assigns initial positions to each player's checkers based on standard setup.
        """
        posiciones = {
            "blanco": [0]*2 + [11]*5 + [16]*3 + [18]*5,
            "negro": [23]*2 + [12]*5 + [7]*3 + [5]*5
        }
        for color, puntos in posiciones.items():
            jugador = self.jugador1 if color == "blanco" else self.jugador2
            for i, punto in enumerate(puntos):
                jugador.fichas[i]._position_ = punto

    def tirar_dados(self):
        """
        Rolls the dice and updates available moves.

        Returns:
            list: The two dice values rolled.
        """
        self.last_roll = self.dice.roll_dice()
        self.available_moves = self.dice.get_moves()
        return self.last_roll

    def jugador_actual(self):
        """
        Returns the player whose turn it is.

        Returns:
            Jugador: The current player.
        """
        return self.turnos.jugador_actual()

    def cambiar_turno(self):
        """
        Switches to the next player's turn.
        """
        self.turnos.siguiente_turno()

    def fichas_en_punto(self, punto, color):
        """
        Returns the checkers of a given color at a specific point.

        Args:
            punto (int): Board point index.
            color (str): Player color.

        Returns:
            list: List of checkers at that point.
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == punto]

    def fichas_en_barra(self, color):
        """
        Returns the checkers of a given color currently on the bar.

        Args:
            color (str): Player color.

        Returns:
            list: List of checkers on the bar.
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == "bar"]

    def fichas_borneadas(self, color):
        """
        Returns the checkers of a given color that have been borne off.

        Args:
            color (str): Player color.

        Returns:
            list: List of checkers with position "off".
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == "off"]

    def puntos_validos_de_origen(self, color):
        """
        Returns the list of valid origin points for the current player.

        Args:
            color (str): Player color.

        Returns:
            list: Valid origin points or ["bar"] if re-entry is required.
        """
        if self.fichas_en_barra(color):
            return ["bar"]
        return [p for p in range(24) if self.fichas_en_punto(p, color)]

    def puede_mover(self, origen, destino, color):
        """
        Validates whether a move is legal based on game rules.

        Args:
            origen (int or str): Origin point or "bar".
            destino (int): Destination point.
            color (str): Player color.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if self.fichas_en_barra(color) and origen != "bar":
            return False
        if destino < 0 or destino > 23:
            return False
        distancia = self._calcular_distancia(origen, destino, color)
        if distancia not in self.available_moves:
            return False
        destino_fichas = self.board._puntos_[destino]
        if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) > 1:
            return False
        return True

    def mover_ficha(self, origen, destino, color):
        """
        Executes a move if it's valid, including capture logic and move tracking.

        Args:
            origen (int or str): Origin point or "bar".
            destino (int): Destination point.
            color (str): Player color.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if not self.puede_mover(origen, destino, color):
            return False

        ficha = self._obtener_ficha_a_mover(origen, color)
        if not ficha:
            return False

        destino_fichas = self.board._puntos_[destino]
        if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) == 1:
            rival_color = "negro" if color == "blanco" else "blanco"
            rival = self.fichas_en_punto(destino, rival_color)[0]
            rival._position_ = "bar"
            self.board._puntos_[destino].pop()

        ficha._position_ = destino
        self.board.mover_ficha(origen, destino, color)

        distancia = self._calcular_distancia(origen, destino, color)
        if distancia in self.available_moves:
            self.available_moves.remove(distancia)

        self.historial.append({
            "jugador": color,
            "origen": origen,
            "destino": destino,
            "dados": self.last_roll
        })

        return True

    def _obtener_ficha_a_mover(self, origen, color):
        """
        Retrieves the checker to be moved from the origin.

        Args:
            origen (int or str): Origin point or "bar".
            color (str): Player color.

        Returns:
            Checker or None: The checker to move, if available.
        """
        if origen == "bar":
            fichas = self.fichas_en_barra(color)
        else:
            fichas = self.fichas_en_punto(origen, color)
        return fichas[0] if fichas else None

    def _jugador_por_color(self, color):
        """
        Returns the player object based on color.

        Args:
            color (str): "blanco" or "negro".

        Returns:
            Jugador: The corresponding player.
        """
        return self.jugador1 if color == "blanco" else self.jugador2

    def _calcular_distancia(self, origen, destino, color):
        """
        Calculates the move distance based on origin and destination.

        Args:
            origen (int or str): Origin point or "bar".
            destino (int): Destination point.
            color (str): Player color.

        Returns:
            int: The distance used for move validation.
        """
        if origen == "bar":
            return destino if color == "blanco" else 23 - destino
        return abs(destino - origen)

    def verificar_ganador(self):
        """
        Checks if any player has won the game.

        Returns:
            str or None: Winner's name or None if no winner yet.
        """
        if self.jugador1.ha_ganado():
            return self.jugador1.nombre
        elif self.jugador2.ha_ganado():
            return self.jugador2.nombre
        return None

    def mostrar_estado(self):
        """
        Displays the current game state in the console.
        """
        jugador = self.jugador_actual()
        print(f"\nTurn: {jugador.nombre} ({jugador.color})")
        print(f"Checkers on bar: {len(self.fichas_en_barra(jugador.color))}")
        print(f"Checkers borne off: {len(self.fichas_borneadas(jugador.color))}")
        print(f"Last roll: {self.last_roll}")
        print(f"Available moves: {self.available_moves}")
