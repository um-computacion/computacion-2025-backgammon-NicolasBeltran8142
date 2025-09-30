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
        """
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == punto]

    def fichas_en_barra(self, color):
        """
        Devuelve las fichas del jugador que están en la barra.
        """
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == "bar"]

    def fichas_borneadas(self, color):
        """
        Devuelve las fichas del jugador que ya fueron retiradas del tablero.
        """
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == "off"]

    def puntos_validos_de_origen(self, color):
        """
        Devuelve los puntos del tablero donde el jugador tiene fichas disponibles para mover.
        """
        return [p for p in range(24) if self.fichas_en_punto(p, color)]

    def puede_mover(self, origen, destino, color):
        """
        Verifica si el movimiento es legal según las reglas básicas.
        """
        if self.fichas_en_barra(color):
            return origen == "bar"
        if destino < 0 or destino > 23:
            return False
        if destino not in [origen + m for m in self.available_moves]:
            return False
        destino_fichas = self.board._puntos_[destino]
        if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) > 1:
            return False
        return True

    def mover_ficha(self, origen, destino, color):
        """
        Mueve una ficha del color dado desde origen a destino, aplicando captura si corresponde.
        """
        if not self.puede_mover(origen, destino, color):
            return False

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
        self.historial.append({
            "jugador": color,
            "origen": origen,
            "destino": destino,
            "dados": self.last_roll
        })
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

    def mostrar_estado(self):
        """
        Imprime el estado actual del juego en consola.
        """
        jugador = self.jugador_actual()
        print(f"\n🔁 Turno de: {jugador.nombre} ({jugador.color})")
        print(f"📍 Fichas en barra: {len(self.fichas_en_barra(jugador.color))}")
        print(f"🎯 Fichas borneadas: {len(self.fichas_borneadas(jugador.color))}")
        print(f"📦 Movimientos disponibles: {self.available_moves}")
