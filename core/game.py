from core.board import Board
from core.dados import Dice
from core.checker import Checker
from core.player import Jugador, TurnManager

class Game:
    def __init__(self):
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
        posiciones = {
            "blanco": [0]*2 + [11]*5 + [16]*3 + [18]*5,
            "negro": [23]*2 + [12]*5 + [7]*3 + [5]*5
        }
        for color, puntos in posiciones.items():
            jugador = self.jugador1 if color == "blanco" else self.jugador2
            for i, punto in enumerate(puntos):
                jugador.fichas[i]._position_ = punto

    def tirar_dados(self):
        self.last_roll = self.dice.roll()
        self.available_moves = self.dice.get_moves(self.last_roll)
        return self.last_roll

    def jugador_actual(self):
        return self.turnos.jugador_actual()

    def cambiar_turno(self):
        self.turnos.siguiente_turno()

    def fichas_en_punto(self, punto, color):
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == punto]

    def fichas_en_barra(self, color):
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == "bar"]

    def fichas_borneadas(self, color):
        jugador = self.jugador1 if color == "blanco" else self.jugador2
        return [f for f in jugador.fichas if f._position_ == "off"]

    def mover_ficha(self, origen, destino, color):
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
        if self.jugador1.ha_ganado():
            return self.jugador1.nombre
        elif self.jugador2.ha_ganado():
            return self.jugador2.nombre
        return None
