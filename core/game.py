from core.board import Board
from core.dados import Dice
from core.checker import Checker
from core.player import Jugador, TurnManager

class Game:
    """
    Clase principal que coordina el estado y la lógica del juego de Backgammon.

    Administra el tablero, los jugadores, los dados, los turnos y las acciones
    como mover fichas, tirar dados y verificar condiciones de victoria.
    """

    def __init__(self):
        """
        Inicializa el juego con tablero, dados, jugadores y gestor de turnos.

        - Crea el tablero y lo inicializa con fichas.
        - Asigna 15 fichas a cada jugador en sus posiciones iniciales.
        - Prepara el historial de jugadas y el estado de los dados.
        """
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Jugador("Jugador 1", "blanco")
        self.jugador2 = Jugador("Jugador 2", "negro")
        self.turnos = TurnManager(self.jugador1, self.jugador2)
        self.last_roll = None
        self.available_moves = []
        self.historial = []

        self.board.inicializar_fichas()
        self._asignar_fichas_a_jugadores()

    def _asignar_fichas_a_jugadores(self):
        """
        Asigna las posiciones iniciales de las fichas a cada jugador.

        Las posiciones están basadas en la configuración estándar de Backgammon.
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
        Tira los dados y actualiza los movimientos disponibles para el turno actual.

        Returns:
            tuple: Una tupla con los dos valores de los dados.
        """
        self.last_roll = self.dice.roll_dice()
        self.available_moves = self.dice.get_moves()
        return self.last_roll

    def jugador_actual(self):
        """
        Devuelve el jugador que tiene el turno actual.

        Returns:
            Jugador: El jugador activo.
        """
        return self.turnos.jugador_actual()

    def cambiar_turno(self):
        """
        Cambia el turno al siguiente jugador.
        """
        self.turnos.siguiente_turno()

    def fichas_en_punto(self, punto, color):
        """
        Devuelve las fichas de un jugador en un punto específico del tablero.

        Args:
            punto (int): Índice del punto en el tablero.
            color (str): Color del jugador ("blanco" o "negro").

        Returns:
            list: Lista de fichas en ese punto.
        """
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == punto]

    def fichas_en_barra(self, color):
        """
        Devuelve las fichas del jugador que están en la barra.

        Args:
            color (str): Color del jugador.

        Returns:
            list: Lista de fichas en la barra.
        """
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == "bar"]

    def fichas_borneadas(self, color):
        """
        Devuelve las fichas del jugador que ya fueron retiradas del tablero.

        Args:
            color (str): Color del jugador.

        Returns:
            list: Lista de fichas fuera del tablero.
        """
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == "off"]

    def mover_ficha(self, origen, destino, color):
        """
        Mueve una ficha del color dado desde origen a destino.

        Valida que el movimiento sea legal según las reglas estándar:
        - Debe haber una ficha del color en origen.
        - No puede moverse a un punto bloqueado (más de una ficha rival).
        - Si hay una ficha rival sola en destino, la captura y la manda a la barra.

        Args:
            origen (int): Punto de origen.
            destino (int): Punto de destino.
            color (str): Color del jugador.

        Returns:
            bool: True si el movimiento fue exitoso, False si fue inválido.
        """
        fichas = self.fichas_en_punto(origen, color)
        if not fichas:
            return False

        ficha = fichas[0]
        destino_fichas = self.board._puntos_[destino]

        if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) == 1:
            rival_color = "negro" if color == "blanco" else "blanco"
            rival = self.fichas_en_punto(destino, rival_color)[0]
            rival._position_ = "bar"
            self.board._puntos_[destino].pop()

        ficha._position_ = destino
        self.board.mover_ficha(origen, destino, color)
        self.historial.append((color, origen, destino))
        return True

    def verificar_ganador(self):
        """
        Verifica si algún jugador ha ganado el juego.

        Returns:
            str or None: Nombre del jugador ganador, o None si aún no hay ganador.
        """
        if self.jugador1.ha_ganado():
            return self.jugador1.nombre
        elif self.jugador2.ha_ganado():
            return self.jugador2.nombre
        return None
